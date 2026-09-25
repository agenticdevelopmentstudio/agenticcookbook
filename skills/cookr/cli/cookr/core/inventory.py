"""Walk the configured roots and list component source files.

Ignore patterns are globs over repo-relative POSIX paths, with globstar
semantics: `*` and `?` never cross `/`, `[...]` is a character class, and a
`**` path segment matches zero or more whole directories (`**/x` at any depth,
`a/**/b` with or without directories between, `a/**` everything below `a`).

A file's component name is its file name with every trailing source suffix
dropped, kebab-cased: `StatCard.xaml` and its code-behind `StatCard.xaml.cs`
are both `stat-card`.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

from cookbook.core.markdown import SKIP_NAMES

from .config import Config, ConfigError
from .naming import kebab

SOURCE_SUFFIXES = (".tsx", ".ts", ".swift", ".kt", ".cs", ".xaml", ".py")


@dataclass(frozen=True)
class Component:
    name: str
    path: str
    tier: str
    platform: str
    kind: str = "ui"


def _segment_regex(seg: str) -> str:
    out, i, n = [], 0, len(seg)
    while i < n:
        c = seg[i]
        if c == "*":
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c == "[":
            j = i + 1
            if j < n and seg[j] in "!^":
                j += 1
            if j < n and seg[j] == "]":
                j += 1
            while j < n and seg[j] != "]":
                j += 1
            if j >= n:  # no closing bracket: a literal `[`
                out.append(re.escape(c))
            else:
                body = seg[i + 1:j]
                neg = body[:1] in ("!", "^")
                if neg:
                    body = body[1:]
                body = body.replace("\\", "\\\\")
                out.append(f"[{'^/' if neg else ''}{body}]")
                i = j
        else:
            out.append(re.escape(c))
        i += 1
    return "".join(out)


def glob_regex(pattern: str) -> str:
    """The regex (for `fullmatch`) of one ignore glob; see the module docstring."""
    parts = pattern.split("/")
    out = []
    for i, seg in enumerate(parts):
        last = i == len(parts) - 1
        if seg == "**":
            out.append(".*" if last else "(?:[^/]+/)*")
        else:
            out.append(_segment_regex(seg) + ("" if last else "/"))
    return "".join(out)


def _compile(regexes: list[str]) -> Optional[re.Pattern]:
    return re.compile("|".join(f"(?:{r})" for r in regexes)) if regexes else None


@dataclass(frozen=True)
class IgnoreSet:
    files: Optional[re.Pattern]  # matches an ignored file path
    dirs: Optional[re.Pattern]   # matches a directory whose whole subtree is ignored

    def ignores(self, rel: str) -> bool:
        return self.files is not None and self.files.fullmatch(rel) is not None

    def prunes(self, rel_dir: str) -> bool:
        return self.dirs is not None and self.dirs.fullmatch(rel_dir) is not None


@lru_cache(maxsize=None)
def ignore_set(patterns: tuple) -> IgnoreSet:
    # `X/**` ignores every path below any directory matching X, so the walk can
    # skip that directory outright; a bare `**` ignores everything.
    dirs = [glob_regex(p[:-3]) if p != "**" else ".*"
            for p in patterns if p == "**" or p.endswith("/**")]
    return IgnoreSet(files=_compile([glob_regex(p) for p in patterns]), dirs=_compile(dirs))


def component_stem(filename: str) -> str:
    stem = filename
    while True:
        base, dot, suffix = stem.rpartition(".")
        if not dot or not base or f".{suffix}" not in SOURCE_SUFFIXES:
            return stem
        stem = base


def _reserved(slug: str) -> bool:
    """True when `<slug>.md` is a name the recipe corpus never loads."""
    return f"{slug}.md" in SKIP_NAMES


def scan(config: Config, tier: Optional[str] = None) -> list[Component]:
    """Every component source file under the configured roots (only `tier`'s roots when given).

    Raises ConfigError when a component resolves to a recipe file name the
    corpus skips (`index`, `references`, ...): its recipe could never be
    matched, so the config must ignore, rename or alias it.
    """
    out = []
    for root in config.roots:
        if tier is not None and root.tier != tier:
            continue
        ignored = ignore_set(tuple(config.ignore) + tuple(root.ignore))
        base = config.repo_root / root.path
        for dirpath, dirnames, filenames in os.walk(base):
            d = Path(dirpath)
            drel = d.relative_to(config.repo_root).as_posix()
            prefix = "" if drel == "." else f"{drel}/"
            dirnames[:] = [n for n in dirnames if not ignored.prunes(prefix + n)]
            for fn in filenames:
                if os.path.splitext(fn)[1] not in SOURCE_SUFFIXES:
                    continue
                rel = prefix + fn
                if ignored.ignores(rel) or not (d / fn).is_file():
                    continue
                name = config.renames.get(rel, kebab(component_stem(fn)))
                out.append(Component(name=name, path=rel, tier=root.tier, platform=root.platform,
                                     kind=root.kind))
    reserved = sorted(c.path for c in out if _reserved(config.aliases.get(c.name, c.name)))
    if reserved:
        raise ConfigError(
            "component name resolves to a file name the recipe corpus skips "
            f"({', '.join(sorted(SKIP_NAMES))}), so its recipe could never be matched: "
            f"{', '.join(reserved)}. Ignore these files, or give them a name in `renames` "
            f"or `aliases`."
        )
    return sorted(out, key=lambda c: (c.tier, c.name, c.path))
