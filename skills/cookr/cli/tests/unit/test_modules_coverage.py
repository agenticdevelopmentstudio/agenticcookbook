from __future__ import annotations

import json

from cookr.cli import main


def test_coverage_table_and_tally(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    assert "complete" in out and "partial" in out
    assert "site-menu" in out          # unmatched recipe listed


def test_coverage_json_shape(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert set(data) == {"rows", "tally", "unmatched_recipes"}
    row = data["rows"][0]
    assert {"name", "slug", "tiers", "platforms", "paths", "state", "recipe", "problems"} <= set(row)
    assert row["slug"] == "button"
    assert row["name"] == "button"
    assert row["tiers"] == ["apple", "primitives"]


def test_require_complete_fails_on_partial(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "complete"]) == 1


def test_require_partial_passes_when_nothing_missing(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 0


def test_require_partial_fails_on_missing(mini_repo, capsys):
    (mini_repo / "recipes" / "chat-composer.md").unlink()
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 1


def test_unknown_tier_exits_2_even_with_require(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--tier", "nope", "--require", "complete"]) == 2
    out = capsys.readouterr().out
    assert "unknown tier `nope`" in out
    for tier in ("primitives", "blocks", "apple"):
        assert tier in out


def test_tier_scoped_require(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--tier", "apple", "--require", "complete"]) == 0


def test_coverage_grades_compliance_citations_against_the_catalog(mini_repo, capsys, monkeypatch, tmp_path):
    from cookr.modules import coverage as coverage_module

    catalog = tmp_path / "compliance"
    catalog.mkdir()
    (catalog / "best-practices.md").write_text("### unit-test-coverage\n")
    monkeypatch.setattr(coverage_module, "compliance_dir", lambda: catalog)
    p = mini_repo / "recipes" / "button.md"
    p.write_text(p.read_text(encoding="utf-8").rstrip()
                 + "\n\n[x](agenticdevelopercookbook://compliance/security#made-up)\n", encoding="utf-8")
    assert main(["-p", str(mini_repo), "coverage", "--json"]) == 0
    row = next(r for r in json.loads(capsys.readouterr().out)["rows"] if r["name"] == "button")
    assert row["problems"] == ["cites compliance checks not in the catalog: security#made-up"]
