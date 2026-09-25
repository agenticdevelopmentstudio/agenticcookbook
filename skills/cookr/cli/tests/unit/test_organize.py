"""`cookr organize`: converting a flat `.cookr.json` corpus into a library cookbook.

`plan()` proposes where each legacy recipe goes; `validate()` refuses a plan
`apply()` cannot safely carry out; `apply()` moves the files, rewrites cross-
references, and writes the new `cookbook.json` manifest.
"""

from __future__ import annotations

import json
import subprocess

import pytest

from cookr.core.config import COOKBOOK_DIR, MANIFEST
from cookr.core.legacy import CONFIG_NAME, load_legacy
from cookr.core.organize import (
    Move,
    OrganizeError,
    PLAN_VERSION,
    _dedupe,
    apply,
    code_block,
    plan,
    platform_prefixes,
    rewrite_references,
    validate,
)


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


# --- validate: refusals ------------------------------------------------------------------


def test_validate_accepts_the_legacy_repos_own_plan(legacy_repo):
    validate(_plan(legacy_repo), legacy_repo)  # must not raise


def test_validate_rejects_a_wrong_plan_version(legacy_repo):
    data = _plan(legacy_repo)
    data["version"] = 2
    with pytest.raises(OrganizeError, match=f"plan version must be {PLAN_VERSION}"):
        validate(data, legacy_repo)


@pytest.mark.parametrize("key", ["recipes", "scheme", "cookbook", "legacy"])
def test_validate_rejects_a_blank_required_string(legacy_repo, key):
    data = _plan(legacy_repo)
    data[key] = ""
    with pytest.raises(OrganizeError, match=f"plan `{key}` must be a non-empty string"):
        validate(data, legacy_repo)


def test_validate_refuses_a_repo_already_organized(legacy_repo):
    (legacy_repo / COOKBOOK_DIR).mkdir()
    (legacy_repo / COOKBOOK_DIR / MANIFEST).write_text("{}", encoding="utf-8")
    data = _plan(legacy_repo)
    with pytest.raises(OrganizeError, match="this repo is organized"):
        validate(data, legacy_repo)


def test_validate_rejects_empty_code_roots(legacy_repo):
    data = _plan(legacy_repo)
    data["code"]["roots"] = []
    with pytest.raises(OrganizeError, match="plan `code.roots` must be a non-empty list"):
        validate(data, legacy_repo)


def test_validate_rejects_a_root_with_a_bad_platform_or_kind(legacy_repo):
    data = _plan(legacy_repo)
    data["code"]["roots"][0]["platform"] = "playstation"
    with pytest.raises(OrganizeError, match=r"code\.roots\[0\] has a bad platform or kind"):
        validate(data, legacy_repo)


def test_validate_rejects_a_root_path_not_found(legacy_repo):
    data = _plan(legacy_repo)
    data["code"]["roots"][0]["path"] = "does/not/exist"
    with pytest.raises(OrganizeError, match="code.roots\\[0\\].path not found: does/not/exist"):
        validate(data, legacy_repo)


def test_validate_rejects_a_non_list_moves(legacy_repo):
    data = _plan(legacy_repo)
    data["moves"] = "nope"
    with pytest.raises(OrganizeError, match="plan `moves` must be a list"):
        validate(data, legacy_repo)


def test_validate_rejects_a_move_source_not_found(legacy_repo):
    data = _plan(legacy_repo)
    data["moves"][0]["from"] = "recipes/nope.md"
    with pytest.raises(OrganizeError, match="plan move source not found: recipes/nope.md"):
        validate(data, legacy_repo)


@pytest.mark.parametrize("bad_to", ["Uppercase", "has space", "-leading-dash", "a/../b"])
def test_validate_rejects_a_move_target_that_is_not_a_lowercase_path(legacy_repo, bad_to):
    data = _plan(legacy_repo)
    data["moves"][0]["to"] = bad_to
    with pytest.raises(OrganizeError, match="is not a lowercase path in the cookbook"):
        validate(data, legacy_repo)


def test_validate_rejects_a_reserved_move_target(legacy_repo):
    data = _plan(legacy_repo)
    data["moves"][0]["to"] = "index"
    with pytest.raises(OrganizeError, match="is a file name the corpus skips"):
        validate(data, legacy_repo)


def test_validate_rejects_two_moves_sharing_a_target(legacy_repo):
    data = _plan(legacy_repo)
    data["moves"][1]["to"] = data["moves"][0]["to"]
    with pytest.raises(OrganizeError, match="plan moves share a target"):
        validate(data, legacy_repo)


def test_validate_rejects_an_implementation_with_a_bad_platform(legacy_repo):
    data = _plan(legacy_repo)
    data["moves"][0]["implementations"] = [{"platform": "playstation", "path": "web/blocks/StatCard.tsx"}]
    with pytest.raises(OrganizeError, match="bad platform `playstation`"):
        validate(data, legacy_repo)


def test_validate_rejects_an_implementation_path_not_found(legacy_repo):
    data = _plan(legacy_repo)
    data["moves"][0]["implementations"] = [{"platform": "web", "path": "web/blocks/Nope.tsx"}]
    with pytest.raises(OrganizeError, match="implementation not found: web/blocks/Nope.tsx"):
        validate(data, legacy_repo)


# --- rewrite_references (pure) ------------------------------------------------------------


def test_rewrite_references_substitutes_a_bare_domain_mention():
    text = "See mini-repo://recipes/button for details."
    out = rewrite_references(text, old_file="recipes/other.md", new_file="cookbook/other.md",
                             moved={}, domains={"mini-repo://recipes/button": "mini-repo://cookbook/ui"},
                             recipes="recipes")
    assert out == "See mini-repo://cookbook/ui for details."


def test_rewrite_references_updates_a_relative_link_to_a_moved_file():
    text = "[Button](button.md) is shared."
    out = rewrite_references(text, old_file="recipes/site-menu.md", new_file="cookbook/site-menu.md",
                             moved={"recipes/button.md": "cookbook/ui.md"}, domains={}, recipes="recipes")
    assert "[Button](ui.md)" in out


def test_rewrite_references_updates_a_bare_recipes_slash_path_mention():
    text = "Its file is at recipes/button.md today."
    out = rewrite_references(text, old_file="recipes/site-menu.md", new_file="cookbook/site-menu.md",
                             moved={"recipes/button.md": "cookbook/ui.md"}, domains={}, recipes="recipes")
    assert out == "Its file is at cookbook/ui.md today."


def test_rewrite_references_leaves_an_unrelated_link_alone(legacy_repo):
    text = "[Other](other.md)"
    out = rewrite_references(text, old_file="recipes/site-menu.md", new_file="recipes/site-menu.md",
                             moved={}, domains={}, recipes="recipes")
    assert out == text


# --- apply: end-to-end on a git-initialized copy ------------------------------------------


def test_apply_moves_rewrites_and_writes_the_manifest(legacy_repo):
    _init_git(legacy_repo)
    data = _plan(legacy_repo)
    validate(data, legacy_repo)
    result = apply(data, legacy_repo, author="Test Author <test@example.com>", day="2026-09-25")

    assert result.moved == 4
    assert result.leftovers == []
    assert result.manifest == f"{COOKBOOK_DIR}/{MANIFEST}"
    assert not (legacy_repo / CONFIG_NAME).exists()
    assert not (legacy_repo / "recipes").exists()

    ui = (legacy_repo / "cookbook" / "ui.md").read_text(encoding="utf-8")
    assert "domain: mini-repo://cookbook/ui" in ui
    assert "| apple | `apple/UI/` |" in ui
    assert "| web | `web/components/Button.tsx` |" in ui

    manifest = json.loads((legacy_repo / "cookbook" / "cookbook.json").read_text(encoding="utf-8"))
    assert manifest["type"] == "cookbook"
    assert manifest["code"] == data["code"]
    assert sorted(manifest["platforms"]) == ["apple", "web"]


def test_apply_bumps_a_moved_recipe_that_already_has_a_version(legacy_repo):
    _init_git(legacy_repo)
    data = _plan(legacy_repo)
    result = apply(data, legacy_repo, author="Test Author <test@example.com>", day="2026-09-25")
    ui = (legacy_repo / "cookbook" / "ui.md").read_text(encoding="utf-8")
    assert "version: 1.1.1" in ui  # button.md had version: 1.1.0; the move patch-bumps it
    assert "Moved into the library cookbook; added Reference Implementations." in ui
    assert not any(f == "cookbook/ui.md" for f, _ in result.bump_failures)


def test_apply_reports_a_bump_failure_for_a_recipe_with_no_version_line(legacy_repo):
    # stat-card.md and chat-composer.md have no `version:` line in the legacy
    # fixture (the old flat model never required one); the patch bump can't
    # apply to them, and apply() reports it rather than crashing.
    _init_git(legacy_repo)
    data = _plan(legacy_repo)
    result = apply(data, legacy_repo, author="Test Author <test@example.com>", day="2026-09-25")
    failed = dict(result.bump_failures)
    assert failed["cookbook/blocks/stat-card.md"] == "the frontmatter has no plain `version:` line"
    assert failed["cookbook/components/chat-composer.md"] == "the frontmatter has no plain `version:` line"


def test_apply_adds_a_domain_line_to_a_recipe_that_never_had_one(legacy_repo):
    _init_git(legacy_repo)
    data = _plan(legacy_repo)
    apply(data, legacy_repo, author="Test Author <test@example.com>", day="2026-09-25")
    text = (legacy_repo / "cookbook" / "components" / "chat-composer.md").read_text(encoding="utf-8")
    assert "domain: mini-repo://cookbook/components/chat-composer" in text
