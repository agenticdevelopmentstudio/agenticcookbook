"""unmeasured.py: the specialities stage 1 cannot measure, placed in their areas.

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reference_format import REFERENCE_FORMAT as FORMAT  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "unmeasured.py"
AREA = "implementing/data"


def topic(survivor, devteam=(), new=False, copies=(), new_home=None):
    t = {"topic": survivor.rsplit("/", 1)[-1], "survivor": survivor, "new": new,
         "devteam": [{"speciality": s} for s in devteam],
         "copies": [{"folder": c, "fold_check": False} for c in copies]}
    if new_home:
        t["new_home"] = new_home
    return t


def building(speciality, topic_path):
    return {"speciality": speciality, "topic": topic_path}


def workspace(tmp_path, topics=(), builds=(), cases=None, references=None, map_topics=None) -> Path:
    ws = tmp_path / "ws"
    (ws / "areas" / AREA).mkdir(parents=True)      # G198 (1.4.39): the area's folder, as stage 1 makes it
    (ws / "worklist.json").write_text(json.dumps(
        {"batches": [{"batch": "1", "topics": list(topics), "building": list(builds)}]}))
    cases = cases or {}
    map_topics = map_topics or {}
    (ws / "speciality-map.json").write_text(json.dumps(
        [{"speciality": s, "topic": None, "case": c} for s, c in cases.items()]
        + [{"speciality": s, "topic": t, "case": "direct"} for s, t in map_topics.items()]))
    references = references if references is not None else [
        {"speciality": s, "topic": None, "file": f"/A/reference/{s.replace('/', '--')}.txt", "format": FORMAT}
        for s in cases]
    (ws / "reference.json").write_text(json.dumps(references))
    return ws


def run(ws: Path, area=AREA):
    (ws / "areas" / area).mkdir(parents=True, exist_ok=True)      # G198 (1.4.39): stage 1 makes the area's folder
    r = subprocess.run([sys.executable, str(SCRIPT), area, "--workspace", str(ws),
                        "--reference", str(ws / "reference.json")], capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip() else None), r.stderr


def test_a_checklist_is_placed_under_the_new_topic_that_claims_it(tmp_path):
    ws = workspace(tmp_path, topics=[topic("guidelines/implementing/data/data-compliance",
                                           ["data/data-compliance"], new=True)],
                   cases={"data/data-compliance": "checklist"})
    code, data, _ = run(ws)
    assert code == 0
    assert data["new_topics"] == [{"speciality": "data/data-compliance",
                                   "topic": "guidelines/implementing/data/data-compliance",
                                   "file": "/A/reference/data--data-compliance.txt", "kind": None}]
    assert data["building"] == [] and data["unplaced"] == []


def test_a_new_topic_of_another_area_is_not_this_areas(tmp_path):
    ws = workspace(tmp_path, topics=[topic("guidelines/implementing/security/security-compliance",
                                           ["security/security-compliance"], new=True)],
                   cases={"security/security-compliance": "checklist"})
    code, data, _ = run(ws)
    assert code == 0 and data["new_topics"] == [] and data["unplaced"] == []


def test_a_building_speciality_is_placed_in_every_area_the_worklist_maps_it_to(tmp_path):
    builds = [building("building/platform-database", "guidelines/implementing/data/indexing"),
              building("building/platform-database", "guidelines/implementing/data/primary-keys"),
              building("building/platform-database", "guidelines/testing/test-data")]
    ws = workspace(tmp_path, builds=builds, cases={"building/platform-database": "building-split"})
    code, data, _ = run(ws)
    assert code == 0
    assert data["building"] == [{"speciality": "building/platform-database",
                                 "topics": ["guidelines/implementing/data/indexing",
                                            "guidelines/implementing/data/primary-keys"],
                                 "by_new_home": [], "measured_by": [], "via": [],
                                 "file": "/A/reference/building--platform-database.txt"}]
    code, data, _ = run(ws, "testing")
    assert code == 0 and [b["topics"] for b in data["building"]] == [["guidelines/testing/test-data"]]
    code, data, _ = run(ws, "implementing/security")
    assert code == 0 and data["building"] == []


def test_an_area_is_the_whole_path_not_a_prefix(tmp_path):
    builds = [building("building/x", "guidelines/implementing/data-sync/merge")]
    ws = workspace(tmp_path, builds=builds, cases={"building/x": "building-split"})
    code, data, _ = run(ws)
    assert code == 0 and data["building"] == []


def test_an_unplaced_building_speciality_exits_2_naming_it(tmp_path):
    ws = workspace(tmp_path, cases={"building/scripting": "building-split"})
    code, data, err = run(ws)
    assert code == 2 and "building/scripting" in err
    assert data["unplaced"] == [{"speciality": "building/scripting",
                                 "why": "a building speciality no worklist building entry maps to a topic"}]


def test_an_unclaimed_speciality_exits_2_naming_it(tmp_path):
    ws = workspace(tmp_path, cases={"performance/per-call-cost": "none"})
    code, data, err = run(ws)
    assert code == 2 and "performance/per-call-cost" in err
    assert data["unplaced"] == [{"speciality": "performance/per-call-cost", "why": "no new row claims it"}]


def test_a_speciality_two_new_rows_claim_exits_2_naming_both(tmp_path):
    ws = workspace(tmp_path, topics=[topic("guidelines/implementing/data/a", ["data/x"], new=True),
                                     topic("guidelines/implementing/data/b", ["data/x"], new=True)],
                   cases={"data/x": "checklist"})
    code, data, err = run(ws)
    assert code == 2 and "data/x" in err
    assert data["unplaced"] == [{"speciality": "data/x", "why": "two or more new rows claim it: "
                                 "guidelines/implementing/data/a, guidelines/implementing/data/b"}]


def test_an_existing_topic_claiming_it_is_not_a_new_row(tmp_path):
    ws = workspace(tmp_path, topics=[topic("guidelines/implementing/data/a", ["data/x"], new=False)],
                   cases={"data/x": "checklist"})
    code, data, _ = run(ws)
    assert code == 2 and data["unplaced"][0]["speciality"] == "data/x"


def test_a_speciality_with_a_topic_is_not_unmeasured(tmp_path):
    refs = [{"speciality": "data/indexing", "topic": "cookbook/guidelines/implementing/data/indexing",
             "file": "/A/reference/data--indexing.txt"}]
    ws = workspace(tmp_path, references=refs)
    code, data, _ = run(ws)
    assert code == 0 and data == {"area": AREA, "new_topics": [], "building": [], "unplaced": [],
                                  "marked_here": [], "mark_conflicts": [],
                                  "against_survivor": [], "survivor_elsewhere": [], "unread_marks": [],
                                  "ignored_marks": []}


def test_a_missing_input_exits_2_naming_it(tmp_path):
    ws = workspace(tmp_path)
    (ws / "speciality-map.json").unlink()
    code, _, err = run(ws)
    assert code == 2 and "speciality-map.json" in err


# 1.4.13, G19/G15: building text reaches the area it belongs to.

def test_a_building_speciality_no_devteam_list_names_is_listed_never_measured(tmp_path):
    # G19: building/codebase-decomposition maps to the area's topics, but no
    # topic's devteam list names it, so roles gaps never measures it.
    builds = [building("building/decomp", "guidelines/implementing/data/indexing")]
    ws = workspace(tmp_path, topics=[topic("guidelines/implementing/data/indexing", ["data/indexing"])],
                   builds=builds, cases={"building/decomp": "building-split"})
    code, data, _ = run(ws)
    assert code == 0
    assert [(b["speciality"], b["measured_by"]) for b in data["building"]] == [("building/decomp", [])]


def test_a_building_speciality_a_devteam_list_names_says_which_topic_measures_it(tmp_path):
    builds = [building("building/decomp", "guidelines/implementing/data/indexing")]
    ws = workspace(tmp_path, topics=[topic("guidelines/implementing/data/indexing", ["building/decomp"])],
                   builds=builds, cases={"building/decomp": "building-split"})
    code, data, _ = run(ws)
    assert code == 0 and data["building"][0]["measured_by"] == ["guidelines/implementing/data/indexing"]


def test_a_building_entry_naming_a_survivors_new_home_reaches_the_survivors_area(tmp_path):
    # G15: the entry names the new_home in another area; the survivor is here,
    # so the text is listed here (its file null: this area's reference run did
    # not write it) as well as in the new_home's area.
    survivor = "guidelines/reviewing/code-quality/law-of-demeter"
    home = "guidelines/implementing/code-quality/law-of-demeter"
    ws = workspace(tmp_path, topics=[topic(survivor, ["code-quality/law-of-demeter"], new_home=home)],
                   builds=[building("building/code-quality", home)],
                   cases={"building/code-quality": "building-split"},
                   references=[{"speciality": "building/code-quality", "topic": None, "file": None}])
    code, data, _ = run(ws, "reviewing/code-quality")
    assert code == 0
    assert data["building"] == [{"speciality": "building/code-quality", "topics": [survivor],
                                 "by_new_home": [home], "measured_by": [], "via": [], "file": None}]
    code, data, _ = run(ws, "implementing/code-quality")
    assert code == 0 and data["building"][0]["topics"] == [home] and data["building"][0]["by_new_home"] == []


def test_a_building_entry_naming_a_survivor_reaches_its_new_homes_area(tmp_path):
    survivor = "guidelines/reviewing/code-quality/code-hygiene"
    home = "guidelines/implementing/code-quality/code-hygiene"
    ws = workspace(tmp_path, topics=[topic(survivor, new_home=home)],
                   builds=[building("building/hygiene", survivor)],
                   cases={"building/hygiene": "building-split"})
    code, data, _ = run(ws, "implementing/code-quality")
    assert code == 0
    assert [(b["topics"], b["by_new_home"]) for b in data["building"]] == [([home], [survivor])]


# 1.4.13, G8: another plan's marks reach the area they name.

def marks(ws: Path, area: str, speciality: str, sentences: list[str], marked: dict, plan: bool = True) -> None:
    d = ws / "areas" / area
    d.mkdir(parents=True, exist_ok=True)
    if plan and not (d / "area-plan.md").exists():      # G109: only an area folder's marks are read
        (d / "area-plan.md").write_text("# Plan\n")
    name = speciality.split("/", 1)[1]
    (d / f"building-{name}.json").write_text(json.dumps(
        {"speciality": speciality, "sentences": [{"n": n, "text": t} for n, t in enumerate(sentences, 1)],
         "marks": {str(n): marked.get(n) for n in range(1, len(sentences) + 1)}}))
    (d / f"building-{name}-quoted.json").write_text(json.dumps({"markdown": "x", "this_area": [], "problems": []}))


WINDOWS = ["Build on WinUI.", "Keep UI and background work apart.", "Never block the UI thread."]


def test_a_sentence_another_plan_marks_for_this_area_is_listed_with_that_plan(tmp_path):
    # the shipping plan marks sentence 3 as implementing/concurrency's, which the
    # worklist never maps platform-windows to.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS,
          {1: "shipping", 2: "implementing/platform-integration", 3: "implementing/concurrency"})
    code, data, _ = run(ws, "implementing/concurrency")
    assert code == 0
    assert data["marked_here"] == [{"speciality": "building/platform-windows", "n": 3,
                                    "text": "Never block the UI thread.", "marked_by": ["shipping"]}]
    assert data["mark_conflicts"] == []


def test_this_areas_own_marks_are_not_listed_as_another_plans(tmp_path):
    ws = workspace(tmp_path)
    marks(ws, AREA, "building/platform-windows", WINDOWS, {1: AREA, 2: AREA, 3: AREA})
    code, data, _ = run(ws)
    assert code == 0 and data["marked_here"] == []


def test_two_plans_marking_one_sentence_for_different_areas_is_a_conflict(tmp_path):
    # G8: shipping gives sentence 2 to implementing/platform-integration,
    # implementing/code-quality gives it to itself.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS,
          {1: "shipping", 2: "implementing/platform-integration", 3: "implementing/concurrency"})
    marks(ws, "implementing/code-quality", "building/platform-windows", WINDOWS,
          {1: "shipping", 2: "implementing/code-quality", 3: "implementing/concurrency"})
    code, data, _ = run(ws, "implementing/code-quality")
    assert code == 0
    assert data["mark_conflicts"] == [{"speciality": "building/platform-windows", "n": 2,
                                       "text": "Keep UI and background work apart.",
                                       "marks": {"implementing/code-quality": "implementing/code-quality",
                                                 "shipping": "implementing/platform-integration"},
                                       "agrees_for": [], "differs_for": ["implementing/code-quality",
                                                                         "implementing/platform-integration"]}]
    # the area the other plan names sees it too; an area neither plan nor mark names does not
    code, data, _ = run(ws, "implementing/platform-integration")
    assert [c["n"] for c in data["mark_conflicts"]] == [2]
    assert data["marked_here"] == [{"speciality": "building/platform-windows", "n": 2,
                                    "text": "Keep UI and background work apart.", "marked_by": ["shipping"]}]
    code, data, _ = run(ws, "implementing/data")
    assert data["mark_conflicts"] == []


def test_this_areas_unreadable_marks_file_exits_2_naming_it(tmp_path):
    ws = workspace(tmp_path)
    bad = ws / "areas" / AREA / "building-x.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text("{not json")
    code, _, err = run(ws)
    assert code == 2 and "building-x.json" in err


def test_another_areas_unreadable_marks_file_is_named_and_skipped(tmp_path):
    # 1.4.14, N3: a half-saved marks file in another area's run does not stop this one.
    ws = workspace(tmp_path)
    bad = ws / "areas" / "shipping" / "building-x.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    (bad.parent / "area-plan.md").write_text("# Plan\n")       # G109: an area folder's file
    bad.write_text("{not json")
    marks(ws, "planning/data", "building/platform-windows", WINDOWS, {1: AREA})
    code, data, err = run(ws)
    assert code == 0
    assert [u["file"] for u in data["unread_marks"]] == [str(bad)]
    assert [m["n"] for m in data["marked_here"]] == [1]
    assert "building-x.json" in err


# 1.4.13, G14: a speciality on a copy is measured in the survivor's area.

def test_a_speciality_on_a_copy_is_measured_against_the_survivor_in_its_area(tmp_path):
    survivor = "guidelines/implementing/code-quality/dependency-injection"
    copy = "guidelines/reviewing/code-quality/dependency-injection"
    refs = [{"speciality": "architecture/dependency-injection", "topic": f"cookbook/{copy}",
             "file": "/A/reference/architecture--dependency-injection.txt"}]
    ws = workspace(tmp_path, topics=[topic(survivor, copies=[copy])], references=refs,
                   map_topics={"architecture/dependency-injection": f"cookbook/{copy}"})
    code, data, _ = run(ws, "implementing/code-quality")
    assert code == 0
    assert data["against_survivor"] == [{"speciality": "architecture/dependency-injection",
                                         "copy": f"cookbook/{copy}", "survivor": f"cookbook/{survivor}",
                                         "file": "/A/reference/architecture--dependency-injection.txt"}]
    assert data["survivor_elsewhere"] == []
    code, data, _ = run(ws, "reviewing/code-quality")
    assert code == 0 and data["against_survivor"] == []
    assert data["survivor_elsewhere"] == [{"speciality": "architecture/dependency-injection",
                                           "copy": f"cookbook/{copy}", "survivor": f"cookbook/{survivor}"}]


def test_a_speciality_on_a_copy_this_areas_reference_run_did_not_write_has_a_null_file(tmp_path):
    survivor = "guidelines/implementing/language/python"
    copy = "guidelines/reviewing/language/python"
    ws = workspace(tmp_path, topics=[topic(survivor, copies=[copy])], references=[],
                   map_topics={"language/python": f"cookbook/{copy}"})
    code, data, _ = run(ws, "implementing/language")
    assert code == 0 and data["against_survivor"][0]["file"] is None


def test_a_via_mapping_is_not_a_measure_but_names_its_topic(tmp_path):
    # 1.4.16, G25: the worklist maps building/security to this area's topics
    # `via` other specialities; that is no measure (over-reporting beats
    # missing), so the row stays unmeasured and lists each `via` topic.
    auth = "guidelines/implementing/security/authentication"
    cors = "guidelines/implementing/security/cors"
    builds = [{**building("building/security", auth), "via": "security/authentication"},
              {**building("building/security", cors), "via": "security/cors"},
              {**building("building/security", "guidelines/shipping/x"), "via": "security/x"},
              building("building/security", "guidelines/implementing/security/plain")]
    ws = workspace(tmp_path, builds=builds, cases={"building/security": "building-split"})
    code, data, _ = run(ws, "implementing/security")
    assert code == 0
    [row] = data["building"]
    assert row["measured_by"] == []
    assert row["via"] == [{"speciality": "security/authentication", "topic": auth},
                          {"speciality": "security/cors", "topic": cors}]


def test_a_via_reached_through_new_home_names_this_areas_topic(tmp_path):
    # 1.4.17, M2: an entry whose topic is a survivor in another area reaches
    # this area through its new_home; its `via` names the new_home topic.
    survivor = "guidelines/reviewing/security/vulnerability-prioritization"
    home = "guidelines/implementing/security/vulnerability-prioritization"
    builds = [{**building("building/security", survivor), "via": "security/vulnerability-prioritization"}]
    ws = workspace(tmp_path, topics=[topic(survivor, new_home=home)], builds=builds,
                   cases={"building/security": "building-split"})
    code, data, _ = run(ws, "implementing/security")
    assert code == 0
    [row] = data["building"]
    assert row["by_new_home"] == [survivor] and row["measured_by"] == []
    assert row["via"] == [{"speciality": "security/vulnerability-prioritization", "topic": home}]


# 1.4.24: G45 --check, G49 grouped marks, G53 new topics, G55 list marks.

def run_check(ws: Path, area=AREA):
    r = subprocess.run([sys.executable, str(SCRIPT), area, "--workspace", str(ws),
                        "--reference", str(ws / "reference.json"), "--check"], capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip() else None), r.stderr


def test_check_compares_with_the_saved_file_and_writes_nothing(tmp_path):
    # G45: --check reads A/unmeasured.json, prints what changed, writes nothing.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA, 2: "shipping", 3: "shipping"})
    saved = ws / "areas" / AREA / "unmeasured.json"
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(run(ws)[1]))
    before = saved.read_bytes()
    code, data, _ = run_check(ws)
    assert code == 0 and data["check"] == "unchanged" and data["changes"] == []
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA, 2: AREA, 3: "shipping"})
    code, data, _ = run_check(ws)
    assert code == 1 and data["check"] == "changed"
    assert {"path": "marked_here", "added": [{"speciality": "building/platform-windows", "n": 2,
                                              "text": "Keep UI and background work apart.",
                                              "marked_by": ["shipping"]}], "removed": []} in data["changes"]
    assert saved.read_bytes() == before


def test_check_without_a_saved_file_exits_2(tmp_path):
    ws = workspace(tmp_path)
    code, _, err = run_check(ws)
    assert code == 2 and "unmeasured.json" in err


def test_a_sentence_two_plans_mark_here_is_one_row(tmp_path):
    # G49: grouped by (speciality, n), every marking plan in `marked_by`.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA})
    marks(ws, "planning/data", "building/platform-windows", WINDOWS, {1: AREA})
    code, data, _ = run(ws)
    assert data["marked_here"] == [{"speciality": "building/platform-windows", "n": 1, "text": "Build on WinUI.",
                                    "marked_by": ["planning/data", "shipping"]}]


def test_a_mark_may_name_several_areas_and_differs_only_when_the_lists_do(tmp_path):
    # G55: a list mark puts the sentence in each named area's `marked_here`;
    # two plans conflict only when their lists differ (order aside).
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: ["shipping", AREA]})
    marks(ws, "planning/data", "building/platform-windows", WINDOWS, {1: [AREA, "shipping"]})
    code, data, _ = run(ws)
    assert [m["n"] for m in data["marked_here"]] == [1] and data["mark_conflicts"] == []
    code, data, _ = run(ws, "shipping")
    assert data["marked_here"][0]["marked_by"] == ["planning/data"]
    marks(ws, "planning/data", "building/platform-windows", WINDOWS, {1: AREA})
    code, data, _ = run(ws)
    assert data["mark_conflicts"][0]["marks"] == {"planning/data": AREA, "shipping": ["shipping", AREA]}


def test_new_topics_come_from_the_worklists_new_rows(tmp_path):
    # G53: a `new` worklist topic of this area is listed even when its
    # speciality's reference row names a topic (a candidate survivor elsewhere).
    t = topic("guidelines/implementing/data/least-astonishment", ["cq/lae"], new=True)
    t["kind"] = "shared-different"
    ws = workspace(tmp_path, topics=[t],
                   references=[{"speciality": "cq/lae", "topic": "cookbook/principles/lae", "file": "/A/r/cq--lae.txt"}])
    code, data, _ = run(ws)
    assert code == 0
    assert data["new_topics"] == [{"speciality": "cq/lae", "topic": "guidelines/implementing/data/least-astonishment",
                                   "file": "/A/r/cq--lae.txt", "kind": "shared-different"}]


def test_a_topicless_speciality_missing_from_the_reference_rows_is_still_placed_or_unplaced(tmp_path):
    # 1.4.24, G57: speciality_reference.py --area now writes only this area's
    # rows; every topicless speciality of speciality-map.json is still placed,
    # and one the worklist cannot place still stops the stage.
    ws = workspace(tmp_path, cases={"building/scripting": "building-split", "performance/per-call-cost": "none",
                                    "data/new-one": "checklist"},
                   topics=[topic("guidelines/implementing/data/new-one", ["data/new-one"], new=True)],
                   references=[{"speciality": "data/new-one", "topic": None, "file": "/A/reference/x.txt"}])
    code, data, err = run(ws)
    assert code == 2 and "building/scripting" in err and "performance/per-call-cost" in err
    assert sorted(u["speciality"] for u in data["unplaced"]) == ["building/scripting", "performance/per-call-cost"]
    assert data["new_topics"][0]["file"] == "/A/reference/x.txt"


def test_a_new_topic_of_several_specialities_lists_each(tmp_path):
    # G53 (1.4.24): one row per speciality of a `new` worklist topic.
    t = topic("guidelines/implementing/data/two-names", ["cq/one", "cq/two"], new=True)
    ws = workspace(tmp_path, topics=[t], references=[
        {"speciality": "cq/one", "topic": None, "file": "/A/r/one.txt"},
        {"speciality": "cq/two", "topic": None, "file": "/A/r/two.txt"}])
    code, data, _ = run(ws)
    assert [(r["speciality"], r["file"]) for r in data["new_topics"]] == [("cq/one", "/A/r/one.txt"),
                                                                       ("cq/two", "/A/r/two.txt")]


def test_check_compares_sentences_of_one_speciality_one_by_one():
    # G45 (1.4.24): rows keyed by (speciality, n), so a change to one
    # sentence of a speciality is reported at that sentence.
    old = {"marked_here": [{"speciality": "building/x", "n": 1, "marked_by": ["a"]},
                           {"speciality": "building/x", "n": 2, "marked_by": ["a"]}]}
    new = {"marked_here": [{"speciality": "building/x", "n": 1, "marked_by": ["a"]},
                           {"speciality": "building/x", "n": 2, "marked_by": ["a", "b"]}]}
    sys.path.insert(0, str(SCRIPT.parent))
    from unmeasured import changes
    assert changes(old, new) == [
        {"path": "marked_here[building/x#2].marked_by", "added": ["b"], "removed": []}]


def test_two_sentences_of_one_text_keep_their_own_rows_and_conflict(tmp_path):
    # fix round 1, I1: marks are keyed on (speciality, n), the text carried as
    # data, so a text a building file has twice is two sentences.
    twice = ["Build on WinUI.", "A review passes when it establishes every item above.", "Ship it.",
             "A review passes when it establishes every item above."]
    ws = workspace(tmp_path)
    marks(ws, "implementing/ui", "building/platform-windows", twice, {2: AREA, 4: AREA})
    marks(ws, "shipping", "building/platform-windows", twice, {2: "implementing/ui", 4: AREA})
    code, data, _ = run(ws)
    assert [(r["n"], r["marked_by"]) for r in data["marked_here"]] == [(2, ["implementing/ui"]),
                                                                      (4, ["implementing/ui", "shipping"])]
    assert data["mark_conflicts"] == [{"speciality": "building/platform-windows", "n": 2, "text": twice[1],
                                       "marks": {"implementing/ui": AREA, "shipping": "implementing/ui"},
                                       "agrees_for": [], "differs_for": [AREA, "implementing/ui"]}]


def test_check_exits_2_on_an_unplaced_speciality_as_a_run_does(tmp_path):
    # fix round 1, M4
    ws = workspace(tmp_path, cases={"data/orphan": "checklist"})
    code, data, _ = run(ws)
    assert code == 2 and data["unplaced"]
    saved = ws / "areas" / AREA / "unmeasured.json"
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(data))
    code, out, err = run_check(ws)
    assert code == 2 and out["check"] == "unchanged" and "data/orphan" in err


def test_a_new_topics_speciality_keeps_its_file_whatever_row_follows(tmp_path):
    # fix round 1, M5: a null-file row of the same speciality never hides the path.
    t = topic("guidelines/implementing/data/fresh", ["data/fresh"], new=True)
    ws = workspace(tmp_path, topics=[t], cases={"data/fresh": "checklist"}, references=[
        {"speciality": "data/fresh", "topic": None, "file": "/A/r/fresh.txt"},
        {"speciality": "data/fresh", "topic": None, "file": None}])
    code, data, _ = run(ws)
    assert code == 0 and [r["file"] for r in data["new_topics"]] == ["/A/r/fresh.txt"]


def test_a_stale_and_a_requoted_marks_file_are_a_numbering_conflict(tmp_path):
    # fix round 2, N-B: plan implementing/ui marked a building file before a
    # re-quote added a first sentence; plan shipping marked it after. The one
    # sentence is n3 in one file and n4 in the other, and n3 has two texts:
    # a conflict for each, naming both plans, both n and the text.
    old = ["Build on WinUI.", "Keep UI apart.", "Never block the UI thread."]
    new = ["Use the platform guide.", *old]
    ws = workspace(tmp_path)
    marks(ws, "implementing/ui", "building/platform-windows", old, {3: AREA})
    marks(ws, "shipping", "building/platform-windows", new, {4: "shipping"})
    marks(ws, "implementing/ui", "building/platform-linux", ["One.", "Two."], {2: "shipping"})
    marks(ws, "shipping", "building/platform-linux", ["Zero.", "One.", "Two."], {3: "shipping"})
    code, data, _ = run(ws)
    # G114 (1.4.33): compared by text, the one sentence's two marks are a
    # conflict too (by number it was hidden: shipping's n3 is unmarked).
    assert data["mark_conflicts"][0] == {
        "speciality": "building/platform-windows", "n": 3, "text": old[2],
        "marks": {"implementing/ui": AREA, "shipping": "shipping"}, "agrees_for": [],
        "differs_for": [AREA, "shipping"], "compared": "by text", "n_by_plan": {"implementing/ui": 3, "shipping": 4}}
    assert data["mark_conflicts"][1:] == [{
        "speciality": "building/platform-windows", "reason": "numbering differs", "plans": [
            {"plan": "implementing/ui", "n": 3, "text": old[2], "mark": AREA},
            {"plan": "shipping", "n": 3, "text": old[1], "mark": None}]}, {
        "speciality": "building/platform-windows", "reason": "numbering differs", "plans": [
            {"plan": "implementing/ui", "n": 3, "text": old[2], "mark": AREA},
            {"plan": "shipping", "n": 4, "text": old[2], "mark": "shipping"}]}]


def test_one_number_two_texts_is_a_numbering_conflict(tmp_path):
    # fix round 2, N-B: the same n with different text in two plans' files
    # names both plans, numbers and texts; this area's own file is a plan; a
    # difference neither file marks is no row.
    ws = workspace(tmp_path)
    marks(ws, AREA, "building/platform-windows", ["A one.", "B two.", "D."], {2: "implementing/ui"})
    marks(ws, "shipping", "building/platform-windows", ["A one.", "C three.", "E."], {2: "shipping"})
    code, data, _ = run(ws)
    assert [c for c in data["mark_conflicts"] if c.get("reason")] == [{
        "speciality": "building/platform-windows", "reason": "numbering differs", "plans": [
        {"plan": AREA, "n": 2, "text": "B two.", "mark": "implementing/ui"},
        {"plan": "shipping", "n": 2, "text": "C three.", "mark": "shipping"}]}]


# 1.4.25: G71 agrees_for/differs_for, G67 saved_file, G76 --repo.

def test_a_conflict_says_which_areas_every_side_agrees_on(tmp_path):
    # G71: ["implementing/testing", "testing"] against "implementing/testing"
    # stays a conflict (over-reporting), with `agrees_for` the areas every
    # side names and `differs_for` the areas some side leaves out.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: ["shipping", AREA], 2: "shipping"})
    marks(ws, "planning/data", "building/platform-windows", WINDOWS, {1: AREA, 2: "planning/data"})
    code, data, _ = run(ws)
    row = data["mark_conflicts"][0]
    assert row["n"] == 1 and row["agrees_for"] == [AREA] and row["differs_for"] == ["shipping"]
    code, data, _ = run(ws, "shipping")
    rows = {r["n"]: r for r in data["mark_conflicts"]}
    assert rows[2]["agrees_for"] == [] and rows[2]["differs_for"] == ["planning/data", "shipping"]


def test_a_numbering_conflict_never_says_it_agrees(tmp_path):
    # 1.4.26 (M5): the two plans' marks are for different sentences, so a
    # `numbering differs` row carries no `agrees_for`/`differs_for`: it is
    # always this plan's to resolve, never read as agreement.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA})
    marks(ws, "planning/data", "building/platform-windows", ["New first."] + WINDOWS, {2: [AREA, "shipping"]})
    code, data, _ = run(ws)
    rows = [r for r in data["mark_conflicts"] if r.get("reason")]
    moved = next(r for r in rows if [p["n"] for p in r["plans"]] == [2, 1])     # "Build on WinUI." moved
    assert moved["plans"][0]["mark"] == [AREA, "shipping"] and moved["plans"][1]["mark"] == AREA
    assert all("agrees_for" not in r and "differs_for" not in r for r in rows)


def test_check_names_the_saved_file_as_saved_file(tmp_path):
    # G67: `saved` read like a write; check mode prints `saved_file`.
    ws = workspace(tmp_path)
    saved = ws / "areas" / AREA / "unmeasured.json"
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(run(ws)[1]))
    code, data, _ = run_check(ws)
    assert data["saved_file"] == str(saved) and "saved" not in data


def test_repo_is_accepted_and_must_be_a_cookbook(tmp_path):
    # G76: every script that reads the cookbook takes --repo; a --repo with
    # no cookbook/guidelines/ exits 2 naming it.
    ws = workspace(tmp_path)
    repo = tmp_path / "repo"
    (repo / "cookbook" / "guidelines").mkdir(parents=True, exist_ok=True)
    base = [sys.executable, str(SCRIPT), AREA, "--workspace", str(ws), "--reference", str(ws / "reference.json")]
    r = subprocess.run(base + ["--repo", str(repo)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    r = subprocess.run(base + ["--repo", str(tmp_path / "nowhere")], capture_output=True, text=True)
    assert r.returncode == 2 and "nowhere" in r.stderr and "cookbook/guidelines" in r.stderr



def test_check_lists_a_reference_written_before_1426_as_stale(tmp_path):
    # Fix round 2, R-I-1: a reference.json row with no format stamp, or an
    # older one, is listed in `stale_reference` and is a change (exit 1).
    ws = workspace(tmp_path, cases={"building/security": "building-split"},
                   builds=[building("building/security", "guidelines/implementing/data/x")])
    (ws / "areas" / AREA).mkdir(parents=True, exist_ok=True)
    assert run(ws)[0] == 0
    (ws / "areas" / AREA / "unmeasured.json").write_text(json.dumps(run(ws)[1]))
    code, out, _ = run_check(ws)
    assert code == 0 and out["stale_reference"] == [], out
    refs = json.loads((ws / "reference.json").read_text())
    refs[0].pop("format")
    refs.append({"speciality": "data/old", "topic": "cookbook/guidelines/implementing/data/x",
                 "file": "/A/reference/data--old.txt", "format": 1})
    (ws / "reference.json").write_text(json.dumps(refs))
    code, out, _ = run_check(ws)
    assert code == 1 and [(r["speciality"], r["format"]) for r in out["stale_reference"]] == [
        ("building/security", None), ("data/old", 1)]
    assert any(c["path"] == "stale_reference" for c in out["changes"])


def test_only_marks_directly_in_an_area_folder_are_read(tmp_path):
    # G109 (1.4.33): a backup kept inside an area folder (A/old-1.4.23/) or a
    # folder that is no area (no area-plan.md, no reference.json) is no plan:
    # its marks are listed in `ignored_marks`, never read.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: "shipping", 2: "shipping", 3: AREA})
    marks(ws, "shipping/old-1.4.23", "building/platform-windows", WINDOWS, {1: AREA, 2: AREA, 3: AREA})
    marks(ws, "scratch", "building/platform-windows", WINDOWS, {1: AREA, 2: AREA, 3: AREA}, plan=False)
    (ws / "areas" / "planning" / "data").mkdir(parents=True, exist_ok=True)
    (ws / "areas" / "planning" / "data" / "reference.json").write_text("[]")
    marks(ws, "planning/data", "building/platform-windows", WINDOWS, {1: "x", 2: "x", 3: "x"}, plan=False)
    code, data, _ = run(ws)
    assert code == 0, data
    assert data["marked_here"] == [{"speciality": "building/platform-windows", "n": 3, "text": WINDOWS[2],
                                    "marked_by": ["shipping"]}]
    assert [Path(r["file"]).parent.name for r in data["ignored_marks"]] == ["scratch", "old-1.4.23"]
    assert all("scratchpad" in r["why"] for r in data["ignored_marks"])


def test_a_renumbered_speciality_is_compared_by_text_never_by_number(tmp_path):
    # G114 (1.4.33): when two plans number a speciality differently, the
    # by-number comparison pairs different sentences (noise beside the real
    # disagreement). Such a speciality is compared by text: one row per text
    # two plans mark differently, `compared: "by text"` and each plan's n.
    old = ["Build on WinUI.", "Keep UI apart.", "Never block the UI thread."]
    new = ["Use the platform guide.", *old]
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", old, {1: "shipping", 2: AREA, 3: "shipping"})
    marks(ws, AREA, "building/platform-windows", new, {1: AREA, 2: "shipping", 3: AREA, 4: "implementing/ui"})
    code, data, _ = run(ws)
    plain = [c for c in data["mark_conflicts"] if not c.get("reason")]
    assert plain == [{"speciality": "building/platform-windows", "n": 4, "text": old[2],     # n: first plan's
                      "marks": {AREA: "implementing/ui", "shipping": "shipping"},
                      "agrees_for": [], "differs_for": ["implementing/ui", "shipping"],
                      "compared": "by text", "n_by_plan": {AREA: 4, "shipping": 3}}], plain
    assert {c["reason"] for c in data["mark_conflicts"] if c.get("reason")} == {"numbering differs"}


# ---- fix round 1 (1.4.34): review M3 (an empty new key) and M5 (renumbering across plans) ----

def test_a_key_the_saved_file_lacks_is_no_change_when_its_new_value_is_empty(tmp_path):
    # an additive release never flips every check by itself; a non-empty new key still does
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA, 2: "shipping", 3: "shipping"})
    saved = ws / "areas" / AREA / "unmeasured.json"
    saved.parent.mkdir(parents=True, exist_ok=True)
    old = run(ws)[1]
    assert old["ignored_marks"] == []
    del old["ignored_marks"]
    saved.write_text(json.dumps(old))
    code, data, _ = run_check(ws)
    assert code == 0 and data["check"] == "unchanged" and data["changes"] == [], data
    assert data["new_keys"] == ["ignored_marks"]
    (ws / "areas" / "scratch").mkdir()
    (ws / "areas" / "scratch" / "building-platform-windows.json").write_text("{}")
    code, data, _ = run_check(ws)
    assert code == 1 and [c["path"] for c in data["changes"]] == ["ignored_marks"], data


def test_changes_lists_an_empty_new_key_apart_at_any_depth():
    sys.path.insert(0, str(SCRIPT.parent))
    from unmeasured import changes
    new_keys: list[str] = []
    old = {"rows": [{"speciality": "s", "n": 1, "text": "x"}]}
    new = {"rows": [{"speciality": "s", "n": 1, "text": "x", "marked_for": [], "topic": None}], "markers": []}
    assert changes(old, new, new_keys=new_keys) == []
    assert new_keys == ["rows[s#1].marked_for", "rows[s#1].topic", "markers"]
    new["rows"][0]["topic"] = "authn"
    assert changes(old, new) == [{"path": "rows[s#1].topic", "was": None, "now": "authn"}]
    for empty in ([], {}, None, False):
        assert changes({}, {"k": empty}) == []
    assert changes({}, {"k": 0}) == [{"path": "k", "was": None, "now": 0}]
    assert changes({}, {"k": ""}) == [{"path": "k", "was": None, "now": ""}]


def test_a_speciality_numbered_differently_by_any_two_plans_is_renumbered():
    # review M5: b and c disagree on n=2 while each agrees with a
    sys.path.insert(0, str(SCRIPT.parent))
    from unmeasured import _renumbered
    def f(texts):
        return [{"speciality": "building/x", "sentences": [{"n": n, "text": t} for n, t in texts.items()]}]
    assert _renumbered({"a": f({1: "A"}), "b": f({1: "A", 2: "B"}), "c": f({1: "A", 2: "C"})}) == {"building/x"}
    assert _renumbered({"a": f({1: "A"}), "b": f({1: "A", 2: "B"}), "c": f({2: "B", 3: "C"})}) == set()
    assert _renumbered({"a": f({1: "A"}), "b": f({2: "B"}), "c": f({3: "B"})}) == {"building/x"}


# ---- gapfix9 (1.4.36) ----

def test_area_flag_default_reference_digest_and_keys(tmp_path):
    # G139: --area as the positional; --reference defaults to A/reference.json.
    # G137: --check --digest prints one line; G138: --keys prints the check's
    # changes and new_keys whole.
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA, 2: "shipping", 3: "shipping"})
    saved = ws / "areas" / AREA / "unmeasured.json"
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(run(ws)[1]))
    (ws / "areas" / AREA / "reference.json").write_bytes((ws / "reference.json").read_bytes())
    (ws / "reference.json").unlink()      # only A/reference.json is left to default to
    base = [sys.executable, str(SCRIPT), "--area", AREA, "--workspace", str(ws), "--check"]
    r = subprocess.run(base, capture_output=True, text=True)
    assert r.returncode == 0 and json.loads(r.stdout)["check"] == "unchanged", r.stderr
    r = subprocess.run(base + ["--digest"], capture_output=True, text=True)
    line = r.stdout.strip()
    assert r.returncode == 0 and "\n" not in line, r.stderr
    assert line.startswith(f"unmeasured.py {AREA}: check unchanged; changes 0; new_keys 0; stale_reference 0; result ")
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA, 2: AREA, 3: "shipping"})
    r = subprocess.run(base + ["--keys"], capture_output=True, text=True)
    out = json.loads(r.stdout)
    assert r.returncode == 1 and out["check"] == "changed" and out["changes"][0]["path"] == "marked_here", out
    r = subprocess.run(base + ["--digest"], capture_output=True, text=True)
    assert r.returncode == 1 and r.stdout.startswith(f"unmeasured.py {AREA}: check changed; changes 1; ")


# ---- gapfix13 (1.4.42) ----

def _g13_saved(tmp_path):
    ws = workspace(tmp_path)
    marks(ws, "shipping", "building/platform-windows", WINDOWS, {1: AREA, 2: "shipping", 3: "shipping"})
    saved = ws / "areas" / AREA / "unmeasured.json"
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(run(ws)[1]))
    (ws / "areas" / AREA / "reference.json").write_bytes((ws / "reference.json").read_bytes())
    return ws, [sys.executable, str(SCRIPT), "--area", AREA, "--workspace", str(ws)]


def test_digest_alone_is_the_checks_digest(tmp_path):
    # G261: --digest works alone; it is always a check's digest and writes nothing.
    ws, base = _g13_saved(tmp_path)
    saved = ws / "areas" / AREA / "unmeasured.json"
    before = saved.read_bytes()
    r = subprocess.run(base + ["--digest"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith(f"unmeasured.py {AREA}: check unchanged; changes 0;")
    assert saved.read_bytes() == before


def test_rows_prints_the_named_keys_whole_and_names_an_unknown_one(tmp_path):
    # G261: --rows KEY[,KEY], one shape on stage_status, run_gaps and unmeasured.
    ws, base = _g13_saved(tmp_path)
    r = subprocess.run(base + ["--rows", "marked_here,new_topics"], capture_output=True, text=True)
    out = json.loads(r.stdout)
    assert r.returncode == 0 and list(out) == ["marked_here", "new_topics"], r.stderr
    r = subprocess.run(base + ["--check", "--rows", "changes"], capture_output=True, text=True)
    assert r.returncode == 0 and json.loads(r.stdout) == {"changes": []}, r.stderr
    r = subprocess.run(base + ["--rows", "measured_total"], capture_output=True, text=True)
    assert r.returncode == 2 and "run_gaps.py" in r.stderr and "no output key 'measured_total'" in r.stderr


def test_check_and_keys_print_at_most_forty_rows_a_key(tmp_path):
    # G271: --check and --keys show at most 40 rows of a key, then `(N more: --rows <key>)`.
    import importlib.util
    spec = importlib.util.spec_from_file_location("json_keys", SCRIPT.parent / "json_keys.py")
    jk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(jk)
    out = jk.cap({"changes": list(range(45)), "check": "changed"})
    assert out["changes"][:40] == list(range(40)) and out["changes"][40] == "(5 more: --rows changes)"
    assert len(out["changes"]) == 41 and out["check"] == "changed"
    ws, base = _g13_saved(tmp_path)
    many = {i: AREA for i in range(1, 4)}
    marks(ws, "shipping", "building/platform-windows", WINDOWS, many)
    saved = ws / "areas" / AREA / "unmeasured.json"
    data = json.loads(saved.read_text())
    data["marked_here"] = [{"speciality": "x/y", "n": i, "text": f"t{i}", "marked_by": ["s"]} for i in range(60)]
    saved.write_text(json.dumps(data))
    r = subprocess.run(base + ["--check"], capture_output=True, text=True)
    out = json.loads(r.stdout)
    assert r.returncode == 1 and len(out["changes"]) <= 41, r.stderr
    rows = [c for c in out["changes"] if c["path"] == "marked_here"][0]
    assert len(rows["removed"]) <= 41 and rows["removed"][-1].endswith("more: --rows changes)"), rows
