"""`cookr convert` and `cookr compile --target doc` at the CLI level."""

from __future__ import annotations

import json
import shutil

import pytest

from cookr.cli import main
from cookr.core.artifact import normalize_document

from ..conftest import FIXTURES

DOCS = FIXTURES / "artifacts" / "docs"


@pytest.fixture
def work(tmp_path, monkeypatch):
    """A cwd holding cookbook/ with the four sample docs."""
    shutil.copytree(DOCS, tmp_path / "cookbook")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_convert_in_place_then_compile_reproduces_the_docs(work, capsys):
    originals = {p.name: p.read_text() for p in (work / "cookbook").glob("*.md")}
    assert main(["convert", "--remove-source"]) == 0
    assert not list((work / "cookbook").glob("*.md"))
    assert (work / "cookbook" / "yagni" / "artifact.json").is_file()
    assert main(["compile", "--target", "doc"]) == 0
    for name, text in originals.items():
        assert (work / "cookbook" / name).read_text() == normalize_document(text)
    assert "4 of 4 compiled" in capsys.readouterr().out


def test_convert_dry_run_writes_nothing(work):
    assert main(["convert", "--dry-run"]) == 0
    assert not (work / "cookbook" / "yagni").exists()


def test_a_spec_with_child_specs_shares_its_folder_with_them(work, capsys):
    # mcp-server.md beside mcp-server/mcp-tool.md: the parent's folder is the
    # directory its child lives in, so both convert and neither is lost.
    child = work / "cookbook" / "mcp-server" / "mcp-tool.md"
    child.parent.mkdir()
    shutil.move(work / "cookbook" / "mcp-tool.md", child)
    originals = {p: p.read_text() for p in (work / "cookbook").rglob("*.md")}
    assert main(["convert", "--json"]) == 0
    assert {r["status"] for r in json.loads(capsys.readouterr().out)} == {"converted"}
    assert (child.parent / "artifact.json").is_file()
    assert (child.parent / "mcp-tool" / "artifact.json").is_file()
    assert main(["compile", "--check"]) == 0
    for p, text in originals.items():
        assert p.read_text() == normalize_document(text)


def test_convert_refuses_a_part_that_would_overwrite_a_child_spec(work, capsys):
    clash = work / "cookbook" / "mcp-server" / "intro.md"   # mcp-server's first part is intro
    clash.parent.mkdir()
    shutil.move(work / "cookbook" / "mcp-tool.md", clash)
    assert main(["convert", "--json"]) == 1
    errors = [r for r in json.loads(capsys.readouterr().out) if r["status"] == "error"]
    assert [e["source"] for e in errors] == ["cookbook/mcp-server.md"]
    assert "intro.md" in errors[0]["detail"]
    assert "MCP" in clash.read_text() and not (clash.parent / "artifact.json").exists()


def test_convert_refuses_contradictory_flags(work):
    assert main(["convert", "--dry-run", "--remove-source"]) == 2


def test_missing_path_is_an_error(work):
    assert main(["convert", "nope"]) == 2
    assert main(["compile", "nope"]) == 2


def test_converting_a_named_file_that_is_not_an_artifact_is_an_error(work):
    (work / "notes.md").write_text("# Notes\n")
    assert main(["convert", "notes.md"]) == 2


def test_out_mirrors_paths(work, tmp_path):
    out = tmp_path / "built"
    assert main(["convert", "--out", str(out)]) == 0
    assert (out / "cookbook" / "mcp-tool" / "artifact.json").is_file()
    assert (work / "cookbook" / "mcp-tool.md").is_file()


def test_compile_check_reports_missing_stale_then_current(work, capsys):
    assert main(["convert", "--remove-source"]) == 0
    assert main(["compile", "--check"]) == 1
    assert main(["compile"]) == 0
    assert main(["compile", "--check"]) == 0
    (work / "cookbook" / "yagni" / "intro.md").write_text("# YAGNI\n\nChanged.\n\n")
    capsys.readouterr()
    assert main(["compile", "--check", "--json"]) == 1
    rows = {r["dest"]: r["status"] for r in json.loads(capsys.readouterr().out)}
    assert rows["cookbook/yagni.md"] == "stale"


def test_compile_reports_a_broken_folder(work, capsys):
    assert main(["convert", "--remove-source"]) == 0
    (work / "cookbook" / "yagni" / "history.md").unlink()
    capsys.readouterr()
    assert main(["compile", "--json"]) == 1
    rows = json.loads(capsys.readouterr().out)
    assert [r["status"] for r in rows if "yagni" in r["source"]] == ["error"]


def test_type_shape_problems_are_reported_not_fatal(work, capsys):
    doc = work / "cookbook" / "mcp-tool.md"
    doc.write_text(doc.read_text().replace("## Compliance\n", "## Compliance Notes\n"))
    assert main(["convert", "--json"]) == 0
    row = next(r for r in json.loads(capsys.readouterr().out) if "mcp-tool" in r["source"])
    assert "missing section: ## Compliance" in row["problems"]


def test_convert_skips_an_artifact_that_is_already_a_folder(work, capsys):
    # After the migration the doc is compiled output; converting it again
    # would overwrite edits made in the folder.
    assert main(["convert"]) == 0
    (work / "cookbook" / "yagni" / "intro.md").write_text("# YAGNI\n\nEdited in the folder.\n\n")
    capsys.readouterr()
    assert main(["convert", "--json"]) == 0
    rows = {r["source"]: r["status"] for r in json.loads(capsys.readouterr().out)}
    assert set(rows.values()) == {"skipped"}
    assert "Edited in the folder" in (work / "cookbook" / "yagni" / "intro.md").read_text()


def test_convert_update_folds_a_doc_edit_into_the_folder(work, capsys):
    assert main(["convert"]) == 0
    folder = work / "cookbook" / "yagni"
    (folder / "attribution.md").write_text("Credit.\n")
    doc = work / "cookbook" / "yagni.md"
    doc.write_text(doc.read_text().replace("# YAGNI", "# YAGNI\n\nAdded in the doc.", 1))
    assert main(["compile", "--check"]) == 1
    capsys.readouterr()
    assert main(["convert", "--update", "--json"]) == 0
    rows = {r["source"]: r["status"] for r in json.loads(capsys.readouterr().out)}
    assert rows["cookbook/yagni.md"] == "updated"
    assert rows["cookbook/mcp-tool.md"] == "unchanged"
    assert "Added in the doc." in (folder / "intro.md").read_text()
    assert (folder / "attribution.md").read_text() == "Credit.\n"
    assert main(["compile", "--check"]) == 0


def test_convert_update_refuses_out_and_remove_source(work):
    assert main(["convert", "--update", "--out", "x"]) == 2
    assert main(["convert", "--update", "--remove-source"]) == 2


def test_convert_refuses_a_file_it_cannot_parse(work, capsys):
    (work / "cookbook" / "worse.md").write_text("---\ntype: guideline\n---\n# x\n## Last")
    assert main(["convert", "--json"]) == 1
    rows = {r["source"]: r["status"] for r in json.loads(capsys.readouterr().out)}
    assert rows["cookbook/worse.md"] == "error"
    assert not (work / "cookbook" / "worse").exists()


def _edit_folder(work):
    (work / "cookbook" / "yagni" / "intro.md").write_text("# YAGNI\n\nEdited in the folder.\n\n")


def _edit_doc(work):
    doc = work / "cookbook" / "yagni.md"
    doc.write_text(doc.read_text().replace("# YAGNI", "# YAGNI\n\nEdited in the doc.", 1))


def _rows(capsys):
    return {r["source"]: r for r in json.loads(capsys.readouterr().out)}


def test_compile_refuses_to_overwrite_an_edited_doc(work, capsys):
    assert main(["convert"]) == 0
    _edit_doc(work)
    capsys.readouterr()
    assert main(["compile", "--json"]) == 1
    row = _rows(capsys)["cookbook/yagni"]
    assert row["status"] == "error" and "convert --update" in row["detail"]
    assert "Edited in the doc." in (work / "cookbook" / "yagni.md").read_text()
    assert main(["compile", "--force"]) == 0
    assert "Edited in the doc." not in (work / "cookbook" / "yagni.md").read_text()


def test_compile_check_names_which_side_changed(work, capsys):
    assert main(["convert"]) == 0
    _edit_doc(work)
    capsys.readouterr()
    assert main(["compile", "--check", "--json"]) == 1
    assert "edited since cookr wrote it" in _rows(capsys)["cookbook/yagni"]["detail"]


def test_compile_writes_a_doc_whose_folder_changed(work):
    assert main(["convert"]) == 0
    _edit_folder(work)
    assert main(["compile"]) == 0
    assert "Edited in the folder." in (work / "cookbook" / "yagni.md").read_text()
    assert main(["compile", "--check"]) == 0


def test_convert_update_refuses_to_discard_a_folder_edit(work, capsys):
    assert main(["convert"]) == 0
    _edit_folder(work)
    capsys.readouterr()
    assert main(["convert", "--update", "--json"]) == 1
    assert "folder was edited" in _rows(capsys)["cookbook/yagni.md"]["detail"]
    assert "Edited in the folder." in (work / "cookbook" / "yagni" / "intro.md").read_text()
    assert main(["convert", "--update", "--force"]) == 0
    assert "Edited in the folder." not in (work / "cookbook" / "yagni" / "intro.md").read_text()


def test_both_sides_edited_is_refused_both_ways(work):
    assert main(["convert"]) == 0
    _edit_folder(work)
    _edit_doc(work)
    assert main(["compile"]) == 1
    assert main(["convert", "--update"]) == 1
    assert main(["convert", "--update", "--force"]) == 0
    text = (work / "cookbook" / "yagni.md").read_text()
    assert "Edited in the doc." in text and "Edited in the folder." not in text
    assert main(["compile", "--check"]) == 0


def test_force_flags_refuse_what_they_do_not_apply_to(work):
    assert main(["convert", "--force"]) == 2
    assert main(["compile", "--check", "--force"]) == 2
    assert main(["compile", "--target", "skill", "--force", "--out", "x"]) == 2
