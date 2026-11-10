"""Git changes: parsing, branch/staged reading, planned paths, rename splitting."""

from __future__ import annotations

import subprocess

import pytest

from cookr.core import changes
from cookr.core.changes import Change
from cookr.core.versions import GitError


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "r"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    _git(r, "config", "user.email", "t@example.com")
    _git(r, "config", "user.name", "Tester")
    (r / "keep.txt").write_text("keep\n" * 20, encoding="utf-8")
    (r / "with space.txt").write_text("space\n" * 20, encoding="utf-8")
    (r / "gone.txt").write_text("gone\n", encoding="utf-8")
    _git(r, "add", "-A")
    _git(r, "commit", "-q", "-m", "base")
    return r


def test_changes_parse_spaces_and_renames(repo):
    _git(repo, "mv", "with space.txt", "moved name.txt")
    (repo / "keep.txt").write_text("changed\n", encoding="utf-8")
    (repo / "gone.txt").unlink()
    (repo / "new file.txt").write_text("n\n", encoding="utf-8")
    _git(repo, "add", "-A")
    got = set(changes.staged(repo))
    assert got == {Change("R", "moved name.txt", "with space.txt"), Change("M", "keep.txt"),
                   Change("D", "gone.txt"), Change("A", "new file.txt")}


def test_rename_below_100_percent_is_delete_plus_add(repo):
    _git(repo, "mv", "with space.txt", "other.txt")
    (repo / "other.txt").write_text("totally different\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert set(changes.staged(repo)) == {Change("D", "with space.txt"), Change("A", "other.txt")}


def test_branch_covers_working_tree_and_untracked(repo):
    (repo / "keep.txt").write_text("edited\n", encoding="utf-8")
    (repo / "fresh.txt").write_text("x\n", encoding="utf-8")
    assert set(changes.branch(repo, "HEAD")) == {Change("M", "keep.txt"), Change("A", "fresh.txt")}


def test_git_failure_raises(tmp_path):
    with pytest.raises(GitError):
        changes.staged(tmp_path)


def test_planned_is_modified_or_added(tmp_path):
    (tmp_path / "there.ts").write_text("x", encoding="utf-8")
    assert changes.planned(["there.ts", "new.ts"], tmp_path) == [
        Change("M", "there.ts"), Change("A", "new.ts")]


def test_rename_out_of_root_is_delete_plus_add():
    in_root = lambda p: p.startswith("web/")
    out = changes.split_rename(Change("R", "docs/x.ts", "web/x.ts"), in_root)
    assert out == [Change("D", "web/x.ts"), Change("A", "docs/x.ts")]
    inside = Change("R", "web/y.ts", "web/x.ts")
    assert changes.split_rename(inside, in_root) == [inside]
