"""Upgrade a repo's cookbook to format 2: UUID identity, index.json, UUID links.

`upgrade` plans everything in memory first (identity, legacy `recipes/`
placement, the index, every link rewrite, the repo config) and writes only
when the whole plan succeeded, and only in a clean git work tree. A format-2
repo is left alone, so running it twice changes nothing.

`derive_index` applies the same rules to a format-1 cookbook without writing,
so a dependency that has not been upgraded yet still resolves (links.Resolver).

Placement of a link (`<scheme>://<path>[#<frag>]`), in order:

- an own scheme: the artifact at `<path>` (minus a leading cookbook-dir
  segment); a legacy `<recipes>/<slug>` through `aliases`; `compliance/<doc>#<name>`
  to the check entry; `<path>#<section or requirement>` to the artifact, the
  fragment dropped and its name kept in the text;
- a foreign scheme: the cookbook remembered in locations.json with that
  `legacy_scheme`, matched the same way;
- a bare meta value (no scheme): a path, an rdid, or a unique folder basename.

A URI in the text that names no artifact (an empty path, one ending in `/`, or
an own folder that holds artifacts) is a mention, not a link: it stays as
written and is listed in `left_as_text`. Anything else stays in place, wrapped
as `NEEDS REVIEW: unresolved link <old>`.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
import subprocess
import uuid
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from . import refimpl
from .artifact import (
    ARTIFACT_TYPES,
    Artifact,
    ArtifactError,
    _load_any,
    compose_document,
    doc_digest,
    doc_path,
    dump_manifest,
    find_documents,
    find_folders,
    folder_for,
    normalize_document,
    occupied,
    read_document,
)
from .artifact_build import compile_doc
from .compliance import load_checks
from .errors import CookbookError
from .identity import (
    MANIFEST,
    CookbookIdentity,
    IdentityError,
    artifact_rdid,
    check_rdid,
    check_uuid,
    is_cookbook_rdid,
    is_uuid,
    write_manifest,
)
from .index import INDEX_FILE, Conformance, Entry, Implementation, Index, IndexFileError, load_index, save_index
from .legacy import COOKBOOK_SCHEME, INDEX, LegacyConfig, LegacyRoot, SchemeError, repo_scheme, scheme_of
from .links import parse_link, read_locations, remember_location
from .markdown import ARTIFACT_FILE
from .naming import kebab
from .repoconfig import (
    CONFIG_NAME,
    COOKBOOK_DIR,
    PLATFORMS,
    Config,
    ConfigFields,
    Dependency,
    NeedsUpgrade,
    Root,
    config_format,
    cookbook_dir_named,
    read_config_fields,
    write_repo_config,
)
from .versions import requirements

__all__ = ["UpgradeReport", "UpgradeError", "DirtyTree", "NeedsUpgrade", "needs_upgrade", "derive_index",
           "upgrade"]

FORMAT_2 = 2
NEEDS_REVIEW = "NEEDS REVIEW: unresolved link "
LINK_FIELDS = ("depends-on", "related", "ingredients")
# The top-level keys a format-2 cookbook.json may carry beside its identity (format, id,
# rdid), as references/cookbook.schema.json allows them. The upgrade keeps these and drops
# the rest: `schema_version` (replaced by `format`), `code` (roots move to .cookr.json) and
# `cookbook` (dependencies move to .cookr.json), plus any key the schema does not know.
KEPT_MANIFEST_KEYS = ("$schema", "type", "name", "version", "description", "author", "license",
                      "created", "modified", "platforms", "resources", "context", "structure")
NOT_COOKBOOK_SCHEMES = frozenset({"http", "https", "file", "mailto", "ftp", "cookbook"})
_URI = re.compile(r"^([a-z][a-z0-9+.-]*)://([^#\s]*)(?:#(\S*))?$")
# A link label: no `[` or `]`, and it may wrap onto the next line but not across a blank one.
_LABEL = r"(?:[^\[\]\n]|\n(?![ \t]*\n))*"
# A markdown link to a relative `.md` path with no scheme and no fragment.
_DOC_LINK = re.compile(rf"\[(?P<label>{_LABEL})\]\((?P<path>(?![a-z][a-z0-9+.-]*:)[^)\s#/][^)\s#]*\.md)\)")
# A fragment may nest (`#section/requirement`); a bare trailing `#` is consumed too,
# so no tail of the old URI is left glued after the rewrite. So is a trailing `/`
# after a fragment (`#states/`): the fragment's segments drop the empty last one.
_URI_TAIL = (r"://[A-Za-z0-9._~/%+-]*[A-Za-z0-9_~/%+-]"
             r"(?:#(?:[A-Za-z0-9._~/-]*[A-Za-z0-9_~-])?/?)?")


class UpgradeError(CookbookError):
    """The upgrade cannot run (dirty tree, unknown identity, a conflict). Raised
    while planning, nothing was written; the one raised while writing (a compiled
    doc that fails) says so and how to restore the clean tree it started from."""


class DirtyTree(UpgradeError):
    """The work tree has uncommitted changes (`paths`), so the upgrade did not run."""

    def __init__(self, paths: list[str]):
        self.paths = list(paths)
        super().__init__("the work tree has uncommitted changes; commit them first (a WIP "
                         "commit is fine), then rerun:\n  " + "\n  ".join(self.paths))


@dataclass
class UpgradeReport:
    cookbook_dir: Path
    identity: CookbookIdentity
    artifacts: int = 0
    links_rewritten: int = 0
    needs_review: list[str] = field(default_factory=list)
    dropped_roots: list[str] = field(default_factory=list)
    root_conflicts: list[str] = field(default_factory=list)  # a root in both sources, differing
    left_as_text: list[str] = field(default_factory=list)  # a scheme/folder mention, no artifact
    self_links_dropped: list[str] = field(default_factory=list)  # a meta link naming its own artifact
    missing_paths: list[str] = field(default_factory=list)
    moved_legacy: int = 0
    legacy_dir: Optional[Path] = None  # the legacy recipes dir the upgrade emptied
    files: list[Path] = field(default_factory=list)


# ── reading ──────────────────────────────────────────────────────────────────

def _json(path: Path) -> Optional[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _format(path: Path) -> object:
    data = _json(path)
    return None if data is None else data.get("format")


def _load_folder(folder: Path) -> Artifact:
    """A source folder in format 1 or 2 (artifact.load_folder reads only FORMAT)."""
    try:
        return _load_any(folder)
    except ArtifactError as e:
        raise UpgradeError(str(e)) from e


def _read_doc(path: Path) -> Artifact:
    text = path.read_text(encoding="utf-8")
    try:
        art = read_document(text)
    except ArtifactError as e:
        raise UpgradeError(f"{path}: {e}") from e
    if compose_document(art) != normalize_document(text):
        raise UpgradeError(f"{path}: would not convert losslessly to a source folder")
    return art


def _legacy_raw(repo_root: Path) -> Optional[dict]:
    path = repo_root / CONFIG_NAME
    if not path.is_file():
        return None
    data = _json(path)
    if data is None:
        raise UpgradeError(f"{path}: not a JSON object")
    return None if config_format(data, path) == FORMAT_2 else data


def _legacy_config(repo_root: Path, raw: dict, scheme: str) -> tuple[LegacyConfig, list[str]]:
    """A LegacyConfig that tolerates roots and renames whose paths are gone
    (legacy.load_legacy refuses them); the dropped root paths come back too."""
    roots, dropped = [], []
    for r in raw.get("roots") or []:
        if not isinstance(r, dict) or not isinstance(r.get("path"), str):
            continue
        if not (repo_root / r["path"].strip("/")).is_dir():
            dropped.append(r["path"].strip("/"))
            continue
        roots.append(LegacyRoot(path=r["path"], tier=str(r.get("tier") or ""),
                                platform=str(r.get("platform") or ""), kind=r.get("kind", "ui"),
                                ignore=tuple(r.get("ignore") or ())))
    renames = {k.strip("/"): v for k, v in (raw.get("renames") or {}).items()
               if isinstance(k, str) and k.strip("/") and (repo_root / k.strip("/")).exists()}
    return LegacyConfig(repo_root=repo_root, recipes=str(raw.get("recipes") or "recipes"),
                        roots=roots, ignore=list(raw.get("ignore") or []),
                        aliases=dict(raw.get("aliases") or {}), renames=renames,
                        declared_scheme=str(raw.get("scheme") or scheme)), dropped


def _index_scheme(cookbook_dir: Path) -> Optional[str]:
    f = cookbook_dir / INDEX
    if not f.is_file():
        return None
    try:
        return scheme_of(read_document(f.read_text(encoding="utf-8")).meta.get("domain"))
    except (OSError, ArtifactError, UnicodeDecodeError):
        return None


def _catalog(cookbook_dir: Path) -> Optional[Path]:
    repo = cookbook_dir.parent
    for c in (repo / "tbd" / "compliance", repo / "compliance", cookbook_dir / "compliance"):
        if c.is_dir():
            return c
    return None


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


# ── the plan ─────────────────────────────────────────────────────────────────

@dataclass
class _Art:
    rel: str  # folder path below the cookbook
    art: Artifact
    folder: Optional[Path] = None  # the existing source folder
    doc: Optional[Path] = None  # an md-only doc, converted and removed
    compiled: Optional[Path] = None  # a compiled doc beside the folder, regenerated
    legacy: Optional[Path] = None  # a legacy recipe, moved and removed
    old_parts: set = field(default_factory=set)
    impls: list = field(default_factory=list)  # [refimpl.Implementation]

    @property
    def uid(self) -> str:
        return str(self.art.meta["id"]).lower()


@dataclass
class _Plan:
    repo_root: Path
    cookbook_dir: Path
    identity: CookbookIdentity
    scheme: Optional[str]
    manifest: dict
    arts: list
    index: Index
    report: UpgradeReport
    legacy_file: bool = False
    legacy_dir: Optional[Path] = None
    legacy_remove: list = field(default_factory=list)
    roots: list = field(default_factory=list)
    ignore: list = field(default_factory=list)
    dependencies: dict = field(default_factory=dict)
    config_file: bool = False  # the repo has a format-2 .cookr.json, kept and rewritten
    slugs: dict = field(default_factory=dict)  # legacy `<recipes>/<slug>` -> _Art


def _sanitize(rel: str) -> str:
    return "/".join(re.sub(r"[^a-z0-9-]+", "-", p.lower()).strip("-") or "x"
                    for p in rel.split("/") if p)


def _artifact_uid(cookbook_id: str, rel: str) -> str:
    return str(uuid.uuid5(uuid.UUID(cookbook_id), f"artifact:{rel}"))


def _rdid_for(scheme: Optional[str]) -> Optional[str]:
    if not scheme:
        return None
    return "adc" if scheme == COOKBOOK_SCHEME else scheme.lower()


def _cookbook_artifacts(cookbook_dir: Path) -> list[_Art]:
    arts = []
    for folder in find_folders([cookbook_dir]):
        art = _load_folder(folder)
        a = _Art(folder.relative_to(cookbook_dir).as_posix(), art, folder=folder,
                 old_parts={p.name for p in art.parts})
        doc = doc_path(folder)
        if doc.is_file():
            text = doc.read_text(encoding="utf-8")
            if text != compose_document(art) and art.synced != doc_digest(text):
                raise UpgradeError(f"{doc} was edited since cookr compiled it; fold it into its "
                                   "folder with `cookr convert --update` first")
            a.compiled = doc
        arts.append(a)
    for doc in find_documents([cookbook_dir]):
        if (folder_for(doc) / ARTIFACT_FILE).is_file():
            continue
        art = _read_doc(doc)
        a = _Art(folder_for(doc).relative_to(cookbook_dir).as_posix(), art, doc=doc)
        problem = occupied(art, folder_for(doc))
        if problem:
            raise UpgradeError(problem)
        arts.append(a)
    return arts


def _take_impls(a: _Art) -> None:
    """Move the Reference Implementations section's rows out of the artifact."""
    kept = []
    for p in a.art.parts:
        if p.heading is not None and p.heading.strip() == refimpl.SECTION:
            a.impls += refimpl.parse(p.text)
        else:
            kept.append(p)
    a.art.parts = kept


def _merge(rows: list, extra: list) -> list:
    out = list(rows)
    for r in extra:
        if all(r.path != o.path or r.platform != o.platform for o in out):
            out.append(r)
    return out


def _legacy_recipes(plan: _Plan, raw: dict, by_uid: dict, by_rel: dict,
                    slugs: dict) -> list[str]:
    """Place each legacy recipe (organize.plan's placement) or merge it into its
    counterpart. Returns the dropped legacy root paths."""
    from .organize import plan as organize_plan

    config, dropped = _legacy_config(plan.repo_root, raw, plan.scheme or "legacy")
    recipes_dir = plan.repo_root / config.recipes
    if not recipes_dir.is_dir():
        return dropped
    plan.legacy_dir = plan.report.legacy_dir = recipes_dir
    try:
        moves = organize_plan(config)["moves"]
    except (CookbookError, ValueError) as e:
        raise UpgradeError(f"cannot place the legacy recipes in {recipes_dir}: {e}") from e
    basenames = Counter(a.rel.rsplit("/", 1)[-1] for a in plan.arts)
    for move in moves:
        src = plan.repo_root / move["from"]
        slug = Path(move["from"]).relative_to(config.recipes).with_suffix("").as_posix()
        art = _read_doc(src)
        legacy_rows = refimpl.implementations(art.body())
        uid = str(art.meta.get("id") or "").lower()
        target = by_uid.get(uid) if uid else None
        if target is None:
            target = by_rel.get(move["to"])
        last = slug.rsplit("/", 1)[-1]
        if target is None and basenames.get(last) == 1:
            target = next(a for a in plan.arts if a.rel.rsplit("/", 1)[-1] == last)
        if target is not None:
            target.impls = _merge(target.impls, legacy_rows)
        else:
            rel = move["to"]
            if not uid:
                uid = _artifact_uid(plan.identity.id, rel)
            art.meta = {"id": uid, **{k: v for k, v in art.meta.items() if k != "id"}}
            target = _Art(rel, art, legacy=src)
            problem = occupied(art, plan.cookbook_dir / rel)
            if problem:
                raise UpgradeError(problem)
            _take_impls(target)
            target.impls = _merge(target.impls, [refimpl.Implementation(i["platform"], i["path"])
                                                 for i in move["implementations"]])
            plan.arts.append(target)
            by_uid[uid] = target
            by_rel[rel] = target
        slugs[f"{config.recipes}/{slug}"] = target
        plan.legacy_remove.append(src)
        plan.report.moved_legacy += 1
    for name, slug in config.aliases.items():
        target = slugs.get(f"{config.recipes}/{slug}")
        if target is not None:
            slugs.setdefault(f"{config.recipes}/{name}", target)
    moved = set(plan.legacy_remove)
    for left in sorted(f for f in recipes_dir.rglob("*") if f.is_file()):
        if left not in moved and left.name != ".gitkeep":
            plan.report.needs_review.append(
                f"{left.relative_to(plan.repo_root).as_posix()}: left in the legacy recipes dir")
    return dropped


def _platform(r: dict) -> str:
    platform = str(r.get("platform") or "")
    if platform == "apple":
        segs = {s.lower() for s in str(r["path"]).split("/")}
        if "macos" in segs:
            return "macos"
        if "ios" in segs:
            return "ios"
    return platform


def _root_entries(code: Optional[dict]) -> list[dict]:
    return [r for r in (code or {}).get("roots") or [] if isinstance(r, dict)]


def _union(*lists) -> list:
    out: list = []
    for items in lists:
        for item in items or ():
            if item not in out:
                out.append(item)
    return out


def _repo_roots(plan: _Plan, code: Optional[dict], raw: Optional[dict],
                current: Optional[ConfigFields] = None) -> None:
    """The format-2 roots: a format-2 `.cookr.json`'s own roots (`current`), then
    `cookbook.json`'s `code` block, then a legacy `.cookr.json`'s roots
    (converted as organize's placement does, so a legacy root's group is the
    folder its recipes moved to). A path in more than one is one root: the
    first source's platform, kind and group win, each difference is listed in
    `root_conflicts`, and the root-scoped ignore lists are united. The
    repo-wide ignore lists are united too. A root whose path is gone is listed
    in `dropped_roots`."""
    from .organize import code_block

    entries = [(r, "cookbook.json code") for r in _root_entries(code)]
    ignore = _union(current.ignore if current else [], (code or {}).get("ignore"))
    if raw is not None and (raw.get("roots") or raw.get("ignore")):
        config, dropped = _legacy_config(plan.repo_root, raw, plan.scheme or "legacy")
        legacy = code_block(config) if config.roots else {"roots": [], "ignore": config.ignore}
        entries += [(r, "legacy .cookr.json") for r in _root_entries(legacy)]
        ignore = _union(ignore, legacy.get("ignore"))
        for path in dropped:
            if path not in plan.report.dropped_roots:
                plan.report.dropped_roots.append(path)
    merged: dict[str, tuple[Root, str]] = {
        r.path: (r, "format-2 .cookr.json") for r in (current.roots if current else [])}
    for r, source in entries:
        path = str(r.get("path", "")).strip("/")
        if not path or not (plan.repo_root / path).is_dir():
            if path and path not in plan.report.dropped_roots:
                plan.report.dropped_roots.append(path)
            continue
        platform = _platform(r)
        if platform not in PLATFORMS:
            raise UpgradeError(f"root {path}: platform {platform!r} is not one of "
                               f"{', '.join(PLATFORMS)}")
        root = Root(path, platform, r.get("kind", "ui"),
                    str(r.get("recipes") or r.get("group") or "").strip("/"),
                    tuple(r.get("ignore") or ()))
        if path not in merged:
            merged[path] = (root, source)
            continue
        kept, kept_source = merged[path]
        for name in ("platform", "kind", "group"):
            ours, theirs = getattr(kept, name), getattr(root, name)
            if ours != theirs and kept_source == source:
                plan.report.root_conflicts.append(
                    f"{path}: {name} {ours or '(none)'} over {theirs or '(none)'}, listed "
                    f"twice in {source}; kept the first")
            elif ours != theirs:
                plan.report.root_conflicts.append(
                    f"{path}: {name} {ours or '(none)'} ({kept_source}) over "
                    f"{theirs or '(none)'} ({source})")
        merged[path] = (Root(kept.path, kept.platform, kept.kind, kept.group,
                             tuple(_union(kept.ignore, root.ignore))), kept_source)
    plan.roots = [root for root, _ in merged.values()]
    plan.ignore = ignore


def _make_plan(repo_root: Path, cookbook_dir: Path, *, rdid: Optional[str], derive: bool) -> _Plan:
    manifest_path = cookbook_dir / MANIFEST
    manifest = _json(manifest_path) or {}
    if manifest_path.is_file() and not manifest:
        raise UpgradeError(f"{manifest_path}: not a JSON object")
    cid = manifest.get("id")
    if is_uuid(str(cid).lower() if cid else ""):
        cid = str(cid).lower()
    elif derive:
        raise NeedsUpgrade(manifest_path, f"{manifest_path}: no cookbook id; run `cookr upgrade`")
    else:
        cid = str(uuid.uuid4())

    raw = _legacy_raw(repo_root)
    arts = _cookbook_artifacts(cookbook_dir) if cookbook_dir.is_dir() else []
    domains = Counter(s for s in (scheme_of(a.art.meta.get("domain")) for a in arts) if s)
    scheme = (domains.most_common(1)[0][0] if domains else None) or \
        (raw or {}).get("scheme") or _index_scheme(cookbook_dir)

    chosen = rdid
    if chosen is None and is_cookbook_rdid(manifest.get("rdid")):
        chosen = manifest["rdid"]
    if chosen is None and derive:
        loc = read_locations().get(cid)
        if isinstance(loc, dict) and is_cookbook_rdid(loc.get("rdid")):
            chosen = loc["rdid"]
    if chosen is None:
        if scheme is None:
            try:
                scheme = repo_scheme(repo_root)
            except SchemeError as e:
                raise UpgradeError(f"{e}; pass --rdid") from e
        chosen = _rdid_for(scheme)
    if not is_cookbook_rdid(chosen):
        raise UpgradeError(f"{chosen!r} is not a valid cookbook rdid; pass --rdid")
    identity = CookbookIdentity(cid, chosen)

    report = UpgradeReport(cookbook_dir=cookbook_dir, identity=identity)
    plan = _Plan(repo_root, cookbook_dir, identity, scheme, manifest, arts,
                 Index(identity), report, legacy_file=raw is not None)

    for a in arts:
        if not a.art.meta.get("id"):
            a.art.meta = {"id": _artifact_uid(cid, a.rel), **a.art.meta}
        else:
            a.art.meta["id"] = str(a.art.meta["id"]).lower()
        _take_impls(a)
    by_uid: dict[str, _Art] = {}
    for a in arts:
        if a.uid in by_uid:
            raise UpgradeError(f"artifact id {a.uid} is used by {by_uid[a.uid].rel} and {a.rel}")
        by_uid[a.uid] = a
    by_rel = {a.rel: a for a in arts}
    if raw is not None and raw.get("recipes"):
        report.dropped_roots += _legacy_recipes(plan, raw, by_uid, by_rel, plan.slugs)

    seen_rdids: dict[str, str] = {}
    for a in sorted(plan.arts, key=lambda a: a.rel):
        type_ = a.art.meta.get("type")
        if type_ not in ARTIFACT_TYPES:
            raise UpgradeError(f"{a.rel}: type {type_!r} is not one of {', '.join(ARTIFACT_TYPES)}")
        try:
            rd = artifact_rdid(identity.rdid, type_, _sanitize(a.rel))
        except IdentityError as e:
            raise UpgradeError(f"{a.rel}: {e}") from e
        if rd in seen_rdids:
            raise UpgradeError(f"rdid {rd} would name both {seen_rdids[rd]} and {a.rel}")
        seen_rdids[rd] = a.rel
        impls = []
        for r in a.impls:
            loc = r.path
            if "://" not in loc and not (repo_root / loc.rstrip("/")).exists():
                report.missing_paths.append(f"{a.rel}: {loc}")
                continue
            impls.append(Implementation(r.platform, loc, Conformance("unverified")))
        plan.index.entries[a.uid] = Entry(a.uid, type_, rd, a.rel, impls)
        a.art.meta.pop("domain", None)
    report.artifacts = len(plan.arts)

    catalog = _catalog(cookbook_dir)
    if catalog is not None:
        plan.index.catalog = Path(os.path.relpath(catalog, cookbook_dir)).as_posix()
        for item in sorted(load_checks(catalog) or ()):
            document, name = item.split("#", 1)
            try:
                rd = check_rdid(identity.rdid, _sanitize(document), name)
            except IdentityError as e:
                raise UpgradeError(f"check {item}: {e}") from e
            uid = check_uuid(cid, document, name)
            plan.index.entries[uid] = Entry(uid, "check", rd, item)

    current = None
    if not derive and raw is None and (repo_root / CONFIG_NAME).is_file():
        current = read_config_fields(repo_root)  # a format-2 config: carried over whole
        plan.config_file = True
        plan.dependencies.update(current.dependencies)
    _repo_roots(plan, manifest.get("code"), raw, current)
    return plan


# ── links ────────────────────────────────────────────────────────────────────

class _Links:
    def __init__(self, plan: _Plan):
        self.plan = plan
        self.index = plan.index
        own = {plan.scheme} if plan.scheme else set()
        own |= {s for s in (scheme_of(a.art.meta.get("domain")) for a in plan.arts) if s}
        if plan.legacy_file:
            raw = _legacy_raw(plan.repo_root) or {}
            if raw.get("scheme"):
                own.add(raw["scheme"])
        idx = _index_scheme(plan.cookbook_dir)
        if idx:
            own.add(idx)
        self.own = own
        self.foreign_schemes = {
            str(v["legacy_scheme"]) for k, v in read_locations().items()
            if isinstance(v, dict) and v.get("legacy_scheme") and k != plan.identity.id}
        self.basenames: dict[str, list[Entry]] = {}
        for e in self.index.entries.values():
            if e.kind != "check":
                self.basenames.setdefault(e.path.rsplit("/", 1)[-1], []).append(e)
        self._foreign: dict[str, list[tuple[Index, Path]]] = {}
        self._anchors: dict[str, set[str]] = {}
        self._folder_set: Optional[set[str]] = None
        self.unknown: set[str] = set()  # foreign schemes no remembered cookbook answers
        self.rewritten = 0

    def schemes(self, extra: set) -> set:
        return (self.own | self.foreign_schemes | {COOKBOOK_SCHEME} | extra) - NOT_COOKBOOK_SCHEMES

    def _foreign_indexes(self, scheme: str) -> list[tuple[Index, Path]]:
        if scheme not in self._foreign:
            found = []
            for cid, loc in sorted(read_locations().items()):
                if (not isinstance(loc, dict) or loc.get("legacy_scheme") != scheme
                        or cid == self.plan.identity.id or not loc.get("path")):
                    continue
                path = Path(loc["path"]).expanduser()
                try:
                    if _format(path / INDEX_FILE) == FORMAT_2:
                        index = load_index(path)
                    else:
                        index = derive_index(path)
                except (CookbookError, OSError, ValueError):
                    continue
                found.append((index, path))
            self._foreign[scheme] = found
        return self._foreign[scheme]

    def _own_anchors(self, e: Entry) -> set[str]:
        if e.id not in self._anchors:
            art = next((a.art for a in self.plan.arts if a.uid == e.id), None)
            self._anchors[e.id] = _anchors(art)
        return self._anchors[e.id]

    def _foreign_anchors(self, cookbook_dir: Path, e: Entry) -> set[str]:
        key = f"{cookbook_dir}/{e.id}"
        if key not in self._anchors:
            art = None
            folder, doc = cookbook_dir / e.path, cookbook_dir / f"{e.path}.md"
            try:
                if (folder / ARTIFACT_FILE).is_file():
                    art = _load_any(folder)
                elif doc.is_file():
                    art = read_document(doc.read_text(encoding="utf-8"))
            except (ArtifactError, OSError, UnicodeDecodeError):
                art = None
            self._anchors[key] = _anchors(art)
        return self._anchors[key]

    @classmethod
    def _match(cls, index: Index, path: str, frag: Optional[str], dirname: str,
               extra: Optional[dict] = None,
               anchors=None) -> Optional[tuple[Entry, Optional[str]]]:
        """(entry, section) for what `path` names. With a fragment: a compliance
        check, or the artifact whose section or named requirement the fragment
        names (the fragment itself is dropped: "#fragment only within a
        document"). A nested fragment (`#accessibility/escape-closes`,
        `#requirements/<name>`) is tried whole, then by its last segment, then by
        its first; `section` is the first of those the target has."""
        if frag:
            if path.startswith("compliance/"):
                e = index.by_path(f"{path[len('compliance/'):]}#{frag}")
                return (e, None) if e is not None and e.kind == "check" else None
            found = cls._match(index, path, None, dirname, extra)
            if found is None or anchors is None:
                return None
            have = anchors(found[0])
            segs = [s for s in frag.split("/") if s]
            for name in (frag, segs[-1] if segs else "", segs[0] if segs else ""):
                if name and name.casefold() in have:
                    return found[0], name
            return None
        path = path.strip("/")
        if path.endswith(".md"):
            path = path[:-3]
        candidates = [path]
        if path.split("/", 1)[0] == dirname and "/" in path:
            candidates.append(path.split("/", 1)[1])
        for c in candidates:
            e = index.by_path(c)
            if e is not None and e.kind != "check":
                return e, None
        if extra and path in extra:
            e = index.entries.get(extra[path].uid)
            return None if e is None else (e, None)
        return None

    def resolve(self, value: str) -> Optional[tuple[str, str, Optional[str]]]:
        """(link, rdid, section) for an old link, or None when it cannot be
        placed. `section` is the dropped fragment when it named a section or
        requirement of the target, else None."""
        m = _URI.match(value.strip())
        if m is None:
            found = self._bare(value.strip())
            return None if found is None else (*found, None)
        scheme, path, frag = m.group(1), m.group(2), m.group(3) or None
        if scheme in self.own:
            found = self._match(self.index, path, frag, self.plan.cookbook_dir.name,
                                self.plan.slugs, self._own_anchors)
            if found is not None:
                return found[0].id, found[0].rdid, found[1]
        foreign = self._foreign_indexes(scheme)
        if not foreign and scheme not in self.own:
            self.unknown.add(scheme)
        for index, cookbook_dir in foreign:
            found = self._match(index, path, frag, cookbook_dir.name, None,
                                lambda e, d=cookbook_dir: self._foreign_anchors(d, e))
            if found is not None:
                e = found[0]
                key = f"{index.cookbook.id}/{e.id}"
                self.plan.dependencies.setdefault(index.cookbook.id, Dependency(
                    index.cookbook.id, index.cookbook.rdid, None))  # keep a configured location
                self.index.foreign[key] = e.rdid
                return key, e.rdid, found[1]
        return None

    def _bare(self, value: str) -> Optional[tuple[str, str]]:
        if not value or "://" in value:
            return None
        path = value.strip("/")
        if path.endswith(".md"):
            path = path[:-3]
        e = self.index.by_path(path)
        if e is None:
            e = self.index.get(value) or self.index.get(f"{self.index.cookbook.rdid}.{value}")
        if e is None:
            found = self.basenames.get(path.rsplit("/", 1)[-1], [])
            e = found[0] if len(found) == 1 else None
        if e is None and "/" not in value and "." in value:
            # A dotted name from before the move (`ingredient.ui.component.x`):
            # its last segment, when unique and of the kind its first names.
            segs = value.split(".")
            found = self.basenames.get(segs[-1], [])
            e = found[0] if len(found) == 1 and found[0].kind == segs[0] else None
        return (e.id, e.rdid) if e is not None and e.kind != "check" else None

    def meta_value(self, rel: str, value: object) -> object:
        if not isinstance(value, str) or value.startswith(NEEDS_REVIEW):
            return value
        try:
            parse_link(value)
            return value  # already a UUID link
        except ValueError:
            pass
        s = scheme_of(value)
        if s is not None and s in NOT_COOKBOOK_SCHEMES:
            return value
        found = self.resolve(value)
        if found is None:
            self.plan.report.needs_review.append(f"{rel}: {value}")
            return f"{NEEDS_REVIEW}{value}"
        self.rewritten += 1
        return found[0]

    def text_re(self, schemes: set) -> re.Pattern:
        alt = "|".join(re.escape(s) for s in sorted(schemes, key=len, reverse=True))
        uri = rf"(?<![A-Za-z0-9+.-])(?:{alt}){_URI_TAIL}"
        return re.compile(
            rf"(?P<done>{re.escape(NEEDS_REVIEW)}(?:\[{_LABEL}\]\({uri}\)|<{uri}>|`{uri}`|{uri}))"
            rf"|\[(?P<label>{_LABEL})\]\((?P<md>{uri})\)"
            rf"|`(?P<code>{uri})`"
            rf"|<(?P<angle>{uri})>"
            rf"|(?P<bare>{uri})")

    def text(self, rel: str, text: str, pattern: re.Pattern) -> str:
        def sub(m: re.Match) -> str:
            if m.group("done"):
                return m.group(0)
            uri = m.group("md") or m.group("code") or m.group("angle") or m.group("bare")
            unknown = set(self.unknown)
            found = self.resolve(uri)
            if found is None and self._names_no_artifact(uri):
                self.unknown = unknown  # a scheme only mentioned is not one to upgrade first
                self.plan.report.left_as_text.append(f"{rel}: {uri}")
                return m.group(0)
            if found is None:
                self.plan.report.needs_review.append(f"{rel}: {uri}")
                return f"{NEEDS_REVIEW}{m.group(0)}"
            self.rewritten += 1
            return _labelled(m.group("label"), uri, found[1], found[0], found[2])
        return _DOC_LINK.sub(lambda m: self._doc_link(rel, m), pattern.sub(sub, text))

    def _folders(self) -> set[str]:
        """Every folder an own-scheme path may name that holds artifacts but
        is none: the cookbook dir, the legacy recipes dir, each artifact's
        parent folders (with and without the cookbook dir in front)."""
        if self._folder_set is None:
            cb = self.plan.cookbook_dir.name
            out = {cb, "compliance"}
            if self.plan.legacy_dir is not None:
                out.add(self.plan.legacy_dir.relative_to(self.plan.repo_root).as_posix())
            for e in self.index.entries.values():
                if e.kind == "check":
                    continue
                parts = e.path.split("/")[:-1]
                for i in range(1, len(parts) + 1):
                    out.add("/".join(parts[:i]))
                    out.add(f"{cb}/" + "/".join(parts[:i]))
            self._folder_set = out - {e.path for e in self.index.entries.values()}
        return self._folder_set

    def _names_no_artifact(self, uri: str) -> bool:
        """A URI that is a scheme or folder mention, not a link: its path is
        empty, ends in `/`, or (own scheme) names a folder that holds artifacts."""
        m = _URI.match(uri)
        if m is None or m.group(3):
            return False
        path = m.group(2)
        if not path.strip("/") or path.endswith("/"):
            return True
        return m.group(1) in self.own and path.strip("/") in self._folders()

    def _doc_link(self, rel: str, m: re.Match) -> str:
        """A relative link to another artifact's compiled doc (`../x/y.md`),
        written from where this artifact's own doc sits (`<rel>.md`). Compiled
        docs are not committed, so it becomes a UUID link; a link to anything
        that is not an artifact stays as written, for validate to check."""
        target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), m.group("path")))
        if target.startswith("../") or not target.endswith(".md"):
            return m.group(0)
        e = self.index.by_path(target[:-3])
        if e is None or e.kind == "check":
            return m.group(0)
        self.rewritten += 1
        return _labelled(m.group("label"), m.group("path"), e.rdid, e.id)


def _anchors(art: Optional[Artifact]) -> set[str]:
    """What a `#fragment` may name in `art`, casefolded: each section (its part
    name or its heading in kebab-case) and each named requirement."""
    if art is None:
        return set()
    out = {p.name for p in art.parts if p.heading is not None}
    out |= {kebab(p.heading) for p in art.parts if p.heading is not None}
    out |= set(requirements(art.body()))
    return {a.casefold() for a in out if a}


def _names(target: str) -> set[str]:
    """What a link label may say that names the target itself: the old target as
    written (its domain or path), its last path segment, and its fragment."""
    path, _, frag = target.partition("#")
    path = path.split("://", 1)[-1].rstrip("/")
    last = path.rsplit("/", 1)[-1]
    names = {target, last, last.removesuffix(".md")}
    if frag:
        names.add(frag)
        names |= set(frag.split("/"))
    return {n.casefold() for n in names if n}


def _labelled(label: Optional[str], target: str, rdid: str, link: str,
              section: Optional[str] = None) -> str:
    """The rewritten link: `[<rdid>](cookbook:<link>)`, the label being a cached
    rdid. An old label that said more than the target's own name (a check or
    requirement name, a phrase) is kept as plain text beside it. A link into a
    section (or requirement) of the target loses its fragment, so the section's
    name is kept as that text when the label does not say more itself."""
    new = f"[{rdid}](cookbook:{link})"
    label = (label or "").strip()
    own = _names(target) | {rdid.casefold()}
    if section:
        own.discard(section.casefold())
    if not label or label.casefold() in own:
        return f"{section} ({new})" if section else new
    return f"{label} ({new})"


def _references_to_related(plan: _Plan, links: "_Links", a) -> None:
    """`references` holds external sources (URLs, citations). A cookbook URI
    there is a link to an artifact, so it moves to `related` as a UUID link
    (once, and never one naming its own artifact). One that cannot be placed is
    dropped and reported: a dead link is no source. URLs and plain text stay."""
    refs = a.art.meta.get("references")
    if not isinstance(refs, list):
        return
    related = a.art.meta.get("related")
    related = list(related) if isinstance(related, list) else ([related] if related else [])
    kept = []
    for v in refs:
        s = scheme_of(v) if isinstance(v, str) else None
        if s is None or s in NOT_COOKBOOK_SCHEMES:
            kept.append(v)
            continue
        found = links.resolve(v)
        if found is None:
            plan.report.needs_review.append(f"{a.rel}: references {v} (dropped)")
        elif found[0] == a.uid:
            plan.report.self_links_dropped.append(f"{a.rel}: references {v}")
        else:
            links.rewritten += 1
            if found[0] not in related:
                related.append(found[0])
    if kept != refs:
        a.art.meta["references"] = kept
        a.art.meta["related"] = related


def _rewrite_links(plan: _Plan) -> None:
    links = _Links(plan)
    extra = set()
    for a in plan.arts:
        for key in LINK_FIELDS:
            vals = a.art.meta.get(key)
            for v in vals if isinstance(vals, list) else [vals]:
                s = scheme_of(v)
                if s:
                    extra.add(s)
    pattern = links.text_re(links.schemes(extra))
    for a in sorted(plan.arts, key=lambda a: a.rel):
        for key in LINK_FIELDS:
            vals = a.art.meta.get(key)
            if isinstance(vals, list):
                kept = []
                for v in vals:
                    new = links.meta_value(a.rel, v)
                    if new == a.uid:  # e.g. a legacy recipe merged into its own artifact
                        plan.report.self_links_dropped.append(f"{a.rel}: {key} {v}")
                    else:
                        kept.append(new)
                a.art.meta[key] = kept
            elif isinstance(vals, str):
                a.art.meta[key] = links.meta_value(a.rel, vals)
        _references_to_related(plan, links, a)
        for p in a.art.parts:
            p.text = links.text(a.rel, p.text, pattern)
    plan.report.links_rewritten = links.rewritten
    plan.report.needs_review += [
        f"scheme '{s}' is not known — upgrade that cookbook first, then rerun"
        for s in sorted(links.unknown)]


# ── writing ──────────────────────────────────────────────────────────────────


def _write(plan: _Plan, legacy_scheme: Optional[str]) -> None:
    report, cb = plan.report, plan.cookbook_dir
    files: list[Path] = []
    cb.mkdir(parents=True, exist_ok=True)

    manifest = cb / MANIFEST
    extra = {k: v for k, v in plan.manifest.items() if k in KEPT_MANIFEST_KEYS}
    if manifest.exists():
        manifest.unlink()
    write_manifest(cb, plan.identity, extra)
    files.append(manifest)

    for a in plan.arts:
        folder = cb / a.rel
        folder.mkdir(parents=True, exist_ok=True)
        a.art.synced = doc_digest(compose_document(a.art))
        (folder / ARTIFACT_FILE).write_text(dump_manifest(a.art), encoding="utf-8")
        files.append(folder / ARTIFACT_FILE)
        for p in a.art.parts:
            f = folder / f"{p.name}.md"
            if not f.is_file() or f.read_text(encoding="utf-8") != p.text:
                f.write_text(p.text, encoding="utf-8")
                files.append(f)
        for gone in a.old_parts - {p.name for p in a.art.parts}:
            (folder / f"{gone}.md").unlink(missing_ok=True)
            files.append(folder / f"{gone}.md")
        for src in (a.doc, a.legacy):
            if src is not None and src.exists():
                src.unlink()
                files.append(src)

    for src in plan.legacy_remove:
        if src.exists():
            src.unlink()
            files.append(src)
    if plan.legacy_dir is not None and plan.legacy_dir.is_dir():
        for keep in plan.legacy_dir.rglob(".gitkeep"):
            keep.unlink()
            files.append(keep)
        for d in sorted((p for p in plan.legacy_dir.rglob("*") if p.is_dir()),
                        key=lambda p: len(p.parts), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
        if not any(plan.legacy_dir.iterdir()):  # leftovers were reported by the plan
            plan.legacy_dir.rmdir()

    save_index(plan.index, cb)
    files.append(cb / INDEX_FILE)

    # A compiled doc committed beside its folder stays, rewritten as `cookr compile
    # --target doc` writes it (the index's Reference Implementations included,
    # `synced` recorded) so validate sees it current. A folder without one gets none.
    compiled = [cb / a.rel for a in plan.arts if a.compiled is not None]
    for r in compile_doc(compiled, base=cb, force=True):
        if r.status == "error":
            raise UpgradeError(
                f"compiling {r.source}: {r.detail}. The upgrade had already written files; it "
                f"started from a clean work tree, so `git checkout -- . && git clean -fd` in "
                f"{plan.repo_root} restores it. Fix the artifact, then rerun")
        files.append(r.dest)

    config_path = plan.repo_root / CONFIG_NAME
    # The config stays whenever it says anything: a format-2 config always does
    # (dropping one that names a custom cookbook dir would orphan the cookbook).
    if (plan.config_file or plan.roots or plan.dependencies or plan.ignore
            or cb.resolve() != (plan.repo_root / COOKBOOK_DIR).resolve()):
        write_repo_config(Config(plan.repo_root, cb, plan.identity, plan.roots, plan.ignore,
                                 dict(sorted(plan.dependencies.items())), config_path))
        files.append(config_path)
    elif config_path.is_file():
        config_path.unlink()
        files.append(config_path)

    remember_location(plan.identity, cb.resolve(), legacy_scheme)
    report.files = sorted(set(files))


# ── public API ───────────────────────────────────────────────────────────────

def _cookbook_dir(repo_root: Path) -> Optional[Path]:
    """The cookbook the upgrade works on. A format-2 `.cookr.json` names it with
    `cookbook`, which must stay inside the repo and hold a cookbook already: the
    upgrade never makes up a cookbook (a new identity) where the config points."""
    from .roots import _is_cookbook

    path = repo_root / CONFIG_NAME
    config = _json(path)
    # A malformed `format` ("2", 2.0) raises here, before anything reads the
    # config as format 1 and rewrites it.
    if config is not None and config_format(config, path) == FORMAT_2:
        cb = cookbook_dir_named(repo_root, config, path)
        if not _is_cookbook(cb):
            raise UpgradeError(f"{path}: `cookbook` names {config.get('cookbook', COOKBOOK_DIR)}, "
                               f"which holds no cookbook; point `cookbook` at the cookbook "
                               f"directory, then rerun")
        return cb
    cb = repo_root / COOKBOOK_DIR
    if _is_cookbook(cb) or (repo_root / CONFIG_NAME).is_file():
        return cb
    return None


def needs_upgrade(repo_root: Path) -> list[Path]:
    """The repo's own cookbook dir when anything in it (or the repo config) is
    not format 2, or the repo still has a legacy `.cookr.json` or recipes dir."""
    repo_root = Path(repo_root)
    cb = _cookbook_dir(repo_root)
    if cb is None:
        return []
    raw = _json(repo_root / CONFIG_NAME)
    stale = (
        _format(cb / MANIFEST) != FORMAT_2
        or _format(cb / INDEX_FILE) != FORMAT_2
        or (raw is not None and raw.get("format") != FORMAT_2)
        or (cb.is_dir() and any(_format(f / ARTIFACT_FILE) != FORMAT_2
                                for f in find_folders([cb])))
        or (cb.is_dir() and any(not (folder_for(d) / ARTIFACT_FILE).is_file()
                                for d in find_documents([cb])))
    )
    return [cb] if stale else []


def derive_index(cookbook_dir: Path) -> Index:
    """The index of a format-1 cookbook, in memory, by the upgrade's rules.
    Raises NeedsUpgrade when the cookbook has no id to derive from."""
    cookbook_dir = Path(cookbook_dir)
    if _format(cookbook_dir / INDEX_FILE) == FORMAT_2:
        try:
            return load_index(cookbook_dir)
        except IndexFileError:
            pass
    plan = _make_plan(cookbook_dir.parent, cookbook_dir, rdid=None, derive=True)
    return plan.index


def _dirty(repo_root: Path) -> list[str]:
    """Every changed or untracked path, exactly: NUL-separated, so spaces and
    quoting survive; every untracked file, whatever status.showUntrackedFiles
    says; both sides of a rename or copy."""
    proc = _git(repo_root, "status", "--porcelain", "-z", "--untracked-files=all")
    if proc.returncode != 0:
        raise UpgradeError(f"{repo_root} is not a git work tree; cookr upgrade needs one so "
                           "every change can be reviewed and undone: put the cookbook in a git "
                           "repo with a clean work tree, then rerun")
    fields = proc.stdout.split("\0")
    out, i = [], 0
    while i < len(fields):
        entry = fields[i]
        i += 1
        if len(entry) < 4:
            continue
        out.append(entry[3:])
        if "R" in entry[:2] or "C" in entry[:2]:
            if i < len(fields) and fields[i]:
                out.append(fields[i])  # the rename's or copy's source path
            i += 1
    return out


def upgrade(repo_root: Path, *, rdid: Optional[str] = None,
            dry_run: bool = False) -> list[UpgradeReport]:
    repo_root = Path(repo_root).resolve()
    targets = needs_upgrade(repo_root)
    if not targets:
        return []
    if not dry_run:
        dirty = _dirty(repo_root)
        if dirty:
            raise DirtyTree(dirty)
    reports = []
    for cb in targets:
        plan = _make_plan(repo_root, cb, rdid=rdid, derive=False)
        _rewrite_links(plan)
        if not dry_run:
            _write(plan, plan.scheme)
        reports.append(plan.report)
    return reports
