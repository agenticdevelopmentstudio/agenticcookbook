"""`cookr arrangement` at the CLI level."""

from __future__ import annotations

import json

from cookr.cli import main


def _drift_button(mini_repo):
    (mini_repo / "cookbook" / "components" / "ui").mkdir()
    (mini_repo / "cookbook" / "components" / "button.md").rename(
        mini_repo / "cookbook" / "components" / "ui" / "button.md")


def test_arrangement_default_table_hides_aligned_specs(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "arrangement"]) == 0
    out = capsys.readouterr().out
    assert "site-menu" in out and "unplaced" in out
    assert "components/button" not in out  # aligned, hidden by default
    assert "aligned=3  drifted=0  unplaced=1  outside=0" in out


def test_arrangement_all_shows_every_spec(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "arrangement", "--all"]) == 0
    out = capsys.readouterr().out
    for name in ("blocks/stat-card", "components/button", "components/chat-composer", "site-menu"):
        assert name in out


def test_arrangement_json_reports_rows_and_tally(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "arrangement", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert {r["name"]: r["state"] for r in data["rows"]} == {
        "blocks/stat-card": "aligned", "components/button": "aligned",
        "components/chat-composer": "aligned", "site-menu": "unplaced",
    }
    assert data["tally"] == {"aligned": 3, "drifted": 0, "unplaced": 1, "outside": 0}


def test_arrangement_tier_filters_the_rows(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "arrangement", "--tier", "components", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [r["name"] for r in data["rows"]] == ["components/button", "components/chat-composer"]


def test_arrangement_unknown_tier_exits_2(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "arrangement", "--tier", "nope"]) == 2
    assert "unknown group `nope`" in capsys.readouterr().out


def test_arrangement_without_config_exits_2(tmp_path, capsys):
    assert main(["-p", str(tmp_path), "arrangement"]) == 2


def test_arrangement_reports_drift_without_strict(mini_repo, capsys):
    _drift_button(mini_repo)
    assert main(["-p", str(mini_repo), "arrangement"]) == 0  # not --strict: still exit 0
    out = capsys.readouterr().out
    assert "components/ui/button" in out and "drifted" in out
    assert "components/button" in out  # the `expected` column


def test_arrangement_strict_exits_1_on_drift(mini_repo, capsys):
    _drift_button(mini_repo)
    assert main(["-p", str(mini_repo), "arrangement", "--strict"]) == 1
    assert "1 spec(s) drifted" in capsys.readouterr().out


def test_arrangement_strict_json_still_exits_1_on_drift(mini_repo, capsys):
    _drift_button(mini_repo)
    assert main(["-p", str(mini_repo), "arrangement", "--strict", "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["tally"]["drifted"] == 1
