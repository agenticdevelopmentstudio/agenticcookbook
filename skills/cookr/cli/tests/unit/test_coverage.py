from __future__ import annotations

from cookr.core.config import load_config
from cookr.core.coverage import compute


def _rows(mini_repo, tier=None):
    cfg = load_config(mini_repo / ".cookr.json")
    return compute(cfg, tier=tier)


def test_one_row_per_component_name_within_tier(mini_repo):
    report = _rows(mini_repo)
    keys = [(r.tier, r.name) for r in report.rows]
    assert keys == [
        ("apple", "button"),
        ("apple", "toolbar-button"),
        ("blocks", "stat-card"),
        ("primitives", "button"),
        ("primitives", "chat-composer"),
    ]


def test_states(mini_repo):
    by = {(r.tier, r.name): r for r in _rows(mini_repo).rows}
    assert by[("primitives", "button")].state == "complete"
    assert by[("apple", "button")].state == "complete"
    assert by[("apple", "toolbar-button")].state == "complete"      # alias → button
    assert by[("apple", "toolbar-button")].recipe == "button"
    assert by[("blocks", "stat-card")].state == "partial"
    assert by[("primitives", "chat-composer")].state == "partial"


def test_missing_when_no_recipe(mini_repo):
    (mini_repo / "recipes" / "chat-composer.md").unlink()
    by = {(r.tier, r.name): r for r in _rows(mini_repo).rows}
    assert by[("primitives", "chat-composer")].state == "missing"
    assert by[("primitives", "chat-composer")].recipe is None


def test_tier_filter(mini_repo):
    assert {r.tier for r in _rows(mini_repo, tier="blocks").rows} == {"blocks"}


def test_unmatched_recipes_listed(mini_repo):
    assert _rows(mini_repo).unmatched_recipes == ["site-menu"]


def test_tally_and_below(mini_repo):
    report = _rows(mini_repo)
    assert report.tally()["primitives"] == {"missing": 0, "partial": 1, "complete": 1}
    assert [r.name for r in report.below("complete")] == ["stat-card", "chat-composer"]
    assert report.below("partial") == []
