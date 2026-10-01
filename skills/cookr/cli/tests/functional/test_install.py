"""The installed `cookr` shim works end to end."""

from __future__ import annotations

from pathlib import Path

import pytest


def test_shim_runs_and_reports_version(run_cookr):
    r = run_cookr(["--version"])
    assert r.returncode == 0
    assert "cookr" in r.stdout


def test_installed_package_has_references(cookr_bin):
    bin_dir = Path(cookr_bin).parent
    extract = bin_dir / "_cookr_pkg" / "cookr" / "modules" / "prompt" / "prompts" / "extract" / "references"
    assert (extract / "guidelines" / "recipe-quality" / "source-fidelity.md").is_file()
    # Templates come from the cookbook package's references, not the extract module's.
    assert (bin_dir / "_cookbook_pkg" / "references" / "templates" / "ingredient.md").is_file()
    assert not (extract / "templates").exists()


def test_shim_coverage_on_fixture(run_cookr, mini_repo):
    r = run_cookr(["-p", str(mini_repo), "coverage", "--json"])
    assert r.returncode == 0
    assert '"unmatched_recipes"' in r.stdout


def test_plugin_bundle_excludes_cli(cookr_bin):
    repo_root = Path(__file__).resolve().parents[5]
    bundled = repo_root / "plugins" / "adh" / "skills" / "cookr"
    if not bundled.is_dir():
        pytest.skip("plugin not assembled in this checkout")
    assert (bundled / "SKILL.md").is_file()
    assert not (bundled / "cli").exists()
    assert not (bundled / "bin").exists()
