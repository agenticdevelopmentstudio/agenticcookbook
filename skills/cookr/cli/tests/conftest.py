"""Shared fixtures for the `cookr` test suite.

Layout:
    skills/cookr/cli/cookr/        the package under test
    skills/cookr/cli/tests/        this suite (unit/ + functional/ + fixtures/)

`skills/cookr/cli/` is pushed onto sys.path so `import cookr` works without
running ./install, and `patch_refs` points `cookr.core.refs.references_dir()` at
a stand-in references/ built from references-src/.

The functional tests of update/validate/lint additionally clone the
cookbook-tests fixture repo into a session tmp dir; per-test copies are made so
tests can mutate freely.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
COOKR_PKG_PARENT = REPO_ROOT / "skills" / "cookr" / "cli"
if str(COOKR_PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(COOKR_PKG_PARENT))

FIXTURE_REPO_URL = os.environ.get(
    "COOKBOOK_TESTS_REPO",
    "git@github.com:agenticdevelopercookbook/cookbook-tests.git",
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def mini_repo(tmp_path) -> Path:
    """Fresh, mutable copy of fixtures/mini-repo (a library cookbook)."""
    dst = tmp_path / "mini-repo"
    shutil.copytree(FIXTURES / "mini-repo", dst)
    return dst


@pytest.fixture
def legacy_repo(tmp_path) -> Path:
    """Fresh, mutable copy of fixtures/legacy-repo (a flat `.cookr.json` corpus)."""
    dst = tmp_path / "legacy-repo"
    shutil.copytree(FIXTURES / "legacy-repo", dst)
    return dst


@pytest.fixture
def cookr_bin():
    found = shutil.which("cookr")
    if not found:
        pytest.skip("`cookr` not on PATH — run ./install first")
    return found


@pytest.fixture
def run_cookr(cookr_bin):
    def _run(args, cwd=None, check=False, env=None):
        return subprocess.run(
            [cookr_bin, *args],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=check,
            env=env,
            timeout=120,
        )

    return _run


@pytest.fixture(scope="session")
def templates_source_dir(tmp_path_factory) -> Path:
    """The repo's own templates laid out as the install materializes them."""
    dst = tmp_path_factory.mktemp("templates")
    for rtype, src in (("ingredient", "ingredients"), ("recipe", "recipes")):
        shutil.copy2(REPO_ROOT / "cookbook" / src / "_template.md", dst / f"{rtype}.md")
    return dst


@pytest.fixture(autouse=True)
def _hermetic_templates(monkeypatch, templates_source_dir):
    """Grade against the checkout's templates, never a stale or absent install."""
    from cookr.core import templates

    monkeypatch.setattr(templates, "templates_dir", lambda: templates_source_dir)


@pytest.fixture
def git_tmp_path(tmp_path) -> Path:
    """tmp_path as a git repo, as a real cookbook's checkout is.

    A cookbook's domain scheme falls back to its repo's name
    (cookr.core.scheme.repo_scheme), which does not resolve outside git.
    """
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True, capture_output=True)
    return tmp_path


@pytest.fixture(scope="session")
def references_dir(tmp_path_factory) -> Path:
    src = COOKR_PKG_PARENT / "references-src"
    dest = tmp_path_factory.mktemp("references")
    for f in src.rglob("*"):
        if f.is_file():
            target = dest / f.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
    return dest


@pytest.fixture
def patch_refs(monkeypatch, references_dir):
    from cookr.core import refs as refs_module

    monkeypatch.setattr(refs_module, "references_dir", lambda: references_dir)
    return references_dir


@pytest.fixture(scope="session")
def cookbook_tests_repo(tmp_path_factory) -> Path:
    """Clone the cookbook-tests fixture repo into a session tmp dir.

    Honor COOKBOOK_TESTS_REPO for overrides (CI mirror, local checkout, etc).
    If the clone fails (no network / no SSH key), skip every test that depends
    on this fixture rather than fail noisily.
    """
    dest = tmp_path_factory.mktemp("cookbook-tests-repo")
    try:
        subprocess.run(
            ["git", "clone", "--depth=1", FIXTURE_REPO_URL, str(dest / "repo")],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        pytest.skip(f"cannot clone {FIXTURE_REPO_URL}: {e}")
    return dest / "repo"


@pytest.fixture
def fixture_cookbook(tmp_path, cookbook_tests_repo):
    """`fixture_cookbook("empty-client")` → a fresh tmp copy of
    `cookbook-tests/fixtures/<name>/` that the test can mutate."""

    def _copy(name: str) -> Path:
        src = cookbook_tests_repo / "fixtures" / name
        if not src.is_dir():
            pytest.skip(f"fixture not present in cookbook-tests: {name}")
        dst = tmp_path / name
        shutil.copytree(src, dst)
        return dst

    return _copy
