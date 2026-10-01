from __future__ import annotations

import json

from cookr.cli import main


def test_inventory_table(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory"]) == 0
    out = capsys.readouterr().out
    assert "components/button" in out
    assert "components/chat-composer" in out
    assert "blocks/stat-card" in out
    assert "stories" not in out


def test_inventory_json(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert {"name", "path", "tier", "platform", "claimed"} <= set(rows[0])
    assert len(rows) == 5
    assert all(r["claimed"] for r in rows)


def test_inventory_tier_filter(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory", "--tier", "blocks", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert [r["name"] for r in rows] == ["blocks/stat-card"]


def test_inventory_unknown_tier_exits_2(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory", "--tier", "nope"]) == 2
    out = capsys.readouterr().out
    assert "unknown group `nope`" in out
    for tier in ("blocks", "components", "ui"):
        assert tier in out


def test_inventory_without_config_exits_2(tmp_path, capsys):
    assert main(["-p", str(tmp_path), "inventory"]) == 2


def _add_bracketed_root(repo):
    for seg in ("[slug]", "[b]", "weird[/x]"):
        d = repo / "web" / "app" / seg
        d.mkdir(parents=True)
        (d / "Page.tsx").write_text("export {}\n", encoding="utf-8")
    p = repo / "cookbook" / "cookbook.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["code"]["roots"].append({"path": "web/app", "platform": "web", "recipes": "pages"})
    p.write_text(json.dumps(data), encoding="utf-8")


def test_inventory_table_prints_bracketed_paths_verbatim(mini_repo, capsys, monkeypatch):
    monkeypatch.setenv("COLUMNS", "300")  # keep each path on one table line
    _add_bracketed_root(mini_repo)
    assert main(["-p", str(mini_repo), "inventory", "--tier", "pages"]) == 0
    out = capsys.readouterr().out
    for seg in ("[slug]", "[b]", "weird[/x]"):
        assert f"web/app/{seg}/Page.tsx" in out
