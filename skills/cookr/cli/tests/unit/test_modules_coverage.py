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
    assert set(row) == {"name", "slug", "tiers", "platforms", "paths", "state", "problems"}
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

    import re

    p = mini_repo / "recipes" / "button.md"
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
    row = next(r for r in json.loads(capsys.readouterr().out)["rows"] if r["name"] == "button")
    assert row["problems"] == ["cites compliance checks not in the catalog: security#made-up"]


def test_table_prints_the_slug_even_for_a_missing_row(mini_repo, capsys):
    (mini_repo / "recipes" / "button.md").unlink()
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    line = next(l for l in out.splitlines() if "toolbar-button" in l)
    assert "missing" in line and "button" in line.replace("toolbar-button", "")


def test_bad_recipe_frontmatter_is_a_clean_exit_2(mini_repo, capsys):
    (mini_repo / "recipes" / "extra.md").write_text("---\ntitle: a: b\n---\n# x\n", encoding="utf-8")
    assert main(["-p", str(mini_repo), "coverage"]) == 2
    assert "extra.md" in capsys.readouterr().out


def test_bracketed_problem_text_is_not_read_as_markup(mini_repo, capsys):
    import json as _json
    d = mini_repo / "web" / "app" / "[slug]"
    d.mkdir(parents=True)
    (d / "Page.tsx").write_text("export {}\n", encoding="utf-8")
    p = mini_repo / ".cookr.json"
    data = _json.loads(p.read_text(encoding="utf-8"))
    data["roots"].append({"path": "web/app", "tier": "[b]pages", "platform": "web"})
    p.write_text(_json.dumps(data), encoding="utf-8")
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    assert "[b]pages" in out
