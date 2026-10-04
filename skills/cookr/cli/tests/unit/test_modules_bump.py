import pytest

from cookr.cli import main


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


HEAD = "| Version | Date | Author | Summary |\n|---------|------|--------|---------|\n"


def _doc(rows, version="1.1.0", modified="'2026-01-02'"):
    return (
        "---\ntitle: \"Alpha\"\n"
        f"version: {version}\nmodified: {modified}\n---\n\n# Alpha\n\n"
        "## Overview\n\nText.\n\n## Change History\n\n" + HEAD + "".join(rows)
    )


NEWEST_FIRST = ["| 1.1.0 | 2026-01-02 | A | second |\n", "| 1.0.0 | 2026-01-01 | A | first |\n"]
OLDEST_FIRST = list(reversed(NEWEST_FIRST))


def _bump(tmp_path, text, *extra):
    f = tmp_path / "alpha.md"
    f.write_text(text, encoding="utf-8")
    code = main(["bump", str(f), "--summary", "Fixed it", "--author", "Tester",
                 "--date", "2026-09-25", *extra])
    return code, f.read_text(encoding="utf-8")


def test_a_converted_artifact_is_bumped_in_its_folder(tmp_path):
    (tmp_path / "alpha.md").write_text(_doc(NEWEST_FIRST).replace("---\n", "---\ntype: guideline\n", 1),
                                       encoding="utf-8")
    assert main(["convert", str(tmp_path / "alpha.md")]) == 0
    folder = tmp_path / "alpha"
    (folder / "attribution.md").write_text("Credit.\n", encoding="utf-8")
    # Bumping the folder and bumping its doc are the same thing.
    assert main(["bump", str(folder), "--summary", "Fixed it", "--author", "Tester",
                 "--date", "2026-09-25"]) == 0
    assert '"version": "1.1.1"' in (folder / "artifact.json").read_text()
    assert "| 1.1.1 | 2026-09-25 | Tester | Fixed it |" in (folder / "history.md").read_text()
    assert (folder / "attribution.md").read_text() == "Credit.\n"  # extras survive
    assert main(["compile", "--check", str(folder)]) == 0  # the doc was recompiled


def _converted(tmp_path):
    (tmp_path / "alpha.md").write_text(_doc(NEWEST_FIRST).replace("---\n", "---\ntype: guideline\n", 1),
                                       encoding="utf-8")
    assert main(["convert", str(tmp_path / "alpha.md")]) == 0
    return tmp_path / "alpha"


def test_a_folder_edited_since_its_doc_was_written_keeps_the_edit(tmp_path):
    folder = _converted(tmp_path)
    (folder / "overview.md").write_text("\nEdited in the folder.\n\n", encoding="utf-8")
    assert main(["bump", str(tmp_path / "alpha.md"), "--summary", "Fixed it", "--author", "Tester",
                 "--date", "2026-09-25"]) == 0
    assert "Edited in the folder." in (folder / "overview.md").read_text()
    assert "Edited in the folder." in (tmp_path / "alpha.md").read_text()
    assert main(["compile", "--check", str(folder)]) == 0


def test_a_doc_and_folder_both_edited_are_refused(tmp_path):
    folder = _converted(tmp_path)
    (folder / "overview.md").write_text("\nEdited in the folder.\n\n", encoding="utf-8")
    doc = tmp_path / "alpha.md"
    doc.write_text(doc.read_text().replace("Text.", "Edited in the doc."), encoding="utf-8")
    assert main(["bump", str(doc), "--summary", "Fixed it", "--author", "Tester",
                 "--date", "2026-09-25"]) == 1
    assert '"version": "1.1.0"' in (folder / "artifact.json").read_text()


def test_newest_first_table_gets_row_at_top(tmp_path):
    code, out = _bump(tmp_path, _doc(NEWEST_FIRST))
    assert code == 0
    assert "version: 1.1.1\n" in out and "modified: '2026-09-25'\n" in out
    assert HEAD + "| 1.1.1 | 2026-09-25 | Tester | Fixed it |\n| 1.1.0" in out


def test_oldest_first_table_gets_row_at_bottom(tmp_path):
    code, out = _bump(tmp_path, _doc(OLDEST_FIRST))
    assert code == 0
    assert out.endswith("| 1.1.0 | 2026-01-02 | A | second |\n| 1.1.1 | 2026-09-25 | Tester | Fixed it |\n")


def test_single_row_table_grows_newest_first(tmp_path):
    code, out = _bump(tmp_path, _doc(["| 1.1.0 | 2026-01-02 | A | only |\n"]))
    assert code == 0
    assert HEAD + "| 1.1.1 | 2026-09-25 | Tester | Fixed it |\n| 1.1.0" in out


def test_mixed_order_table_is_refused_and_nothing_written(tmp_path):
    mixed = ["| 1.0.0 | 2026-01-01 | A | a |\n", "| 1.1.0 | 2026-01-02 | A | b |\n",
             "| 1.0.1 | 2026-01-01 | A | c |\n"]
    before = _doc(mixed)
    code, out = _bump(tmp_path, before)
    assert code != 0
    assert out == before


def test_minor_and_major_levels(tmp_path):
    code, out = _bump(tmp_path, _doc(NEWEST_FIRST), "--level", "minor")
    assert code == 0 and "version: 1.2.0\n" in out
    code, out = _bump(tmp_path, _doc(NEWEST_FIRST), "--level", "major")
    assert code == 0 and "version: 2.0.0\n" in out


def test_dry_run_writes_nothing(tmp_path):
    before = _doc(NEWEST_FIRST)
    code, out = _bump(tmp_path, before, "--dry-run")
    assert code == 0 and out == before


def test_quoting_style_and_other_keys_survive(tmp_path):
    code, out = _bump(tmp_path, _doc(NEWEST_FIRST, version='"1.1.0"', modified="2026-01-02"))
    assert code == 0
    assert 'version: "1.1.1"\n' in out and "modified: 2026-09-25\n" in out
    assert 'title: "Alpha"\n' in out


def test_existing_row_for_new_version_is_refused(tmp_path):
    rows = ["| 1.1.1 | 2026-01-03 | A | already |\n"] + NEWEST_FIRST
    before = _doc(rows)
    code, out = _bump(tmp_path, before)
    assert code != 0 and out == before
