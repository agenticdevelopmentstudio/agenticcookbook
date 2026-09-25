from __future__ import annotations

import json
import re

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
    assert set(row) == {"name", "tiers", "platforms", "paths", "state", "problems"}
    assert row["name"] == "blocks/stat-card"
    assert row["tiers"] == ["blocks"]


def test_require_complete_fails_on_partial(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "complete"]) == 1


def test_require_partial_passes_when_nothing_missing(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 0


def test_require_partial_fails_on_missing(mini_repo, capsys):
    (mini_repo / "cookbook" / "components" / "chat-composer.md").unlink()
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 1


def test_unknown_tier_exits_2_even_with_require(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--tier", "nope", "--require", "complete"]) == 2
    out = capsys.readouterr().out
    assert "unknown group `nope`" in out
    for tier in ("blocks", "components", "ui"):
        assert tier in out


def test_tier_scoped_require_passes_vacuously_when_the_tier_has_no_rows(mini_repo, capsys):
    # The apple/UI root's `recipes` group ("ui") never gets its own coverage
    # row here: every apple source is claimed under `components/button`. An
    # empty scope is trivially "every component in scope is at least X".
    assert main(["-p", str(mini_repo), "coverage", "--tier", "ui", "--require", "complete"]) == 0
    assert "every component in scope is at least" in capsys.readouterr().out


def test_coverage_grades_compliance_citations_against_the_catalog(mini_repo, capsys, monkeypatch, tmp_path):
    from cookr.modules import coverage as coverage_module

    p = mini_repo / "cookbook" / "components" / "button.md"
    # A catalog holding exactly the checks the fixture cites, so only the
    # made-up citation added below is unknown.
    catalog = tmp_path / "compliance"
    catalog.mkdir()
    cited = re.findall(r"://compliance/([\w-]+)#([\w-]+)", p.read_text(encoding="utf-8"))
    for category in {c for c, _ in cited}:
        (catalog / f"{category}.md").write_text(
            "".join(f"### {check}\n" for c, check in cited if c == category), encoding="utf-8")
    monkeypatch.setattr(coverage_module, "compliance_dir", lambda: catalog)
    p.write_text(p.read_text(encoding="utf-8").rstrip()
                 + "\n\n[x](agenticdevelopercookbook://compliance/security#made-up)\n", encoding="utf-8")
    assert main(["-p", str(mini_repo), "coverage", "--json"]) == 0
    row = next(r for r in json.loads(capsys.readouterr().out)["rows"] if r["name"] == "components/button")
    assert row["problems"] == ["cites compliance checks not in the catalog: security#made-up"]


def test_missing_row_falls_back_to_the_codes_arrangement_when_unclaimed(mini_repo, capsys):
    # Deleting the spec drops its Reference Implementations claim: the web
    # source keeps the same name by coincidence (it already matches the
    # code's own arrangement), but the two apple sources it used to fold
    # under `components/button` (via a whole-directory claim) split back
    # into their own arrangement-derived names.
    (mini_repo / "cookbook" / "components" / "button.md").unlink()
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    for name in ("components/button", "ui/button", "ui/toolbar-button"):
        line = next(l for l in out.splitlines() if name in l)
        assert "missing" in line


def test_bad_recipe_frontmatter_is_a_clean_exit_2(mini_repo, capsys):
    (mini_repo / "cookbook" / "extra.md").write_text("---\ntitle: a: b\n---\n# x\n", encoding="utf-8")
    assert main(["-p", str(mini_repo), "coverage"]) == 2
    assert "extra.md" in capsys.readouterr().out


def test_bracketed_problem_text_is_not_read_as_markup(mini_repo, capsys):
    d = mini_repo / "web" / "app" / "[slug]"
    d.mkdir(parents=True)
    (d / "Page.tsx").write_text("export {}\n", encoding="utf-8")
    p = mini_repo / "cookbook" / "cookbook.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["code"]["roots"].append({"path": "web/app", "platform": "web", "recipes": "[b]pages"})
    p.write_text(json.dumps(data), encoding="utf-8")
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    assert "[b]pages" in out
