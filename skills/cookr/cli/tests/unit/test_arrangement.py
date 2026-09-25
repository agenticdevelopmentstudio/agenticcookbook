"""`cookr arrangement`: does each spec's name follow from where its code sits?

`place()` compares a spec's own name against the name its first platform's
Reference Implementations rows would produce (`inventory.expected_name`), and
classifies it `aligned`, `drifted`, `unplaced` (no rows at all), or `outside`
(a row under no `code.roots` entry). `report()` runs `place()` over a whole
corpus, optionally scoped to one tier.
"""

from __future__ import annotations

import pytest

from cookr.core.arrangement import Placement, place, report
from cookr.core.config import load_config
from cookr.core.recipes import RecipeInfo, load_corpus


def _cfg(mini_repo):
    return load_config(mini_repo / "cookbook")


def _info(mini_repo, slug, body):
    return RecipeInfo(slug=slug, path=mini_repo / "cookbook" / f"{slug}.md",
                       type="ingredient", status="draft", body=body, data={})


# --- place: aligned/unplaced on the fixture as-is ------------------------------------------


def test_place_reports_every_fixture_spec_as_aligned_except_the_unmatched_one(mini_repo):
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    placements = {name: place(cfg, name, info) for name, info in corpus.items()}
    assert placements["blocks/stat-card"].state == "aligned"
    assert placements["components/chat-composer"].state == "aligned"
    assert placements["site-menu"].state == "unplaced"  # site-menu.md has no source code at all
    assert placements["site-menu"].expected == ""


def test_place_for_a_single_row_spec_matches_its_own_stem(mini_repo):
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    p = place(cfg, "blocks/stat-card", corpus["blocks/stat-card"])
    assert p == Placement(
        name="blocks/stat-card", state="aligned", expected="blocks/stat-card")


def test_place_uses_only_the_first_listed_platforms_rows(mini_repo):
    # button.md lists a `web` row before its `apple` directory row; place()
    # judges the spec purely by the web row (a single row -> single expected
    # name), never touching the apple directory claim at all.
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    p = place(cfg, "components/button", corpus["components/button"])
    assert p.state == "aligned"
    assert p.expected == "components/button"


# --- place: drifted (renamed spec, code untouched) ------------------------------------------


def test_place_flags_a_renamed_spec_as_drifted_against_its_untouched_code(mini_repo):
    (mini_repo / "cookbook" / "components" / "ui").mkdir()
    (mini_repo / "cookbook" / "components" / "button.md").rename(
        mini_repo / "cookbook" / "components" / "ui" / "button.md")
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    p = place(cfg, "components/ui/button", corpus["components/ui/button"])
    assert p.state == "drifted"
    assert p.expected == "components/button"


# --- place: directory-group rows (several rows share a common group) ------------------------


_DIR_ROWS = """
## Reference Implementations

| Platform | Path |
|----------|------|
| apple | `apple/UI/Button.swift` |
| apple | `apple/UI/ToolbarButton.swift` |
"""


def test_place_for_a_directory_group_is_aligned_when_the_name_matches_the_group(mini_repo):
    cfg = _cfg(mini_repo)
    p = place(cfg, "ui", _info(mini_repo, "ui", _DIR_ROWS))
    assert p.state == "aligned"
    assert p.expected == "ui/"


def test_place_for_a_directory_group_is_drifted_when_the_name_does_not_match(mini_repo):
    cfg = _cfg(mini_repo)
    p = place(cfg, "wrong-name", _info(mini_repo, "wrong-name", _DIR_ROWS))
    assert p.state == "drifted"
    assert p.expected == "ui/"


def test_place_for_a_directory_group_is_aligned_with_a_leaf_under_the_group(mini_repo):
    cfg = _cfg(mini_repo)
    p = place(cfg, "ui/button", _info(mini_repo, "ui/button", _DIR_ROWS))
    assert p.state == "aligned"


# --- place: unplaced / outside ---------------------------------------------------------------


def test_place_with_no_reference_implementations_is_unplaced(mini_repo):
    cfg = _cfg(mini_repo)
    p = place(cfg, "components/nothing", _info(mini_repo, "components/nothing", "no refimpl here"))
    assert p == Placement(name="components/nothing", state="unplaced", expected="")


def test_place_with_a_row_under_no_configured_root_is_outside(mini_repo):
    body = """
## Reference Implementations

| Platform | Path |
|----------|------|
| web | `docs/misc.tsx` |
"""
    cfg = _cfg(mini_repo)
    p = place(cfg, "components/misc", _info(mini_repo, "components/misc", body))
    assert p.state == "outside"
    assert p.expected == ""


# --- report: whole-corpus and tier-scoped -----------------------------------------------------


def test_report_covers_the_whole_corpus_sorted_by_name(mini_repo):
    cfg = _cfg(mini_repo)
    placements = report(cfg)
    assert [p.name for p in placements] == [
        "blocks/stat-card", "components/button", "components/chat-composer", "site-menu"]


def test_report_scoped_to_a_tier_only_returns_that_tiers_specs(mini_repo):
    cfg = _cfg(mini_repo)
    placements = report(cfg, tier="components")
    assert [p.name for p in placements] == ["components/button", "components/chat-composer"]


def test_report_accepts_a_precomputed_corpus_instead_of_reloading(mini_repo):
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    placements = report(cfg, corpus=corpus)
    assert len(placements) == len(corpus)
