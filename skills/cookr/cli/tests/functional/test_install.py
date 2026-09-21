"""The installed `cookr` shim works end to end."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def test_shim_runs_and_reports_version(run_cookr):
    r = run_cookr(["--version"])
    assert r.returncode == 0
    assert "cookr" in r.stdout


def test_installed_package_has_references(cookr_bin):
    pkg = Path(cookr_bin).parent / "_cookr_pkg" / "cookr" / "modules" / "prompt" / "prompts" / "extract" / "references"
    assert (pkg / "templates" / "ingredient.md").is_file()
    assert (pkg / "guidelines" / "recipe-quality" / "source-fidelity.md").is_file()


def test_shim_coverage_on_fixture(run_cookr, mini_repo):
    r = run_cookr(["-p", str(mini_repo), "coverage", "--json"])
    assert r.returncode == 0
    assert '"unmatched_recipes"' in r.stdout


def test_plugin_bundle_excludes_cli(cookr_bin):
    repo_root = Path(__file__).resolve().parents[5]
    bundled = repo_root / "plugins" / "adh" / "skills" / "cookr"
    # install.sh always mkdir()s the per-skill bundle dir, even when the skill
    # has no non-excluded content to copy — so an empty dir here just means
    # skills/cookr has no SKILL.md yet (added in a later task), not that the
    # plugin failed to assemble.
    if not bundled.is_dir() or not any(bundled.iterdir()):
        pytest.skip("plugin not assembled (or has no SKILL.md yet) in this checkout")
    assert (bundled / "SKILL.md").is_file()
    assert not (bundled / "cli").exists()
    assert not (bundled / "bin").exists()
