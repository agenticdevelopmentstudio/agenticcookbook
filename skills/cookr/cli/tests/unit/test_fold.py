"""`cookr fold <copy> --into <topic>` (modules/fold.py, core/rolework.py)."""

from __future__ import annotations

import json

import pytest

from cookr.cli import main
from cookr.core.artifact import Artifact, Part, load_folder, split_body, write_folder

pytestmark = pytest.mark.usefixtures("git_tmp_path")

TOPIC_ID = "6f1c1e2a-0000-4000-8000-000000000001"
COPY_ID = "6f1c1e2a-0000-4000-8000-000000000002"
OTHER_ID = "6f1c1e2a-0000-4000-8000-000000000003"
HISTORY = ("\n| Version | Date | Author | Summary |\n|---------|------|--------|---------|\n"
           "| 1.0.0 | 2026-01-01 | A | first |\n")
RULES = "\n- **must-index-foreign-keys**: Every foreign key MUST have an index.\n\n"
BAR = "\n- `must-index-foreign-keys`: every foreign key is indexed.\n\n"


def _meta(uid, **extra):
    m = {"id": uid, "title": "T", "type": "guideline", "version": "1.0.0", "modified": "2026-01-01"}
    m.update(extra)
    return m


def _topic(cb):
    folder = cb / "guidelines/implementing/data/t"
    write_folder(Artifact(meta=_meta(TOPIC_ID, related=[COPY_ID]), parts=[
        Part("intro", "# T\n\nIndexes keep reads fast.\n\n"),
        Part("rules", RULES, "Rules", "rules"),
        Part("covering", "\nA covering index holds every column.\n\n", "Covering Indexes", "how-to"),
        Part("focus", "\nLook at the joins.\n\n", "Review focus", "review-focus"),
        Part("review-bar", "\nFlag an unindexed key.\n\n", "Review bar", "review-bar"),
        Part("build-bar", BAR, "Build bar", "build-bar"),
        Part("history", HISTORY, "Change History"),
    ]), folder)
    return folder


def _copy(cb, extra="", meta=None):
    folder = cb / "guidelines/planning/data/t"
    body = ("# T\n\nIndexes keep reads fast.\n\n## Covering Indexes\n\n"
            "A covering index holds every column.\n\n" + extra + "## Change History\n" + HISTORY)
    write_folder(Artifact(meta=meta or _meta(COPY_ID, related=[TOPIC_ID]), parts=split_body(body)),
                 folder)
    return folder


def _linker(cb, rel, type_="recipe", uid=OTHER_ID):
    folder = cb / rel
    body = (f"# L\n\nSee [adc.guideline.planning.data.t](cookbook:{COPY_ID}).\n\n"
            "## Change History\n" + HISTORY)
    write_folder(Artifact(meta=_meta(uid, type=type_, related=[COPY_ID, TOPIC_ID], **{"depends-on": [COPY_ID]}),
                          parts=split_body(body)), folder)
    return folder


def _fold(copy, topic, capsys):
    capsys.readouterr()
    code = main(["fold", str(copy), "--into", str(topic), "--author", "Tester", "--date", "2026-11-16"])
    return code, (json.loads(capsys.readouterr().out) if code == 0 else None)


def test_fold_of_an_identical_copy_adds_no_part_and_redirects_links(tmp_path, capsys):
    cb = tmp_path / "cookbook"
    topic, copy = _topic(cb), _copy(cb)
    linker = _linker(cb, "recipes/l")
    code, out = _fold(copy, topic, capsys)
    assert code == 0
    assert out["identical"] is True and out["parts_added"] == []
    assert not copy.exists()
    assert out["redirected"] == ["cookbook/recipes/l"]
    art = load_folder(linker)
    assert art.meta["related"] == [TOPIC_ID] and art.meta["depends-on"] == [TOPIC_ID]
    assert f"(cookbook:{TOPIC_ID})" in art.part("intro").text
    assert COPY_ID not in art.part("intro").text
    folded = load_folder(topic)
    assert folded.meta["related"] == []  # its link to the copy would be a link to itself
    assert [p.name for p in folded.parts] == ["intro", "rules", "covering", "focus", "review-bar",
                                              "build-bar", "history"]
    assert "guidelines/planning/data/t" in folded.part("history").text
    assert folded.meta["version"] == "1.0.1"


def test_fold_of_a_differing_copy_adds_its_extra_text_as_an_unroled_part(tmp_path, capsys):
    cb = tmp_path / "cookbook"
    topic = _topic(cb)
    copy = _copy(cb, extra="## Planning Notes\n\nPlan the indexes before the tables.\n\n")
    code, out = _fold(copy, topic, capsys)
    assert code == 0
    assert out["identical"] is False and out["parts_added"] == ["planning-notes"]
    art = load_folder(topic)
    added = art.part("planning-notes")
    assert added.role is None and added.heading == "Planning Notes"
    assert "Plan the indexes before the tables." in added.text
    assert art.parts[-1].name == "history"
    capsys.readouterr()
    assert main(["roles", "check", str(topic)]) == 1
    findings = json.loads(capsys.readouterr().out)["findings"]
    assert {"kind": "unroled-part", "detail": "part 'planning-notes' has no role"} in findings


def test_fold_redirects_links_from_ingredients_recipes_and_principles(tmp_path, capsys):
    cb = tmp_path / "cookbook"
    topic, copy = _topic(cb), _copy(cb)
    linkers = [_linker(cb, "recipes/l", "recipe"), _linker(cb, "ingredients/i", "ingredient", OTHER_ID[:-1] + "4"),
               _linker(cb, "principles/p", "principle", OTHER_ID[:-1] + "5")]
    code, out = _fold(copy, topic, capsys)
    assert code == 0
    assert sorted(out["redirected"]) == ["cookbook/ingredients/i", "cookbook/principles/p",
                                         "cookbook/recipes/l"]
    for folder in linkers:
        art = load_folder(folder)
        assert COPY_ID not in json.dumps(art.meta) and COPY_ID not in art.part("intro").text
        assert art.meta["related"] == [TOPIC_ID]  # the redirected link is not listed twice


def test_fold_refuses_a_copy_that_is_itself_roled(tmp_path, capsys):
    cb = tmp_path / "cookbook"
    topic = _topic(cb)
    copy = cb / "guidelines/planning/data/t"
    write_folder(Artifact(meta=_meta(COPY_ID), parts=[
        Part("intro", "# T\n"), Part("rules", RULES, "Rules", "rules"),
        Part("history", HISTORY, "Change History")]), copy)
    before = (topic / "artifact.json").read_text()
    assert main(["fold", str(copy), "--into", str(topic), "--author", "Tester"]) != 0
    assert copy.is_dir()
    assert (topic / "artifact.json").read_text() == before


def test_fold_redirects_links_from_another_guideline(tmp_path, capsys):
    cb = tmp_path / "cookbook"
    topic, copy = _topic(cb), _copy(cb)
    other = _linker(cb, "guidelines/implementing/data/other", "guideline")
    code, out = _fold(copy, topic, capsys)
    assert code == 0
    assert out["redirected"] == ["cookbook/guidelines/implementing/data/other"]
    art = load_folder(other)
    assert art.meta["related"] == [TOPIC_ID] and art.meta["depends-on"] == [TOPIC_ID]
    assert f"(cookbook:{TOPIC_ID})" in art.part("intro").text


def test_fold_unlinks_the_topics_own_in_text_link_to_the_copy(tmp_path, capsys):
    cb = tmp_path / "cookbook"
    topic, copy = _topic(cb), _copy(cb)
    art = load_folder(topic)
    art.part("intro").text = (f"# T\n\nIndexes keep reads fast. See [the planning copy](cookbook:{COPY_ID}) "
                              "and [itself](cookbook:" + COPY_ID + ").\n\n")
    write_folder(art, topic)
    code, out = _fold(copy, topic, capsys)
    assert code == 0
    intro = load_folder(topic).part("intro").text
    assert "See the planning copy and itself." in intro
    assert COPY_ID not in intro and f"cookbook:{TOPIC_ID}" not in intro   # never a link to itself


def test_fold_writes_nothing_when_a_cookbook_folder_cannot_be_read(tmp_path, capsys):
    cb = tmp_path / "cookbook"
    topic, copy = _topic(cb), _copy(cb)
    broken = cb / "recipes/broken"
    broken.mkdir(parents=True)
    (broken / "artifact.json").write_text("{ not json", encoding="utf-8")
    before = {f.name: f.read_text() for f in topic.iterdir() if f.is_file()}
    assert main(["fold", str(copy), "--into", str(topic), "--author", "Tester",
                 "--date", "2026-11-16"]) != 0
    assert copy.is_dir()
    assert {f.name: f.read_text() for f in topic.iterdir() if f.is_file()} == before
    assert not (topic / "versions").exists()
