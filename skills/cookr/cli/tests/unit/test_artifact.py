"""The artifact source folder: lossless split, compose and frontmatter."""

from __future__ import annotations

import filecmp
import json

import pytest

from cookr.core.artifact import (
    ArtifactError,
    compose_document,
    emit_frontmatter,
    find_documents,
    find_folders,
    load_folder,
    normalize_document,
    parse_frontmatter,
    read_document,
    split_body,
    write_folder,
)

from ..conftest import FIXTURES, REPO_ROOT

SAMPLES = FIXTURES / "artifacts"
DOCS = sorted((SAMPLES / "docs").glob("*.md"))


@pytest.mark.parametrize("doc", DOCS, ids=lambda p: p.stem)
def test_sample_folder_composes_its_document(doc):
    folder = SAMPLES / "folders" / doc.stem
    assert compose_document(load_folder(folder)) == normalize_document(doc.read_text())


@pytest.mark.parametrize("doc", DOCS, ids=lambda p: p.stem)
def test_sample_folder_is_what_convert_writes(doc, tmp_path):
    out = tmp_path / doc.stem
    write_folder(read_document(doc.read_text()), out)
    cmp = filecmp.dircmp(out, SAMPLES / "folders" / doc.stem)
    assert not (cmp.left_only or cmp.right_only or cmp.diff_files)


def test_every_cookbook_artifact_round_trips(tmp_path, repo_v2):
    # Source folders are the only form committed: compile each to its doc,
    # split that doc back into a folder, and the folder must compose the same doc.
    folders = find_folders([repo_v2 / "cookbook"])
    assert len(folders) > 400
    for folder in folders:
        text = compose_document(load_folder(folder))
        out = tmp_path / folder.relative_to(repo_v2)
        write_folder(read_document(text), out)
        assert compose_document(load_folder(out)) == normalize_document(text), folder


def test_no_compiled_doc_is_committed_beside_its_folder():
    """A doc beside its folder is a stale copy of it; the folder is the source."""
    assert find_documents([REPO_ROOT / "cookbook"]) == []


def test_split_keeps_every_byte():
    body = "\n# T\n\nStatement.\n\n## A\ntext\n\n## B b\n\n## Change History\n\n| x |\n"
    parts = split_body(body)
    assert [p.name for p in parts] == ["intro", "a", "b-b", "history"]
    assert "".join(p.text if p.heading is None else f"## {p.heading}\n{p.text}" for p in parts) == body


def test_split_ignores_headings_inside_fences():
    body = "# T\n\n## Code\n```md\n## not a section\n```\n~~~\n## nor this\n~~~\n## Next\nx\n"
    assert [p.name for p in split_body(body)] == ["intro", "code", "next"]


def test_split_disambiguates_repeated_and_reserved_names():
    body = "# T\n## Intro\n## Notes\n## Notes\n## Artifact\n"
    assert [p.name for p in split_body(body)] == ["intro", "intro-2", "notes", "notes-2", "artifact-2"]


def test_split_without_intro_or_sections():
    assert [p.name for p in split_body("## Only\nx\n")] == ["only"]
    assert [p.name for p in split_body("# T\nbody\n")] == ["intro"]
    assert split_body("") == []


def test_heading_on_unterminated_last_line_is_refused():
    with pytest.raises(ArtifactError):
        split_body("# T\n## Last")


@pytest.mark.parametrize("value", [
    "plain", "has: colon", "- leading dash", "# hash", "it's", 'say "hi"', "", "yes", "null",
    "1.0", "2026-06-09", "trailing ", "[bracket", "ünïcode — dash", "a #b",
])
def test_frontmatter_strings_round_trip(value):
    meta = {"summary": value, "tags": [value], "other": value, "created": value}
    assert parse_frontmatter(emit_frontmatter(meta)) == meta


def test_frontmatter_layout():
    meta = {"id": "x", "title": "T", "created": "2026-06-09", "tags": [], "related": ["a", "b"],
            "approved-by": ""}
    assert emit_frontmatter(meta) == (
        'id: x\ntitle: "T"\ncreated: 2026-06-09\ntags: []\nrelated:\n  - a\n  - b\napproved-by: ""\n'
    )


def test_yaml_dates_become_iso_strings():
    assert parse_frontmatter("created: 2026-06-09") == {"created": "2026-06-09"}


def test_nested_frontmatter_values_are_refused():
    with pytest.raises(ArtifactError):
        emit_frontmatter({"references": [{"Eberle, SCAMPER": "Games"}]})


def test_document_without_frontmatter_is_refused():
    with pytest.raises(ArtifactError):
        read_document("# T\n")


def test_load_refuses_a_missing_part(tmp_path):
    write_folder(read_document(DOCS[0].read_text()), tmp_path / "a")
    (tmp_path / "a" / "history.md").unlink()
    with pytest.raises(ArtifactError, match="history"):
        load_folder(tmp_path / "a")


def test_load_refuses_an_unknown_format(tmp_path):
    (tmp_path / "artifact.json").write_text(json.dumps({"format": 3, "meta": {}, "parts": []}))
    with pytest.raises(ArtifactError, match="format"):
        load_folder(tmp_path)


def test_load_folder_refuses_format_1(tmp_path):
    (tmp_path / "artifact.json").write_text(json.dumps({"format": 1, "meta": {}, "parts": []}))
    with pytest.raises(ArtifactError, match="format 1; run `cookr upgrade`"):
        load_folder(tmp_path)


def test_load_folder_reads_its_manifest_once(tmp_path, monkeypatch):
    from pathlib import Path

    write_folder(read_document(DOCS[0].read_text()), tmp_path / "a")
    reads: list = []
    real = Path.read_text
    monkeypatch.setattr(Path, "read_text", lambda self, *a, **k: (
        reads.append(self.name), real(self, *a, **k))[1])
    load_folder(tmp_path / "a")
    assert reads.count("artifact.json") == 1


def test_load_refuses_a_boolean_format(tmp_path):
    (tmp_path / "artifact.json").write_text(json.dumps({"format": True, "meta": {}, "parts": []}))
    with pytest.raises(ArtifactError, match="unsupported format True"):
        load_folder(tmp_path)


def test_write_folder_writes_format_2():
    manifest = json.loads((SAMPLES / "folders" / DOCS[0].stem / "artifact.json").read_text())
    assert manifest["format"] == 2
    assert "domain" not in manifest["meta"]


def test_write_replaces_a_stale_folder(tmp_path):
    out = tmp_path / "a"
    write_folder(read_document(DOCS[0].read_text()), out)
    (out / "stale.md").write_text("x")
    write_folder(read_document(DOCS[0].read_text()), out)
    assert not (out / "stale.md").exists()


def test_a_folder_shared_with_child_specs_keeps_them(tmp_path):
    # A spec with child specs (a.md beside a/child.md) shares its folder with them.
    parent, child = (read_document(d.read_text()) for d in DOCS[:2])
    out = tmp_path / "a"
    write_folder(child, out / "child")
    (out / "child.md").write_text(DOCS[1].read_text())
    (out / "notes.txt").write_text("x")
    write_folder(parent, out)
    write_folder(parent, out)   # rewriting replaces only its own files
    assert load_folder(out).meta == parent.meta and load_folder(out / "child").meta == child.meta
    assert (out / "child.md").is_file() and (out / "notes.txt").is_file()


def test_a_part_never_overwrites_a_file_it_does_not_own(tmp_path):
    artifact = read_document(DOCS[0].read_text())
    out = tmp_path / "a"
    write_folder(artifact, out / "child")
    clash = out / f"{artifact.parts[0].name}.md"
    clash.write_text("someone else's")
    with pytest.raises(ArtifactError, match="would overwrite"):
        write_folder(artifact, out)
    assert clash.read_text() == "someone else's" and not (out / "artifact.json").exists()


def test_a_child_spec_named_hosts_is_refused_either_way(tmp_path):
    # `<spec>/hosts/` holds the spec's tuning additions; a child there would be read as them.
    parent, child = (read_document(d.read_text()) for d in DOCS[:2])
    write_folder(parent, tmp_path / "a")
    with pytest.raises(ArtifactError, match="host additions live"):
        write_folder(child, tmp_path / "a" / "hosts")
    write_folder(child, tmp_path / "b" / "hosts")   # no spec `b` (yet): nothing to collide with
    with pytest.raises(ArtifactError, match="is a child spec"):
        write_folder(parent, tmp_path / "b")


def test_a_child_spec_whose_doc_is_a_part_of_its_parent_is_refused(tmp_path):
    parent, child = (read_document(d.read_text()) for d in DOCS[:2])
    write_folder(parent, tmp_path / "a")
    with pytest.raises(ArtifactError, match="is a part of"):
        write_folder(child, tmp_path / "a" / parent.parts[0].name)


def test_find_skips_templates_indexes_and_non_artifacts(tmp_path):
    for name, kind in (("_template.md", "guideline"), ("INDEX.md", "guideline"),
                       ("ref.md", "reference"), ("g.md", "guideline")):
        (tmp_path / name).write_text(f"---\ntype: {kind}\n---\n# x\n")
    assert [p.name for p in find_documents([tmp_path])] == ["g.md"]


def test_find_folders(tmp_path):
    write_folder(read_document(DOCS[0].read_text()), tmp_path / "x" / "a")
    assert find_folders([tmp_path]) == [tmp_path / "x" / "a"]
    assert find_folders([tmp_path / "x" / "a"]) == [tmp_path / "x" / "a"]


def _synced(tmp_path):
    """A folder and its doc as cookr writes them together."""
    from cookr.core.artifact import doc_path, save_document
    folder = tmp_path / "a"
    write_folder(read_document(DOCS[0].read_text()), folder)
    doc = doc_path(folder)
    doc.write_text(compose_document(load_folder(folder)))
    save_document(doc, doc.read_text())
    return folder, doc


def test_sync_state_names_the_side_that_changed(tmp_path):
    from cookr.core.artifact import sync_state
    folder, doc = _synced(tmp_path)
    assert sync_state(folder) == "current"
    original = doc.read_text()
    doc.write_text(original + "doc edit\n")
    assert sync_state(folder) == "doc-edited"
    doc.write_text(original)
    intro = folder / "intro.md"
    intro.write_text(intro.read_text() + "folder edit\n")
    assert sync_state(folder) == "folder-edited"
    doc.write_text(original + "doc edit\n")
    assert sync_state(folder) == "both-edited"
    doc.unlink()
    assert sync_state(folder) == "missing"


def test_an_unrecorded_folder_that_disagrees_is_both_edited(tmp_path):
    from cookr.core.artifact import doc_path, sync_state
    folder = tmp_path / "a"
    write_folder(read_document(DOCS[0].read_text()), folder)
    doc_path(folder).write_text("---\ntype: guideline\n---\n# other\n")
    assert sync_state(folder) == "both-edited"


def test_edit_text_starts_from_the_newer_side(tmp_path):
    from cookr.core.artifact import edit_text
    folder, doc = _synced(tmp_path)
    original = doc.read_text()
    doc.write_text(original + "doc edit\n")
    assert edit_text(doc).endswith("doc edit\n")
    doc.write_text(original)
    intro = folder / "intro.md"
    intro.write_text(intro.read_text() + "folder edit\n")
    assert "folder edit" in edit_text(doc)
    doc.write_text(original + "doc edit\n")
    with pytest.raises(ArtifactError, match="both edited"):
        edit_text(doc)


def test_save_document_records_what_it_wrote(tmp_path):
    from cookr.core.artifact import doc_digest, save_document, sync_state
    folder, doc = _synced(tmp_path)
    save_document(doc, doc.read_text().replace("\n## ", "\nAdded.\n\n## ", 1))
    assert sync_state(folder) == "current"
    assert json.loads((folder / "artifact.json").read_text())["synced"] == doc_digest(doc.read_text())


# --- derived sections: with_part, authored_text, without_derived ----------------------

def _derived():
    from cookr.core import refimpl
    from cookr.core.index import Conformance, Implementation
    rows = [Implementation("apple", "A/B.swift", Conformance("conforms")),
            Implementation("web", None, Conformance("planned"))]
    return refimpl.part(rows)


_RI = ("## Reference Implementations\n\n| Platform | Location | Conformance |\n"
       "|----------|----------|-------------|\n| apple | `A/B.swift` | conforms |\n"
       "| web | (planned) | planned |\n\n")


def _placed(body: str) -> str:
    from cookr.core.artifact import Artifact, with_part
    return with_part(Artifact(meta={}, parts=split_body(body)), _derived()).body()


@pytest.mark.parametrize("anchor", ["Design Decisions", "Compliance", "Change History"])
def test_with_part_goes_before_its_anchor(anchor):
    body = f"# T\n\n## Overview\n\nx\n\n## {anchor}\n\ny\n"
    assert _placed(body) == f"# T\n\n## Overview\n\nx\n\n{_RI}## {anchor}\n\ny\n"


def test_with_part_prefers_design_decisions_then_compliance_then_change_history():
    out = _placed("## Change History\n\nc\n\n## Compliance\n\nb\n\n## Design Decisions\n\na\n")
    assert out.index("## Compliance") < out.index("## Reference Implementations") < out.index(
        "## Design Decisions")
    out = _placed("## Change History\n\nc\n\n## Compliance\n\nb\n")
    assert out.index("## Change History") < out.index("## Reference Implementations") < out.index(
        "## Compliance")


def test_with_part_appends_when_no_anchor_exists():
    assert _placed("# T\n\n## Overview\n\nx\n") == f"# T\n\n## Overview\n\nx\n\n{_RI}"


def test_with_part_adds_the_missing_trailing_newline_before_appending():
    assert _placed("# T\n\n## Overview\n\nx") == f"# T\n\n## Overview\n\nx\n\n{_RI}"


def test_with_part_ignores_an_anchor_heading_inside_a_fence():
    body = "# T\n\n## Notes\n\n```\n## Design Decisions\n```\n\n## Overview\n\nx\n"
    out = _placed(body)
    assert out == body + "\n" + _RI  # appended: the fenced heading is not a section
    assert out.index("```\n## Design Decisions\n```") < out.index("## Reference Implementations")


def test_with_part_leaves_the_original_artifact_unchanged():
    from cookr.core.artifact import Artifact, with_part
    art = Artifact(meta={}, parts=split_body("# T\n\n## Design Decisions\n\ny\n"))
    names = [p.name for p in art.parts]
    with_part(art, _derived())
    assert [p.name for p in art.parts] == names


def test_without_derived_drops_only_derived_sections():
    from cookr.core.artifact import Artifact, derived_parts, without_derived
    body = f"# T\n\n## Overview\n\nx\n\n{_RI}## Design Decisions\n\ny\n"
    art = Artifact(meta={}, parts=split_body(body))
    assert [p.heading for p in derived_parts(art)] == ["Reference Implementations"]
    assert without_derived(art).body() == "# T\n\n## Overview\n\nx\n\n## Design Decisions\n\ny\n"


def test_authored_text_strips_the_derived_section_and_save_document_restores_it(tmp_path):
    from cookr.core.artifact import authored_text, doc_path, save_document
    plain = ("---\nid: 11111111-2222-4333-8444-555555555555\ntype: ingredient\n---\n"
             "# T\n\n## Overview\n\nx\n\n## Design Decisions\n\ny\n")
    with_ri = plain.replace("## Design Decisions", _RI + "## Design Decisions")
    assert authored_text(with_ri) == plain
    assert authored_text(plain) == plain

    folder = tmp_path / "t"
    write_folder(read_document(plain), folder)
    doc = doc_path(folder)
    doc.write_text(with_ri, encoding="utf-8")
    save_document(doc, with_ri.replace("\nx\n", "\nx, edited\n"))
    assert not (folder / "reference-implementations.md").exists()
    assert "Reference Implementations" not in load_folder(folder).body()
    assert compose_document(load_folder(folder)) == plain.replace("\nx\n", "\nx, edited\n")
    assert doc.read_text(encoding="utf-8") == with_ri.replace("\nx\n", "\nx, edited\n")

