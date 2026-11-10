import json

import pytest

from cookr.core.repoconfig import ConfigError
from cookr.core.repoconfig import (Dependency, NeedsUpgrade, config_for_cookbook, find_repo,
                                   load_repo_config, write_repo_config)

CID = "11111111-1111-4111-8111-111111111111"
DEP = "9d02a1b2-1111-4111-8111-222222222222"


def cookbook(repo, manifest=None):
    cb = repo / "cookbook"
    cb.mkdir(parents=True, exist_ok=True)
    (cb / "cookbook.json").write_text(json.dumps(
        manifest or {"format": 2, "id": CID, "rdid": "demo"}))
    return cb


def repo_cfg(repo, **over):
    d = {"format": 2, "cookbook": "cookbook",
         "dependencies": {DEP: {"rdid": "adhsdk", "location": "ext/cb"}},
         "roots": [{"path": "src", "platform": "macos", "kind": "logic", "group": "core/x"}],
         "ignore": ["**/Gen/**"]}
    d.update(over)
    (repo / ".cookr.json").write_text(json.dumps(d))


def test_load_v2_config(tmp_path):
    cookbook(tmp_path)
    (tmp_path / "src").mkdir()
    repo_cfg(tmp_path)
    c = load_repo_config(tmp_path)
    assert c.identity.rdid == "demo"
    assert c.roots[0].tier == "core" and c.roots[0].kind == "logic"
    assert c.dependencies[DEP] == Dependency(DEP, "adhsdk", "ext/cb")
    assert c.ignore == ["**/Gen/**"]
    assert c.root_for("src/a.swift") is c.roots[0]
    assert c.is_group("core")


def test_unknown_platform_rejected(tmp_path):
    cookbook(tmp_path)
    (tmp_path / "src").mkdir()
    repo_cfg(tmp_path, roots=[{"path": "src", "platform": "beos"}])
    with pytest.raises(ConfigError, match="beos"):
        load_repo_config(tmp_path)


def test_unknown_kind_and_bad_dependency_rejected(tmp_path):
    cookbook(tmp_path)
    (tmp_path / "src").mkdir()
    repo_cfg(tmp_path, roots=[{"path": "src", "platform": "web", "kind": "odd"}])
    with pytest.raises(ConfigError, match="odd"):
        load_repo_config(tmp_path)
    repo_cfg(tmp_path, dependencies={"nope": {"rdid": "x"}})
    with pytest.raises(ConfigError, match="nope"):
        load_repo_config(tmp_path)


def test_an_absolute_dependency_location_is_refused(tmp_path):
    cookbook(tmp_path)
    (tmp_path / "src").mkdir()
    repo_cfg(tmp_path, dependencies={DEP: {"rdid": "adhsdk", "location": str(tmp_path / "x")}})
    with pytest.raises(ConfigError, match="relative to the repo"):
        load_repo_config(tmp_path)
    repo_cfg(tmp_path, dependencies={DEP: {"rdid": "adhsdk", "location": "../sibling/cookbook"}})
    assert load_repo_config(tmp_path).dependencies[DEP].location == "../sibling/cookbook"


@pytest.mark.parametrize("fmt", ["2", 2.0, True])
def test_a_format_that_is_not_the_integer_2_says_so(tmp_path, fmt):
    cookbook(tmp_path)
    (tmp_path / "src").mkdir()
    repo_cfg(tmp_path, format=fmt)
    with pytest.raises(ConfigError, match="`format` must be the integer 2"):
        load_repo_config(tmp_path)


def test_tiers_of_a_config_whose_cookbook_dir_is_gone(tmp_path):
    import shutil

    cookbook(tmp_path)
    (tmp_path / "src").mkdir()
    repo_cfg(tmp_path)
    c = load_repo_config(tmp_path)
    shutil.rmtree(tmp_path / "cookbook")
    assert c.tiers == ["core"]  # the roots' tiers still count; no cookbook dir to list


def test_v1_cookbook_json_code_block_raises_needs_upgrade(tmp_path):
    cb = cookbook(tmp_path, {"id": CID, "code": {"roots": []}})
    repo_cfg(tmp_path, roots=[])
    with pytest.raises(NeedsUpgrade) as e:
        load_repo_config(tmp_path)
    assert e.value.path == cb.resolve() / "cookbook.json"
    with pytest.raises(NeedsUpgrade):
        config_for_cookbook(cb)


def test_legacy_cookr_json_raises_needs_upgrade(tmp_path):
    cookbook(tmp_path)
    (tmp_path / ".cookr.json").write_text(json.dumps({"recipes": "recipes", "roots": []}))
    with pytest.raises(NeedsUpgrade) as e:
        load_repo_config(tmp_path)
    assert e.value.path == tmp_path.resolve() / ".cookr.json"
    assert isinstance(e.value, ConfigError)


def test_cookbook_without_repo_config_has_no_roots(tmp_path):
    cb = cookbook(tmp_path)
    c = config_for_cookbook(cb)
    assert c.roots == [] and c.dependencies == {} and c.config_file is None
    assert c.identity.id == CID


def test_find_repo_walks_up(tmp_path):
    cookbook(tmp_path)
    deep = tmp_path / "a" / "b"
    deep.mkdir(parents=True)
    assert find_repo(deep) == tmp_path.resolve()


def test_write_round_trip(tmp_path):
    cookbook(tmp_path)
    (tmp_path / "src").mkdir()
    repo_cfg(tmp_path)
    c = load_repo_config(tmp_path)
    write_repo_config(c)
    assert list(json.loads((tmp_path / ".cookr.json").read_text())) == [
        "format", "cookbook", "dependencies", "roots", "ignore"]
    assert load_repo_config(tmp_path) == c
    assert not (tmp_path / ".cookr.json.tmp").exists()


@pytest.mark.parametrize("p", ["../outside", "/abs", "src/../../x"])
def test_root_path_escape_rejected(tmp_path, p):
    cookbook(tmp_path)
    repo_cfg(tmp_path, roots=[{"path": p, "platform": "web"}])
    with pytest.raises(ConfigError, match="inside the repo"):
        load_repo_config(tmp_path)


@pytest.mark.parametrize("fmt", [1, None])
def test_an_older_format_needs_the_upgrade(tmp_path, fmt):
    cookbook(tmp_path)
    repo_cfg(tmp_path, format=fmt) if fmt is not None else repo_cfg(tmp_path)
    if fmt is None:
        data = json.loads((tmp_path / ".cookr.json").read_text())
        del data["format"]
        (tmp_path / ".cookr.json").write_text(json.dumps(data))
    with pytest.raises(NeedsUpgrade):
        load_repo_config(tmp_path)


def test_config_error_is_one_class():
    from cookr.core import legacy, repoconfig
    assert legacy.ConfigError is repoconfig.ConfigError


# --- ported from the format-1 config tests -------------------------------------------

def _roots(repo, roots, **over):
    """A repo whose only config is `roots` (their dirs created) plus `over`."""
    cookbook(repo)
    for r in roots:
        if isinstance(r, dict) and isinstance(r.get("path"), str):
            (repo / r["path"]).mkdir(parents=True, exist_ok=True)
    (repo / ".cookr.json").write_text(json.dumps({"format": 2, "roots": roots, **over}))
    return repo


def test_root_for_prefers_the_deepest_nested_root(tmp_path):
    c = load_repo_config(_roots(tmp_path, [
        {"path": "src", "platform": "web", "group": "outer"},
        {"path": "src/widgets", "platform": "web", "group": "inner"},
    ]))
    assert c.root_for("src/widgets/Widget.tsx").group == "inner"
    assert c.root_for("src/Other.tsx").group == "outer"
    assert c.root_for("src/widgets").group == "inner"


def test_root_for_returns_none_outside_any_root(tmp_path):
    c = load_repo_config(_roots(tmp_path, [{"path": "src", "platform": "web", "group": "w"}]))
    assert c.root_for("docs/README.md") is None
    assert c.root_for("srcs/x.ts") is None


def test_tiers_lists_cookbook_dirs_and_root_groups(tmp_path):
    c = load_repo_config(_roots(tmp_path, [{"path": "src", "platform": "web",
                                            "group": "widgets/small"}]))
    (c.cookbook_dir / "components").mkdir()
    assert c.tiers == ["components", "widgets"]


def test_tiers_includes_a_cookbook_dir_with_no_root(tmp_path):
    c = load_repo_config(_roots(tmp_path, [{"path": "src", "platform": "web", "group": "widgets"}]))
    (c.cookbook_dir / "docs").mkdir()
    assert c.tiers == ["docs", "widgets"]


def test_tiers_excludes_dotdirs_and_top_level_roots(tmp_path):
    c = load_repo_config(_roots(tmp_path, [{"path": "src", "platform": "web"}]))  # no group: top level
    (c.cookbook_dir / ".git").mkdir()
    assert c.tiers == []


def test_is_group_matches_a_roots_nested_group(tmp_path):
    c = load_repo_config(_roots(tmp_path, [{"path": "src", "platform": "web",
                                            "group": "components/buttons"}]))
    assert c.is_group("components") is True
    assert c.is_group("components/buttons") is True
    assert c.is_group("components/inputs") is False
    assert c.is_group("") is False and c.is_group("/") is False


def test_root_path_not_found_raises(tmp_path):
    cookbook(tmp_path)
    (tmp_path / ".cookr.json").write_text(json.dumps(
        {"format": 2, "roots": [{"path": "nope", "platform": "web"}]}))
    with pytest.raises(ConfigError, match="path not found: nope"):
        load_repo_config(tmp_path)


@pytest.mark.parametrize("root,field", [({"platform": "web"}, "path"),
                                        ({"path": "src"}, "platform"),
                                        ({"path": "", "platform": "web"}, "path")])
def test_root_missing_path_or_platform_raises(tmp_path, root, field):
    _roots(tmp_path, [root])
    with pytest.raises(ConfigError, match=rf"roots\[0\]\.{field} must be a non-empty string"):
        load_repo_config(tmp_path)


@pytest.mark.parametrize("group", ["../outside", "a/../../b", ".."])
def test_root_group_with_dotdot_raises(tmp_path, group):
    _roots(tmp_path, [{"path": "src", "platform": "web", "group": group}])
    with pytest.raises(ConfigError, match="group must be a directory inside the cookbook"):
        load_repo_config(tmp_path)


@pytest.mark.parametrize("ignore", ["**/Gen/**", [1], ["ok", None], {"a": "b"}])
def test_root_ignore_not_list_of_strings_raises(tmp_path, ignore):
    _roots(tmp_path, [{"path": "src", "platform": "web", "ignore": ignore}])
    with pytest.raises(ConfigError, match=r"roots\[0\]\.ignore must be a list of strings"):
        load_repo_config(tmp_path)


@pytest.mark.parametrize("ignore", ["**/Gen/**", [1], ["ok", None], {"a": "b"}])
def test_top_level_ignore_not_list_of_strings_raises(tmp_path, ignore):
    _roots(tmp_path, [], ignore=ignore)
    with pytest.raises(ConfigError, match="`ignore` must be a list of strings"):
        load_repo_config(tmp_path)


def test_invalid_json_raises(tmp_path):
    cookbook(tmp_path)
    (tmp_path / ".cookr.json").write_text("{not json")
    with pytest.raises(ConfigError, match="invalid JSON"):
        load_repo_config(tmp_path)


@pytest.mark.parametrize("top", ["[]", '"x"', "2", "null"])
def test_non_object_top_level_raises(tmp_path, top):
    cookbook(tmp_path)
    (tmp_path / ".cookr.json").write_text(top)
    with pytest.raises(ConfigError, match="top level must be an object"):
        load_repo_config(tmp_path)

