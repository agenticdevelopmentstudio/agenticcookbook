"""The `skill` target: names, routes, templates, variants, the compiled set."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import hosts, skill, tuning
from cookr.core.artifact import Artifact, Part, dump_manifest, find_folders, load_folder, save_document, unconverted, write_folder

REPO = Path(__file__).resolve().parents[5]


def make(root: Path, rel: str, type_: str, *, triggers=None, platforms=None, routes=None,
         summary="Does the thing.", body="Guidance.\n"):
    folder = root / rel
    meta = {"id": "00000000-0000-0000-0000-000000000000", "title": "T", "type": type_,
            "domain": f"agenticdevelopercookbook://{rel}", "version": "1.2.0", "summary": summary}
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


@pytest.fixture
def book(tmp_path):
    root = tmp_path / "cookbook"
    make(root, "guidelines/implementing/data/use-wal", "guideline", triggers=["database-operations"])
    make(root, "principles/simplicity", "principle")
    make(root, "ingredients/ui/components/badge", "ingredient", platforms=["macos", "ios"])
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
                  body="Write `{{version}}` and `{{domain}}` in a template.\n")
    text = skill.compose(folder).text
    assert "Write `{{version}}` and `{{domain}}` in a template." in text
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


def test_the_template_omits_rationale_and_history_and_keeps_requirements(book):
    text = skill.compose(book / "guidelines/implementing/data/use-wal").text
    assert "## Rules\n- MUST do it." in text
    assert "Why this matters" not in text and "Change History" not in text
    assert text.endswith("_From `agenticdevelopercookbook://guidelines/implementing/data/use-wal` v1.2.0._\n")


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


def test_the_whole_cookbook_compiles_within_the_fanout_cap(tmp_path):
    """The plan's P5 gate: every artifact becomes a skill that loads on every
    host, names are unique, and no route node is over the cap."""
    rep = skill.compile_set(find_folders([REPO / "cookbook"]), tmp_path / "out")
    assert [r.as_json() for r in rep.results if r.failed] == []
    assert rep.over_cap == {}
    assert len(rep.results) == len(find_folders([REPO / "cookbook"]))
    assert unconverted([REPO / "cookbook"]) == []
