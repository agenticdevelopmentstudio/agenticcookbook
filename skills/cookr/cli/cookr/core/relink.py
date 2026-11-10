"""Follow code that moved: rewrite the index's implementation locations from git's renames.

Git's rename detection (`git diff -M <since>`: the commits since `since`, and
whatever is staged, `git mv` included) maps each moved file's old path to its
new one. A file location follows its file. A directory location follows when
every moved file below it moved to one new directory with the same path below
that (`AIPluginKit/` → `AIPluginKit/Chat/` only if everything moved there
alike). A location that is gone with no rename to follow is reported, never
guessed. Planned rows and URL locations are left alone.

An artifact folder that moved has its index `path` brought up to date too.
Everything relink changes is in `index.json`; no artifact's content changes,
so nothing is bumped.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .index import (INDEX_FILE, Entry, Implementation, Index, load_index, save_index,
                    sync_from_folders)
from .repoconfig import Config, ConfigError


def git_renames(repo_root: Path, since: str = "HEAD") -> dict[str, str]:
    """Old repo-relative path -> new, for every file git sees as renamed since `since`."""
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "diff", "-M", "--name-status", "--diff-filter=R", "-z", since],
        capture_output=True, text=True)
    if proc.returncode != 0:
        raise ConfigError(f"git diff {since} failed: {proc.stderr.strip()}")
    fields = [f for f in proc.stdout.split("\0") if f]
    out = {}
    for i in range(0, len(fields) - 2, 3):  # status, old, new
        out[fields[i + 1]] = fields[i + 2]
    return out


def _dir_target(old_dir: str, renames: dict[str, str]) -> Optional[str]:
    """The one directory everything that moved out of `old_dir` moved to, alike."""
    targets = set()
    for old, new in renames.items():
        if old.startswith(old_dir):
            rest = old[len(old_dir):]
            if not new.endswith("/" + rest):
                return None
            targets.add(new[:-len(rest)])
    return targets.pop() if len(targets) == 1 else None


@dataclass
class Change:
    spec: str  # the entry's rdid
    rows: list = field(default_factory=list)  # [(old location, new location)]
    lost: list = field(default_factory=list)  # locations gone with no rename to follow
    folder: tuple = ()  # (old path, new path) when the artifact's folder moved


def relink_rows(repo_root: Path, entry: Entry, renames: dict[str, str]
                ) -> tuple[list[Implementation], Change]:
    change = Change(entry.rdid)
    rows = []
    for impl in entry.implementations:
        loc = impl.location
        if not loc or "://" in loc or impl.conformance.state == "planned":
            rows.append(impl)  # nothing on disk to follow
            continue
        new = renames.get(loc) if not loc.endswith("/") else _dir_target(loc, renames)
        if new and new != loc:
            change.rows.append((loc, new))
            rows.append(Implementation(impl.platform, new, impl.conformance))
            continue
        if not (repo_root / loc).exists():
            change.lost.append(loc)
        rows.append(impl)
    return rows, change


def relink(config: Config, renames: dict[str, str], *, dry_run: bool = False,
           index: Optional[Index] = None) -> list[Change]:
    """Rewrite every implementation that moved, and every moved folder's path;
    the changes, and the locations lost. Writes `index.json` unless `dry_run`."""
    cookbook = config.cookbook_dir
    if index is None:
        index = (load_index(cookbook) if (cookbook / INDEX_FILE).is_file()
                 else Index(cookbook=config.identity))
    before = {uid: e.path for uid, e in index.entries.items()}
    dirty = bool(sync_from_folders(index, cookbook))
    out = []
    for entry in sorted(index.entries.values(), key=lambda e: e.rdid):
        rows, change = relink_rows(config.repo_root, entry, renames)
        old_path = before.get(entry.id, entry.path)
        if old_path != entry.path:
            change.folder = (old_path, entry.path)
        if not change.rows and not change.lost and not change.folder:
            continue
        out.append(change)
        if change.rows or change.folder:
            dirty = True
        entry.implementations = rows
    if dirty and not dry_run:
        save_index(index, cookbook)
    return out
