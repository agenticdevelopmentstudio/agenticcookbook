"""End-to-end: a fresh client cookbook goes through the full lifecycle without
errors. Uses the installed `cookr` shim (real subprocess, real PYTHONPATH)
so we exercise ./install's output, not just in-process Python."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")



def test_create_scaffolds_expected_files(tmp_path, run_cookr):
    r = run_cookr(["create"], cwd=tmp_path)
    assert r.returncode == 0, r.stderr or r.stdout
    cb = tmp_path / "cookbook"
    assert (cb / "index.md").is_file()
    assert (cb / "description.md").is_file()
    assert (cb / "recipes" / ".gitkeep").is_file()
    assert (cb / "reference" / ".gitkeep").is_file()


def test_create_is_idempotent(tmp_path, run_cookr):
    assert run_cookr(["create"], cwd=tmp_path).returncode == 0
    r2 = run_cookr(["create"], cwd=tmp_path)
    assert r2.returncode == 0
    assert "skipped" in r2.stdout


def test_update_validate_lint_green(tmp_path, run_cookr):
    assert run_cookr(["create"], cwd=tmp_path).returncode == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "hello.md").write_text("# Hello\n", encoding="utf-8")

    upd = run_cookr(["update", "-p", str(cb), "--author", "Tester"])
    assert upd.returncode == 0, upd.stderr or upd.stdout
    assert (cb / "recipes" / "INDEX.md").is_file()

    val = run_cookr(["validate", "-p", str(cb)])
    assert val.returncode == 0, val.stdout

    lin = run_cookr(["lint", "-p", str(cb), "--no-llm"])
    assert lin.returncode == 0, lin.stdout


def test_update_is_idempotent_no_changes_second_run(tmp_path, run_cookr):
    assert run_cookr(["create"], cwd=tmp_path).returncode == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "x.md").write_text("# X\n", encoding="utf-8")
    assert run_cookr(["update", "-p", str(cb), "--author", "T"]).returncode == 0

    # Capture a snapshot, run update again, expect no INDEX.md diff and validate green.
    before = (cb / "recipes" / "INDEX.md").read_text()
    assert run_cookr(["update", "-p", str(cb), "--author", "T"]).returncode == 0
    after = (cb / "recipes" / "INDEX.md").read_text()
    assert before == after

    val = run_cookr(["validate", "-p", str(cb)])
    assert val.returncode == 0, val.stdout


def test_validate_detects_drift(tmp_path, run_cookr):
    assert run_cookr(["create"], cwd=tmp_path).returncode == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "alpha.md").write_text("# Alpha\n", encoding="utf-8")
    assert run_cookr(["update", "-p", str(cb), "--author", "T"]).returncode == 0
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
    r = run_cookr(["validate", "-p", str(cb)])
    assert r.returncode != 0
    assert "drift" in r.stdout.lower() or "drift" in r.stderr.lower()


def test_help_lists_modules(run_cookr):
    r = run_cookr(["--help"])
    assert r.returncode == 0
    for name in ("create", "update", "lint", "validate", "bump"):
        assert name in r.stdout
