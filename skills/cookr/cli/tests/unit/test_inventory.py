from __future__ import annotations

import json
import re

import pytest

from cookr.core.config import ConfigError, Root, load_config
from cookr.core.inventory import (
    claims,
    component_stem,
    expected_name,
    glob_regex,
    group_parts,
    ignore_set,
    in_group,
    join_name,
    owners,
    scan,
)
from cookr.core.recipes import load_corpus


def _corpus(cookbook_dir):
    return load_corpus(cookbook_dir)


def _cfg(repo):
    return load_config(repo / "cookbook")


def _manifest(repo):
    p = repo / "cookbook" / "cookbook.json"
    return p, json.loads(p.read_text(encoding="utf-8"))


def _write_manifest(p, data):
    p.write_text(json.dumps(data), encoding="utf-8")


# --- scan(): end-to-end against the mini-repo fixture -------------------------


def test_scan_lists_every_claimed_component_by_name_and_tier(mini_repo):
    cfg = _cfg(mini_repo)
    rows = scan(cfg, _corpus(cfg.cookbook_dir))
    names = [(r.name, r.tier, r.path, r.platform) for r in rows]
    assert names == [
        ("blocks/stat-card", "blocks", "web/blocks/StatCard.tsx", "web"),
        ("components/button", "components", "apple/UI/Button.swift", "apple"),
        ("components/button", "components", "apple/UI/ToolbarButton.swift", "apple"),
        ("components/button", "components", "web/components/Button.tsx", "web"),
        ("components/chat-composer", "components", "web/components/chat-composer.tsx", "web"),
    ]


def test_scan_marks_every_row_claimed_in_the_fixture(mini_repo):
    cfg = _cfg(mini_repo)
    rows = scan(cfg, _corpus(cfg.cookbook_dir))
    assert all(r.claimed for r in rows)


def test_scan_drops_ignored(mini_repo):
    cfg = _cfg(mini_repo)
    paths = [r.path for r in scan(cfg, _corpus(cfg.cookbook_dir))]
    assert "web/components/button.stories.tsx" not in paths
    assert "web/components/index.ts" not in paths


def test_scan_paths_are_repo_relative_posix(mini_repo):
    cfg = _cfg(mini_repo)
    assert "web/components/Button.tsx" in [r.path for r in scan(cfg, _corpus(cfg.cookbook_dir))]


def test_root_ignore_applies_to_its_own_root_only(mini_repo):
    p, data = _manifest(mini_repo)
    for r in data["code"]["roots"]:
        if r["path"] == "apple/UI":
            r["ignore"] = ["**/ToolbarButton.swift"]
    _write_manifest(p, data)
    cfg = _cfg(mini_repo)
    paths = [r.path for r in scan(cfg, _corpus(cfg.cookbook_dir))]
    assert "apple/UI/ToolbarButton.swift" not in paths
    assert "apple/UI/Button.swift" in paths
    assert "web/components/Button.tsx" in paths  # another root is unaffected


def test_a_directory_claim_names_every_file_below_it_unless_a_file_claim_wins(mini_repo):
    # apple/UI/ is claimed whole by components/button; both its files carry that name.
    cfg = _cfg(mini_repo)
    rows = {r.path: r.name for r in scan(cfg, _corpus(cfg.cookbook_dir))}
    assert rows["apple/UI/Button.swift"] == "components/button"
    assert rows["apple/UI/ToolbarButton.swift"] == "components/button"


def test_unclaimed_new_file_is_named_by_the_codes_arrangement(mini_repo):
    (mini_repo / "web" / "components" / "NewThing.tsx").write_text("export {}\n", encoding="utf-8")
    cfg = _cfg(mini_repo)
    rows = {r.path: r for r in scan(cfg, _corpus(cfg.cookbook_dir))}
    row = rows["web/components/NewThing.tsx"]
    assert row.name == "components/new-thing"
    assert row.claimed is False


def test_a_file_claim_beats_a_directory_claim_above_it(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "Card.tsx").write_text("", encoding="utf-8")
    (tmp_path / "src" / "Other.tsx").write_text("", encoding="utf-8")
    cookbook = tmp_path / "cookbook"
    cookbook.mkdir()
    _write_manifest(cookbook / "cookbook.json", {
        "code": {"roots": [{"path": "src", "platform": "web", "recipes": "widgets"}]},
    })
    (cookbook / "module.md").write_text(
        "---\ntype: ingredient\nstatus: draft\n---\n\n"
        "## Reference Implementations\n\n| Platform | Path |\n| --- | --- |\n"
        "| web | `src/` |\n", encoding="utf-8")
    (cookbook / "card.md").write_text(
        "---\ntype: ingredient\nstatus: draft\n---\n\n"
        "## Reference Implementations\n\n| Platform | Path |\n| --- | --- |\n"
        "| web | `src/Card.tsx` |\n", encoding="utf-8")
    cfg = load_config(cookbook)
    rows = {r.path: r.name for r in scan(cfg, _corpus(cookbook))}
    assert rows["src/Card.tsx"] == "card"       # its own file claim wins
    assert rows["src/Other.tsx"] == "module"    # falls back to the directory claim


# --- unclaimed naming: expected_name / join_name / group_parts ----------------


def test_expected_name_for_a_file():
    root = Root(path="web/components", platform="web", recipes="components")
    assert expected_name(root, "web/components/ChatComposer.tsx") == "components/chat-composer"


def test_expected_name_for_a_directory_uses_its_whole_path():
    root = Root(path="web", platform="web", recipes="components")
    assert expected_name(root, "web/blocks/") == "components/blocks"


def test_expected_name_folds_a_stem_repeating_its_directory():
    root = Root(path="src", platform="web", recipes="data")
    assert expected_name(root, "src/docs/Docs.swift") == "data/docs"


def test_expected_name_folds_a_reserved_stem_into_the_group():
    root = Root(path="src", platform="web", recipes="widgets")
    assert expected_name(root, "src/Index.tsx") == "widgets"


def test_expected_name_top_level_reserved_stem_has_no_group_to_fold_into():
    root = Root(path="src", platform="web", recipes="")
    assert expected_name(root, "src/Index.tsx") == "index"


def test_expected_name_drops_a_source_dir_segment():
    root = Root(path="pkg", platform="web", recipes="widgets")
    assert expected_name(root, "pkg/src/Card.tsx") == "widgets/card"


def test_group_parts_drops_src_and_sources_and_kebabs_the_rest():
    assert group_parts(["src", "Widgets"]) == ["widgets"]
    assert group_parts(["Sources", "ChatKit"]) == ["chat-kit"]


@pytest.mark.parametrize("group,leaf,expected", [
    (["docs"], "docs", ["docs"]),
    (["widgets"], "index", ["widgets"]),
    (["widgets"], "card", ["widgets", "card"]),
    ([], "index", ["index"]),
])
def test_join_name(group, leaf, expected):
    assert join_name(group, leaf) == expected


# --- claims / owners: how a spec's Reference Implementations names a source --


def test_claims_builds_a_path_to_spec_platform_table(mini_repo):
    cfg = _cfg(mini_repo)
    table = claims(_corpus(cfg.cookbook_dir))
    assert table["web/components/Button.tsx"] == [("components/button", "web")]
    assert table["apple/UI/"] == [("components/button", "apple")]
    assert table["web/blocks/StatCard.tsx"] == [("blocks/stat-card", "web")]


def test_owners_own_path_beats_a_directory_claim():
    table = {"a/b.tsx": [("file-spec", "web")], "a/": [("dir-spec", "web")]}
    assert owners(table, "a/b.tsx") == [("file-spec", "web")]


def test_owners_falls_back_to_the_deepest_directory_claim():
    table = {"a/": [("outer", "web")], "a/b/": [("inner", "web")]}
    assert owners(table, "a/b/c.tsx") == [("inner", "web")]


def test_owners_returns_empty_list_when_nothing_claims_it():
    assert owners({}, "a/b.tsx") == []


# --- in_group ------------------------------------------------------------------


@pytest.mark.parametrize("name,tier,expected", [
    ("components/button", "components", True),
    ("components/button", "blocks", False),
    ("components/button", None, True),
    ("components/button", "components/", True),
])
def test_in_group(name, tier, expected):
    assert in_group(name, tier) is expected


def test_scan_tier_filters_the_returned_names_but_still_walks_every_root(mini_repo, monkeypatch):
    # A tier's specs may claim files under any root, so scan always walks every
    # root and filters the resulting components by name afterward.
    import os

    from cookr.core import inventory
    tops = []
    real_walk = os.walk
    monkeypatch.setattr(
        inventory.os, "walk",
        lambda top, *a, **k: tops.append(str(top)) or real_walk(top, *a, **k),
    )
    cfg = _cfg(mini_repo)
    rows = scan(cfg, _corpus(cfg.cookbook_dir), tier="blocks")
    assert [r.name for r in rows] == ["blocks/stat-card"]
    assert len(tops) > 1  # every root (and claimed directory) was walked, not just blocks'


# --- glob semantics -------------------------------------------------------------


def _matches(pattern, path):
    return re.fullmatch(glob_regex(pattern), path) is not None


@pytest.mark.parametrize("pattern,path,expected", [
    # `*` stays inside one directory
    ("a/*.ts", "a/c.ts", True),
    ("a/*.ts", "a/b/c.ts", False),
    ("packages/chat/src/modes/*.ts", "packages/chat/src/modes/three-pane/Foo.ts", False),
    # every `**/` is zero or more directories, not only the first
    ("**/__tests__/**/*.ts", "__tests__/x.ts", True),
    ("**/__tests__/**/*.ts", "a/__tests__/x.ts", True),
    ("**/__tests__/**/*.ts", "src/a/__tests__/x.ts", True),
    ("**/__tests__/**/*.ts", "src/a/__tests__/b/x.ts", True),
    ("**/src/**/*.test.ts", "pkg/src/x.test.ts", True),
    ("**/src/**/*.test.ts", "pkg/src/a/x.test.ts", True),
    ("**/src/**/*.test.ts", "pkg/lib/x.test.ts", False),
    # trailing `/**` is everything below
    ("**/generated/**", "a/generated/models/x.py", True),
    ("**/generated/**", "a/generated.py", False),
    ("**", "any/thing.ts", True),
    # `?` and classes never cross `/`
    ("a/?.ts", "a/b.ts", True),
    ("a/?.ts", "a/bc.ts", False),
    ("a?b.ts", "a/b.ts", False),
    ("a/[bc].ts", "a/c.ts", True),
    ("a/[!bc].ts", "a/c.ts", False),
    ("a/[!bc].ts", "a/d.ts", True),
    ("a/[x.ts", "a/[x.ts", True),   # unclosed class is a literal `[`
    ("a/b+c.ts", "a/b+c.ts", True),  # regex metacharacters are literal
])
def test_glob_semantics(pattern, path, expected):
    assert _matches(pattern, path) is expected


def test_ignore_set_prunes_only_wholly_ignored_directories():
    s = ignore_set(("**/generated/**", "**/*.test.ts", "a/*.ts"))
    assert s.prunes("pkg/generated")
    assert not s.prunes("pkg/src")
    assert s.ignores("a/x.ts") and not s.ignores("a/b/x.ts")


def _set_ignore(repo, patterns):
    p, data = _manifest(repo)
    data["code"]["ignore"] = patterns
    _write_manifest(p, data)
    return p


def test_star_ignore_keeps_nested_files(mini_repo):
    nested = mini_repo / "web" / "components" / "three-pane"
    nested.mkdir()
    (nested / "useLayout.ts").write_text("export {}\n", encoding="utf-8")
    _set_ignore(mini_repo, ["web/components/*.ts", "**/*.stories.tsx"])
    cfg = _cfg(mini_repo)
    paths = [r.path for r in scan(cfg, _corpus(cfg.cookbook_dir))]
    assert "web/components/index.ts" not in paths
    assert "web/components/three-pane/useLayout.ts" in paths


def test_second_globstar_matches_files_directly_in_the_directory(mini_repo):
    tests = mini_repo / "web" / "components" / "__tests__"
    tests.mkdir()
    (tests / "widget.ts").write_text("export {}\n", encoding="utf-8")
    _set_ignore(mini_repo, ["**/__tests__/**/*.ts", "**/*.stories.tsx", "**/index.ts"])
    cfg = _cfg(mini_repo)
    paths = [r.path for r in scan(cfg, _corpus(cfg.cookbook_dir))]
    assert "web/components/__tests__/widget.ts" not in paths


def test_wholly_ignored_directories_are_not_walked(mini_repo, monkeypatch):
    import os

    from cookr.core import inventory
    gen = mini_repo / "web" / "components" / "generated" / "deep"
    gen.mkdir(parents=True)
    (gen / "Model.ts").write_text("export {}\n", encoding="utf-8")
    _set_ignore(mini_repo, ["**/generated/**", "**/*.stories.tsx", "**/index.ts"])
    seen = []
    real_walk = os.walk

    def spy(top, *a, **k):
        for entry in real_walk(top, *a, **k):
            seen.append(entry[0])
            yield entry

    monkeypatch.setattr(inventory.os, "walk", spy)
    cfg = _cfg(mini_repo)
    paths = [r.path for r in scan(cfg, _corpus(cfg.cookbook_dir))]
    assert "web/components/generated/deep/Model.ts" not in paths
    assert not any("generated" in d for d in seen)


# --- component names -----------------------------------------------------------


@pytest.mark.parametrize("filename,stem", [
    ("StatCard.xaml.cs", "StatCard"),
    ("StatCard.xaml", "StatCard"),
    ("Button.tsx", "Button"),
    ("x.test.ts", "x.test"),        # `.test` is not a source suffix
    ("types.d.ts", "types.d"),
])
def test_component_stem_drops_every_trailing_source_suffix(filename, stem):
    assert component_stem(filename) == stem


def test_xaml_code_behind_is_one_unclaimed_component(mini_repo):
    win = mini_repo / "win" / "Controls"
    win.mkdir(parents=True)
    (win / "StatCard.xaml").write_text("<UserControl/>\n", encoding="utf-8")
    (win / "StatCard.xaml.cs").write_text("class StatCard {}\n", encoding="utf-8")
    p, data = _manifest(mini_repo)
    data["code"]["roots"].append(
        {"path": "win/Controls", "platform": "windows", "recipes": "windows"})
    _write_manifest(p, data)
    cfg = _cfg(mini_repo)
    rows = [r for r in scan(cfg, _corpus(cfg.cookbook_dir)) if r.name == "windows/stat-card"]
    assert {r.path for r in rows} == {"win/Controls/StatCard.xaml", "win/Controls/StatCard.xaml.cs"}
    assert all(not r.claimed for r in rows)


# --- reserved names --------------------------------------------------------------


def test_unclaimed_reserved_stem_at_the_cookbooks_top_level_is_a_config_error(mini_repo):
    (mini_repo / "web" / "misc").mkdir()
    (mini_repo / "web" / "misc" / "index.tsx").write_text("export {}\n", encoding="utf-8")
    p, data = _manifest(mini_repo)
    data["code"]["roots"].append({"path": "web/misc", "platform": "web"})  # recipes="" (top level)
    _write_manifest(p, data)
    cfg = _cfg(mini_repo)
    with pytest.raises(ConfigError, match=re.escape("web/misc/index.tsx")):
        scan(cfg, _corpus(cfg.cookbook_dir))


def test_reserved_stem_is_fine_once_a_spec_claims_it_directly(mini_repo):
    (mini_repo / "web" / "misc").mkdir()
    (mini_repo / "web" / "misc" / "index.tsx").write_text("export {}\n", encoding="utf-8")
    p, data = _manifest(mini_repo)
    data["code"]["roots"].append({"path": "web/misc", "platform": "web"})
    _write_manifest(p, data)
    (mini_repo / "cookbook" / "entry-point.md").write_text(
        "---\ntype: ingredient\nstatus: draft\n---\n\n"
        "## Reference Implementations\n\n| Platform | Path |\n| --- | --- |\n"
        "| web | `web/misc/index.tsx` |\n", encoding="utf-8")
    cfg = _cfg(mini_repo)
    rows = scan(cfg, _corpus(cfg.cookbook_dir))
    row = next(r for r in rows if r.path == "web/misc/index.tsx")
    assert row.name == "entry-point"
    assert row.claimed is True
