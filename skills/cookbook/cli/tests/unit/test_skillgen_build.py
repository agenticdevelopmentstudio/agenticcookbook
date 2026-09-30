"""`cookbook skills build` end to end: golden output for both source layouts,
byte stability, the output-directory guard, and `--check` drift detection.

Regenerate the golden trees after an intended output change with
`UPDATE_GOLDEN=1 python3 -m pytest tests/unit/test_skillgen_build.py`, and
review the diff before committing it.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

from cookbook.cli import main
from cookbook.skillgen import build as skill_build
from cookbook.skillgen import source as skill_source

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "skillgen"
CASES = {"cookbook": "cookbook-src", "recipes": "recipes-src"}


def _built(case: str) -> skill_build.Build:
    src = skill_source.resolve(FIXTURES / CASES[case])
    assert src is not None
    return skill_build.build(src)


@pytest.mark.parametrize("case", sorted(CASES))
def test_output_matches_golden(case):
    result = _built(case)
    assert result.errors == []
    expected_dir = FIXTURES / f"{case}-expected"
    if os.environ.get("UPDATE_GOLDEN"):
        if expected_dir.exists():
            shutil.rmtree(expected_dir)
        skill_build.write(expected_dir, result.files)
    assert skill_build.drift(result.files, skill_build.read_tree(expected_dir)) == []


def test_the_cookbook_fixture_exercises_aliases_drift_skips_and_split_sections():
    result = _built("cookbook")
    kinds = sorted({w.kind for w in result.warnings})
    assert kinds == ["drift", "skipped"]
    manifest = json.loads(result.files["manifest.json"])
    # The reviewing copy is identical to the implementing one: one leaf, two routers.
    assert manifest["routers"]["review-security"]["leaves"] == ["implement-security/input-validation"]
    assert "review-security" in manifest["leaves"]["implement-security/input-validation"]["routers"]
    # A verify router reuses its review router's index rather than writing its own.
    assert "skills/verify-security/index.md" not in result.files
    assert "skills/recipes-ui/leaves/login-form--states.md" in result.files


def test_the_recipes_fixture_records_its_code_roots_and_warns_on_a_rule_less_doc():
    result = _built("recipes")
    manifest = json.loads(result.files["manifest.json"])
    assert manifest["code_roots"] == ["src"]
    assert sorted(manifest["routers"]) == ["implement-general", "implement-status-server"]
    assert [(w.kind, w.where) for w in result.warnings] == [("no-rules", "notes.md")]


def test_a_leaf_over_the_cap_is_an_error_not_a_silent_truncation():
    src = skill_source.resolve(FIXTURES / "cookbook-src")
    result = skill_build.build(src, cap=200)
    assert any("leaf cap" in e for e in result.errors)


def test_write_refuses_a_directory_it_does_not_own(tmp_path):
    (tmp_path / "keep.txt").write_text("mine")
    with pytest.raises(skill_build.RefusedOutput):
        skill_build.write(tmp_path, {"a.md": "x"})
    assert (tmp_path / "keep.txt").read_text() == "mine"


def test_write_replaces_its_own_output_and_keeps_git(tmp_path):
    files = _built("recipes").files
    skill_build.write(tmp_path, files)
    (tmp_path / ".git").mkdir()
    (tmp_path / "skills" / "stale.md").write_text("old")
    skill_build.write(tmp_path, files)
    assert not (tmp_path / "skills" / "stale.md").exists()
    assert (tmp_path / ".git").is_dir()
    assert skill_build.drift(files, skill_build.read_tree(tmp_path)) == []


def test_cli_build_then_check_then_drift(tmp_path, patch_refs):
    out = tmp_path / "plugin"
    args = ["skills", "build", "--source", str(FIXTURES / "recipes-src"), "--out", str(out)]
    assert main(args) == 0
    assert main(args + ["--check"]) == 0
    (out / "skills" / "implement-general" / "index.md").write_text("edited\n")
    assert main(args + ["--check"]) == 1


def test_cli_rejects_a_source_that_is_neither_layout(tmp_path, patch_refs):
    assert main(["skills", "build", "--source", str(tmp_path), "--out", str(tmp_path / "o")]) == 2
