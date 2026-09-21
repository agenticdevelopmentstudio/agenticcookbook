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
    assert {"name", "tier", "platforms", "paths", "state", "recipe", "problems"} <= set(row)


def test_require_complete_fails_on_partial(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "complete"]) == 1


def test_require_partial_passes_when_nothing_missing(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 0


def test_require_partial_fails_on_missing(mini_repo, capsys):
    (mini_repo / "recipes" / "chat-composer.md").unlink()
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 1


def test_tier_scoped_require(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--tier", "apple", "--require", "complete"]) == 0
