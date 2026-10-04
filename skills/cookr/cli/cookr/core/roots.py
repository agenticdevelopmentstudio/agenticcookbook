"""Cookbook root resolution.

Rules:
1. An explicit -p wins: its `cookbook/` subdir when that is a cookbook (a repo root),
   else the path itself when it is one, else None.
2. If cwd contains a `cookbook/` subdir that is a cookbook, that subdir is the root (the
   agenticcookbook layout, and a library cookbook inside the repo it specifies).
3. Walk up from cwd; the first dir that is a cookbook is the root.
4. Return None when nothing is found; the modules that need a root refuse to run.

A directory is a cookbook when it holds a `cookbook.json` manifest, or an `index.md`
beside any canonical subdir.
"""

from __future__ import annotations

from pathlib import Path

MANIFEST = "cookbook.json"

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
