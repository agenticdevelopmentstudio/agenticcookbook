from __future__ import annotations

from cookr.core.config import load_config
from cookr.core.coverage import compute


def _rows(mini_repo, tier=None):
    cfg = load_config(mini_repo / ".cookr.json")
    return compute(cfg, tier=tier)


def test_one_row_per_component_name_across_tiers(mini_repo):
    report = _rows(mini_repo)
    assert [r.name for r in report.rows] == [
        "button", "chat-composer", "stat-card", "toolbar-button",
    ]


def test_cross_platform_name_is_one_row(mini_repo):
    by = {r.name: r for r in _rows(mini_repo).rows}
    row = by["button"]
    assert row.tiers == ("apple", "primitives")
    assert row.platforms == ("apple", "web")
    assert row.paths == ("apple/UI/Button.swift", "web/components/Button.tsx")
    assert row.state == "complete"


def test_states(mini_repo):
    by = {r.name: r for r in _rows(mini_repo).rows}
    assert by["button"].state == "complete"
    assert by["toolbar-button"].state == "complete"      # alias → button
    assert by["toolbar-button"].recipe == "button"
    assert by["stat-card"].state == "partial"
    assert by["chat-composer"].state == "partial"


def test_missing_when_no_recipe(mini_repo):
    (mini_repo / "recipes" / "chat-composer.md").unlink()
    by = {r.name: r for r in _rows(mini_repo).rows}
    assert by["chat-composer"].state == "missing"
    assert by["chat-composer"].recipe is None


def test_tier_filter_keeps_rows_whose_tiers_include_it(mini_repo):
    report = _rows(mini_repo, tier="apple")
    assert [r.name for r in report.rows] == ["button", "toolbar-button"]
    assert all("apple" in r.tiers for r in report.rows)


def test_unmatched_recipes_listed(mini_repo):
    assert _rows(mini_repo).unmatched_recipes == ["site-menu"]


def test_unmatched_recipes_survive_a_tier_filter(mini_repo):
    assert _rows(mini_repo, tier="apple").unmatched_recipes == _rows(mini_repo).unmatched_recipes


def test_tally_counts_a_row_under_each_of_its_tiers(mini_repo):
    tally = _rows(mini_repo).tally()
    assert tally["primitives"] == {"missing": 0, "partial": 1, "complete": 1}
    assert tally["blocks"] == {"missing": 0, "partial": 1, "complete": 0}
    assert tally["apple"] == {"missing": 0, "partial": 0, "complete": 2}


def test_tally_under_a_tier_filter_reports_only_that_tier(mini_repo):
    # `button` sits in both apple and primitives; a scoped report must not
    # leak a primitives line into the apple view.
    assert _rows(mini_repo, tier="apple").tally() == {
        "apple": {"missing": 0, "partial": 0, "complete": 2},
    }


def test_below(mini_repo):
    report = _rows(mini_repo)
    assert [r.name for r in report.below("complete")] == ["chat-composer", "stat-card"]
    assert report.below("partial") == []


def test_slug_is_the_alias_resolved_recipe_stem(mini_repo):
    by = {r.name: r for r in _rows(mini_repo).rows}
    assert by["toolbar-button"].slug == "button"
    assert by["button"].slug == "button"


def test_slug_is_set_even_when_the_recipe_is_missing(mini_repo):
    (mini_repo / "recipes" / "button.md").unlink()
    by = {r.name: r for r in _rows(mini_repo).rows}
    assert by["toolbar-button"].state == "missing"
    assert by["toolbar-button"].recipe is None
    assert by["toolbar-button"].slug == "button"


def test_renamed_component_gets_its_own_row(mini_repo):
    import json
    from cookr.core.config import load_config
    from cookr.core.coverage import compute
    p = mini_repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["renames"] = {"web/components/Button.tsx": "web-button"}
    p.write_text(json.dumps(data), encoding="utf-8")
    rows = {r.name: r for r in compute(load_config(p)).rows}
    assert rows["web-button"].paths == ("web/components/Button.tsx",)
    assert rows["web-button"].slug == "web-button"
    assert "web/components/Button.tsx" not in rows["button"].paths
