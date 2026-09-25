"""Every component source file, and the spec that names it.

A spec claims its sources in its `## Reference Implementations` table
(`cookbook.core.refimpl`): a file path claims that file, a directory path
(trailing `/`) every source file below it. A file path beats any directory
path, and the deepest directory wins, so a spec for a module directory can
leave one file inside it to another spec. A source file under a `code.roots`
entry that no spec claims is named where the code's arrangement puts it:
`<root.recipes>/<its directories below the root>/<its stem>`, kebab-cased
(`naming.path_name`), with `src` and `Sources` directories dropped. A stem
that repeats its directory's name, or is a reserved name like `index`, folds
into the directory (`join_name`): `data/docs/Docs.swift` is `data/docs`.

Ignore patterns are globs over repo-relative POSIX paths, with globstar
semantics: `*` and `?` never cross `/`, `[...]` is a character class, and a
`**` path segment matches zero or more whole directories (`**/x` at any depth,
`a/**/b` with or without directories between, `a/**` everything below `a`).
They drop a file found by walking (a root, or a claimed directory); a file a
spec names outright is never dropped.

A file's stem is its file name with every trailing source suffix dropped:
`StatCard.xaml` and its code-behind `StatCard.xaml.cs` are both `StatCard`.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

from cookbook.core.markdown import SKIP_NAMES

from .config import Config, ConfigError, Root
from .naming import path_name
from .recipes import RecipeInfo

SOURCE_SUFFIXES = (".tsx", ".ts", ".swift", ".kt", ".cs", ".xaml", ".py")
# Directories that hold a package's sources without naming anything.
SOURCE_DIRS = frozenset({"src", "Sources"})


@dataclass(frozen=True)
class Component:
    name: str
    path: str
    tier: str
    platform: str
    kind: str = "ui"
    claimed: bool = False  # a spec's Reference Implementations names it (or a directory above it)


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


def group_parts(dirs: list[str]) -> list[str]:
    """Code directory names as cookbook directory names: kebab-cased, `src` and
    `Sources` dropped."""
    return [path_name(d) for d in dirs if d not in SOURCE_DIRS and path_name(d)]


def join_name(group: list[str], leaf: str) -> list[str]:
    """`group` + `leaf`, except that a leaf repeating the group's last directory
    (`docs/docs.ts`) or one the corpus skips (`query/index.tsx`) names the group."""
    if group and (leaf == group[-1] or f"{leaf}.md" in SKIP_NAMES):
        return group
    return group + [leaf]


def expected_name(root: Root, rel: str) -> str:
    """Where the code's arrangement puts the spec for `rel` under `root`: a source
    file's own spec, or for a directory (trailing `/`) the module's."""
    parts = _below(root, rel.rstrip("/"))
    group = _split(root.recipes) + group_parts(parts if rel.endswith("/") else parts[:-1])
    if rel.endswith("/"):
        return "/".join(group)
    return "/".join(join_name(group, path_name(component_stem(parts[-1]))))


def _below(root: Root, rel: str) -> list[str]:
    return _split(rel[len(root.path):])


def _split(path: str) -> list[str]:
    return [p for p in path.split("/") if p]



def _walk(repo_root: Path, base: str, ignored: IgnoreSet):
    """Repo-relative source files below repo-relative directory `base`."""
    for dirpath, dirnames, filenames in os.walk(repo_root / base):
        d = Path(dirpath)
        drel = d.relative_to(repo_root).as_posix()
        prefix = "" if drel == "." else f"{drel}/"
        dirnames[:] = sorted(n for n in dirnames if not ignored.prunes(prefix + n))
        for fn in filenames:
            rel = prefix + fn
            if (os.path.splitext(fn)[1] in SOURCE_SUFFIXES and not ignored.ignores(rel)
                    and (d / fn).is_file()):
                yield rel


def _ignored(config: Config, root: Optional[Root]) -> IgnoreSet:
    return ignore_set(tuple(config.ignore) + (tuple(root.ignore) if root else ()))


Claims = dict[str, list[tuple[str, str]]]  # claimed path -> [(spec, platform)]


def claims(corpus: dict[str, RecipeInfo]) -> Claims:
    """Every path a spec's Reference Implementations names, with who names it."""
    out: Claims = {}
    for spec, info in sorted(corpus.items()):
        for impl in info.implementations:
            out.setdefault(impl.path, []).append((spec, impl.platform))
    return out


def owners(table: Claims, rel: str) -> list[tuple[str, str]]:
    """The claims on source file `rel`: its own path's, else its deepest directory's."""
    if rel in table:
        return table[rel]
    parts = rel.split("/")
    for i in range(len(parts) - 1, 0, -1):
        found = table.get("/".join(parts[:i]) + "/")
        if found:
            return found
    return []


def _reserved(name: str) -> bool:
    """True when `<name>.md` is a file name the spec corpus never loads."""
    return f"{name.rsplit('/', 1)[-1]}.md" in SKIP_NAMES


def in_group(name: str, tier: Optional[str]) -> bool:
    """True when spec `name` is in group `tier` (a cookbook directory; None is every group)."""
    return tier is None or name.startswith(tier.strip("/") + "/")


def scan(config: Config, corpus: dict[str, RecipeInfo],
         tier: Optional[str] = None) -> list[Component]:
    """Every component source file (only those whose spec is in group `tier` when given).

    A file claimed by several specs at once is one row per spec; coverage
    reports the clash. Raises ConfigError when an unclaimed file's name is a
    file name the corpus skips (`index`, `references`, ...): its spec could
    never be matched, so it must be ignored or claimed.
    """
    table = claims(corpus)
    found: dict[str, Optional[Root]] = {}  # rel -> the root holding it, if any
    for root in config.roots:
        for rel in _walk(config.repo_root, root.path, _ignored(config, root)):
            found.setdefault(rel, config.root_for(rel))
    for path in table:
        if path.endswith("/"):
            base = path.rstrip("/")
            if (config.repo_root / base).is_dir():
                for rel in _walk(config.repo_root, base, _ignored(config, config.root_for(base))):
                    found.setdefault(rel, config.root_for(rel))
        elif (config.repo_root / path).is_file():
            found.setdefault(path, config.root_for(path))

    out = []
    for rel, root in found.items():
        kind = root.kind if root is not None else "ui"
        claim = owners(table, rel)
        if claim:
            out += [Component(name=spec, path=rel, tier=spec.split("/", 1)[0], platform=platform,
                              kind=kind, claimed=True) for spec, platform in claim]
        elif root is not None:
            name = expected_name(root, rel)
            out.append(Component(name=name, path=rel, tier=name.split("/", 1)[0],
                                 platform=root.platform, kind=kind))
    reserved = sorted(c.path for c in out if not c.claimed and _reserved(c.name))
    if reserved:
        raise ConfigError(
            "an unclaimed source file is named with a file name the spec corpus skips "
            f"({', '.join(sorted(SKIP_NAMES))}), so its spec could never be matched: "
            f"{', '.join(reserved)}. Ignore these files in `code.ignore`, or claim them "
            f"in a spec's `## Reference Implementations`."
        )
    return sorted((c for c in out if in_group(c.name, tier)), key=lambda c: (c.name, c.path))
