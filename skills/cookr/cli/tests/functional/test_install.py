"""The installed `cookr` shim works end to end."""

from __future__ import annotations

from pathlib import Path


def test_shim_runs_and_reports_version(run_cookr):
    r = run_cookr(["--version"])
    assert r.returncode == 0
    assert "cookr" in r.stdout


def test_installed_package_has_references(cookr_bin):
    bin_dir = Path(cookr_bin).parent
    extract = bin_dir / "_cookr_pkg" / "cookr" / "modules" / "prompt" / "prompts" / "extract" / "references"
    assert (extract / "guidelines" / "recipe-quality" / "source-fidelity.md").is_file()
    # Templates come from the package's own references, not the extract module's.
    assert (bin_dir / "_cookr_pkg" / "references" / "templates" / "ingredient.md").is_file()
    assert not (extract / "templates").exists()


def test_shim_coverage_on_fixture(run_cookr, mini_repo):
    r = run_cookr(["-p", str(mini_repo), "coverage", "--json"])
    assert r.returncode == 0
    assert '"unmatched_recipes"' in r.stdout

