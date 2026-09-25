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
    assert by["toolbar-button"].slug == "button"
    assert by["stat-card"].state == "partial"
    assert by["chat-composer"].state == "partial"


def test_missing_when_no_recipe(mini_repo):
    (mini_repo / "recipes" / "chat-composer.md").unlink()
    by = {r.name: r for r in _rows(mini_repo).rows}
    assert by["chat-composer"].state == "missing"
    assert by["chat-composer"].slug == "chat-composer"


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


def test_row_has_no_derived_recipe_field(mini_repo):
    # `recipe` was `slug if state != "missing" else None`: one fact, two fields.
    row = _rows(mini_repo).rows[0]
    assert not hasattr(row, "recipe")


# --- name collisions -------------------------------------------------------

def _add_root(repo, path, tier, platform, files):
    import json
    d = repo / path
    d.mkdir(parents=True, exist_ok=True)
    for f in files:
        (d / f).write_text("export {}\n", encoding="utf-8")
    p = repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["roots"].append({"path": path, "tier": tier, "platform": platform})
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_same_platform_name_in_two_tiers_is_a_collision_problem(mini_repo):
    _add_root(mini_repo, "web/settings", "settings", "web", ["Button.tsx"])
    by = {r.name: r for r in _rows(mini_repo).rows}
    row = by["button"]
    assert row.state == "partial"            # button.md alone is complete
    assert any(p.startswith("name collision across tiers (web in primitives, settings)")
               for p in row.problems)


def test_collision_shows_on_a_missing_row_too(mini_repo):
    _add_root(mini_repo, "web/settings", "settings", "web", ["Button.tsx"])
    (mini_repo / "recipes" / "button.md").unlink()
    row = {r.name: r for r in _rows(mini_repo).rows}["button"]
    assert row.state == "missing"
    assert row.problems and row.problems[0].startswith("name collision")


def test_renaming_both_sides_to_the_name_records_a_deliberate_merge(mini_repo):
    import json
    p = _add_root(mini_repo, "web/settings", "settings", "web", ["Button.tsx"])
    data = json.loads(p.read_text(encoding="utf-8"))
    data["renames"] = {"web/settings/Button.tsx": "button", "web/components/Button.tsx": "button"}
    p.write_text(json.dumps(data), encoding="utf-8")
    row = {r.name: r for r in _rows(mini_repo).rows}["button"]
    assert row.state == "complete" and row.problems == ()


def test_cross_platform_and_same_tier_twins_are_not_collisions(mini_repo):
    # button: web + apple (cross-platform merge). A second web root in the
    # same tier (an iOS/macOS-style twin) is one component, not a collision.
    _add_root(mini_repo, "web/twin", "primitives", "web", ["Button.tsx"])
    row = {r.name: r for r in _rows(mini_repo).rows}["button"]
    assert row.state == "complete" and row.problems == ()


# --- grading cost ----------------------------------------------------------

def test_tier_filter_grades_only_in_scope_rows_once_per_slug(mini_repo, monkeypatch):
    from cookr.core import coverage as cov
    graded = []
    real = cov.problems
    monkeypatch.setattr(cov, "problems", lambda info, checks, platforms=None, domain=None: graded.append(info.slug) or real(info, checks, platforms, domain))
    report = _rows(mini_repo, tier="apple")
    assert [r.name for r in report.rows] == ["button", "toolbar-button"]
    # button and toolbar-button (aliased to button) share one grade; the
    # primitives/blocks rows are never graded for an apple-scoped report.
    assert graded == ["button"]
    assert report.unmatched_recipes == ["site-menu"]


def test_platforms_are_graded_against_every_aliased_component(mini_repo, monkeypatch):
    from cookr.core import coverage as cov
    seen = {}
    real = cov.problems
    monkeypatch.setattr(cov, "problems", lambda info, checks, platforms=None, domain=None: seen.setdefault(info.slug, platforms) and real(info, checks, platforms, domain))
    _rows(mini_repo)
    # button's components (Button.tsx, the Swift ToolbarButton aliased to it) span both platforms
    assert seen["button"] == {"web", "apple"}


def test_a_wrong_scheme_domain_keeps_the_row_partial(mini_repo):
    path = mini_repo / "recipes" / "button.md"
    path.write_text(path.read_text().replace("mini-repo://", "agenticdevelopercookbook://"))
    row = {r.name: r for r in _rows(mini_repo).rows}["button"]
    assert row.state == "partial"
    assert any("frontmatter `domain`" in p for p in row.problems)
