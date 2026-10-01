"""Cookbook root resolution.

Rules:
1. Explicit --path wins. Validate it looks like a cookbook (or is empty/missing for `create`).
2. If cwd contains a `cookbook/` subdir that is a cookbook, that subdir is the root (the
   agenticcookbook layout, and a library cookbook inside the repo it specifies).
3. Walk up from cwd; the first dir that is a cookbook is the root.
4. Return None when nothing is found — `create` is allowed without a root; other modules error.

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
        return p if p.is_dir() else None

    start = start.resolve()
    if _is_cookbook(start / "cookbook"):
        return start / "cookbook"

    for d in (start, *start.parents):
        if _is_cookbook(d):
            return d

    return None
