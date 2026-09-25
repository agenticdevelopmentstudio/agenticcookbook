"""Convert a flat `.cookr.json` corpus into a library cookbook, in two steps.

`plan` reads `.cookr.json` and its flat recipes directory and proposes where
each recipe goes: a path in `cookbook/` that mirrors the code it describes.
The plan is JSON, meant to be read and edited before `apply` carries it out.

Where a recipe goes, from its sources (the old scan's files for it):

- Each platform's root paths share a directory prefix (the library's own
  directory, `packages/apple/AgenticToolkit`); a source's group is its
  directories below that prefix, kebab-cased, with `src`/`Sources` dropped.
- One source file: `<group of its directory>/<its stem>`.
- Several source files that are every source file of their common directory:
  the directory is the module and the recipe claims it with a `dir/` row,
  named `<group of that directory>`.
- Otherwise: `<group of their common directory>/<the old slug without its tier>`,
  each file its own row.
- The platform with the most sources decides the name; the other platforms'
  sources are extra rows.
- A recipe with no sources goes to the top level, named by its old slug
  without its tier. A name two recipes share, or one the corpus skips
  (`index`), becomes `<group>/<old slug>`.

`apply` moves each recipe with `git mv`, points its `domain` at its new path,
writes its Reference Implementations, rewrites every reference to its old
domain or path across the repo's tracked markdown, patch-bumps it, writes
`cookbook/cookbook.json` from the plan's `code` block, and removes
`.cookr.json`.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Optional

from cookbook import __version__ as COOKBOOK_VERSION
from cookbook.core import refimpl
from cookbook.core.markdown import SKIP_NAMES
from cookbook.core.scheme import repo_scheme
from cookbook.modules import bump

from .config import COOKBOOK_DIR, KINDS, MANIFEST, PLATFORMS, ConfigError
from .inventory import Component, component_stem, group_parts, join_name
from .legacy import CONFIG_NAME, LegacyConfig, legacy_scan
from .naming import path_name
from .recipes import load_corpus

PLAN_VERSION = 1
COOKBOOK_REPO = "https://github.com/agenticdevelopercookbook/cookbook"
BUMP_SUMMARY = "Moved into the library cookbook; added Reference Implementations."


class OrganizeError(ConfigError):
    """Raised when a plan cannot be made or applied."""


# ---- plan -----------------------------------------------------------------------------------

def _parts(path: str) -> list[str]:
    return [p for p in path.split("/") if p]


def _common(paths: list[list[str]]) -> list[str]:
    out = []
    for column in zip(*paths):
        if len(set(column)) != 1:
            break
        out.append(column[0])
    return out


def platform_prefixes(config: LegacyConfig) -> dict[str, list[str]]:
    """Per platform, the directory its roots share, never a root itself:
    the library's own directory, below which the groups start."""
    out = {}
    for platform in {r.platform for r in config.roots}:
        roots = [_parts(r.path) for r in config.roots if r.platform == platform]
        common = _common(roots)
        if any(common == r for r in roots):
            common = common[:-1]
        out[platform] = common
    return out


def _strip_tier(slug: str, tiers: list[str]) -> str:
    """`slug` without the longest old tier it starts with; `slug` when that leaves nothing."""
    for tier in sorted(tiers, key=len, reverse=True):
        if slug.startswith(tier + "-") and len(slug) > len(tier) + 1:
            return slug[len(tier) + 1:]
    return slug


@dataclass
class Move:
    slug: str  # the old recipe's file stem
    to: str  # its spec name in the cookbook
    implementations: list = field(default_factory=list)  # [refimpl.Implementation]
    group: list = field(default_factory=list)  # the name's directories, for the fallback


class _Namer:
    def __init__(self, config: LegacyConfig, comps: list[Component]):
        self.config = config
        self.prefixes = platform_prefixes(config)
        self.tiers = config.tiers
        self.by_dir: dict[str, set[str]] = {}  # every directory -> every source path below it
        for c in comps:
            parts = _parts(c.path)
            for i in range(1, len(parts)):
                self.by_dir.setdefault("/".join(parts[:i]), set()).add(c.path)

    def group(self, dir_parts: list[str], platform: str) -> list[str]:
        prefix = self.prefixes.get(platform, [])
        below = dir_parts[len(prefix):] if dir_parts[:len(prefix)] == prefix else dir_parts
        return group_parts(below)

    def rows(self, paths: list[str], platform: str) -> tuple[list, Optional[list[str]]]:
        """The Reference Implementations rows for one platform's sources, and the
        module directory's parts when they are one whole directory."""
        common = _common([_parts(p)[:-1] for p in paths])
        if len(paths) > 1 and common and self.by_dir.get("/".join(common)) == set(paths):
            return [refimpl.Implementation(platform, "/".join(common) + "/")], common
        return [refimpl.Implementation(platform, p) for p in sorted(paths)], None

    def move(self, slug: str, comps: list[Component]) -> Move:
        if not comps:
            return Move(slug, _strip_tier(slug, self.tiers))
        counts = Counter(c.platform for c in comps)
        order = sorted(counts, key=lambda p: (-counts[p], PLATFORMS.index(p)))
        rows, name = [], []
        for platform in order:
            paths = sorted({c.path for c in comps if c.platform == platform})
            got, module = self.rows(paths, platform)
            rows += got
            if name:
                continue
            if module is not None and self.group(module, platform):
                name = self.group(module, platform)
            elif len(paths) == 1:
                parts = _parts(paths[0])
                name = join_name(self.group(parts[:-1], platform), path_name(component_stem(parts[-1])))
            else:
                common = _common([_parts(p)[:-1] for p in paths])
                tier = Counter(c.tier for c in comps if c.platform == platform).most_common(1)[0][0]
                name = join_name(self.group(common, platform), _strip_tier(slug, [tier] + self.tiers))
        return Move(slug, "/".join(name), rows, name[:-1])



def _reserved(name: str) -> bool:
    return f"{name.rsplit('/', 1)[-1]}.md" in SKIP_NAMES


def _dedupe(moves: list[Move]) -> None:
    """A name two recipes share, or one the corpus skips, becomes `<group>/<old slug>`."""
    counts = Counter(m.to for m in moves)
    for m in moves:
        if counts[m.to] > 1 or _reserved(m.to):
            m.to = "/".join(m.group + [m.slug])
    counts = Counter(m.to for m in moves)
    clash = sorted(n for n, k in counts.items() if k > 1)
    if clash:
        raise OrganizeError(f"recipes still share a name after the fallback: {', '.join(clash)}")


def code_block(config: LegacyConfig) -> dict:
    """`cookbook.json`'s `code` block: the old roots, each with the group its
    unclaimed files land in."""
    prefixes = platform_prefixes(config)
    roots = []
    for r in config.roots:
        parts = _parts(r.path)
        prefix = prefixes.get(r.platform, [])
        entry = {"path": r.path.strip("/"), "platform": r.platform, "kind": r.kind,
                 "recipes": "/".join(group_parts(parts[len(prefix):]))}
        if r.ignore:
            entry["ignore"] = list(r.ignore)
        roots.append(entry)
    return {"roots": roots, "ignore": list(config.ignore)}


def plan(config: LegacyConfig) -> dict:
    """The proposed conversion of `config`'s repo, as editable JSON."""
    comps = legacy_scan(config)
    corpus = load_corpus(config.recipes_dir)
    by_recipe: dict[str, list[Component]] = {}
    for c in comps:
        by_recipe.setdefault(config.aliases.get(c.name, c.name), []).append(c)
    namer = _Namer(config, comps)
    moves = [namer.move(slug, by_recipe.get(slug, [])) for slug in sorted(corpus)]
    _dedupe(moves)
    return {
        "version": PLAN_VERSION,
        "legacy": CONFIG_NAME,
        "recipes": config.recipes,
        "scheme": config.scheme,
        "cookbook": COOKBOOK_DIR,
        "code": code_block(config),
        "moves": [{"from": corpus[m.slug].path.relative_to(config.repo_root).as_posix(),
                   "to": m.to,
                   "implementations": [{"platform": r.platform, "path": r.path}
                                       for r in m.implementations]}
                  for m in sorted(moves, key=lambda m: m.to)],
        "unmatched": sorted(m.slug for m in moves if not m.implementations),
    }


# ---- apply ----------------------------------------------------------------------------------

@dataclass
class Applied:
    moved: int = 0
    rewritten: list = field(default_factory=list)  # repo-relative files whose references changed
    bump_failures: list = field(default_factory=list)  # (file, reason)
    manifest: str = ""
    leftovers: list = field(default_factory=list)  # files left in the old recipes directory


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise OrganizeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*(/[a-z0-9][a-z0-9._-]*)*$")


def validate(data: dict, repo_root: Path) -> None:
    """Refuse a plan `apply` cannot carry out, before anything is touched."""
    if data.get("version") != PLAN_VERSION:
        raise OrganizeError(f"plan version must be {PLAN_VERSION}")
    for key in ("recipes", "scheme", "cookbook", "legacy"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise OrganizeError(f"plan `{key}` must be a non-empty string")
    if (repo_root / data["cookbook"] / MANIFEST).exists():
        raise OrganizeError(f"{data['cookbook']}/{MANIFEST} already exists; this repo is organized")
    code = data.get("code")
    if not isinstance(code, dict) or not isinstance(code.get("roots"), list) or not code["roots"]:
        raise OrganizeError("plan `code.roots` must be a non-empty list")
    for i, r in enumerate(code["roots"]):
        if r.get("platform") not in PLATFORMS or r.get("kind", "ui") not in KINDS:
            raise OrganizeError(f"plan code.roots[{i}] has a bad platform or kind")
        if not (repo_root / str(r.get("path", ""))).is_dir():
            raise OrganizeError(f"plan code.roots[{i}].path not found: {r.get('path')}")
    moves = data.get("moves")
    if not isinstance(moves, list):
        raise OrganizeError("plan `moves` must be a list")
    names = Counter()
    for m in moves:
        src, to = m.get("from", ""), m.get("to", "")
        if not (repo_root / src).is_file():
            raise OrganizeError(f"plan move source not found: {src}")
        if not isinstance(to, str) or not _NAME.match(to) or ".." in to.split("/"):
            raise OrganizeError(f"plan move target `{to}` is not a lowercase path in the cookbook")
        if _reserved(to):
            raise OrganizeError(f"plan move target `{to}` is a file name the corpus skips")
        names[to] += 1
        for impl in m.get("implementations", []):
            if impl.get("platform") not in PLATFORMS:
                raise OrganizeError(f"{to}: bad platform `{impl.get('platform')}`")
            if not (repo_root / impl.get("path", "")).exists():
                raise OrganizeError(f"{to}: implementation not found: {impl.get('path')}")
    clash = sorted(n for n, k in names.items() if k > 1)
    if clash:
        raise OrganizeError(f"plan moves share a target: {', '.join(clash)}")


def _set_domain(text: str, domain: str) -> str:
    """`text` with its frontmatter `domain` set, the line added (after `id`) when absent."""
    line = f"domain: {domain}"
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 3)
    if end < 0:
        return text
    head, rest = text[:end], text[end:]
    if re.search(r"(?m)^domain:", head):
        return re.sub(r"(?m)^domain:.*$", lambda _: line, head, count=1) + rest
    after_id = re.search(r"(?m)^id:.*$", head)
    at = after_id.end() if after_id else len("---")
    return head[:at] + "\n" + line + head[at:] + rest


_LINK = re.compile(r"\]\(([^)\s#]+\.md)(#[^)\s]*)?\)")


def _rel(target: PurePosixPath, start: PurePosixPath) -> str:
    return PurePosixPath(os.path.relpath(target.as_posix(), start.as_posix() or ".")).as_posix()


def _normal(path: PurePosixPath) -> PurePosixPath:
    return PurePosixPath(os.path.normpath(path.as_posix()))


def rewrite_references(text: str, *, old_file: str, new_file: str,
                       moved: dict[str, str], domains: dict[str, str], recipes: str) -> str:
    """`text` (the file `old_file`, now at `new_file`) with every reference to a
    moved recipe pointing at its new place: old domains, relative `.md` links
    (and the same string anywhere else in the file, such as a link's backticked
    text), and bare repo-relative `<recipes>/<slug>.md` mentions."""
    if domains:
        pattern = re.compile("(" + "|".join(re.escape(d) for d in
                                            sorted(domains, key=len, reverse=True)) + r")(?![\w-])")
        text = pattern.sub(lambda m: domains[m.group(1)], text)

    old_dir, new_dir = PurePosixPath(old_file).parent, PurePosixPath(new_file).parent
    swaps: dict[str, str] = {}
    for m in _LINK.finditer(text):
        ref = m.group(1)
        if "://" in ref or ref.startswith("/"):
            continue
        target = _normal(old_dir / ref).as_posix()
        dest = moved.get(target, target)
        if dest == target and old_dir == new_dir:
            continue
        new_ref = _rel(PurePosixPath(dest), new_dir)
        if new_ref != ref:
            swaps[ref] = new_ref
    for ref in sorted(swaps, key=len, reverse=True):
        text = re.sub(rf"(?<![\w./-]){re.escape(ref)}", lambda _, r=ref: swaps[r], text)

    bare = {k: v for k, v in moved.items() if k.startswith(recipes + "/")}
    if bare:
        pattern = re.compile(r"(?<![\w./-])(" + "|".join(re.escape(k) for k in
                                                          sorted(bare, key=len, reverse=True)) + r")(?![\w-])")
        text = pattern.sub(lambda m: bare[m.group(1)], text)
    return text


def _manifest(data: dict, repo_root: Path, author: str, day: str) -> dict:
    platforms = sorted({r["platform"] for r in data["code"]["roots"]})
    name = repo_root.name
    return {
        "$schema": f"{COOKBOOK_REPO}/blob/main/cookbook/reference/cookbook.schema.json",
        "type": "cookbook",
        "schema_version": "1.0.0",
        "name": name,
        "id": str(uuid.uuid4()),
        "version": "1.0.0",
        "description": f"Specs for {name}'s shared code, arranged as the code is.",
        "author": author,
        "license": "MIT",
        "created": day,
        "modified": day,
        "platforms": platforms,
        "cookbook": {"repo": COOKBOOK_REPO, "version": COOKBOOK_VERSION},
        "structure": {"name": name, "kind": "library"},
        "code": data["code"],
    }


def apply(data: dict, repo_root: Path, *, author: str = "", day: Optional[str] = None) -> Applied:
    """Carry out plan `data` in the git work tree at `repo_root`."""
    validate(data, repo_root)
    day = day or date.today().isoformat()
    author = author or bump._git_user(repo_root)
    cookbook = data["cookbook"].strip("/")
    new_scheme = data["scheme"]
    result = Applied()

    moved: dict[str, str] = {}  # old repo-relative file -> new
    domains: dict[str, str] = {}  # old domain -> new
    for m in data["moves"]:
        new = f"{cookbook}/{m['to']}.md"
        moved[m["from"]] = new
        slug = PurePosixPath(m["from"]).with_suffix("").as_posix()
        domains[f"{data['scheme']}://{slug}"] = f"{new_scheme}://{cookbook}/{m['to']}"

    for old, new in moved.items():
        (repo_root / new).parent.mkdir(parents=True, exist_ok=True)
        _git(repo_root, "mv", old, new)
        result.moved += 1
    back = {new: old for old, new in moved.items()}

    tracked = [p for p in _git(repo_root, "ls-files", "-z", "--", "*.md").split("\0") if p]
    for rel in tracked:
        path = repo_root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        new_text = rewrite_references(text, old_file=back.get(rel, rel), new_file=rel,
                                      moved=moved, domains=domains, recipes=data["recipes"])
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", errors="surrogateescape")
            result.rewritten.append(rel)

    for m in data["moves"]:
        new = repo_root / moved[m["from"]]
        text = new.read_text(encoding="utf-8")
        text = _set_domain(text, f"{new_scheme}://{cookbook}/{m['to']}")
        rows = [refimpl.Implementation(i["platform"], i["path"]) for i in m.get("implementations", [])]
        new.write_text(refimpl.with_section(text, rows), encoding="utf-8")
        try:
            new.write_text(bump.plan(new, level="patch", summary=BUMP_SUMMARY, author=author,
                                     day=day).text, encoding="utf-8")
        except bump.BumpError as e:
            result.bump_failures.append((moved[m["from"]], str(e)))

    manifest = repo_root / cookbook / MANIFEST
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(_manifest(data, repo_root, author, day), indent=2) + "\n",
                        encoding="utf-8")
    result.manifest = manifest.relative_to(repo_root).as_posix()
    if new_scheme != repo_scheme(repo_root):
        # The cookbook's scheme is its index.md's, else the repo's name.
        (repo_root / cookbook / "index.md").write_text(
            f"---\ndomain: {new_scheme}://index\n---\n", encoding="utf-8")

    _git(repo_root, "rm", "-q", data["legacy"])
    recipes_dir = repo_root / data["recipes"]
    if (recipes_dir / ".gitkeep").is_file():
        _git(repo_root, "rm", "-q", f"{data['recipes']}/.gitkeep")
    if recipes_dir.is_dir():
        result.leftovers = sorted(p.relative_to(repo_root).as_posix()
                                  for p in recipes_dir.rglob("*") if p.is_file())
        if not result.leftovers:
            for d in sorted(recipes_dir.rglob("*"), reverse=True):
                d.rmdir()
            recipes_dir.rmdir()
    return result
