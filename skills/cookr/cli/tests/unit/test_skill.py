"""The `skill` target: names, routes, templates, variants, the compiled set."""

from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import hosts, skill, tuning
from cookr.core.artifact import Artifact, Part, dump_manifest, find_folders, load_folder, save_document, unconverted, write_folder

REPO = Path(__file__).resolve().parents[5]
BOOK_ID = "b0000000-0000-4000-8000-000000000000"


def test_too_long_lists_each_rendering_over_the_line_limit():
    s = skill.Skill(name="a", routes=(), text="", folder=Path("a"), type="recipe")
    b = skill.Built(s, {"a/SKILL.md": "x\n" * 3, "a/targets/claude.SKILL.md": "x\n" * 5,
                        "a/references/testing.md": "x\n" * 9}, [])
    assert skill.too_long([b], limit=4) == {"a/targets/claude.SKILL.md": 5}   # references load on demand
    assert skill.too_long([b], limit=5) == {}


def make(root: Path, rel: str, type_: str, *, triggers=None, platforms=None, routes=None,
         summary="Does the thing.", body="Guidance.\n"):
    folder = root / rel
    meta = {"id": str(uuid.uuid5(uuid.UUID(BOOK_ID), rel)), "title": "T", "type": type_,
            "version": "1.2.0", "summary": summary}
    if triggers is not None:
        meta["triggers"] = triggers
    if platforms is not None:
        meta["platforms"] = platforms
    write_folder(Artifact(meta=meta, routes=routes, parts=[
        Part("intro", f"# T\n\n{body}\n"),
        Part("why-this-matters", "Because.\n\n", "Why this matters"),
        Part("rules", "- MUST do it.\n\n", "Rules"),
        Part("history", "| Version | Date | Author | Summary |\n", "Change History"),
    ]), folder)
    return folder


def manifest(root: Path, rdid: str = "book") -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "cookbook.json").write_text(json.dumps({"format": 2, "id": BOOK_ID, "rdid": rdid}))


def index_folders(root: Path) -> None:
    """Record every folder under `root` in its index.json, as a format-2 cookbook has."""
    from cookr.core.identity import read_manifest
    from cookr.core.index import Index, save_index, sync_from_folders
    index = Index(cookbook=read_manifest(root))
    sync_from_folders(index, root)
    save_index(index, root)


@pytest.fixture
def book(tmp_path):
    root = tmp_path / "cookbook"
    manifest(root)
    make(root, "guidelines/implementing/data/use-wal", "guideline", triggers=["database-operations"])
    make(root, "principles/simplicity", "principle")
    make(root, "ingredients/ui/components/badge", "ingredient", platforms=["macos", "ios"])
    index_folders(root)
    return root


def test_names_are_the_path_below_the_type_dir():
    assert skill.skill_name("guidelines", ("implementing", "data", "use-wal")) == "implementing-data-use-wal"
    assert skill.skill_name("principles", ("simplicity",)) == "principle-simplicity"
    assert skill.skill_name("ingredients", ("ui", "badge"), "adtoolkit") == "adtoolkit-ui-badge"


def test_a_long_name_is_cut_and_hashed_stably():
    long = ("implementing", "code-quality", "no-external-dependencies-in-core-libraries-ever")
    name = skill.skill_name("guidelines", long)
    assert len(name) <= skill.NAME_MAX and name == skill.skill_name("guidelines", long)
    assert name != skill.skill_name("guidelines", long[:2] + ("no-external-dependencies-in-core-libraries-nope",))


def test_routes_are_derived_per_type(book):
    g = skill.compose(book / "guidelines/implementing/data/use-wal")
    assert g.routes == ("coding/implementing/data", "coding/when/database-operations/implementing/data")
    assert skill.compose(book / "principles/simplicity").routes == ("principles",)
    i = skill.compose(book / "ingredients/ui/components/badge", library="adtoolkit")
    assert i.routes == ("components/adtoolkit/ui/components",
                        "components/adtoolkit/platform/macos/ui/components",
                        "components/adtoolkit/platform/ios/ui/components")
    assert i.name == "adtoolkit-ui-components-badge"


def test_a_library_organized_by_concept_is_placed_below_its_cookbook_root(tmp_path):
    root = tmp_path / "lib" / "cookbook"
    root.mkdir(parents=True)
    (root / "cookbook.json").write_text("{}")
    folder = make(root, "ui/settings/rows", "ingredient", platforms=["macos"])
    assert skill.path_below_type(folder) == ("ingredients", ("ui", "settings", "rows"))
    s = skill.compose(folder, library="adtoolkit")
    assert s.name == "adtoolkit-ui-settings-rows"
    assert "components/adtoolkit/platform/macos/ui/settings" in s.routes


def test_a_folder_under_no_type_dir_and_no_cookbook_is_an_error(tmp_path):
    folder = make(tmp_path / "loose", "ui/rows", "ingredient")
    with pytest.raises(skill.SkillError, match="cookbook.json"):
        skill.path_below_type(folder)


def test_placeholders_an_artifact_quotes_are_left_as_written(tmp_path):
    folder = make(tmp_path / "cookbook", "guidelines/cookbook/templates", "guideline",
                  body="Write `{{version}}` and `{{rdid}}` in a template.\n")
    text = skill.compose(folder).text
    assert "Write `{{version}}` and `{{rdid}}` in a template." in text
    assert "1.2.0" in text                                          # the template's own placeholder


def test_templates_come_from_the_checkout_cookr_ships_from_not_the_installed_copy(tmp_path, monkeypatch):
    monkeypatch.delenv(skill.TEMPLATES_ENV, raising=False)
    assert skill.templates_root(REPO / "cookbook") == (REPO / skill.SOURCE_TEMPLATES)
    assert skill.templates_root(tmp_path / "cookbook") == skill.PACKAGED_TEMPLATES
    assert skill.templates_root() == skill.PACKAGED_TEMPLATES
    monkeypatch.setenv(skill.TEMPLATES_ENV, str(tmp_path / "mine"))
    assert skill.templates_root(REPO / "cookbook") == tmp_path / "mine"


def test_compile_renders_with_the_cookbooks_templates(book, tmp_path, monkeypatch, capsys):
    mine = tmp_path / "mine"
    shutil.copytree(skill.PACKAGED_TEMPLATES, mine)
    t = mine / "skill" / "principle.md"
    t.write_text(t.read_text().replace("{{body}}", "Edited template.\n\n{{body}}"))
    monkeypatch.setenv(skill.TEMPLATES_ENV, str(mine))
    monkeypatch.chdir(tmp_path)
    assert main(["compile", "--target", "skill", str(book), "--out", "out"]) == 0
    assert "Edited template." in (tmp_path / "out" / "principle-simplicity" / "SKILL.md").read_text()


def test_routes_in_artifact_json_override_and_survive_a_doc_edit(tmp_path):
    folder = make(tmp_path / "cookbook", "guidelines/testing/flaky", "guideline", routes=["testing/flaky"])
    assert skill.compose(folder).routes == ("testing/flaky",)
    assert '"routes": ["testing/flaky"]' in dump_manifest(load_folder(folder))
    save_document(folder.parent / "flaky.md", "---\nid: x\ntype: guideline\n---\n# T\n\nEdited.\n")
    assert load_folder(folder).routes == ["testing/flaky"]


def test_the_template_keeps_requirements_drops_history_and_refers_rationale(book):
    s = skill.compose(book / "guidelines/implementing/data/use-wal")
    assert "## Rules\n- MUST do it." in s.text
    assert "Why this matters" not in s.text and "Change History" not in s.text
    assert s.text.endswith("_From `book.guideline.implementing.data.use-wal` v1.2.0._\n")


def test_referred_sections_move_to_a_linked_file_named_with_when_to_read_it(book):
    s = skill.compose(book / "guidelines/implementing/data/use-wal")
    assert ("## More\n\nRead one of these only when its line applies to what you are doing:\n\n"
            "- [Rationale](references/rationale.md): why this guideline exists; read when you need "
            "to justify it or weigh an exception.\n\n_From ") in s.text
    assert s.references == {"rationale.md": (
        "# T: Rationale\n\nPart of the `implementing-data-use-wal` skill, from "
        "`book.guideline.implementing.data.use-wal` v1.2.0.\n\n## Why this matters\nBecause.\n")}


def test_a_skill_with_nothing_to_refer_has_no_more_section_and_no_references(book):
    s = skill.compose(book / "principles/simplicity")
    assert "## More" not in s.text and s.references == {}


def test_a_section_referred_to_two_files_is_a_template_error(tmp_path):
    (tmp_path / "principle.md").write_text(
        "---\nrefer:\n  - {file: a, title: A, when: w, sections: [X]}\n"
        "  - {file: b, title: B, when: w, sections: [X]}\n---\n{{body}}\n")
    with pytest.raises(skill.SkillError, match="more than one file"):
        skill.template("principle", tmp_path)
    (tmp_path / "recipe.md").write_text("---\nrefer:\n  - {file: a, title: A}\n---\n{{body}}\n")
    with pytest.raises(skill.SkillError, match="needs file, title, when and sections"):
        skill.template("recipe", tmp_path)


def test_skill_metadata_source_is_rdid(book):
    s = skill.compose(book / "guidelines/implementing/data/use-wal")
    fm, _ = tuning.split(s.text)
    import yaml
    assert yaml.safe_load("".join(fm))["metadata"]["source"] == "book.guideline.implementing.data.use-wal"


def test_outside_a_cookbook_the_folder_path_names_the_skill(tmp_path):
    folder = make(tmp_path / "loose", "principles/simplicity", "principle")
    text = skill.compose(folder).text
    assert text.endswith("_From `principles/simplicity` v1.2.0._\n")


def _uid(rel):
    return str(uuid.uuid5(uuid.UUID(BOOK_ID), rel))


def test_the_body_renders_implementations_dependencies_and_link_labels_from_the_index(book):
    from cookr.core.index import Conformance, Implementation, current_index, save_index
    simplicity = _uid("principles/simplicity")
    badge = book / "ingredients/ui/components/badge"
    manifest_path = badge / "artifact.json"
    data = json.loads(manifest_path.read_text())
    data["meta"]["depends-on"] = [simplicity, "f0000000-0000-4000-8000-000000000000/" + simplicity]
    manifest_path.write_text(json.dumps(data))
    (badge / "intro.md").write_text(f"# T\n\nSee [stale-label](cookbook:{simplicity}).\n\n")
    index = current_index(book)
    index.entries[_uid("ingredients/ui/components/badge")].implementations = [
        Implementation("macos", "Sources/Badge.swift", Conformance("confirmed", "1.2.0")),
        Implementation("ios", None, Conformance("planned")),
    ]
    save_index(index, book)
    text = skill.compose(badge).text
    assert ("## Reference Implementations\n\n| Platform | Location | Conformance |\n"
            "|----------|----------|-------------|\n"
            "| macos | `Sources/Badge.swift` | confirmed (1.2.0) |\n"
            "| ios | (planned) | planned |\n") in text
    assert f"See [book.principle.simplicity](cookbook:{simplicity})." in text
    assert ("Depends on: `book.principle.simplicity`, "
            f"`f0000000-0000-4000-8000-000000000000/{simplicity}`.") in text
    assert "_From `book.ingredient.ui.components.badge` v1.2.0._" in text


def test_a_spec_with_no_implementations_has_no_reference_implementations_section(book):
    text = skill.compose(book / "ingredients/ui/components/badge").text
    assert "Reference Implementations" not in text


def test_frontmatter_keeps_cookr_keys_under_metadata_and_loads_everywhere(book):
    s = skill.compose(book / "guidelines/implementing/data/use-wal")
    fm, _ = tuning.split(s.text)
    import yaml
    data = yaml.safe_load("".join(fm))
    assert set(data) == {"name", "description", "metadata"}
    assert data["metadata"]["routes"] == "; ".join(s.routes)
    assert data["description"] == "Does the thing. Use when: database-operations."
    for h in hosts.manifest().values():
        assert tuning.load_problems(s.text, h) == []


def test_platforms_go_under_metadata_only_when_the_artifact_names_some(book):
    import yaml
    badge = skill.compose(book / "ingredients/ui/components/badge")
    data = yaml.safe_load("".join(tuning.split(badge.text)[0]))
    assert data["metadata"]["platforms"] == "macos, ios"
    for h in hosts.manifest().values():
        assert tuning.load_problems(badge.text, h) == []
    wal = skill.compose(book / "guidelines/implementing/data/use-wal")
    assert "platforms" not in yaml.safe_load("".join(tuning.split(wal.text)[0]))["metadata"]


def test_bold_markers_leave_the_description():
    a = Artifact(meta={"summary": "**Never trust input.** Validate __everything__ on the server."})
    assert skill.description(a) == "Never trust input. Validate everything on the server."


def test_angle_brackets_leave_the_description():
    a = Artifact(meta={"summary": 'Keep LCP <= 2.5s and use <Nullable> "on".'})
    assert skill.description(a) == 'Keep LCP ≤ 2.5s and use ‹Nullable› "on".'


def test_variants_exist_only_where_additions_change_the_text(book, tmp_path):
    bare = tmp_path / "templates"   # the shipped templates without their own additions
    shutil.copytree(skill.TEMPLATES, bare, ignore=shutil.ignore_patterns("hosts"))
    s = skill.compose(book / "guidelines/implementing/data/use-wal", templates=bare)
    assert skill.variants(s, bare) == ({}, [])
    d = s.folder / "hosts"
    d.mkdir()
    (d / "claude.add.md").write_text("Host.\n")
    (d / "claude.opus-5-5.add.md").write_text("Version.\n")
    vs, problems = skill.variants(s, bare)
    assert problems == [] and set(vs) == {"claude", "claude.opus-5-5"}
    assert vs["claude.opus-5-5"].endswith("Host.\n\nVersion.\n")


def test_template_level_additions_apply_before_the_artifacts_own(book, tmp_path):
    templates = tmp_path / "templates"
    for t in ("guideline",):
        (templates / t / "hosts").mkdir(parents=True)
        (templates / f"{t}.md").write_text((skill.TEMPLATES / f"{t}.md").read_text())
    (templates / "guideline" / "hosts" / "codex.add.md").write_text("Template.\n")
    s = skill.compose(book / "guidelines/implementing/data/use-wal", templates=templates)
    (s.folder / "hosts").mkdir()
    (s.folder / "hosts" / "codex.add.md").write_text("Own.\n")
    vs, _ = skill.variants(s, templates)
    assert vs["codex"].endswith("Template.\n\nOwn.\n")


def test_a_variant_that_breaks_its_host_is_a_problem(book):
    s = skill.compose(book / "principles/simplicity")
    (s.folder / "hosts").mkdir()
    (s.folder / "hosts" / "codex.add.yaml").write_text("model: gpt-5\n")
    _, problems = skill.variants(s)
    assert problems and problems[0].startswith("codex: ")


def test_fanout_counts_children_and_skills_at_each_node():
    fo = skill.fanout([("a", ["x/y", "x/z"]), ("b", ["x/y"]), ("c", ["x"])])
    assert fo == {"": 1, "x": 3, "x/y": 2, "x/z": 1}
    assert skill.over_cap([("a", ["x/y"]), ("b", ["x/y"])], cap=1) == {"x/y": 2}


def test_compile_set_writes_checks_and_prunes(book, tmp_path):
    out = tmp_path / "out"
    rep = skill.compile_set(find_folders([book]), out)
    assert not rep.failed and {r.status for r in rep.results} == {"compiled"}
    assert (out / "principle-simplicity" / "SKILL.md").is_file()
    assert json.loads((out / "targets.json").read_text())["hosts"]["claude"]["model_prefix"] == "claude-"
    receipt = json.loads((out / "skills.json").read_text())["skills"]
    assert set(receipt) == {"implementing-data-use-wal", "principle-simplicity", "ui-components-badge"}
    assert not skill.compile_set(find_folders([book]), out, write=False).failed

    (out / "mine.txt").write_text("not cookr's")
    import shutil
    shutil.rmtree(book / "principles")
    rep = skill.compile_set(find_folders([book]), out, write=False)
    assert rep.failed and rep.removed == ["principle-simplicity (would remove)"]
    rep = skill.compile_set(find_folders([book]), out)
    assert not (out / "principle-simplicity").exists() and (out / "mine.txt").exists()
    assert rep.removed == ["principle-simplicity/SKILL.md"]


def test_references_are_written_and_pruned_with_their_section(book, tmp_path):
    out = tmp_path / "out"
    skill.compile_set(find_folders([book]), out)
    ref = out / "implementing-data-use-wal" / "references" / "rationale.md"
    assert ref.is_file()
    receipt = json.loads((out / "skills.json").read_text())["skills"]["implementing-data-use-wal"]
    assert "implementing-data-use-wal/references/rationale.md" in receipt["files"]
    folder = book / "guidelines/implementing/data/use-wal"
    a = load_folder(folder)
    write_folder(Artifact(meta=a.meta, routes=a.routes,
                          parts=[pt for pt in a.parts if pt.heading != "Why this matters"]), folder)
    assert skill.compile_set(find_folders([book]), out, write=False).failed
    skill.compile_set(find_folders([book]), out)
    assert not ref.parent.exists()
    assert "## More" not in (out / "implementing-data-use-wal" / "SKILL.md").read_text()


def test_a_variant_no_longer_needed_is_removed(book, tmp_path):
    out = tmp_path / "out"
    folder = book / "principles/simplicity"
    (folder / "hosts").mkdir()
    (folder / "hosts" / "claude.add.md").write_text("Claude only.\n")
    skill.compile_set(find_folders([book]), out)
    assert (out / "principle-simplicity" / "targets" / "claude.SKILL.md").is_file()
    (folder / "hosts" / "claude.add.md").unlink()
    assert skill.compile_set(find_folders([book]), out, write=False).failed
    skill.compile_set(find_folders([book]), out)
    assert not (out / "principle-simplicity" / "targets").exists()


def test_duplicate_names_and_broken_renderings_fail_the_set(book, tmp_path):
    make(book, "guidelines/implementing-data/use-wal", "guideline")  # same derived name
    (book / "principles/simplicity/hosts").mkdir()
    (book / "principles/simplicity/hosts/codex.add.yaml").write_text("model: x\n")
    rep = skill.compile_set(find_folders([book]), tmp_path / "out")
    assert rep.failed
    assert sorted(r.status for r in rep.results if r.failed) == ["broken", "error", "error"]


def test_the_cli_needs_out_and_reports_json(book, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["compile", "--target", "skill", str(book)]) == 2
    capsys.readouterr()
    assert main(["compile", "--target", "skill", str(book), "--out", "out", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["over_cap"] == {} and len(data["results"]) == 3


def test_a_doc_with_no_source_folder_fails_compile(book, tmp_path, monkeypatch, capsys):
    (book / "principles" / "loose.md").write_text("---\ntype: principle\n---\n# Loose\n")
    (book / "principles" / "notes.md").write_text("# Not an artifact\n")
    monkeypatch.chdir(tmp_path)
    assert main(["compile", "--check", str(book)]) == 1
    out = capsys.readouterr().out
    assert "loose.md" in out and "notes.md" not in out
    assert main(["compile", "--target", "skill", str(book), "--out", "out", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["unconverted"] == [str(book / "principles" / "loose.md")]


def test_the_whole_cookbook_compiles_within_the_fanout_cap(tmp_path, repo_v2):
    """The plan's P5 gate: every artifact becomes a skill that loads on every
    host, names are unique, and no route node is over the cap."""
    folders = find_folders([repo_v2 / "cookbook"])
    rep = skill.compile_set(folders, tmp_path / "out")
    assert [r.as_json() for r in rep.results if r.failed] == []
    assert rep.over_cap == {}
    assert len(rep.results) == sum(4 if load_folder(f).roled else 1 for f in folders)
    assert unconverted([REPO / "cookbook"]) == []


# ── a roled artifact: a builder, a reviewer and their two verifiers ──────────

ROLED = "guidelines/implementing/data/t"


def make_roled(root: Path, rel: str = ROLED, *, drop=(), triggers=None, summary="Does the thing.",
               routes=None, type_: str = "guideline") -> Path:
    """A roled artifact (a guideline unless `type_` says) with a part for
    every role, less the roles in `drop`."""
    folder = root / rel
    meta = {"id": str(uuid.uuid5(uuid.UUID(BOOK_ID), rel)), "title": "T", "type": type_,
            "version": "1.2.0", "summary": summary}
    if triggers is not None:
        meta["triggers"] = triggers
    parts = [
        Part("rules", "- **must-do-it**: Code MUST do it.\n\n", "Rules", "rules"),
        Part("how-to", "How to do it.\n\n", "How to", "how-to"),
        Part("examples", "An example.\n\n", "Examples", "examples"),
        Part("review-focus", "Look for the thing.\n\n", "Review focus", "review-focus"),
        Part("build-bar", "- `must-do-it`: it is done.\n\n", "Build bar", "build-bar"),
        Part("review-bar", "- The review names it.\n\n", "Review bar", "review-bar"),
        Part("rationale", "Because.\n\n", "Why this matters", "rationale"),
        Part("references", "- A source.\n\n", "References", "references"),
    ]
    write_folder(Artifact(meta=meta, routes=routes, parts=[Part("intro", "# T\n\nGuidance.\n\n")]
                          + [p for p in parts if p.role not in drop]
                          + [Part("history", "| Version | Date | Author | Summary |\n", "Change History")]),
                 folder)
    return folder


@pytest.fixture
def roled(book):
    folder = make_roled(book, triggers=["database-operations"])
    index_folders(book)
    return folder


def _fm(text):
    import yaml
    return yaml.safe_load("".join(tuning.split(text)[0]))


def test_a_roled_artifact_compiles_to_four_skills(roled):
    names = {s.name: s for s in skill.compose_all(roled)}
    assert set(names) == {"implementing-data-t", "verifying-build-data-t",
                          "reviewing-data-t", "verifying-review-data-t"}
    assert "How to" in names["implementing-data-t"].text and "Look for" not in names["implementing-data-t"].text
    assert "Look for" in names["reviewing-data-t"].text and "How to" not in names["reviewing-data-t"].text
    assert "**must-do-it**" in names["implementing-data-t"].text and "**must-do-it**" in names["reviewing-data-t"].text
    assert "**must-do-it**" not in names["verifying-review-data-t"].text
    assert names["verifying-review-data-t"].kind == "review-verifier"
    assert [s.kind for s in names.values()] == ["builder", "build-verifier", "reviewer", "review-verifier"]
    for s in names.values():
        assert s.text.split("---\n", 2)[2].startswith("# T\n\nGuidance.\n")    # the intro opens each
        assert "Change History" not in s.text


def test_the_verifiers_end_their_bar_with_the_line_they_grade_by(roled):
    by = {s.kind: s for s in skill.compose_all(roled)}
    assert ("## Build bar\n- `must-do-it`: it is done.\n\nA build passes when every item above holds.\n\n## More"
            in by["build-verifier"].text)
    assert ("## Review bar\n- The review names it.\n\nA review passes when it establishes every item "
            "above.\n\n## More" in by["review-verifier"].text)
    assert "passes when" not in by["builder"].text + by["reviewer"].text


def test_each_of_the_four_names_its_source_and_kind(roled):
    fms = [_fm(s.text) for s in skill.compose_all(roled)]
    assert {f["metadata"]["source"] for f in fms} == {"book.guideline.implementing.data.t"}
    assert [f["metadata"]["skill"] for f in fms] == ["builder", "build-verifier", "reviewer", "review-verifier"]
    assert [f["name"] for f in fms] == ["implementing-data-t", "verifying-build-data-t",
                                        "reviewing-data-t", "verifying-review-data-t"]
    for s in skill.compose_all(roled):
        for h in hosts.manifest().values():
            assert tuning.load_problems(s.text, h) == []


def test_the_four_route_by_their_use_case_with_the_same_tail(roled):
    routes = {s.kind: s.routes for s in skill.compose_all(roled)}
    assert routes == {
        "builder": ("coding/implementing/data", "coding/when/database-operations/implementing/data"),
        "build-verifier": ("coding/verifying-build/data",
                           "coding/when/database-operations/verifying-build/data"),
        "reviewer": ("coding/reviewing/data", "coding/when/database-operations/reviewing/data"),
        "review-verifier": ("coding/verifying-review/data",
                            "coding/when/database-operations/verifying-review/data"),
    }


def test_rationale_is_linked_never_inlined(roled):
    for s in skill.compose_all(roled):
        assert "Because." not in s.text and "A source." not in s.text
        assert set(s.references) == {"rationale.md", "references.md"}
        assert "Because." in s.references["rationale.md"]
        assert "A source." in s.references["references.md"]
        assert f"Part of the `{s.name}` skill" in s.references["rationale.md"]
        assert "- [Rationale](references/rationale.md): " in s.text
        assert "- [References](references/references.md): " in s.text


def test_an_unroled_artifact_still_compiles_to_its_one_skill_unchanged(book):
    for rel in ("guidelines/implementing/data/use-wal", "principles/simplicity",
                "ingredients/ui/components/badge"):
        [only] = skill.compose_all(book / rel)
        assert only == skill.compose(book / rel)
        assert only.kind == "" and "skill:" not in only.text


def test_a_roled_artifact_missing_a_role_is_refused_by_name(book):
    folder = make_roled(book, drop=("build-bar",))
    with pytest.raises(skill.SkillError, match="missing-role.*build-verifier"):
        skill.compose_all(folder)


@pytest.mark.parametrize("part", ["review-focus", "rationale"])
def test_a_roled_part_headed_like_an_omitted_section_is_refused_by_name(roled, part):
    meta = json.loads((roled / "artifact.json").read_text())
    for p in meta["parts"]:
        if p["part"] == part:
            p["heading"] = "Change History"
    (roled / "artifact.json").write_text(json.dumps(meta, indent=2))
    with pytest.raises(skill.SkillError, match=f"part '{part}' .*'Change History'"):
        skill.compose_all(roled)


def test_a_blank_review_bar_is_refused_by_name(book):
    folder = make_roled(book)
    (folder / "review-bar.md").write_text("\n", encoding="utf-8")
    with pytest.raises(skill.SkillError, match=r"data/t: .*empty-part: part 'review-bar' with role "
                                               r"'review-bar' has no text, so no review-verifier skill"):
        skill.compose_all(folder)


@pytest.mark.parametrize("prose", ["These rules may be applied in any order.",
                                   "> Note: you should read the how-to."])
def test_lower_case_words_in_rules_prose_compile(book, prose):
    folder = make_roled(book)
    (folder / "rules.md").write_text(f"{prose}\n\n- **must-do-it**: Code MUST do it.\n\n", encoding="utf-8")
    assert prose in {s.kind: s for s in skill.compose_all(folder)}["builder"].text


def test_an_upper_case_requirement_in_rules_prose_is_refused(book):
    folder = make_roled(book)
    (folder / "rules.md").write_text("Code MUST x.\n\n- **must-do-it**: Code MUST do it.\n\n", encoding="utf-8")
    with pytest.raises(skill.SkillError, match=r"unnamed-rule: part 'rules': 'Code MUST x\.'"):
        skill.compose_all(folder)


def test_a_tuned_roled_artifact_is_refused(roled):
    (roled / "hosts").mkdir()
    (roled / "hosts" / "claude.add.md").write_text("Host.\n")
    with pytest.raises(skill.SkillError, match="tuned"):
        skill.compose_all(roled)


def test_a_roled_planning_topic_compiles_four_skills_named_by_its_tail(book):
    folder = make_roled(book, "guidelines/planning/data/t", triggers=["database-operations"])
    by = {s.kind: s for s in skill.compose_all(folder)}
    assert {k: s.name for k, s in by.items()} == {
        "builder": "planning-data-t", "build-verifier": "verifying-build-data-t",
        "reviewer": "reviewing-data-t", "review-verifier": "verifying-review-data-t"}
    assert by["builder"].name == skill.skill_name("guidelines", ("planning", "data", "t"))
    assert by["builder"].routes == ("coding/planning/data", "coding/when/database-operations/planning/data")
    assert by["reviewer"].routes == ("coding/reviewing/data", "coding/when/database-operations/reviewing/data")
    assert "How to" in by["builder"].text and "Look for" in by["reviewer"].text


def test_a_roled_principle_compiles_four_skills(book):
    folder = make_roled(book, "principles/t", type_="principle")
    by = {s.kind: s for s in skill.compose_all(folder)}
    assert {k: s.name for k, s in by.items()} == {
        "builder": "principle-t", "build-verifier": "verifying-build-principle-t",
        "reviewer": "reviewing-principle-t", "review-verifier": "verifying-review-principle-t"}
    assert all(s.routes == ("principles",) for s in by.values())
    assert "How to" in by["builder"].text and "Look for" in by["reviewer"].text


def test_a_roled_guideline_under_reviewing_is_refused(tmp_path):
    root = tmp_path / "cookbook"
    manifest(root)
    folder = make_roled(root, "guidelines/reviewing/data/t")
    with pytest.raises(skill.SkillError, match="reviewing-folder: it lives under guidelines/reviewing/"):
        skill.compose_all(folder)


def test_a_roled_ingredient_is_refused(tmp_path):
    root = tmp_path / "cookbook"
    manifest(root)
    folder = make_roled(root, "ingredients/ui/t", type_="ingredient")
    with pytest.raises(skill.SkillError, match="unroled-type: an ingredient is never roled"):
        skill.compose_all(folder)


def test_two_roled_topics_whose_cut_names_collide_are_refused_naming_both(tmp_path):
    root = tmp_path / "cookbook"
    manifest(root)
    tail = "code-quality/no-external-dependencies-in-core-libraries-ever"
    a = make_roled(root, f"guidelines/implementing/{tail}")
    b = make_roled(root, f"guidelines/planning/{tail}")
    rep = skill.compile_set([a, b], tmp_path / "out")
    assert rep.failed
    errors = [r for r in rep.results if r.failed]
    shared = {s.name for s in skill.compose_all(a)} & {s.name for s in skill.compose_all(b)}
    assert len(shared) == 3 and all(len(n) <= skill.NAME_MAX for n in shared)
    assert len("reviewing-" + tail.replace("/", "-")) > skill.NAME_MAX   # so each name is cut
    assert len(errors) == 6 and {r.status for r in errors} == {"error"}
    for mine, other in ((a, b), (b, a)):
        assert sum(1 for r in errors if r.source == mine and str(other) in r.detail) == 3


def test_a_roled_artifact_has_no_variants(roled):
    for s in skill.compose_all(roled):
        assert skill.variants(s) == ({}, [])          # not even the guideline template's own
    [plain] = skill.compose_all(roled.parent / "use-wal")
    assert set(skill.variants(plain)[0]) == {"claude"}


def test_the_set_receipt_records_all_four_and_prunes_them_together(roled, book, tmp_path):
    out = tmp_path / "out"
    rep = skill.compile_set(find_folders([book]), out)
    assert not rep.failed
    receipt = json.loads((out / "skills.json").read_text())["skills"]
    four = {"implementing-data-t": "builder", "verifying-build-data-t": "build-verifier",
            "reviewing-data-t": "reviewer", "verifying-review-data-t": "review-verifier"}
    for name, kind in four.items():
        assert receipt[name]["kind"] == kind and receipt[name]["source"] == str(roled)
        assert f"{name}/references/rationale.md" in receipt[name]["files"]
        assert (out / name / "SKILL.md").is_file()
    assert "kind" not in receipt["implementing-data-use-wal"]
    shutil.rmtree(roled)
    rep = skill.compile_set(find_folders([book]), out)
    assert not any((out / name).exists() for name in four)
    assert set(json.loads((out / "skills.json").read_text())["skills"]) == {
        "implementing-data-use-wal", "principle-simplicity", "ui-components-badge"}


def test_four_long_names_stay_distinct_within_the_limit(tmp_path):
    root = tmp_path / "cookbook"
    manifest(root)
    long = "guidelines/implementing/code-quality/no-external-dependencies-in-core-libraries-ever"
    names = [s.name for s in skill.compose_all(make_roled(root, long))]
    assert len(names) == 4 and len(set(names)) == 4
    assert all(len(n) <= skill.NAME_MAX for n in names)
    assert names[0] == skill.skill_name("guidelines", tuple(long.split("/")[1:]))


def test_each_of_the_four_has_its_own_description_and_the_builder_keeps_todays(roled):
    by = {s.kind: _fm(s.text)["description"] for s in skill.compose_all(roled)}
    assert by["builder"] == skill.description(load_folder(roled)) == "Does the thing. Use when: database-operations."
    assert len(set(by.values())) == 4
    assert by["reviewer"].startswith("Review code against")
    assert by["build-verifier"].startswith("Check that a build meets")
    assert by["review-verifier"].startswith("Check that a review")
    assert all(v.endswith("Does the thing. Use when: database-operations.") for v in by.values())


def test_a_long_description_stays_within_the_limit_on_all_four(book):
    folder = make_roled(book, summary="Word " * 300)
    for s in skill.compose_all(folder):
        d = _fm(s.text)["description"]
        assert len(d) <= skill.DESCRIPTION_MAX and d.endswith("…")


def test_a_roled_artifact_with_its_own_routes_is_refused(book):
    folder = make_roled(book, routes=["coding/data"])
    with pytest.raises(skill.SkillError, match="routed"):
        skill.compose_all(folder)


def test_only_the_builder_shows_the_reference_implementations(roled, book):
    from cookr.core.index import Conformance, Implementation, current_index, save_index
    index = current_index(book)
    index.entries[_uid(ROLED)].implementations = [
        Implementation("macos", "Sources/T.swift", Conformance("confirmed", "1.2.0"))]
    save_index(index, book)
    by = {s.kind: s for s in skill.compose_all(roled)}
    assert "## Reference Implementations\n\n| Platform | Location | Conformance |" in by["builder"].text
    assert "| macos | `Sources/T.swift` | confirmed (1.2.0) |" in by["builder"].text
    assert all("Reference Implementations" not in by[k].text
               for k in ("build-verifier", "reviewer", "review-verifier"))


def test_the_cli_counts_each_skill_of_a_set_with_a_roled_artifact(tmp_path, monkeypatch, capsys):
    root = tmp_path / "cookbook"
    manifest(root)
    make_roled(root)
    make(root, "principles/simplicity", "principle")
    index_folders(root)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("COLUMNS", "300")
    assert main(["compile", "--target", "skill", str(root), "--out", "out", "--json"]) == 0
    results = json.loads(capsys.readouterr().out)["results"]
    assert sorted(Path(r["dest"]).name for r in results) == [
        "implementing-data-t", "principle-simplicity", "reviewing-data-t",
        "verifying-build-data-t", "verifying-review-data-t"]
    assert main(["compile", "--target", "skill", str(root), "--out", "out2"]) == 0
    assert "5 of 5 compiled" in capsys.readouterr().out


# ── NEEDS REVIEW markers: the builder is told to settle them (main 0.14.0) ──

def _recipe_with(tmp_path, rules: str, platforms_note: str = "- **macos**: Built.\n\n"):
    root = tmp_path / "cookbook"
    manifest(root)
    folder = root / "recipes/ui/menu"
    write_folder(Artifact(meta={"id": str(uuid.uuid5(uuid.UUID(BOOK_ID), "menu")), "title": "Menu",
                                "type": "recipe", "version": "1.0.0", "summary": "A menu."}, parts=[
        Part("intro", "# Menu\n\nThe menu.\n\n"),
        Part("rules", rules, "Behavioral Requirements"),
        Part("platform-notes", platforms_note, "Platform Notes"),
        Part("history", "| 1.0.0 | removed a NEEDS REVIEW marker |\n\n", "Change History"),
    ]), folder)
    index_folders(root)
    return folder


def test_a_recipe_with_open_markers_tells_the_builder_to_stop_and_settle_them(tmp_path):
    folder = _recipe_with(tmp_path, "- **delete**: NEEDS REVIEW: Not implemented in source. "
                                    "Is Option-only delete wanted?\n\n")
    text = skill.compose(folder).text
    body = text.split("---\n", 2)[2]
    assert body.index("# Menu") < body.index(skill.OPEN_QUESTIONS_HEADING) < body.index("## Behavioral Requirements")
    notice = body.split(skill.OPEN_QUESTIONS_HEADING, 1)[1].split("\n## ", 1)[0]
    assert "stop" in notice and "ask the user" in notice and "cookr bump" in notice


def test_a_marker_only_in_a_referred_section_still_raises_the_notice(tmp_path):
    folder = _recipe_with(tmp_path, "- **open**: MUST open.\n\n",
                          "- **ios**: NEEDS REVIEW: Not implemented in source. Which gesture?\n\n")
    text = skill.compose(folder).text
    assert skill.OPEN_QUESTIONS_HEADING in text
    assert "references/" in text.split(skill.OPEN_QUESTIONS_HEADING, 1)[1].split("\n## ", 1)[0]


def test_a_settled_recipe_carries_no_notice_even_when_its_history_mentions_markers(tmp_path):
    folder = _recipe_with(tmp_path, "- **open**: MUST open.\n\n")
    assert skill.OPEN_QUESTIONS_HEADING not in skill.compose(folder).text


def test_only_the_builder_of_a_roled_artifact_carries_the_open_questions_notice(book):
    # 0.22.0: the notice tells whoever builds to settle the markers first; the reviewer and the two verifiers
    # do not build from the artifact, so theirs carry none.
    folder = make_roled(book)
    (folder / "how-to.md").write_text("NEEDS REVIEW: Which order?\n\n", encoding="utf-8")
    by = {s.kind: s for s in skill.compose_all(folder)}
    assert skill.OPEN_QUESTIONS_HEADING in by["builder"].text
    for kind in ("build-verifier", "reviewer", "review-verifier"):
        assert skill.OPEN_QUESTIONS_HEADING not in by[kind].text, kind
