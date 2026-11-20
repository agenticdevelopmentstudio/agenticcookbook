"""Cookbook root resolution.

Rules:
1. An explicit -p wins: its `cookbook/` subdir when that is a cookbook (a repo root),
   else the path itself when it is one, else None.
2. If cwd contains a `cookbook/` subdir that is a cookbook, that subdir is the root (the
   agenticcookbook layout, and a library cookbook inside the repo it specifies).
3. Walk up from cwd; the first dir that is a cookbook is the root.
4. Return None when nothing is found; the modules that need a root refuse to run.

An artifact named on the command line is found the same way from any working
directory (`artifact_path`), and the cookbook holding it is found from the
artifact itself (`cookbook_of`), never from the cwd.

A directory is a cookbook when it holds a `cookbook.json` manifest, or an `index.md`
beside any canonical subdir.
"""

from __future__ import annotations

from pathlib import Path

from .identity import MANIFEST, TYPE_DIRS

CANONICAL_SUBDIRS = (
    "recipes",
    "reference",
    "principles",
    "guidelines",
    "ingredients",
)


def _looks_like_cookbook(d: Path) -> bool:
    return any((d / sub).is_dir() for sub in CANONICAL_SUBDIRS)


def _is_cookbook(d: Path) -> bool:
    return (d / MANIFEST).is_file() or ((d / "index.md").exists() and _looks_like_cookbook(d))


def resolve(start: Path, explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        p = explicit.expanduser().resolve()
        return next((c for c in (p / "cookbook", p) if _is_cookbook(c)), None)

    start = start.resolve()
    if _is_cookbook(start / "cookbook"):
        return start / "cookbook"

    for d in (start, *start.parents):
        if _is_cookbook(d):
            return d

    return None


def cookbook_of(path: Path) -> Path | None:
    """The cookbook holding `path` (resolved), the one way cookr finds it from
    an artifact: the nearest directory at or above it with a manifest; else the
    nearest that is a cookbook by its `index.md`; else the parent of the
    nearest principles/guidelines/ingredients/recipes directory; else None."""
    p = Path(path).expanduser().resolve()
    up = (p, *p.parents)
    return (next((d for d in up if (d / MANIFEST).is_file()), None)
            or next((d for d in up if _is_cookbook(d)), None)
            or next((d.parent for d in p.parents if d.name in TYPE_DIRS), None))


def artifact_path(path: Path, cookbook_root: Path | None = None,
                  repo_root: Path | None = None, cwd: Path | None = None) -> Path:
    """`path`, an artifact named on the command line, found the same way from any
    working directory. Absolute stays as given; a relative path is tried against
    the cwd, then the repo (`cookbook/...`), then the cookbook (`guidelines/...`):
    the first that exists wins. A path that exists nowhere (a copy folded away
    since a base revision) takes the first whose parent directory exists, else
    the cwd's, so its error names it there. A path found against the cwd is
    returned as it was spelled, so what a command records or prints from it
    (skills.json's `source`, a report's `folder`) is unchanged; one found
    against the repo or the cookbook is returned absolute. `cwd` is the working
    directory to read from (a caller's own, e.g. CookrContext.cwd), the
    process's when None; a path found against a `cwd` other than the process's
    is returned absolute, since spelled relative it would name another file."""
    p = Path(path).expanduser()
    if p.is_absolute():
        return p
    here = Path(cwd).expanduser().absolute() if cwd is not None else Path.cwd()
    bases = [here]
    if cookbook_root is not None:
        cookbook_root = Path(cookbook_root).expanduser().absolute()
        bases += [Path(repo_root).expanduser().absolute() if repo_root is not None
                  else cookbook_root.parent, cookbook_root]
    candidates = [b / p for b in bases]
    found = (next((c for c in candidates if c.exists()), None)
             or next((c for c in candidates if c.parent.is_dir()), candidates[0]))
    return p if found == candidates[0] and here == Path.cwd() else found
