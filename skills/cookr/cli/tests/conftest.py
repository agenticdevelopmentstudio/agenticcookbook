"""Shared fixtures for the `cookr` test suite.

Layout:
    skills/cookr/cli/cookr/        the package under test
    skills/cookr/cli/tests/        this suite (unit/ + functional/ + fixtures/)

Both `skills/cookr/cli/` and `skills/cookbook/cli/` are pushed onto sys.path so
`import cookr` and `import cookbook` work without running install.sh.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
COOKR_PKG_PARENT = REPO_ROOT / "skills" / "cookr" / "cli"
COOKBOOK_PKG_PARENT = REPO_ROOT / "skills" / "cookbook" / "cli"
for p in (COOKR_PKG_PARENT, COOKBOOK_PKG_PARENT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

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
        pytest.skip("`cookr` not on PATH — run install.sh first")
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
