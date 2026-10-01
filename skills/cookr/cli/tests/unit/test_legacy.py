"""`cookr.core.legacy`: reading the old, pre-library-cookbook `.cookr.json` and
naming its components the way cookr used to (for `cookr organize` to match
against the new corpus)."""

from __future__ import annotations

import json

import pytest
from cookbook.core.errors import CookbookError

from cookr.core.config import ConfigError
from cookr.core.legacy import CONFIG_NAME, LegacyConfig, legacy_scan, load_legacy


def _manifest(roots, recipes="recipes", **extra):
    data = {"recipes": recipes, "roots": roots}
    data.update(extra)
    return data


def _write(repo_root, data):
    (repo_root / CONFIG_NAME).write_text(json.dumps(data), encoding="utf-8")
    return repo_root / CONFIG_NAME


# --- load_legacy: happy path --------------------------------------------------


def test_load_legacy_reads_the_fixture(legacy_repo):
    cfg = load_legacy(legacy_repo / CONFIG_NAME)
    assert cfg.repo_root == legacy_repo
    assert cfg.recipes == "recipes"
    assert [r.tier for r in cfg.roots] == ["primitives", "blocks", "apple"]
    assert [r.path for r in cfg.roots] == ["web/components", "web/blocks", "apple/UI"]
    assert [r.platform for r in cfg.roots] == ["web", "web", "apple"]
    assert cfg.ignore == ["**/*.stories.tsx", "**/index.ts"]
    assert cfg.aliases == {"toolbar-button": "button"}
    assert cfg.renames == {}
    assert cfg.declared_scheme == "mini-repo"


def test_root_defaults_kind_and_ignore(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "widgets", "platform": "web"}]))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    root = cfg.roots[0]
    assert root.kind == "ui"
    assert root.ignore == ()


def test_root_reads_kind_and_ignore(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([
        {"path": "src", "tier": "widgets", "platform": "python", "kind": "logic",
         "ignore": ["**/*_test.py"]},
    ]))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    root = cfg.roots[0]
    assert root.kind == "logic"
    assert root.ignore == ("**/*_test.py",)


def test_recipes_dir_is_repo_root_slash_recipes(legacy_repo):
    cfg = load_legacy(legacy_repo / CONFIG_NAME)
    assert cfg.recipes_dir == legacy_repo / "recipes"


def test_domain_uses_scheme_recipes_and_slug(legacy_repo):
    cfg = load_legacy(legacy_repo / CONFIG_NAME)
    assert cfg.domain("button") == "mini-repo://recipes/button"


def test_tiers_is_insertion_order_deduped(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    _write(tmp_path, _manifest([
        {"path": "a", "tier": "x", "platform": "web"},
        {"path": "b", "tier": "y", "platform": "web"},
        {"path": "a", "tier": "x", "platform": "apple"},
    ]))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    assert cfg.tiers == ["x", "y"]


def test_config_error_is_a_cookbook_error(tmp_path):
    with pytest.raises(CookbookError):
        load_legacy(tmp_path / CONFIG_NAME)


def test_symlinked_config_resolves_repo_root_by_its_own_parent(tmp_path):
    real = tmp_path / "real"
    (real / "recipes").mkdir(parents=True)
    (real / "src").mkdir()
    _write(real, _manifest([{"path": "src", "tier": "widgets", "platform": "web"}]))
    link_root = tmp_path / "linked"
    link_root.symlink_to(real)
    cfg = load_legacy(link_root / CONFIG_NAME)
    assert cfg.repo_root == real


# --- load_legacy: validation errors -------------------------------------------


def test_missing_file_raises(tmp_path):
    with pytest.raises(ConfigError, match=f"no {CONFIG_NAME} at"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_invalid_json_raises(tmp_path):
    (tmp_path / CONFIG_NAME).write_text("{oops", encoding="utf-8")
    with pytest.raises(CookbookError, match="invalid JSON"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_non_object_top_level_raises(tmp_path):
    (tmp_path / CONFIG_NAME).write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(CookbookError, match="top level must be an object"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_missing_recipes_key_raises(tmp_path):
    _write(tmp_path, {"roots": []})
    with pytest.raises(CookbookError, match="`recipes` must be a non-empty string"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_recipes_dir_not_found_raises(tmp_path):
    _write(tmp_path, _manifest([], recipes="nope"))
    with pytest.raises(CookbookError, match="recipes dir not found: nope"):
        load_legacy(tmp_path / CONFIG_NAME)


@pytest.mark.parametrize("roots", [None, [], "nope"])
def test_empty_or_non_list_roots_raises(tmp_path, roots):
    (tmp_path / "recipes").mkdir()
    _write(tmp_path, {"recipes": "recipes", "roots": roots})
    with pytest.raises(CookbookError, match="`roots` must be a non-empty list"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_root_missing_field_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "platform": "web"}]))
    with pytest.raises(CookbookError, match=r"roots\[0\]\.tier must be a non-empty string"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_root_unknown_platform_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "playstation"}]))
    with pytest.raises(CookbookError, match="platform `playstation` is not one of"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_root_path_not_found_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    _write(tmp_path, _manifest([{"path": "missing", "tier": "x", "platform": "web"}]))
    with pytest.raises(CookbookError, match="path not found: missing"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_root_unknown_kind_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web", "kind": "backend"}]))
    with pytest.raises(CookbookError, match="kind `backend` is not one of"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_root_ignore_not_list_of_strings_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web", "ignore": [1]}]))
    with pytest.raises(CookbookError, match=r"roots\[0\]\.ignore must be a list of strings"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_top_level_ignore_not_list_of_strings_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}], ignore="nope"))
    with pytest.raises(CookbookError, match="`ignore` must be a list of strings"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_aliases_not_str_to_str_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}],
                                aliases={"a": 1}))
    with pytest.raises(CookbookError, match="`aliases` must map strings to strings"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_renames_key_not_found_raises(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}],
                                renames={"src/Missing.tsx": "widget"}))
    with pytest.raises(CookbookError, match="renames key not found: src/Missing.tsx"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_renames_non_empty_value_required(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}],
                                renames={"src": ""}))
    with pytest.raises(CookbookError, match="`renames` must map source paths to non-empty names"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_renames_keys_are_stripped_of_slashes(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}],
                                renames={"/src/": "widget"}))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    assert cfg.renames == {"src": "widget"}


@pytest.mark.parametrize("scheme", ["", "has/slash", "has://scheme"])
def test_bad_scheme_raises(tmp_path, scheme):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}], scheme=scheme))
    with pytest.raises(CookbookError, match="`scheme` must be a non-empty name without `/`"):
        load_legacy(tmp_path / CONFIG_NAME)


def test_no_scheme_key_leaves_declared_scheme_empty(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}]))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    assert cfg.declared_scheme == ""


def test_scheme_falls_back_to_repo_scheme_when_undeclared(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src").mkdir()
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}]))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    from cookbook.core.scheme import SchemeError
    with pytest.raises(SchemeError):
        _ = cfg.scheme


# --- LegacyConfig.renamed ------------------------------------------------------


def test_renamed_file_key_wins_over_directory_key():
    cfg = LegacyConfig(
        repo_root=None, recipes="recipes",
        renames={"widgets": "widget-module", "widgets/Card.tsx": "card"},
    )
    assert cfg.renamed("widgets/Card.tsx") == "card"
    assert cfg.renamed("widgets/Other.tsx") == "widget-module"


def test_renamed_longest_directory_key_wins():
    cfg = LegacyConfig(
        repo_root=None, recipes="recipes",
        renames={"src": "outer", "src/widgets": "inner"},
    )
    assert cfg.renamed("src/widgets/Card.tsx") == "inner"


def test_renamed_returns_none_when_uncovered():
    cfg = LegacyConfig(repo_root=None, recipes="recipes", renames={"other": "x"})
    assert cfg.renamed("src/Card.tsx") is None


# --- legacy_scan ----------------------------------------------------------------


def test_legacy_scan_names_the_fixture_with_kebab_case(legacy_repo):
    cfg = load_legacy(legacy_repo / CONFIG_NAME)
    comps = legacy_scan(cfg)
    by_path = {c.path: c for c in comps}
    assert by_path["web/components/Button.tsx"].name == "button"
    assert by_path["web/components/Button.tsx"].tier == "primitives"
    assert by_path["web/components/Button.tsx"].platform == "web"
    assert by_path["web/blocks/StatCard.tsx"].name == "stat-card"
    assert by_path["web/blocks/StatCard.tsx"].tier == "blocks"
    assert by_path["apple/UI/Button.swift"].name == "button"
    assert by_path["apple/UI/Button.swift"].tier == "apple"
    assert by_path["apple/UI/ToolbarButton.swift"].name == "toolbar-button"


def test_legacy_scan_ignores_globs(legacy_repo):
    cfg = load_legacy(legacy_repo / CONFIG_NAME)
    comps = legacy_scan(cfg)
    paths = {c.path for c in comps}
    assert "web/components/button.stories.tsx" not in paths
    assert "web/components/index.ts" not in paths


def test_legacy_scan_applies_renames(tmp_path):
    (tmp_path / "recipes").mkdir()
    src = tmp_path / "src"
    src.mkdir()
    (src / "Card.tsx").write_text("", encoding="utf-8")
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}],
                                renames={"src/Card.tsx": "landing-card"}))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    comps = legacy_scan(cfg)
    assert comps[0].name == "landing-card"


def test_legacy_scan_sorted_by_tier_name_path(tmp_path):
    (tmp_path / "recipes").mkdir()
    a = tmp_path / "a"
    a.mkdir()
    (a / "Zeta.tsx").write_text("", encoding="utf-8")
    (a / "Alpha.tsx").write_text("", encoding="utf-8")
    _write(tmp_path, _manifest([{"path": "a", "tier": "z-tier", "platform": "web"}]))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    comps = legacy_scan(cfg)
    assert [c.name for c in comps] == ["alpha", "zeta"]


def test_legacy_scan_raises_on_reserved_name(tmp_path):
    (tmp_path / "recipes").mkdir()
    src = tmp_path / "src"
    src.mkdir()
    (src / "index.tsx").write_text("", encoding="utf-8")
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}]))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    with pytest.raises(CookbookError, match="file name the recipe corpus skips"):
        legacy_scan(cfg)


def test_legacy_scan_reserved_check_applies_after_alias_resolution(tmp_path):
    # A name that resolves through `aliases` to a reserved slug is caught too.
    (tmp_path / "recipes").mkdir()
    src = tmp_path / "src"
    src.mkdir()
    (src / "Card.tsx").write_text("", encoding="utf-8")
    _write(tmp_path, _manifest([{"path": "src", "tier": "x", "platform": "web"}],
                                aliases={"card": "index"}))
    cfg = load_legacy(tmp_path / CONFIG_NAME)
    with pytest.raises(CookbookError, match="file name the recipe corpus skips"):
        legacy_scan(cfg)
