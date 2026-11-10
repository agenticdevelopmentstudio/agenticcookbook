"""cookr.core.legacy — the format-1 domain scheme a repo was named by, which
only `cookr upgrade` still reads."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from cookr.core.legacy import SchemeError, repo_scheme, scheme_of


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


_GIT = ["git", "-c", "user.name=T", "-c", "user.email=t@example.com",
        "-c", "init.defaultBranch=main", "-c", "protocol.file.allow=always"]


def git(cwd: Path, *args: str) -> str:
    return subprocess.run([*_GIT, "-C", str(cwd), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def make_repo(path: Path, origin: str | None = None) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q")
    (path / "README.md").write_text("x\n", encoding="utf-8")
    git(path, "add", "README.md")
    git(path, "commit", "-q", "-m", "init")
    if origin:
        git(path, "remote", "add", "origin", origin)
    return path


@pytest.fixture
def outside_git(tmp_path_factory) -> Path:
    """A directory in no git repo (tmp_path itself is one; see conftest)."""
    return tmp_path_factory.mktemp("nogit")


@pytest.mark.parametrize("url", [
    "git@github.com:org/my-repo.git",
    "https://github.com/org/my-repo.git",
    "https://github.com/org/my-repo",
    "https://github.com/org/my-repo/",
    "ssh://git@host:22/org/my-repo.git",
    "/srv/git/my-repo.git",
    "../my-repo",
])
def test_origin_url_basename(tmp_path, url):
    repo = make_repo(tmp_path / "checkout", origin=url)
    assert repo_scheme(repo) == "my-repo"


def test_without_origin_the_main_checkouts_directory_names_the_repo(tmp_path):
    repo = make_repo(tmp_path / "my-project")
    (repo / "sub").mkdir()
    assert repo_scheme(repo) == "my-project"
    assert repo_scheme(repo / "sub") == "my-project"


def test_linked_worktree_uses_the_main_checkouts_name_not_its_own(tmp_path):
    repo = make_repo(tmp_path / "my-project")
    wt = repo / ".claude" / "worktrees" / "multiplatform"
    git(repo, "worktree", "add", "-q", str(wt), "-b", "multiplatform")
    assert repo_scheme(wt) == "my-project"


def test_linked_worktree_with_origin_uses_the_origin(tmp_path):
    repo = make_repo(tmp_path / "local-dir", origin="git@github.com:org/real-name.git")
    wt = tmp_path / "feature-branch"
    git(repo, "worktree", "add", "-q", str(wt), "-b", "feature-branch")
    assert repo_scheme(wt) == "real-name"


def test_submodule_checkout_uses_its_own_origin(tmp_path):
    lib = make_repo(tmp_path / "toolkit-upstream")
    app = make_repo(tmp_path / "app", origin="git@github.com:org/app.git")
    git(app, "submodule", "add", "-q", str(lib), "external/toolkit")
    sub = app / "external" / "toolkit"
    assert repo_scheme(sub) == "toolkit-upstream"   # not `app`, not `toolkit`


def test_submodule_without_origin_uses_its_checkout_directory(tmp_path):
    lib = make_repo(tmp_path / "toolkit-upstream")
    app = make_repo(tmp_path / "app", origin="git@github.com:org/app.git")
    git(app, "submodule", "add", "-q", str(lib), "external/toolkit")
    sub = app / "external" / "toolkit"
    git(sub, "remote", "remove", "origin")
    assert repo_scheme(sub) == "toolkit"            # its own checkout, not the superproject


def test_outside_git_raises_a_clear_error(outside_git):
    with pytest.raises(SchemeError, match="scheme"):
        repo_scheme(outside_git)


def test_scheme_of():
    assert scheme_of("agenticdevelopercookbook://index") == "agenticdevelopercookbook"
    assert scheme_of("no scheme") is None
    assert scheme_of(None) is None

