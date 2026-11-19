"""Shared fixtures for the `cookr` test suite.

Layout:
    skills/cookr/cli/cookr/        the package under test
    skills/cookr/cli/tests/        this suite (unit/ + functional/ + fixtures/)

`skills/cookr/cli/` is pushed onto sys.path so `import cookr` works without
running ./install, and `patch_refs` points `cookr.core.refs.references_dir()` at
a stand-in references/ built from references-src/.

The functional tests of update/validate/lint build named cookbook states with
the installed cookr from the docs in fixtures/cookbook-states/ (`fixture_cookbook`).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
COOKR_PKG_PARENT = REPO_ROOT / "skills" / "cookr" / "cli"
if str(COOKR_PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(COOKR_PKG_PARENT))

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


@pytest.fixture(scope="session")
def repo_v2(tmp_path_factory) -> Path:
    """A copy of this repo's `cookbook/` (format 2) and `tbd/compliance/`, for
    the tests that read the real corpus. Read-only: tests must not mutate it."""
    root = tmp_path_factory.mktemp("repo-v2")
    shutil.copytree(REPO_ROOT / "cookbook", root / "cookbook")
    shutil.copytree(REPO_ROOT / "tbd" / "compliance", root / "tbd" / "compliance")
    return root


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


# The user's real cookr home, captured before any test can repoint HOME.
REAL_COOKR_HOME = Path("~/.cookr").expanduser().resolve()


def real_locations() -> "bytes | None":
    """The real ~/.cookr/locations.json as bytes (None when absent). Read only."""
    try:
        return (REAL_COOKR_HOME / "locations.json").read_bytes()
    except OSError:
        return None


# Snapshotted when the suite is collected, before any test runs.
REAL_LOCATIONS_AT_START = real_locations()


def report_failure(session, message: str) -> None:
    """Write `message` through the terminal reporter, or to stderr when there is
    none (`-p no:terminal`), so the real failure is never hidden."""
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is not None:
        reporter.write_line(message, red=True)
    else:
        sys.stderr.write(message + "\n")


def pytest_sessionfinish(session, exitstatus):
    """Fail the run if any test changed the user's real locations.json."""
    if real_locations() != REAL_LOCATIONS_AT_START:
        report_failure(session, f"FAIL: a test changed {REAL_COOKR_HOME / 'locations.json'}")
        session.exitstatus = 1


@pytest.fixture(autouse=True)
def _hermetic_cookr_home(tmp_path_factory, monkeypatch):
    """Every test runs under a scratch COOKR_HOME, so nothing a test does (an
    upgrade remembering a location, an install receipt) can reach ~/.cookr. The
    default path is repointed too, for a test that unsets COOKR_HOME. A test that
    wants its own home still sets COOKR_HOME; it lands in tmp_path, not here."""
    from cookr.core import links

    home = tmp_path_factory.mktemp("cookr-home")
    monkeypatch.setenv("COOKR_HOME", str(home))
    monkeypatch.setattr(links, "LOCATIONS", home / "locations.json")
    return home


@pytest.fixture(autouse=True)
def _outside_the_checkout(tmp_path, monkeypatch):
    """Run from a scratch directory: a cookr command upgrades the repo it finds
    from cwd, and cwd must never be this checkout's own (format 1) cookbook."""
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def git_tmp_path(tmp_path) -> Path:
    """tmp_path as a git repo, as a real cookbook's checkout is.

    A format-1 cookbook's domain scheme falls back to its repo's name
    (cookr.core.legacy.repo_scheme), which does not resolve outside git.
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


COOKBOOK_STATES = FIXTURES / "cookbook-states"

# Each named state: the docs converted and indexed, then the docs added after the last
# `update` (`late`, converted, so only the index is stale) and the docs written raw.
STATES = {
    "empty-client": {},
    "recipes-only-valid": {"indexed": ["hello.md", "world.md"]},
    "with-drift": {"late": ["added-but-not-indexed.md"]},
    "broken-frontmatter": {"raw": ["missing-fields.md"]},
}


@pytest.fixture
def fixture_cookbook(tmp_path, run_cookr):
    """`fixture_cookbook("empty-client")` -> a git repo holding that cookbook state, built
    with the cookr under test, so a fixture is never older than the format it tests."""

    def _build(name: str) -> Path:
        state = STATES[name]
        repo = tmp_path / name
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        def ok(*args):
            r = run_cookr(list(args), cwd=repo)
            assert r.returncode == 0, f"{name}: cookr {' '.join(args)}\n{r.stdout}{r.stderr}"
        ok("create", "--rdid", "testbook")
        cb = repo / "cookbook"
        (cb / "recipes").mkdir()
        def add(group, convert):
            for doc in state.get(group, []):
                shutil.copy2(COOKBOOK_STATES / doc, cb / "recipes" / doc)
                if convert:
                    ok("convert", str(cb / "recipes" / doc))
        add("indexed", True)
        ok("update", "-p", str(cb), "--author", "cookbook-tests")
        add("late", True)
        add("raw", False)
        return repo

    return _build
