"""End-to-end: a fresh client cookbook goes through the full lifecycle without
errors. Uses the installed `cookr` shim (real subprocess, real PYTHONPATH)
so we exercise ./install's output, not just in-process Python."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")



CREATE = ["create", "--rdid", "testbook"]


def _create(run_cookr, tmp_path):
    """A format-2 cookbook with an empty recipes/ for the hand-written docs below."""
    r = run_cookr(CREATE, cwd=tmp_path)
    assert r.returncode == 0, r.stderr or r.stdout
    cb = tmp_path / "cookbook"
    (cb / "recipes").mkdir()
    return cb


def test_create_scaffolds_expected_files(tmp_path, run_cookr):
    # Format 2: create writes the manifest and an empty index, nothing else.
    r = run_cookr(CREATE, cwd=tmp_path)
    assert r.returncode == 0, r.stderr or r.stdout
    cb = tmp_path / "cookbook"
    assert sorted(p.name for p in cb.iterdir()) == ["cookbook.json", "index.json"]


def test_create_is_idempotent(tmp_path, run_cookr):
    assert run_cookr(CREATE, cwd=tmp_path).returncode == 0
    before = (tmp_path / "cookbook" / "cookbook.json").read_text()
    r2 = run_cookr(CREATE, cwd=tmp_path)
    assert r2.returncode == 0
    assert "already is the cookbook" in r2.stdout
    assert (tmp_path / "cookbook" / "cookbook.json").read_text() == before


def _convert(run_cookr, doc):
    """Fold a hand-written doc into its source folder: validate fails any
    artifact doc that has none, since the folder is the artifact's source.
    The folder is a new artifact, so `update` indexes it, as after any change."""
    r = run_cookr(["convert", str(doc)])
    assert r.returncode == 0, r.stderr or r.stdout
    r = run_cookr(["update", "-p", str(doc.parent.parent), "--author", "T"])
    assert r.returncode == 0, r.stderr or r.stdout


def test_update_validate_lint_green(tmp_path, run_cookr):
    cb = _create(run_cookr, tmp_path)
    (cb / "recipes" / "hello.md").write_text("# Hello\n", encoding="utf-8")

    upd = run_cookr(["update", "-p", str(cb), "--author", "Tester"])
    assert upd.returncode == 0, upd.stderr or upd.stdout
    assert (cb / "recipes" / "INDEX.md").is_file()
    _convert(run_cookr, cb / "recipes" / "hello.md")

    val = run_cookr(["validate", "-p", str(cb)])
    assert val.returncode == 0, val.stdout

    lin = run_cookr(["lint", "-p", str(cb), "--no-llm"])
    assert lin.returncode == 0, lin.stdout


def test_update_is_idempotent_no_changes_second_run(tmp_path, run_cookr):
    cb = _create(run_cookr, tmp_path)
    (cb / "recipes" / "x.md").write_text("# X\n", encoding="utf-8")
    assert run_cookr(["update", "-p", str(cb), "--author", "T"]).returncode == 0
    _convert(run_cookr, cb / "recipes" / "x.md")

    # Capture a snapshot, run update again, expect no INDEX.md diff and validate green.
    before = (cb / "recipes" / "INDEX.md").read_text()
    assert run_cookr(["update", "-p", str(cb), "--author", "T"]).returncode == 0
    after = (cb / "recipes" / "INDEX.md").read_text()
    assert before == after

    val = run_cookr(["validate", "-p", str(cb)])
    assert val.returncode == 0, val.stdout


def test_validate_detects_drift(tmp_path, run_cookr):
    cb = _create(run_cookr, tmp_path)
    (cb / "recipes" / "alpha.md").write_text("# Alpha\n", encoding="utf-8")
    assert run_cookr(["update", "-p", str(cb), "--author", "T"]).returncode == 0
    _convert(run_cookr, cb / "recipes" / "alpha.md")
    assert run_cookr(["validate", "-p", str(cb)]).returncode == 0

    # Add a new recipe that has full frontmatter so Phase A is clean — but skip
    # update so the index goes stale. validate must detect drift.
    (cb / "recipes" / "gamma.md").write_text(
        "---\nid: 22222222-3333-4444-5555-666666666666\ntitle: Gamma\n"
        "domain: agenticdevelopercookbook://cookbook/recipes/gamma\ntype: recipe\n"
        "version: 1.0.0\nstatus: draft\nlanguage: en\ncreated: 2026-05-15\n"
        "modified: 2026-05-15\nauthor: T\ncopyright: 2026 T\nlicense: MIT\n"
        "summary: x\n---\n# Gamma\n",
        encoding="utf-8",
    )
    assert run_cookr(["convert", str(cb / "recipes" / "gamma.md")]).returncode == 0  # no update: the index goes stale
    r = run_cookr(["validate", "-p", str(cb)])
    assert r.returncode != 0
    assert "drift" in r.stdout.lower() or "drift" in r.stderr.lower()


def test_help_lists_modules(run_cookr):
    r = run_cookr(["--help"])
    assert r.returncode == 0
    for name in ("create", "update", "lint", "validate", "bump"):
        assert name in r.stdout
