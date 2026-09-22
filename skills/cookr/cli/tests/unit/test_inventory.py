from __future__ import annotations

from cookr.core.config import load_config
from cookr.core.inventory import scan


def test_scan_lists_sources_by_tier(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    rows = scan(cfg)
    names = [(r.tier, r.name, r.platform) for r in rows]
    assert names == [
        ("apple", "button", "apple"),
        ("apple", "toolbar-button", "apple"),
        ("blocks", "stat-card", "web"),
        ("primitives", "button", "web"),
        ("primitives", "chat-composer", "web"),
    ]


def test_scan_drops_ignored(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    paths = [r.path for r in scan(cfg)]
    assert "web/components/button.stories.tsx" not in paths
    assert "web/components/index.ts" not in paths


def test_scan_paths_are_repo_relative_posix(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    assert "web/components/Button.tsx" in [r.path for r in scan(cfg)]


def test_scan_applies_a_rename_to_one_path(mini_repo):
    import json
    p = mini_repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["renames"] = {"web/components/Button.tsx": "web-button"}
    p.write_text(json.dumps(data), encoding="utf-8")
    rows = scan(load_config(p))
    by_path = {r.path: r.name for r in rows}
    assert by_path["web/components/Button.tsx"] == "web-button"
    assert "button" in {r.name for r in rows if r.platform == "apple"}
