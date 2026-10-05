"""iter_markdown skip rules."""

from __future__ import annotations

from cookr.core.markdown import SKIP_NAMES, iter_markdown, reserved_name


def test_skip_reserved_filenames(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "recipes" / "good.md").write_text("# Good\n", encoding="utf-8")
    for name in SKIP_NAMES:
        (tmp_path / "recipes" / name).write_text("# skip\n", encoding="utf-8")
    files = iter_markdown(tmp_path)
    assert [f.name for f in files] == ["good.md"]


def test_skip_directories(tmp_path):
    (tmp_path / "recipes").mkdir()
    (tmp_path / "appendix").mkdir()
    (tmp_path / "recipes" / "r.md").write_text("# r\n", encoding="utf-8")
    (tmp_path / "appendix" / "a.md").write_text("# a\n", encoding="utf-8")
    files = iter_markdown(tmp_path, skip_dirs=("appendix",))
    assert {f.name for f in files} == {"r.md"}


def test_sorted_output(tmp_path):
    (tmp_path / "recipes").mkdir()
    for name in ("z.md", "a.md", "m.md"):
        (tmp_path / "recipes" / name).write_text("# x\n", encoding="utf-8")
    files = iter_markdown(tmp_path)
    assert [f.name for f in files] == ["a.md", "m.md", "z.md"]


def test_empty_dir(tmp_path):
    assert iter_markdown(tmp_path) == []


def test_skip_the_parts_of_source_folders(tmp_path):
    # The compiled doc beside a folder is the artifact; its parts are not.
    folder = tmp_path / "guidelines" / "alpha"
    (folder / "examples").mkdir(parents=True)
    (folder / "hosts").mkdir()
    (folder / "artifact.json").write_text('{"parts": [{"part": "intro"}, {"part": "history"}]}',
                                          encoding="utf-8")
    for part in ("intro.md", "history.md", "examples/good.md", "hosts/claude.add.md"):
        (folder / part).write_text("x\n", encoding="utf-8")
    (tmp_path / "guidelines" / "alpha.md").write_text("# Alpha\n", encoding="utf-8")
    assert [f.relative_to(tmp_path).as_posix() for f in iter_markdown(tmp_path)] == ["guidelines/alpha.md"]
    assert iter_markdown(folder) == []  # walking a folder itself finds only parts


def test_an_unreadable_manifest_keeps_its_folder_out_of_the_walk(tmp_path):
    (tmp_path / "alpha").mkdir()
    (tmp_path / "alpha" / "artifact.json").write_text("{", encoding="utf-8")
    (tmp_path / "alpha" / "intro.md").write_text("x\n", encoding="utf-8")
    assert iter_markdown(tmp_path) == []


def test_a_child_specs_doc_in_its_parents_folder_is_a_doc(tmp_path):
    folder = tmp_path / "telemetry"
    (folder / "sources").mkdir(parents=True)
    (folder / "artifact.json").write_text('{"parts": [{"part": "intro"}]}', encoding="utf-8")
    for f in ("intro.md", "sources.md", "sources/files.md"):
        (folder / f).write_text("x\n", encoding="utf-8")
    (tmp_path / "telemetry.md").write_text("x\n", encoding="utf-8")
    assert sorted(f.relative_to(tmp_path).as_posix() for f in iter_markdown(tmp_path)) == [
        "telemetry.md", "telemetry/sources.md", "telemetry/sources/files.md"]


def test_an_artifact_doc_grouped_under_a_parents_folder_is_a_doc(tmp_path):
    folder = tmp_path / "vscode-api"
    (folder / "languages").mkdir(parents=True)
    (folder / "hosts").mkdir()
    (folder / "examples").mkdir()
    (folder / "artifact.json").write_text('{"parts": [{"part": "intro"}]}', encoding="utf-8")
    doc = "---\ntype: ingredient\n---\n# Diagnostic Types\n"
    (folder / "intro.md").write_text("x\n", encoding="utf-8")
    (folder / "languages" / "diagnostic-types.md").write_text(doc, encoding="utf-8")
    (folder / "hosts" / "claude.add.md").write_text(doc, encoding="utf-8")
    (folder / "examples" / "good.md").write_text("x\n", encoding="utf-8")
    (tmp_path / "vscode-api.md").write_text(doc, encoding="utf-8")
    assert sorted(f.relative_to(tmp_path).as_posix() for f in iter_markdown(tmp_path)) == [
        "vscode-api.md", "vscode-api/languages/diagnostic-types.md"]


def test_reserved_names(tmp_path):
    assert "skips" in reserved_name("ui/index")
    assert "host additions" in reserved_name("ui/hosts")
    assert reserved_name("ui/rows") is None
    (tmp_path / "ui").mkdir()
    (tmp_path / "ui" / "artifact.json").write_text('{"parts": [{"part": "rules"}]}', encoding="utf-8")
    assert "part of the `ui` source folder" in reserved_name("ui/rules", tmp_path)
    assert reserved_name("ui/rows", tmp_path) is None
