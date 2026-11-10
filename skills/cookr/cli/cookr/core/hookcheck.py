"""The deterministic check behind `cookr check --hook` (spec section 7).

Given the files a change set touches, it says what recipe work is still owed:

stage       (--staged only) a path the rules read differs between the git index and
            the working tree
update      code covered by artifact X changed (or was deleted) and nothing in X's
            own folder did
create      an added or modified file in a root that no artifact covers
validate    a touched implementation does not end the set `confirmed` at its
            recipe's current version
dependency  a changed artifact lists a `depends-on` link that is missing or malformed
bump        an artifact's content changed since the base but its version did not

A dependency in an unreachable cookbook is not a finding (spec section 3: a
warning); `analyze` returns those apart. Findings are unique per kind and
subject and ordered by kind, then subject.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .artifact import ARTIFACT_FILE, ArtifactError, is_folder, load_folder
from .changes import Change, split_rename
from .errors import CookbookError
from .conformance import current_hash, effective_state, entry_version, is_missing
from .history import parse_version
from .index import Entry, Index, parse_index
from .inventory import ignored_for
from .links import Resolver
from .markdown import in_versions
from .repoconfig import Config
from .scope import WALKED, in_frozen_version, link_state
from .versions import base_text, file_at, git, has_commit, compose_files, content_changed, folder_files, version_of

KINDS = ("stage", "update", "create", "validate", "dependency", "bump")


@dataclass(frozen=True)
class Finding:
    kind: str
    subject: str
    message: str


@dataclass
class Analysis:
    findings: list[Finding] = field(default_factory=list)
    unreachable: list[str] = field(default_factory=list)


def _folder_prefix(config: Config, entry: Entry) -> str:
    base = config.cookbook
    return entry.path if base == "." else f"{base}/{entry.path}"


def _touched_artifacts(config: Config, index: Index, paths: set[str]) -> dict[str, Entry]:
    """Artifacts whose own `artifact.json` or part files are among `paths`
    (never a `versions/` freeze, never a file in a subdirectory)."""
    by_folder = {_folder_prefix(config, e): e for e in index.entries.values() if "#" not in e.path}
    touched: dict[str, Entry] = {}
    for path in paths:
        folder, _, name = path.rpartition("/")
        entry = by_folder.get(folder)
        if entry is not None and (name == ARTIFACT_FILE or name.endswith(".md")):
            touched[entry.id] = entry
    return touched


def _pure_rename_absorbed(index: Index, change: Change) -> bool:
    """A 100% rename whose new path is covered and whose old path is no longer
    claimed apart from by the same rows: the index location was updated (or a
    directory row covers both), which is what `relink` absorbs."""
    new = {e.id for e, _ in index.owners(change.path)}
    old = {e.id for e, _ in index.owners(change.old_path or "")}
    return bool(new) and (not old or old == new)


def _version_past(new: str, old: str) -> bool:
    a, b = parse_version(new), parse_version(old)
    if a is None:
        return False
    return b is None or a > b


def analyze(config: Config, index: Index, resolver: Resolver, changes: list[Change],
            base: str, base_index: Optional[Index] = None) -> Analysis:
    out: dict[tuple[str, str], Finding] = {}

    def add(kind: str, subject: str, message: str) -> None:
        out.setdefault((kind, subject), Finding(kind, subject, message))

    def validate(entry: Entry, impl) -> None:
        version = entry_version(config.cookbook_dir, entry)
        state = effective_state(impl, version, current_hash(config, impl),
                                is_missing(config, impl))
        if state != "confirmed":
            seen = impl.conformance.version
            msg = f"validate {entry.rdid} against {version or 'its current version'}"
            if seen and seen != version:
                msg += f" (see `cookr diff {entry.rdid} {seen}`)"
            add("validate", entry.rdid, msg)

    cookbook_prefix = "" if config.cookbook == "." else config.cookbook + "/"

    flat: list[Change] = []
    for change in changes:
        flat.extend(split_rename(change, lambda p: config.root_for(p) is not None))
    all_paths = {c.path for c in flat} | {c.old_path for c in flat if c.old_path}
    touched = _touched_artifacts(
        config, index, {p for p in all_paths
                         if not in_versions(config.repo_root / p, config.repo_root)})

    # --- code files: update / create / validate -------------------------------
    for change in flat:
        if change.status == "R" and _pure_rename_absorbed(index, change):
            continue
        sides = ([Change("D", change.old_path), Change("A", change.path)]
                 if change.status == "R" else [change])
        for c in sides:
            root = config.root_for(c.path)
            if root is None or (cookbook_prefix and c.path.startswith(cookbook_prefix)) \
                    or in_frozen_version(config, c.path) \
                    or ignored_for(config, root).ignores(c.path):
                continue
            owners = index.owners(c.path)
            if c.status == "D" and base_index is not None:
                have = {(e.id, i.platform, i.location) for e, i in owners}
                owners = owners + [(e, i) for e, i in base_index.owners(c.path)
                                   if (e.id, i.platform, i.location) not in have]
            if not owners:
                if c.status != "D":
                    add("create", c.path, f"create a recipe covering {c.path} "
                        "(or claim it into an existing recipe with `cookr implements` "
                        "and update that recipe)")
                continue
            for entry, impl in owners:
                if entry.kind not in WALKED:
                    continue                      # rules, not code: no recipe work owed
                # An artifact gone from the index had its folder deleted: touched.
                if entry.id not in touched and entry.id in index.entries:
                    add("update", entry.rdid,
                        f"update {entry.rdid}: {c.path} was "
                        f"{'deleted' if c.status == 'D' else 'changed'} and the recipe was not")
                if c.status != "D" and entry.id in index.entries:
                    validate(entry, impl)

    # --- claimed rows: present now, absent from the base index ----------------
    if base_index is not None:
        before = {(e.id, i.platform, i.location)
                  for e in base_index.entries.values() for i in e.implementations}
        for entry in index.entries.values():
            if entry.kind not in WALKED:
                continue
            for impl in entry.implementations:
                if impl.location and "://" not in impl.location \
                        and (entry.id, impl.platform, impl.location) not in before:
                    validate(entry, impl)

    # --- changed artifacts: dependencies and version bumps --------------------
    unreachable: list[str] = []
    own_id = index.cookbook.id
    for entry in sorted(touched.values(), key=lambda e: e.rdid):
        folder = config.cookbook_dir / entry.path
        if not is_folder(folder):
            continue
        try:
            meta = load_folder(folder).meta
        except (ArtifactError, OSError) as e:
            raise CookbookError(f"{entry.rdid}: cannot read its source folder: {e}") from e
        for raw in meta.get("depends-on") or []:
            state = link_state(resolver, own_id, str(raw))
            if state in ("missing", "unresolvable"):
                add("dependency", f"{entry.rdid} -> {raw}",
                    f"create or fix dependency {raw} of {entry.rdid} ({state})")
            elif state == "unreachable":
                unreachable.append(f"{entry.rdid} depends on {raw}, in a cookbook that "
                                   "cannot be reached")
        if not base:
            continue
        files = folder_files(folder)
        try:
            old = base_text(config.repo_root, folder, base)
            if old is None or files is None:
                continue                              # new at the base: nothing to bump
            new = compose_files(files)
            changed = content_changed(old, new)
        except ArtifactError as e:
            raise CookbookError(f"{entry.rdid}: cannot compare with the base: {e}") from e
        if changed and not _version_past(version_of(new), version_of(old)):
            add("bump", entry.rdid, f"bump {entry.rdid}: its content changed since the "
                f"base but its version is still {version_of(new) or 'unset'} (cookr bump)")

    return Analysis(ordered(list(out.values())), sorted(set(unreachable)))


def run(config: Config, index: Index, resolver: Resolver, changes: list[Change],
        base: str, base_index: Optional[Index] = None) -> list[Finding]:
    """The findings for a change set; `base` is the commit to compare versions
    with ("" skips the bump rule); `base_index` is the cookbook index there, if any."""
    return analyze(config, index, resolver, changes, base, base_index).findings


def base_index_at(config: Config, ref: str) -> Optional[Index]:
    """The cookbook's `index.json` as of `ref`; None when there is no such commit,
    no index there, or one that is unparseable or not format 2."""
    if not ref or not has_commit(config.repo_root, ref):
        return None
    rel = "index.json" if config.cookbook == "." else f"{config.cookbook}/index.json"
    data = file_at(config.repo_root, ref, rel)
    if data is None:
        return None
    try:
        return parse_index(data.decode("utf-8"), f"{ref}:{rel}")
    except (CookbookError, UnicodeDecodeError):
        return None


def staged_divergence(config: Config, index: Index, base_index: Optional[Index],
                      changes: list[Change]) -> list[Finding]:
    """For a staged check: every path the rules read (changed paths, the folders
    and locations of what owns them, `index.json`) that differs between the git
    index and the working tree. The check must never read the working tree as if
    it were the commit."""
    cb = config.cookbook
    paths = {"index.json" if cb == "." else f"{cb}/index.json"}
    for c in changes:
        for p in (c.path, c.old_path):
            if not p:
                continue
            paths.add(p)
            owners = index.owners(p) + (base_index.owners(p) if base_index else [])
            for entry, impl in owners:
                if impl.location:
                    paths.add(impl.location)
                if "#" not in entry.path and entry.id in index.entries:
                    paths.add(entry.path if cb == "." else f"{cb}/{entry.path}")
    # Touched artifacts' own folders are read for dependencies and bumps.
    for entry in _touched_artifacts(config, index, paths).values():
        paths.add(entry.path if cb == "." else f"{cb}/{entry.path}")
    raw = git(config.repo_root, "--literal-pathspecs", "diff", "--name-only", "-z",
              "--", *sorted(paths))
    diverged = sorted(p for p in raw.decode("utf-8", "surrogateescape").split("\0") if p)
    return [Finding("stage", p, f"stage or revert {p} first") for p in diverged]


def ordered(findings: list[Finding]) -> list[Finding]:
    order = {k: i for i, k in enumerate(KINDS)}
    return sorted(findings, key=lambda f: (order[f.kind], f.subject))
