"""Subprocess wrapper + claude_p stub guard + git_changed_markdown.

We can't depend on `claude` being installed in CI, so the tests cover the
detect-and-bail path and the generic `run()` wrapper end-to-end on real
processes."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from cookr.core import shell


def test_run_captures_stdout():
    r = shell.run(["echo", "hello"])
    assert r.ok
    assert r.stdout.strip() == "hello"


def test_run_captures_nonzero_exit():
    r = shell.run(["sh", "-c", "exit 3"])
    assert not r.ok
    assert r.returncode == 3


def test_run_captures_stderr():
    r = shell.run(["sh", "-c", "echo oops 1>&2; exit 1"])
    assert r.stderr.strip() == "oops"


def test_run_passes_stdin():
    r = shell.run(["cat"], stdin="payload\n")
    assert r.stdout == "payload\n"


def test_claude_p_returns_127_when_unavailable(monkeypatch):
    monkeypatch.setattr(shell, "claude_available", lambda: False)
    r = shell.claude_p("anything")
    assert r.returncode == 127
    assert not r.ok
    assert "not found" in r.stderr.lower()


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    )


def _init_git_repo(repo: Path) -> None:
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "T")
    _git(repo, "commit", "--allow-empty", "-m", "root")


def test_git_changed_markdown_lists_added_files(tmp_path):
    _init_git_repo(tmp_path)
    (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
    _git(tmp_path, "add", "a.md")
    _git(tmp_path, "commit", "-m", "add a")

    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.strip()

    (tmp_path / "b.md").write_text("# B\n", encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("nope", encoding="utf-8")
    _git(tmp_path, "add", "b.md", "ignored.txt")
    _git(tmp_path, "commit", "-m", "add b")

    paths = shell.git_changed_markdown(tmp_path, base)
    names = sorted(p.name for p in paths)
    assert names == ["b.md"]


def test_git_changed_markdown_filters_outside_root(tmp_path):
    _init_git_repo(tmp_path)
    (tmp_path / "cookbook").mkdir()
    (tmp_path / "cookbook" / "in.md").write_text("# in\n", encoding="utf-8")
    (tmp_path / "out.md").write_text("# out\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-m", "seed")

    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.strip()

    (tmp_path / "cookbook" / "in.md").write_text("# in v2\n", encoding="utf-8")
    (tmp_path / "out.md").write_text("# out v2\n", encoding="utf-8")
    _git(tmp_path, "commit", "-am", "edit")

    paths = shell.git_changed_markdown(tmp_path / "cookbook", base)
    assert [p.name for p in paths] == ["in.md"]


def test_git_changed_markdown_raises_on_unknown_ref(tmp_path):
    _init_git_repo(tmp_path)
    with pytest.raises(subprocess.CalledProcessError):
        shell.git_changed_markdown(tmp_path, "does-not-exist")
