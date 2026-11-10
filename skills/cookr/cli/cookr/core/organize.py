"""Place a flat `.cookr.json` corpus's recipes in a library cookbook.

`plan` reads a legacy `.cookr.json` and its flat recipes directory and proposes
where each recipe goes: a path in `cookbook/` that mirrors the code it
describes. Only the upgrader (core/upgrade.py) uses it, to move a legacy
corpus into the format-2 cookbook.

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
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from cookr.core import refimpl
from cookr.core.markdown import iter_markdown, reserved_name

from .inventory import Component, component_stem, group_parts, join_name
from .legacy import CONFIG_NAME, LegacyConfig, legacy_scan
from .naming import path_name
from .repoconfig import COOKBOOK_DIR, PLATFORMS, ConfigError


PLAN_VERSION = 1


class OrganizeError(ConfigError):
    """Raised when a plan cannot be made."""


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
    return reserved_name(name) is not None


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


def _legacy_recipes(recipes_dir: Path) -> dict[str, Path]:
    """Every flat recipe doc, keyed by its path below `recipes_dir` without `.md`."""
    return {md.relative_to(recipes_dir).with_suffix("").as_posix(): md
            for md in iter_markdown(recipes_dir)}


def plan(config: LegacyConfig) -> dict:
    """The proposed conversion of `config`'s repo, as editable JSON."""
    comps = legacy_scan(config)
    corpus = _legacy_recipes(config.recipes_dir)
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
        "moves": [{"from": corpus[m.slug].relative_to(config.repo_root).as_posix(),
                   "to": m.to,
                   "implementations": [{"platform": r.platform, "path": r.path}
                                       for r in m.implementations]}
                  for m in sorted(moves, key=lambda m: m.to)],
        "unmatched": sorted(m.slug for m in moves if not m.implementations),
    }
