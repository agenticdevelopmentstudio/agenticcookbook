"""Git changes as data: what a staged set, a branch or a plan touches.

`Change.status` is `A`, `M`, `D` or `R`; `R` only for a 100% similar rename
(`old_path` is where it came from). Everything is read NUL-separated so paths
with spaces or odd characters survive. git failures raise `GitError`; they are
never read as "no changes".
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from .versions import GitError, git


@dataclass(frozen=True)
class Change:
    status: str
    path: str
    old_path: Optional[str] = None


def parse_name_status(raw: bytes) -> list[Change]:
    """Changes from `git diff --name-status -z` output."""
    tokens = raw.decode("utf-8", "surrogateescape").split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()
    out: list[Change] = []
    i = 0
    while i < len(tokens):
        letter = tokens[i][:1]
        if letter in ("R", "C"):
            old, new = tokens[i + 1], tokens[i + 2]
            i += 3
            out.append(Change("R", new, old) if letter == "R" else Change("A", new))
        else:
            path = tokens[i + 1]
            i += 2
            out.append(Change(letter if letter in ("A", "M", "D") else "M", path))
    return out


def untracked(repo_root: Path) -> list[Change]:
    raw = git(repo_root, "ls-files", "--others", "--exclude-standard", "-z")
    return [Change("A", p) for p in raw.decode("utf-8", "surrogateescape").split("\0") if p]


def staged(repo_root: Path) -> list[Change]:
    return parse_name_status(git(repo_root, "diff", "--cached", "--name-status", "-z", "-M100%"))


def branch(repo_root: Path, base: str) -> list[Change]:
    """Everything since `base` (a commit, normally the merge base): committed,
    staged and unstaged changes, plus untracked files."""
    tracked = parse_name_status(git(repo_root, "diff", "--name-status", "-z", "-M100%", base))
    return tracked + untracked(repo_root)


def uncommitted(repo_root: Path) -> list[Change]:
    """Staged and unstaged edits plus untracked files: the diff against HEAD. A
    repo with no commit yet (unborn HEAD) has no HEAD to diff, so its staged
    changes plus untracked files."""
    try:
        git(repo_root, "rev-parse", "--verify", "--quiet", "HEAD")
    except GitError:
        return staged(repo_root) + untracked(repo_root)   # raises GitError if git is really broken
    return branch(repo_root, "HEAD")


def planned(paths: list[str], repo_root: Optional[Path] = None) -> list[Change]:
    """Planned paths as changes: `M`, or `A` when the file does not exist yet
    (existence is judged under `repo_root`, else the current directory)."""
    base = Path(repo_root) if repo_root is not None else Path()
    return [Change("M" if (base / p).exists() else "A", p) for p in paths]


def split_rename(change: Change, in_root: Callable[[str], bool]) -> list[Change]:
    """A rename that crosses a root boundary is a delete plus an add; anything
    else comes back unchanged."""
    if change.status == "R" and change.old_path is not None \
            and in_root(change.old_path) != in_root(change.path):
        return [Change("D", change.old_path), Change("A", change.path)]
    return [change]
