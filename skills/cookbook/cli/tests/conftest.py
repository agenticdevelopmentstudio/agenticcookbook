"""Shared fixtures for the `cookbook` test suite.

Layout:
    skills/cookbook/cli/cookbook/        the package under test
    skills/cookbook/cli/references-src/  bundled configs + prompts
    skills/cookbook/cli/tests/           this test suite (unit/ + functional/)

We push `skills/cookbook/cli/` onto sys.path so `import cookbook` works without
running install.sh, and point `cookbook.core.refs.references_dir()` at a
stand-in references/ built from references-src/.

Functional tests additionally clone the cookbook-tests fixture repo into a
session tmp dir; per-test copies are made so tests can mutate freely.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
PKG_PARENT = REPO_ROOT / "skills" / "cookbook" / "cli"
sys.path.insert(0, str(PKG_PARENT))

FIXTURE_REPO_URL = os.environ.get(
    "COOKBOOK_TESTS_REPO",
    "git@github.com:agenticdevelopercookbook/cookbook-tests.git",
)


@pytest.fixture(autouse=True)
def tmp_path_is_a_git_repo(request):
    """Make each test's tmp_path a git repo, as a real cookbook's checkout is.

    A cookbook's domain scheme falls back to its repo's name
    (cookbook.core.scheme.repo_scheme), which does not resolve outside git.
    Tests of the no-git case use tmp_path_factory for a directory outside it.
    """
    if "tmp_path" in request.fixturenames:
        tmp = request.getfixturevalue("tmp_path")
        subprocess.run(["git", "init", "-q", str(tmp)], check=True, capture_output=True)


@pytest.fixture(scope="session")
def references_dir(tmp_path_factory) -> Path:
    src = PKG_PARENT / "references-src"
    dest = tmp_path_factory.mktemp("references")
    if src.is_dir():
        for f in src.rglob("*"):
            if f.is_file():
                rel = f.relative_to(src)
                target = dest / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
    return dest


@pytest.fixture
def patch_refs(monkeypatch, references_dir):
    from cookbook.core import refs as refs_module
    monkeypatch.setattr(refs_module, "references_dir", lambda: references_dir)
    return references_dir


@pytest.fixture(scope="session")
def cookbook_tests_repo(tmp_path_factory) -> Path:
    """Clone (or refresh) the cookbook-tests fixture repo into a session tmp dir.

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
    """Returns a callable: `fixture_cookbook("empty-client")` → fresh tmp copy
    of `cookbook-tests/fixtures/<name>/` that the test can mutate."""

    def _copy(name: str) -> Path:
        src = cookbook_tests_repo / "fixtures" / name
        if not src.is_dir():
            pytest.skip(f"fixture not present in cookbook-tests: {name}")
        dst = tmp_path / name
        shutil.copytree(src, dst)
        return dst

    return _copy


@pytest.fixture
def cookbook_bin():
    """Path to the installed `cookbook` CLI, or skip if not on PATH.

    Functional tests run the real shim. Subprocess invocation tests the
    install pipeline (shim → PYTHONPATH → python3 -m cookbook), not just
    the in-process Python.
    """
    found = shutil.which("cookbook")
    if not found:
        pytest.skip("`cookbook` not on PATH — run install.sh first")
    return found


@pytest.fixture
def run_cookbook(cookbook_bin):
    """Returns a callable: `run_cookbook(["create"], cwd=path)` → CompletedProcess."""

    def _run(args, cwd=None, check=False, env=None):
        return subprocess.run(
            [cookbook_bin, *args],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=check,
            env=env,
            timeout=120,
        )

    return _run
