"""cookbook.core.scheme — a repo's / cookbook's domain scheme."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from cookbook.core.scheme import (
    SchemeError,
    cookbook_scheme,
    declared_scheme,
    index_domain,
    repo_scheme,
    scheme_of,
)

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


# --- cookbook_scheme: the root's own index.md first, then the repo ------------------

def _index(d: Path, text: str) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.md").write_text(text, encoding="utf-8")


def test_declared_scheme_wins_over_the_repo_name(tmp_path):
    repo = make_repo(tmp_path / "checkout", origin="git@github.com:org/agenticcookbook.git")
    _index(repo / "cookbook", "---\ndomain: agenticdevelopercookbook://index\n---\n# Cookbook\n")
    assert cookbook_scheme(repo / "cookbook") == "agenticdevelopercookbook"


def test_a_subdirectory_root_reads_its_cookbooks_index(tmp_path):
    """`cookbook update -p recipes` roots at recipes/, below the cookbook's index.md."""
    repo = make_repo(tmp_path / "checkout", origin="git@github.com:org/agenticcookbook.git")
    _index(repo / "cookbook", "---\ndomain: agenticdevelopercookbook://index\n---\n")
    (repo / "cookbook" / "recipes").mkdir()
    assert cookbook_scheme(repo / "cookbook" / "recipes") == "agenticdevelopercookbook"


@pytest.mark.parametrize("index_text", [None, "", "# Title only\n", "---\ntitle: x\n---\n"])
def test_empty_or_absent_index_falls_back_to_the_repo(tmp_path, index_text):
    repo = make_repo(tmp_path / "checkout", origin="git@github.com:org/agenticdevelopertoolkit.git")
    (repo / "recipes").mkdir()
    if index_text is not None:
        _index(repo, index_text)
    assert declared_scheme(repo / "recipes") is None
    assert cookbook_scheme(repo / "recipes") == "agenticdevelopertoolkit"


def test_the_walk_stops_at_the_repo_top(tmp_path):
    _index(tmp_path, "---\ndomain: unrelated://index\n---\n")   # above the repo
    repo = make_repo(tmp_path / "toolkit")
    (repo / "recipes").mkdir()
    assert cookbook_scheme(repo / "recipes") == "toolkit"


def test_outside_git_only_the_roots_own_index_counts(tmp_path_factory):
    base = tmp_path_factory.mktemp("nogit-walk")
    _index(base, "---\ndomain: above://index\n---\n")
    (base / "cb").mkdir()
    with pytest.raises(SchemeError):
        cookbook_scheme(base / "cb")
    _index(base / "cb", "---\ndomain: mine://index\n---\n")
    assert cookbook_scheme(base / "cb") == "mine"


def test_index_domain_keeps_an_existing_domain_without_deriving_a_scheme(outside_git):
    out = outside_git / "INDEX.md"
    out.write_text("---\ndomain: kept://recipes/INDEX\n---\n", encoding="utf-8")
    assert index_domain(outside_git, out, "x/recipes/index") == "kept://recipes/INDEX"


def test_index_domain_derives_one_for_a_new_file(tmp_path):
    repo = make_repo(tmp_path / "my-project")
    assert index_domain(repo, repo / "INDEX.md", "my-project/recipes/index") \
        == "my-project://my-project/recipes/index"
