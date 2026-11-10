"""The checkout holding a path: its top directory, and the walk up to it."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def run_vcs(start: Path, *args: str) -> Optional[str]:
    """The version-control tool run in `start` with `args`: its stripped stdout;
    None when it fails, prints nothing or is absent."""
    try:
        proc = subprocess.run(["git", "-C", str(start), *args],
                              capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return None
    out = proc.stdout.strip()
    return out if proc.returncode == 0 and out else None


def repo_top(start: Path) -> Optional[Path]:
    """The top-level directory of the checkout holding `start`; None outside one."""
    top = run_vcs(Path(start), "rev-parse", "--show-toplevel")
    return Path(top).resolve() if top else None


def up_to_repo_top(start: Path) -> list[Path]:
    """`start` and its parents up to the top of the checkout holding it, nearest
    first; just `[start]` outside one. Never a directory above the checkout."""
    start = Path(start).resolve()
    top = repo_top(start)
    if top is None or (start != top and top not in start.parents):
        return [start]
    return [start, *[d for d in start.parents if d == top or top in d.parents]]
