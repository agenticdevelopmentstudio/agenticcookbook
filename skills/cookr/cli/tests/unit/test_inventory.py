from __future__ import annotations

from cookr.core.config import load_config
from cookr.core.inventory import scan


def test_scan_lists_sources_by_tier(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    rows = scan(cfg)
    names = [(r.tier, r.name, r.platform) for r in rows]
    assert names == [
        ("apple", "button", "apple"),
        ("apple", "toolbar-button", "apple"),
        ("blocks", "stat-card", "web"),
        ("primitives", "button", "web"),
        ("primitives", "chat-composer", "web"),
    ]


def test_scan_drops_ignored(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    paths = [r.path for r in scan(cfg)]
    assert "web/components/button.stories.tsx" not in paths
    assert "web/components/index.ts" not in paths


def test_scan_paths_are_repo_relative_posix(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    assert "web/components/Button.tsx" in [r.path for r in scan(cfg)]


def test_scan_applies_a_rename_to_one_path(mini_repo):
    import json
    p = mini_repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["renames"] = {"web/components/Button.tsx": "web-button"}
    p.write_text(json.dumps(data), encoding="utf-8")
    rows = scan(load_config(p))
    by_path = {r.path: r.name for r in rows}
    assert by_path["web/components/Button.tsx"] == "web-button"
    assert "button" in {r.name for r in rows if r.platform == "apple"}


def test_root_ignore_applies_to_its_own_root_only(mini_repo):
    import json
    p = mini_repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    for r in data["roots"]:
        if r["path"] == "apple/UI":
            r["ignore"] = ["**/Toolbar*.swift", "**/Button.*"]
    p.write_text(json.dumps(data), encoding="utf-8")
    paths = [r.path for r in scan(load_config(p))]
    assert "apple/UI/ToolbarButton.swift" not in paths
    assert "apple/UI/Button.swift" not in paths
    assert "web/components/Button.tsx" in paths     # another root's Button survives


# --- glob semantics (K05, A-cookr_7) ----------------------------------------

import re  # noqa: E402

import pytest  # noqa: E402

from cookr.core.inventory import component_stem, glob_regex, ignore_set  # noqa: E402


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
    import json
    p = repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["ignore"] = patterns
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_star_ignore_keeps_nested_files(mini_repo):
    nested = mini_repo / "web" / "components" / "three-pane"
    nested.mkdir()
    (nested / "useLayout.ts").write_text("export {}\n", encoding="utf-8")
    p = _set_ignore(mini_repo, ["web/components/*.ts", "**/*.stories.tsx"])
    paths = [r.path for r in scan(load_config(p))]
    assert "web/components/index.ts" not in paths
    assert "web/components/three-pane/useLayout.ts" in paths


def test_second_globstar_matches_files_directly_in_the_directory(mini_repo):
    tests = mini_repo / "web" / "components" / "__tests__"
    tests.mkdir()
    (tests / "widget.ts").write_text("export {}\n", encoding="utf-8")
    p = _set_ignore(mini_repo, ["**/__tests__/**/*.ts", "**/*.stories.tsx", "**/index.ts"])
    assert "web/components/__tests__/widget.ts" not in [r.path for r in scan(load_config(p))]


def test_wholly_ignored_directories_are_not_walked(mini_repo, monkeypatch):
    import os
    from cookr.core import inventory
    gen = mini_repo / "web" / "components" / "generated" / "deep"
    gen.mkdir(parents=True)
    (gen / "Model.ts").write_text("export {}\n", encoding="utf-8")
    p = _set_ignore(mini_repo, ["**/generated/**", "**/*.stories.tsx", "**/index.ts"])
    seen = []
    real_walk = os.walk

    def spy(top, *a, **k):
        for entry in real_walk(top, *a, **k):
            seen.append(entry[0])
            yield entry

    monkeypatch.setattr(inventory.os, "walk", spy)
    paths = [r.path for r in scan(load_config(p))]
    assert "web/components/generated/deep/Model.ts" not in paths
    assert not any("generated" in d for d in seen)


def test_tier_scan_walks_only_that_tiers_roots(mini_repo, monkeypatch):
    import os
    from cookr.core import inventory
    tops = []
    real_walk = os.walk
    monkeypatch.setattr(inventory.os, "walk", lambda top, *a, **k: tops.append(str(top)) or real_walk(top, *a, **k))
    rows = scan(load_config(mini_repo / ".cookr.json"), tier="blocks")
    assert [r.name for r in rows] == ["stat-card"]
    assert len(tops) == 1 and tops[0].endswith("web/blocks")


# --- component names (A-cookr_5) --------------------------------------------

@pytest.mark.parametrize("filename,stem", [
    ("StatCard.xaml.cs", "StatCard"),
    ("StatCard.xaml", "StatCard"),
    ("Button.tsx", "Button"),
    ("x.test.ts", "x.test"),        # `.test` is not a source suffix
    ("types.d.ts", "types.d"),
])
def test_component_stem_drops_every_trailing_source_suffix(filename, stem):
    assert component_stem(filename) == stem


def test_xaml_code_behind_is_one_component(mini_repo):
    import json
    win = mini_repo / "win" / "Controls"
    win.mkdir(parents=True)
    (win / "StatCard.xaml").write_text("<UserControl/>\n", encoding="utf-8")
    (win / "StatCard.xaml.cs").write_text("class StatCard {}\n", encoding="utf-8")
    p = mini_repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["roots"].append({"path": "win/Controls", "tier": "windows", "platform": "windows"})
    p.write_text(json.dumps(data), encoding="utf-8")
    rows = [r for r in scan(load_config(p)) if r.tier == "windows"]
    assert {(r.name, r.path) for r in rows} == {
        ("stat-card", "win/Controls/StatCard.xaml"),
        ("stat-card", "win/Controls/StatCard.xaml.cs"),
    }


# --- reserved recipe names (C_6) --------------------------------------------

@pytest.mark.parametrize("filename", ["References.tsx", "index.tsx", "INDEX.swift"])
def test_component_named_like_a_skipped_recipe_file_is_a_config_error(mini_repo, filename):
    from cookr.core.config import ConfigError
    (mini_repo / "web" / "blocks" / filename).write_text("export {}\n", encoding="utf-8")
    with pytest.raises(ConfigError, match=f"web/blocks/{re.escape(filename)}"):
        scan(load_config(mini_repo / ".cookr.json"))


def test_reserved_name_is_fine_once_aliased(mini_repo):
    import json
    (mini_repo / "web" / "blocks" / "References.tsx").write_text("export {}\n", encoding="utf-8")
    p = mini_repo / ".cookr.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["aliases"]["references"] = "reference-list"
    p.write_text(json.dumps(data), encoding="utf-8")
    assert "references" in {r.name for r in scan(load_config(p))}
