"""Follow code that moved: rewrite Reference Implementations paths from git's renames.

Git's rename detection (`git diff -M <since>`: the commits since `since`, and
whatever is staged, `git mv` included) maps each moved file's old path to its
new one. A file row follows its file. A directory row follows when every
moved file below it moved to one new directory with the same path below that
(`AIPluginKit/` → `AIPluginKit/Chat/` only if everything moved there alike).
A row whose path is gone with no rename to follow is reported, never guessed.
Each spec that changes is patch-bumped.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

from cookbook.core import refimpl
from cookbook.modules import bump

from .config import Config, ConfigError
from .recipes import RecipeInfo, load_corpus

BUMP_SUMMARY = "Relinked Reference Implementations after the code moved."


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
    spec: str
    rows: list = field(default_factory=list)  # [(old path, new path)]
    lost: list = field(default_factory=list)  # paths gone with no rename to follow
    bump_error: str = ""


def relink_rows(repo_root: Path, info: RecipeInfo, renames: dict[str, str]
                ) -> tuple[list[refimpl.Implementation], Change]:
    change = Change(info.slug)
    rows = []
    for impl in info.implementations:
        new = renames.get(impl.path) if not impl.is_dir else _dir_target(impl.path, renames)
        if new and new != impl.path:
            change.rows.append((impl.path, new))
            rows.append(refimpl.Implementation(impl.platform, new))
            continue
        if not (repo_root / impl.path).exists():
            change.lost.append(impl.path)
        rows.append(impl)
    return rows, change


def relink(config: Config, renames: dict[str, str], *, dry_run: bool = False, author: str = "",
           day: Optional[str] = None, corpus: Optional[dict[str, RecipeInfo]] = None
           ) -> list[Change]:
    """Rewrite every spec whose rows moved; the changes, and the rows lost."""
    corpus = load_corpus(config.cookbook_dir) if corpus is None else corpus
    day = day or date.today().isoformat()
    author = author or bump._git_user(config.repo_root)
    out = []
    for name, info in sorted(corpus.items()):
        rows, change = relink_rows(config.repo_root, info, renames)
        if not change.rows and not change.lost:
            continue
        out.append(change)
        if dry_run or not change.rows:
            continue
        text = info.path.read_text(encoding="utf-8")
        info.path.write_text(refimpl.with_section(text, rows), encoding="utf-8")
        try:
            info.path.write_text(bump.plan(info.path, level="patch", summary=BUMP_SUMMARY,
                                           author=author, day=day).text, encoding="utf-8")
        except bump.BumpError as e:
            change.bump_error = str(e)
    return out
