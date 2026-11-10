"""Subprocess wrappers — particularly `claude -p` for LLM steps."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ShellResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run(cmd: list[str], stdin: str | None = None, timeout: int | None = None) -> ShellResult:
    proc = subprocess.run(
        cmd,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return ShellResult(proc.returncode, proc.stdout, proc.stderr)


def claude_available() -> bool:
    return shutil.which("claude") is not None


def claude_p(prompt: str, timeout: int = 600) -> ShellResult:
    """Run `claude -p` with the given prompt on stdin. Returns the model's stdout."""
    if not claude_available():
        return ShellResult(127, "", "claude CLI not found on PATH")
    return run(["claude", "-p", prompt], timeout=timeout)


def git_changed_markdown(root: Path, since: str) -> list[Path]:
    """Markdown files changed under `root` since `since` (a git ref)."""
    return git_changed_files(root, since, suffixes=(".md",))


def git_changed_files(root: Path, since: str, suffixes: tuple = (),
                      deleted: bool = False) -> list[Path]:
    """Files changed under `root` since `since` (a git ref), limited to
    `suffixes` when given.

    Returns absolute paths to files that still exist on disk, plus the paths
    of deleted files when `deleted` is set. Raises CalledProcessError if the
    ref is unknown or `git` is not available.
    """
    out = subprocess.run(
        ["git", "diff", "--name-only", f"--diff-filter={'AMRD' if deleted else 'AMR'}",
         f"{since}...HEAD"],
        capture_output=True,
        text=True,
        check=True,
        cwd=root,
    )
    repo_top = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        cwd=root,
    ).stdout.strip()
    repo_root = Path(repo_top)
    paths: list[Path] = []
    for line in out.stdout.splitlines():
        name = line.strip()
        if suffixes and not name.endswith(suffixes):
            continue
        abs_path = (repo_root / name).resolve()
        try:
            abs_path.relative_to(root.resolve())
        except ValueError:
            continue
        if abs_path.is_file() or (deleted and not abs_path.exists()):
            paths.append(abs_path)
    return paths
