from __future__ import annotations

import dataclasses
import json

from cookr.core.config import load_config
from cookr.core.coverage import CoverageRow, claim_problems, collision, compute
from cookr.core.inventory import Component
from cookr.core.recipes import load_corpus


def _cfg(repo):
    return load_config(repo / "cookbook")


def _report(repo, tier=None):
    return compute(_cfg(repo), tier=tier)


def _manifest(repo):
    p = repo / "cookbook" / "cookbook.json"
    return p, json.loads(p.read_text(encoding="utf-8"))


def _write(p, data):
    p.write_text(json.dumps(data), encoding="utf-8")


def _add_root(repo, path, platform, recipes, files):
    d = repo / path
    d.mkdir(parents=True, exist_ok=True)
    for f in files:
        (d / f).write_text("export {}\n", encoding="utf-8")
    p, data = _manifest(repo)
    data["code"]["roots"].append({"path": path, "platform": platform, "recipes": recipes})
    _write(p, data)


# --- rows: one per claimed/unclaimed component name ---------------------------


def test_one_row_per_component_name(mini_repo):
    report = _report(mini_repo)
    assert [r.name for r in report.rows] == [
        "blocks/stat-card", "components/button", "components/chat-composer",
    ]


def test_cross_platform_claims_are_one_complete_row(mini_repo):
    by = {r.name: r for r in _report(mini_repo).rows}
    row = by["components/button"]
    assert row.tiers == ("components",)
    assert row.platforms == ("apple", "web")
    assert row.paths == ("apple/UI/Button.swift", "apple/UI/ToolbarButton.swift", "web/components/Button.tsx")
    assert row.state == "complete"
    assert row.problems == ()


def test_partial_rows_carry_completeness_and_claim_problems(mini_repo):
    by = {r.name: r for r in _report(mini_repo).rows}
    assert by["blocks/stat-card"].state == "partial"
    assert any("NEEDS REVIEW" in p for p in by["blocks/stat-card"].problems)
    assert by["components/chat-composer"].state == "partial"
    assert any("Change History" in p for p in by["components/chat-composer"].problems)


def test_missing_when_no_spec_claims_a_name(mini_repo):
    (mini_repo / "cookbook" / "components" / "chat-composer.md").unlink()
    by = {r.name: r for r in _report(mini_repo).rows}
    assert by["components/chat-composer"].state == "missing"
    assert by["components/chat-composer"].paths == ("web/components/chat-composer.tsx",)


def test_row_has_no_slug_field(mini_repo):
    row = _report(mini_repo).rows[0]
    assert not hasattr(row, "slug")
    assert {f.name for f in dataclasses.fields(CoverageRow)} == {
        "name", "tiers", "platforms", "paths", "state", "problems",
    }


# --- tier scoping ---------------------------------------------------------------


def test_tier_filter_keeps_only_names_in_that_group(mini_repo):
    report = _report(mini_repo, tier="components")
    assert [r.name for r in report.rows] == ["components/button", "components/chat-composer"]


def test_unmatched_recipes_survive_a_tier_filter(mini_repo):
    assert _report(mini_repo, tier="components").unmatched_recipes == _report(mini_repo).unmatched_recipes


def test_unmatched_recipes_lists_specs_with_no_claimed_sources(mini_repo):
    assert _report(mini_repo).unmatched_recipes == ["site-menu"]


# --- tally / below ----------------------------------------------------------------


def test_tally_counts_each_row_under_its_one_tier(mini_repo):
    tally = _report(mini_repo).tally()
    assert tally == {
        "blocks": {"missing": 0, "partial": 1, "complete": 0},
        "components": {"missing": 0, "partial": 1, "complete": 1},
    }


def test_tally_under_a_tier_filter_reports_only_that_tier(mini_repo):
    assert _report(mini_repo, tier="components").tally() == {
        "components": {"missing": 0, "partial": 1, "complete": 1},
    }


def test_below(mini_repo):
    report = _report(mini_repo)
    assert [r.name for r in report.below("complete")] == ["blocks/stat-card", "components/chat-composer"]
    assert report.below("partial") == []


def test_below_missing_after_deleting_a_spec(mini_repo):
    (mini_repo / "cookbook" / "components" / "chat-composer.md").unlink()
    report = _report(mini_repo)
    assert [r.name for r in report.below("partial")] == ["components/chat-composer"]


# --- collision: unclaimed sources across roots landing on one name ------------


def test_collision_names_the_colliding_root_paths(mini_repo):
    # Same platform, two different real roots (web/blocks and web/components):
    # collision() is purely path/root based, so this needs no files on disk.
    cfg = _cfg(mini_repo)
    items = [
        Component(name="widgets/card", path="web/components/Card.tsx", tier="widgets", platform="web"),
        Component(name="widgets/card", path="web/blocks/Card.tsx", tier="widgets", platform="web"),
    ]
    assert collision(items, cfg) == (
        "name collision across roots (web in web/blocks, web/components): write a spec for one "
        "side under another name and claim its file in `## Reference Implementations`"
    )


def test_collision_is_none_for_a_single_root_or_a_claimed_component(mini_repo):
    cfg = _cfg(mini_repo)
    one_root = [
        Component(name="components/button", path="web/components/A.tsx", tier="components", platform="web"),
        Component(name="components/button", path="web/components/B.tsx", tier="components", platform="web"),
    ]
    assert collision(one_root, cfg) is None
    claimed = [
        Component(name="widgets/card", path="web/components/Card.tsx", tier="widgets",
                  platform="web", claimed=True),
        Component(name="widgets/card", path="web/blocks/Card.tsx", tier="widgets",
                  platform="web", claimed=True),
    ]
    assert collision(claimed, cfg) is None


def test_two_unclaimed_roots_landing_on_one_name_is_a_collision(mini_repo):
    _add_root(mini_repo, "web/settings-a", "web", "settings", ["Card.tsx"])
    _add_root(mini_repo, "web/settings-b", "web", "settings", ["Card.tsx"])
    by = {r.name: r for r in _report(mini_repo).rows}
    row = by["settings/card"]
    assert row.state == "missing"
    assert row.problems and row.problems[0].startswith(
        "name collision across roots (web in web/settings-a, web/settings-b)"
    )


def test_collision_survives_even_when_the_name_has_a_matched_spec(mini_repo):
    _add_root(mini_repo, "web/settings-a", "web", "settings", ["Card.tsx"])
    _add_root(mini_repo, "web/settings-b", "web", "settings", ["Card.tsx"])
    (mini_repo / "cookbook" / "settings").mkdir()
    (mini_repo / "cookbook" / "settings" / "card.md").write_text(
        "---\ntype: ingredient\nstatus: accepted\n---\n\n"
        "## Reference Implementations\n\n| Platform | Path |\n| --- | --- |\n",
        encoding="utf-8",
    )
    by = {r.name: r for r in _report(mini_repo).rows}
    row = by["settings/card"]
    assert row.state == "partial"
    assert any(p.startswith("name collision") for p in row.problems)


def test_claiming_one_side_removes_it_from_the_collision(mini_repo):
    _add_root(mini_repo, "web/settings-a", "web", "settings", ["Card.tsx"])
    _add_root(mini_repo, "web/settings-b", "web", "settings", ["Card.tsx"])
    (mini_repo / "cookbook" / "settings").mkdir()
    (mini_repo / "cookbook" / "settings" / "card.md").write_text(
        "---\ntype: ingredient\nstatus: accepted\n---\n\n"
        "## Reference Implementations\n\n| Platform | Path |\n| --- | --- |\n"
        "| web | `web/settings-a/Card.tsx` |\n",
        encoding="utf-8",
    )
    by = {r.name: r for r in _report(mini_repo).rows}
    row = by["settings/card"]
    # only one unclaimed root remains ("settings-b"); no collision.
    assert not any(p.startswith("name collision") for p in row.problems)


# --- claim_problems: what a spec's Reference Implementations gets wrong -------


def test_unclaimed_source_under_a_named_spec_is_a_claim_problem(mini_repo):
    (mini_repo / "web" / "components" / "NewThing.tsx").write_text("export {}\n", encoding="utf-8")
    (mini_repo / "cookbook" / "components" / "new-thing.md").write_text(
        "---\ntype: ingredient\nstatus: draft\n---\n\n"
        "## Reference Implementations\n\n| Platform | Path |\n| --- | --- |\n",
        encoding="utf-8",
    )
    by = {r.name: r for r in _report(mini_repo).rows}
    row = by["components/new-thing"]
    assert row.state == "partial"
    assert "Reference Implementations does not list `web/components/NewThing.tsx` (web)" in row.problems


def test_two_specs_claiming_one_path_are_each_told_about_the_other(mini_repo):
    (mini_repo / "cookbook" / "components" / "button-twin.md").write_text(
        "---\ntype: ingredient\nstatus: draft\n---\n\n"
        "## Reference Implementations\n\n| Platform | Path |\n| --- | --- |\n"
        "| web | `web/components/Button.tsx` |\n",
        encoding="utf-8",
    )
    by = {r.name: r for r in _report(mini_repo).rows}
    assert "`web/components/Button.tsx` is also claimed by components/button-twin" in by["components/button"].problems
    assert "`web/components/Button.tsx` is also claimed by components/button" in by["components/button-twin"].problems


def test_claim_problems_flags_an_unknown_platform(mini_repo):
    # RecipeInfo.implementations is a property parsed live from `body`, so
    # replacing `body` is enough to exercise a bad-platform Reference
    # Implementations row without touching any file on disk.
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    info = corpus["components/button"]
    bad_info = dataclasses.replace(
        info, body=info.body.replace(
            "| apple | `apple/UI/` |", "| apple | `apple/UI/` |\n| playstation | `apple/UI/` |"
        ),
    )
    probs = claim_problems(bad_info, [], cfg, {})
    assert any("platform `playstation` is not one of" in p for p in probs)


def test_claim_problems_flags_a_missing_path(mini_repo):
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    info = corpus["components/chat-composer"]
    bad_info = dataclasses.replace(
        info, body=info.body.replace(
            "web/components/chat-composer.tsx", "web/components/does-not-exist.tsx",
        ),
    )
    probs = claim_problems(bad_info, [], cfg, {})
    assert any("does not exist" in p for p in probs)


# --- domain checks feed into completeness, not a separate check ---------------


def test_a_wrong_domain_scheme_keeps_the_row_partial(mini_repo):
    path = mini_repo / "cookbook" / "components" / "button.md"
    path.write_text(path.read_text().replace("mini-repo://", "agenticdevelopercookbook://"), encoding="utf-8")
    by = {r.name: r for r in _report(mini_repo).rows}
    row = by["components/button"]
    assert row.state == "partial"
    assert any("frontmatter `domain`" in p for p in row.problems)
