from __future__ import annotations

import json

from cookr.cli import main


def test_inventory_table(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory"]) == 0
    out = capsys.readouterr().out
    assert "toolbar-button" in out
    assert "stories" not in out


def test_inventory_json(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert {"name", "path", "tier", "platform"} <= set(rows[0])
    assert len(rows) == 5


def test_inventory_tier_filter(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory", "--tier", "blocks", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert [r["name"] for r in rows] == ["stat-card"]


def test_inventory_without_config_exits_2(tmp_path, capsys):
    assert main(["-p", str(tmp_path), "inventory"]) == 2
