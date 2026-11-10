"""core/organize.plan: where each recipe of a flat `.cookr.json` corpus goes in
a library cookbook (the upgrader's placement of legacy recipes)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from cookr.core.repoconfig import COOKBOOK_DIR
from cookr.core.legacy import CONFIG_NAME, load_legacy
from cookr.core.organize import (
    Move,
    OrganizeError,
    PLAN_VERSION,
    _dedupe,
    code_block,
    plan,
    platform_prefixes,
)


# cookbook.schema.json in this repo: tests/unit -> tests -> cli -> cookr -> skills -> root
SCHEMA = Path(__file__).resolve().parents[5] / "references" / "cookbook.schema.json"


def _cfg(repo):
    return load_legacy(repo / CONFIG_NAME)


def _plan(repo):
    return plan(_cfg(repo))


def _git(repo, *args):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def _init_git(repo):
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test Author")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")


# --- platform_prefixes / code_block ---------------------------------------------------


def test_platform_prefixes_is_the_shared_directory_above_each_platforms_roots(legacy_repo):
    # web has two roots (web/components, web/blocks): their shared prefix is
    # "web" itself, which is not a root, so nothing is dropped.
    # apple has one root (apple/UI): the "shared prefix" of a single root is
    # the whole root, so its last segment is dropped to "apple".
    assert platform_prefixes(_cfg(legacy_repo)) == {"web": ["web"], "apple": ["apple"]}


def test_code_block_names_each_roots_recipes_group_from_below_the_prefix(legacy_repo):
    block = code_block(_cfg(legacy_repo))
    by_path = {r["path"]: r for r in block["roots"]}
    assert by_path["web/components"]["recipes"] == "components"
    assert by_path["web/blocks"]["recipes"] == "blocks"
    assert by_path["apple/UI"]["recipes"] == "ui"
    assert all(r["kind"] == "ui" for r in block["roots"])
    assert block["ignore"] == ["**/*.stories.tsx", "**/index.ts"]


# --- plan: naming ----------------------------------------------------------------------


def test_plan_carries_the_legacy_configs_scheme_and_recipes_dir(legacy_repo):
    data = _plan(legacy_repo)
    assert data["version"] == PLAN_VERSION
    assert data["legacy"] == CONFIG_NAME
    assert data["recipes"] == "recipes"
    assert data["scheme"] == "mini-repo"
    assert data["cookbook"] == COOKBOOK_DIR
    assert data["code"] == code_block(_cfg(legacy_repo))


def test_plan_names_a_whole_directory_claim_by_its_group(legacy_repo):
    # `button` (plus its alias `toolbar-button`) claims every file under
    # apple/UI, which is every apple source there is: the move is named after
    # the group ("ui"), not "ui/button", and the web source rides along as an
    # extra row rather than deciding the name (apple has 2 sources, web has 1).
    data = _plan(legacy_repo)
    by_from = {m["from"]: m for m in data["moves"]}
    move = by_from["recipes/button.md"]
    assert move["to"] == "ui"
    assert move["implementations"] == [
        {"platform": "apple", "path": "apple/UI/"},
        {"platform": "web", "path": "web/components/Button.tsx"},
    ]


def test_plan_names_a_single_source_recipe_by_group_and_stem(legacy_repo):
    data = _plan(legacy_repo)
    by_from = {m["from"]: m for m in data["moves"]}
    assert by_from["recipes/stat-card.md"]["to"] == "blocks/stat-card"
    assert by_from["recipes/stat-card.md"]["implementations"] == [
        {"platform": "web", "path": "web/blocks/StatCard.tsx"}]
    assert by_from["recipes/chat-composer.md"]["to"] == "components/chat-composer"
    assert by_from["recipes/chat-composer.md"]["implementations"] == [
        {"platform": "web", "path": "web/components/chat-composer.tsx"}]


def test_plan_recipe_with_no_sources_falls_back_to_slug_without_tier(legacy_repo):
    data = _plan(legacy_repo)
    by_from = {m["from"]: m for m in data["moves"]}
    move = by_from["recipes/site-menu.md"]
    assert move["to"] == "site-menu"
    assert move["implementations"] == []
    assert data["unmatched"] == ["site-menu"]


def test_plan_ignores_globs_and_button_alias_when_scanning_sources(legacy_repo):
    # `web/components/button.stories.tsx` and `web/components/index.ts` are
    # ignored by `code.ignore`; they must not show up as sources anywhere.
    data = _plan(legacy_repo)
    all_paths = {i["path"] for m in data["moves"] for i in m["implementations"]}
    assert "web/components/button.stories.tsx" not in all_paths
    assert "web/components/index.ts" not in all_paths


# --- _dedupe -----------------------------------------------------------------------------


def test_dedupe_falls_back_to_group_plus_slug_on_a_name_clash():
    a = Move(slug="widget-a", to="shared", group=["widgets"])
    b = Move(slug="widget-b", to="shared", group=["widgets"])
    _dedupe([a, b])
    assert {a.to, b.to} == {"widgets/widget-a", "widgets/widget-b"}


def test_dedupe_raises_when_the_fallback_still_collides():
    a = Move(slug="widget", to="shared", group=["widgets"])
    b = Move(slug="widget", to="shared", group=["widgets"])
    with pytest.raises(OrganizeError, match="recipes still share a name after the fallback"):
        _dedupe([a, b])


def test_dedupe_sends_a_reserved_name_to_its_fallback_too():
    m = Move(slug="widget", to="index", group=["docs"])
    _dedupe([m])
    assert m.to == "docs/widget"
