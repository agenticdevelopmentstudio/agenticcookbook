"""`cookr.core.config`: parsing and validating a library cookbook's `cookbook.json`,
and the `Config`/`Root` helpers that read its `code` block.

Scheme derivation itself (`cookbook.core.scheme.repo_scheme`/`cookbook_scheme`) is
covered exhaustively by `skills/cookbook/cli/tests/unit/test_scheme.py`; the tests
here only check that `Config.scheme` delegates to it against `cookbook_dir`.
"""

from __future__ import annotations

import json

import pytest
from cookbook.core.errors import CookbookError

from cookr.core.config import Config, ConfigError, Root, find_cookbook, load_config


def _manifest(roots, ignore=None):
    data = {"code": {"roots": roots}}
    if ignore is not None:
        data["code"]["ignore"] = ignore
    return data


def _write(cookbook_dir, data):
    cookbook_dir.mkdir(parents=True, exist_ok=True)
    (cookbook_dir / "cookbook.json").write_text(json.dumps(data), encoding="utf-8")
    return cookbook_dir


# --- Root -------------------------------------------------------------------


@pytest.mark.parametrize("recipes,tier", [
    ("", ""),
    ("components", "components"),
    ("components/buttons", "components"),
])
def test_root_tier_is_the_top_level_group(recipes, tier):
    assert Root(path="src", platform="web", recipes=recipes).tier == tier


# --- load_config: happy path -------------------------------------------------


def test_load_config_reads_mini_repo(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.repo_root == mini_repo
    assert cfg.cookbook_dir == mini_repo / "cookbook"
    assert [r.path for r in cfg.roots] == ["web/components", "web/blocks", "apple/UI"]
    assert [r.recipes for r in cfg.roots] == ["components", "blocks", "ui"]
    assert {r.platform for r in cfg.roots} == {"web", "apple"}
    assert all(r.kind == "ui" for r in cfg.roots)
    assert cfg.ignore == ["**/*.stories.tsx", "**/index.ts"]


def test_root_defaults_kind_and_recipes(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web"}],
    ))
    cfg = load_config(cookbook_dir)
    root = cfg.roots[0]
    assert root.kind == "ui"
    assert root.recipes == ""
    assert root.ignore == ()


def test_root_reads_kind_recipes_and_ignore(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "cookbook" / "widgets").mkdir(parents=True)
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "python", "kind": "logic", "recipes": "widgets",
          "ignore": ["**/*_test.py"]}],
    ))
    cfg = load_config(cookbook_dir)
    root = cfg.roots[0]
    assert root.kind == "logic"
    assert root.recipes == "widgets"
    assert root.ignore == ("**/*_test.py",)


def test_root_path_and_recipes_are_stripped_of_slashes(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "/src/", "platform": "web", "recipes": "/widgets/"}],
    ))
    cfg = load_config(cookbook_dir)
    assert cfg.roots[0].path == "src"
    assert cfg.roots[0].recipes == "widgets"


def test_repo_root_is_the_cookbook_dirs_parent(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web"}],
    ))
    cfg = load_config(cookbook_dir)
    assert cfg.repo_root == tmp_path


def test_symlinked_cookbook_dir_resolves_repo_root_by_the_symlinks_own_parent(tmp_path):
    # `cookbook_dir` itself may be a symlink (a monorepo linking a shared cookbook
    # into place); repo_root is the directory holding that symlink, not the
    # parent of wherever the symlink's target actually lives.
    actual = tmp_path / "elsewhere" / "actual-cookbook"
    actual.mkdir(parents=True)
    (actual / "cookbook.json").write_text(json.dumps(_manifest(
        [{"path": "src", "platform": "web"}],
    )), encoding="utf-8")
    repo_root = tmp_path / "repo"
    (repo_root / "src").mkdir(parents=True)
    (repo_root / "cookbook").symlink_to(actual)

    cfg = load_config(repo_root / "cookbook")
    assert cfg.repo_root == repo_root
    assert cfg.cookbook_dir == repo_root / "cookbook"


# --- load_config: validation errors -----------------------------------------


def test_missing_manifest_raises(tmp_path):
    cookbook_dir = tmp_path / "cookbook"
    cookbook_dir.mkdir()
    with pytest.raises(ConfigError, match=f"no cookbook.json at {cookbook_dir}"):
        load_config(cookbook_dir)


def test_invalid_json_raises(tmp_path):
    cookbook_dir = tmp_path / "cookbook"
    cookbook_dir.mkdir()
    (cookbook_dir / "cookbook.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(ConfigError, match="invalid JSON"):
        load_config(cookbook_dir)


def test_non_object_top_level_raises(tmp_path):
    cookbook_dir = _write(tmp_path / "cookbook", ["not", "an", "object"])
    with pytest.raises(ConfigError, match="top level must be an object"):
        load_config(cookbook_dir)


def test_missing_code_block_raises(tmp_path):
    cookbook_dir = _write(tmp_path / "cookbook", {"name": "x"})
    with pytest.raises(ConfigError, match="no `code` block"):
        load_config(cookbook_dir)


@pytest.mark.parametrize("roots", [None, [], "nope"])
def test_empty_or_non_list_roots_raises(tmp_path, roots):
    cookbook_dir = _write(tmp_path / "cookbook", {"code": {"roots": roots}})
    with pytest.raises(ConfigError, match=r"code\.roots.*must be a non-empty list"):
        load_config(cookbook_dir)


def test_root_missing_path_or_platform_raises(tmp_path):
    cookbook_dir = _write(tmp_path / "cookbook", _manifest([{"platform": "web"}]))
    with pytest.raises(ConfigError, match=r"code\.roots\[0\]\.path must be a non-empty string"):
        load_config(cookbook_dir)


def test_root_unknown_platform_raises(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "playstation"}],
    ))
    with pytest.raises(ConfigError, match="platform `playstation` is not one of"):
        load_config(cookbook_dir)


def test_root_path_not_found_raises(tmp_path):
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "missing", "platform": "web"}],
    ))
    with pytest.raises(ConfigError, match="path not found: missing"):
        load_config(cookbook_dir)


def test_root_unknown_kind_raises(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web", "kind": "backend"}],
    ))
    with pytest.raises(ConfigError, match="kind `backend` is not one of"):
        load_config(cookbook_dir)


def test_root_recipes_with_dotdot_raises(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web", "recipes": "../escape"}],
    ))
    with pytest.raises(ConfigError, match="recipes must be a directory inside the cookbook"):
        load_config(cookbook_dir)


def test_root_ignore_not_list_of_strings_raises(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web", "ignore": [1, 2]}],
    ))
    with pytest.raises(ConfigError, match=r"code\.roots\[0\]\.ignore must be a list of strings"):
        load_config(cookbook_dir)


def test_top_level_ignore_not_list_of_strings_raises(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web"}], ignore="not-a-list",
    ))
    with pytest.raises(ConfigError, match=r"`code\.ignore` must be a list of strings"):
        load_config(cookbook_dir)


def test_config_error_is_a_cookbook_error(tmp_path):
    with pytest.raises(CookbookError):
        load_config(tmp_path / "cookbook")


# --- Config.root_for ----------------------------------------------------------


def test_root_for_finds_the_owning_root(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    root = cfg.root_for("web/components/Button.tsx")
    assert root is not None
    assert root.path == "web/components"


def test_root_for_matches_the_root_path_itself(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.root_for("web/components") is not None


def test_root_for_returns_none_outside_any_root(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.root_for("docs/README.md") is None


def test_root_for_prefers_the_deepest_nested_root(tmp_path):
    (tmp_path / "src" / "widgets").mkdir(parents=True)
    cookbook_dir = _write(tmp_path / "cookbook", _manifest([
        {"path": "src", "platform": "web", "recipes": "outer"},
        {"path": "src/widgets", "platform": "web", "recipes": "inner"},
    ]))
    cfg = load_config(cookbook_dir)
    root = cfg.root_for("src/widgets/Widget.tsx")
    assert root.recipes == "inner"


# --- Config.tiers / is_group ---------------------------------------------------


def test_tiers_lists_cookbook_dirs_and_root_recipes(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.tiers == ["blocks", "components", "ui"]


def test_tiers_includes_a_cookbook_dir_with_no_root(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web", "recipes": "widgets"}],
    ))
    (cookbook_dir / "docs").mkdir()
    cfg = load_config(cookbook_dir)
    assert cfg.tiers == ["docs", "widgets"]


def test_tiers_excludes_dotdirs_and_top_level_roots(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web"}],  # recipes="" -> top level, no tier
    ))
    (cookbook_dir / ".git").mkdir()
    cfg = load_config(cookbook_dir)
    assert cfg.tiers == []


@pytest.mark.parametrize("tier,expected", [
    ("components", True),
    ("components/buttons", False),  # no such nested dir and no root claims it
    ("", False),
    ("/", False),
    ("nope", False),
])
def test_is_group(mini_repo, tier, expected):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.is_group(tier) is expected


def test_is_group_matches_a_roots_nested_recipes(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web", "recipes": "components/buttons"}],
    ))
    cfg = load_config(cookbook_dir)
    assert cfg.is_group("components") is True
    assert cfg.is_group("components/buttons") is True


# --- Config.domain / spec_path / cookbook / recipes_dir -----------------------


def test_cookbook_is_relative_to_repo_root(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.cookbook == "cookbook"


def test_recipes_dir_is_the_cookbook_dir(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.recipes_dir == cfg.cookbook_dir


def test_spec_path_appends_md_under_the_cookbook(mini_repo):
    cfg = load_config(mini_repo / "cookbook")
    assert cfg.spec_path("components/button") == mini_repo / "cookbook" / "components" / "button.md"


def test_domain_uses_the_scheme_cookbook_and_spec(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web"}],
    ))
    (cookbook_dir / "index.md").write_text(
        "---\ndomain: mini-repo://index\n---\n# Index\n", encoding="utf-8")
    cfg = load_config(cookbook_dir)
    assert cfg.domain("components/button") == "mini-repo://cookbook/components/button"


# --- Config.scheme (delegates to cookbook.core.scheme.cookbook_scheme) --------


def test_scheme_falls_back_to_repo_scheme_outside_git(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web"}],
    ))
    cfg = load_config(cookbook_dir)
    # Outside git, repo_scheme has nothing to derive a name from and raises.
    from cookbook.core.scheme import SchemeError
    with pytest.raises(SchemeError):
        _ = cfg.scheme


def test_scheme_prefers_an_index_md_declared_domain(tmp_path):
    (tmp_path / "src").mkdir()
    cookbook_dir = _write(tmp_path / "cookbook", _manifest(
        [{"path": "src", "platform": "web"}],
    ))
    (cookbook_dir / "index.md").write_text(
        "---\ndomain: custom-scheme://index\n---\n# Index\n", encoding="utf-8")
    cfg = load_config(cookbook_dir)
    assert cfg.scheme == "custom-scheme"


# --- find_cookbook -------------------------------------------------------------


def test_find_cookbook_locates_a_cookbook_subdirectory(mini_repo):
    assert find_cookbook(mini_repo) == mini_repo / "cookbook"


def test_find_cookbook_locates_from_a_nested_start_dir(mini_repo):
    nested = mini_repo / "web" / "components"
    assert find_cookbook(nested) == mini_repo / "cookbook"


def test_find_cookbook_treats_start_itself_as_the_cookbook_when_it_holds_the_manifest(tmp_path):
    (tmp_path / "cookbook.json").write_text("{}", encoding="utf-8")
    assert find_cookbook(tmp_path) == tmp_path


def test_find_cookbook_returns_none_when_nothing_is_found(tmp_path):
    assert find_cookbook(tmp_path) is None
