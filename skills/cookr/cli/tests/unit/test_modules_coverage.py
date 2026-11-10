from __future__ import annotations

import json

import pytest

from cookr.cli import main
from cookr.core.identity import check_uuid

from .cookbook_helpers import ADC_ID, SpecDoc, add_dependency, add_root, remove_spec


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
    remove_spec(mini_repo, "components/chat-composer")
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


def test_coverage_grades_compliance_citations_against_the_reachable_checks(mini_repo, capsys):
    # A reachable dependency holding exactly the checks the fixture cites, so
    # only the made-up citation added below names nothing.
    add_dependency(mini_repo, "deps/adc", checks=[("best-practices", "unit-test-coverage"),
                                                  ("best-practices", "separation-of-concerns")])
    made_up = check_uuid(ADC_ID, "security", "made-up")
    doc = SpecDoc(mini_repo, "components/button")
    doc.write_text(doc.read_text().rstrip()
                   + f"\n\n[adc.check.security.made-up](cookbook:{ADC_ID}/{made_up})\n")
    assert main(["-p", str(mini_repo), "coverage", "--json"]) == 0
    row = next(r for r in json.loads(capsys.readouterr().out)["rows"] if r["name"] == "components/button")
    assert row["problems"] == ["cites compliance checks that do not exist: "
                               f"adc.check.security.made-up ({ADC_ID}/{made_up})"]


def test_missing_row_falls_back_to_the_codes_arrangement_when_unclaimed(mini_repo, capsys):
    # Deleting the spec drops its index implementations claim: the web
    # source keeps the same name by coincidence (it already matches the
    # code's own arrangement), but the two apple sources it used to fold
    # under `components/button` (via a whole-directory claim) split back
    # into their own arrangement-derived names.
    remove_spec(mini_repo, "components/button")
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    for name in ("components/button", "ui/button", "ui/toolbar-button"):
        line = next(l for l in out.splitlines() if name in l)
        assert "missing" in line


# Opts out of upgrade-on-contact: an unparseable artifact.json cannot be upgraded, only reported.
@pytest.mark.usefixtures("legacy_no_upgrade")
def test_unreadable_artifact_is_a_clean_exit_2(mini_repo, capsys):
    extra = mini_repo / "cookbook" / "extra"
    extra.mkdir()
    (extra / "artifact.json").write_text("{not json", encoding="utf-8")
    assert main(["-p", str(mini_repo), "coverage"]) == 2
    assert "extra" in capsys.readouterr().out


def test_bracketed_problem_text_is_not_read_as_markup(mini_repo, capsys):
    d = mini_repo / "web" / "app" / "[slug]"
    d.mkdir(parents=True)
    (d / "Page.tsx").write_text("export {}\n", encoding="utf-8")
    add_root(mini_repo, "web/app", "web", "[b]pages")
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    assert "[b]pages" in out
