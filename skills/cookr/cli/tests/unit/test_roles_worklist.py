"""`cookr roles worklist` (modules/convert_roles.py, core/worklist.py).

cookr inventories the cookbook; who reviews what, the batches and the topics
still to write arrive in three input files the caller writes."""

from __future__ import annotations

import json

import pytest

from cookr.cli import main
from cookr.core.artifact import Artifact, Part, write_folder

_N = iter(range(1, 10_000))
BATCHES = {"labels": {"sec": "Security", "lang": "Language", "net": "Networking", "rest": "The rest"},
           "areas": {"security": "sec", "language": "lang", "networking": "net"}, "default": "rest"}


def _guideline(cookbook, rel, body="Indexes keep reads fast.\n\nJoins need them.\n", roled=False):
    parts = [
        Part("intro", f"# T\n\n{body}\n"),
        Part("rules", "\n- **must-x**: X MUST hold.\n\n", "Rules", "rules" if roled else None),
        Part("history", "\n| Version | Date | Author | Summary |\n|---|---|---|---|\n"
                        "| 1.0.0 | 2026-01-01 | A | first |\n", "Change History"),
    ]
    folder = cookbook / "guidelines" / rel
    uid = f"6f1c1e2a-0000-4000-8000-{next(_N):012d}"
    write_folder(Artifact(meta={"id": uid, "type": "guideline", "title": "T",
                                "version": "1.0.0", "modified": "2026-01-01"}, parts=parts), folder)
    return folder


def _a(speciality, topic, case="direct", specialists=("s",)):
    return {"speciality": speciality, "case": case, "specialists": list(specialists),
            "topic": f"guidelines/{topic}" if topic else None}


def _new(path, kind, specialities=(), owner=False):
    return {"path": f"guidelines/{path}", "kind": kind, "specialities": list(specialities),
            "owner_decision": owner}


def _files(tmp_path, assignments=(), covers=(), new_rows=(), batches=None, specialities=None):
    declared = specialities if specialities is not None else sorted(
        {a["speciality"] for a in assignments} | {c["speciality"] for c in covers}
        | {c["via"] for c in covers} | {s for r in new_rows for s in r["specialities"]}) or ["unused"]
    if specialities is None and declared == ["unused"]:     # the map may not be empty: one principle
        principle = tmp_path / "cookbook" / "principles" / "unused"
        principle.mkdir(parents=True, exist_ok=True)
        (principle / "artifact.json").write_text("{}", encoding="utf-8")
        assignments = [{**_a("unused", None), "topic": "principles/unused"}]
    paths = {}
    for name, data in (("map", {"specialities": declared, "assignments": list(assignments),
                                "covers": list(covers)}),
                       ("batches", batches if batches is not None else BATCHES),
                       ("new-rows", {"rows": list(new_rows)})):
        paths[name] = tmp_path / f"{name}.json"
        paths[name].write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return paths


def _argv(tmp_path, paths, *extra):
    return ["roles", "worklist", "--cookbook", str(tmp_path / "cookbook"), "--map", str(paths["map"]),
            "--batches", str(paths["batches"]), "--new-rows", str(paths["new-rows"]), *extra]


def _run(tmp_path, capsys, **kw):
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    paths = _files(tmp_path, **kw)
    capsys.readouterr()
    assert main(_argv(tmp_path, paths, "--json")) == 0
    return json.loads(capsys.readouterr().out)


def _fails(tmp_path, capsys, paths=None, **kw):
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    paths = paths or _files(tmp_path, **kw)
    capsys.readouterr()
    assert main(_argv(tmp_path, paths, "--json")) == 2
    captured = capsys.readouterr()
    assert "Traceback" not in captured.err
    return "".join((captured.out + captured.err).split())   # rich wraps long lines


def _has(msg, text):
    return "".join(text.split()) in msg


def _topics(out):
    return {r["topic"]: r for b in out["batches"] for r in b["topics"]}


# ── survivors and homes ──────────────────────────────────────────────────────

def test_worklist_picks_the_implementing_copy_as_survivor(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "reviewing/security/cors")
    _guideline(cookbook, "planning/security/cors")
    _guideline(cookbook, "implementing/security/cors")
    out = _run(tmp_path, capsys, assignments=[_a("security/cors", "reviewing/security/cors")])
    row = _topics(out)["cors"]
    assert row["survivor"] == "guidelines/implementing/security/cors"
    assert [c["folder"] for c in row["copies"]] == ["guidelines/planning/security/cors",
                                                   "guidelines/reviewing/security/cors"]
    assert out["counts"]["topics"] == 1 and out["counts"]["copies"] == 2


def test_worklist_ranks_reviewing_after_every_other_use_case(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "reviewing/security/cors")
    _guideline(cookbook, "storytelling/cors")
    row = _topics(_run(tmp_path, capsys))["cors"]
    assert row["survivor"] == "guidelines/storytelling/cors"
    assert [c["folder"] for c in row["copies"]] == ["guidelines/reviewing/security/cors"]


def test_worklist_moves_a_solo_reviewing_folder_to_implementing(tmp_path, capsys):
    _guideline(tmp_path / "cookbook", "reviewing/language/law-of-demeter")
    row = _topics(_run(tmp_path, capsys))["law-of-demeter"]
    assert row["survivor"] == "guidelines/reviewing/language/law-of-demeter"
    assert row["new_home"] == "guidelines/implementing/language/law-of-demeter"
    assert row["batch"] == "lang"


def test_worklist_takes_a_new_home_and_a_batch_from_an_override(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "reviewing/review-report-writing")
    _guideline(cookbook, "shipping/supply-chain-integrity")
    batches = {**BATCHES, "overrides": {
        "guidelines/reviewing/review-report-writing":
            {"new_home": "guidelines/implementing/code-review/review-report-writing"},
        "guidelines/shipping/supply-chain-integrity": {"batch": "sec"}}}
    topics = _topics(_run(tmp_path, capsys, batches=batches))
    assert topics["review-report-writing"]["new_home"] == \
        "guidelines/implementing/code-review/review-report-writing"
    assert topics["supply-chain-integrity"]["batch"] == "sec"
    assert "new_home" not in topics["supply-chain-integrity"]


def test_worklist_ignores_folders_under_versions(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    folder = _guideline(cookbook, "implementing/security/cors")
    _guideline(cookbook, "implementing/security/cors/versions/1.0.2")
    assert folder.joinpath("versions", "1.0.2", "artifact.json").is_file()
    out = _run(tmp_path, capsys)
    assert set(_topics(out)) == {"cors"} and out["counts"]["copies"] == 0


def test_worklist_ignores_folders_under_research(tmp_path, capsys):
    # review f10: an artifact kept in a topic's research/ is source material, never a copy of the topic
    cookbook = tmp_path / "cookbook"
    folder = _guideline(cookbook, "implementing/security/cors")
    _guideline(cookbook, "implementing/security/cors/research/cors")
    assert folder.joinpath("research", "cors", "artifact.json").is_file()
    out = _run(tmp_path, capsys)
    assert set(_topics(out)) == {"cors"} and out["counts"]["copies"] == 0


# ── devteam and authored ─────────────────────────────────────────────────────

def test_worklist_marks_a_topic_without_a_speciality_as_authored(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/security/cors")
    _guideline(cookbook, "implementing/security/csrf")
    out = _run(tmp_path, capsys, assignments=[_a("security/cors", "implementing/security/cors")])
    topics = _topics(out)
    assert topics["csrf"]["devteam"] == "authored"
    assert topics["cors"]["devteam"] == [{"speciality": "security/cors", "case": "direct",
                                          "specialists": ["s"]}]
    assert out["counts"]["authored"] == 1


def test_worklist_reports_roled_from_the_survivor(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/data/indexing", roled=True)
    _guideline(cookbook, "planning/data/indexing")
    out = _run(tmp_path, capsys)
    assert _topics(out)["indexing"]["roled"] is True
    assert out["counts"]["roled"] == 1


def test_worklist_lists_a_shared_different_speciality_only_on_its_new_topic(tmp_path, capsys):
    _guideline(tmp_path / "cookbook", "implementing/code-quality/atomic-commits")
    topic = "implementing/code-quality/atomic-commits"
    out = _run(tmp_path, capsys,
               assignments=[_a("code-quality/atomic-commits", topic, "shared-different"),
                            _a("code-quality/version-discipline", topic, "shared-different")],
               new_rows=[_new("implementing/code-quality/version-discipline", "shared-different",
                              ["code-quality/version-discipline"])])
    topics = _topics(out)
    assert [d["speciality"] for d in topics["atomic-commits"]["devteam"]] == ["code-quality/atomic-commits"]
    new = topics["version-discipline"]
    assert new["new"] is True and new["kind"] == "shared-different"
    assert new["survivor"] == "guidelines/implementing/code-quality/version-discipline"
    assert [d["speciality"] for d in new["devteam"]] == ["code-quality/version-discipline"]


def test_worklist_adds_new_rows_for_a_checklist_and_a_variant(tmp_path, capsys):
    _guideline(tmp_path / "cookbook", "implementing/networking/timeouts")
    out = _run(tmp_path, capsys,
               assignments=[_a("security/security-compliance", None, "checklist"),
                            _a("api/timeouts", "implementing/networking/timeouts", "variant"),
                            _a("api/timeouts-client", "implementing/networking/timeouts", "variant")],
               new_rows=[_new("implementing/security/security-compliance", "checklist",
                              ["security/security-compliance"]),
                         _new("implementing/networking/timeouts-client", "variant",
                              ["api/timeouts-client"])])
    topics = _topics(out)
    checklist = topics["security-compliance"]
    assert checklist["new"] and checklist["kind"] == "checklist" and checklist["batch"] == "sec"
    assert checklist["devteam"] == [{"speciality": "security/security-compliance", "case": "checklist",
                                     "specialists": ["s"]}]
    variant = topics["timeouts-client"]
    assert variant["survivor"] == "guidelines/implementing/networking/timeouts-client"
    assert [d["speciality"] for d in variant["devteam"]] == ["api/timeouts-client"]
    assert [d["speciality"] for d in topics["timeouts"]["devteam"]] == ["api/timeouts"]
    assert out["counts"]["topics"] == 1
    assert out["counts"]["new"] == {"checklist": 1, "variant": 1}


def test_worklist_marks_owner_decisions_from_the_new_rows(tmp_path, capsys):
    (tmp_path / "cookbook" / "principles" / "x").mkdir(parents=True)
    (tmp_path / "cookbook" / "principles" / "x" / "artifact.json").write_text("{}")
    a = _a("ui-ux/least-astonishment", None, "shared-different")
    a["topic"] = "principles/x"
    out = _run(tmp_path, capsys, assignments=[a, {**a, "speciality": "api/other"}],
               new_rows=[_new("implementing/ui/least-astonishment", "shared-different",
                              ["ui-ux/least-astonishment"], owner=True)])
    owner = {r["topic"] for b in out["batches"] for r in b["topics"] if r["owner_decision"]}
    assert owner == {"least-astonishment"}
    assert out["counts"]["owner_decision"] == 1
    assert out["counts"]["assignments_outside_the_guidelines"] == 1


# ── copies ───────────────────────────────────────────────────────────────────

def test_worklist_flags_an_identical_copy_and_a_differing_one(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/ui/color")
    _guideline(cookbook, "reviewing/ui/color")
    _guideline(cookbook, "shipping/color", body="Something else entirely.\n\nNothing alike here.\n")
    out = _run(tmp_path, capsys)
    copies = {c["folder"]: c for c in _topics(out)["color"]["copies"]}
    assert copies["guidelines/reviewing/ui/color"]["identical"] is True
    assert copies["guidelines/reviewing/ui/color"]["exact"] is True
    assert copies["guidelines/shipping/color"]["identical"] is False
    assert copies["guidelines/shipping/color"]["exact"] is False
    assert out["counts"]["copies_identical"] == 1 and out["counts"]["copies_differing"] == 1


def _lines(n, changed):
    return "".join(f"Line {i} {'changed' if i < changed else 'same'}.\n\n" for i in range(n))


@pytest.mark.parametrize("changed, identical", [(2, True), (3, False)])
def test_worklist_calls_a_copy_identical_from_a_ratio_of_0_9(tmp_path, capsys, changed, identical):
    # 10 lines of body plus the shared frame: 2 changed lines leave the ratio
    # above 0.9, 3 leave it below; neither copy is byte-equal.
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/ui/color", body=_lines(10, 0))
    _guideline(cookbook, "reviewing/ui/color", body=_lines(10, changed))
    copy = _topics(_run(tmp_path, capsys))["color"]["copies"][0]
    assert copy["exact"] is False
    assert copy["identical"] is identical
    assert (copy["similarity"] >= 0.9) is identical


def test_worklist_marks_copies_to_check_before_folding(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/ui/color")
    _guideline(cookbook, "reviewing/ui/color")
    _guideline(cookbook, "cookbook/ui/color")
    _guideline(cookbook, "shipping/color", body=_lines(30, 30))
    out = _run(tmp_path, capsys, batches={**BATCHES, "fold_check": ["guidelines/cookbook/ui/color"]})
    check = {c["folder"]: c["fold_check"] for c in _topics(out)["color"]["copies"]}
    assert check == {"guidelines/cookbook/ui/color": True, "guidelines/reviewing/ui/color": False,
                     "guidelines/shipping/color": True}
    assert out["counts"]["copies_fold_check"] == 2


# ── batches ──────────────────────────────────────────────────────────────────

def test_worklist_groups_topics_into_the_batches_by_area(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/security/cors")
    _guideline(cookbook, "implementing/language/swift")
    _guideline(cookbook, "implementing/networking/timeouts")
    _guideline(cookbook, "testing/test-data")
    out = _run(tmp_path, capsys)
    batch_of = {r["topic"]: b["batch"] for b in out["batches"] for r in b["topics"]}
    assert batch_of == {"cors": "sec", "swift": "lang", "timeouts": "net", "test-data": "rest"}
    assert [b["name"] for b in out["batches"]] == ["Security", "Language", "Networking", "The rest"]


def test_worklist_maps_a_building_speciality_to_its_specialists_topics(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/security/cors")
    _guideline(cookbook, "reviewing/security/cors")
    out = _run(tmp_path, capsys,
               assignments=[_a("security/cors", "reviewing/security/cors", specialists=("security",)),
                            _a("security/security-compliance", None, "checklist", ("security",))],
               covers=[{"speciality": "building/security", "specialist": "security", "via": v}
                       for v in ("security/cors", "security/security-compliance")],
               new_rows=[_new("implementing/security/security-compliance", "checklist",
                              ["security/security-compliance"])])
    building = {(r["speciality"], r["topic"]) for b in out["batches"] for r in b["building"]}
    assert building == {("building/security", "guidelines/implementing/security/cors"),
                        ("building/security", "guidelines/implementing/security/security-compliance")}
    assert out["counts"]["building"] == 2


def test_worklist_lists_a_building_speciality_once_per_topic(tmp_path, capsys):
    cookbook = tmp_path / "cookbook"
    _guideline(cookbook, "implementing/security/cors")
    out = _run(tmp_path, capsys,
               assignments=[_a("security/cors", "implementing/security/cors", "shared-same"),
                            _a("web/cors", "implementing/security/cors", "shared-same")],
               covers=[{"speciality": "building/security", "specialist": "security", "via": "security/cors"},
                       {"speciality": "building/security", "specialist": "web", "via": "web/cors"}])
    assert out["counts"]["building"] == 1


# ── input files ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("which", ["map", "batches", "new-rows"])
def test_worklist_names_a_missing_input_file(tmp_path, capsys, which):
    paths = _files(tmp_path)
    paths[which].unlink()
    msg = _fails(tmp_path, capsys, paths)
    assert _has(msg, f"--{which}") and _has(msg, "no such file")


@pytest.mark.parametrize("which", ["map", "batches", "new-rows"])
def test_worklist_names_an_input_file_that_is_not_json(tmp_path, capsys, which):
    paths = _files(tmp_path)
    paths[which].write_text("{not json", encoding="utf-8")
    msg = _fails(tmp_path, capsys, paths)
    assert _has(msg, f"--{which}") and _has(msg, "not JSON")


@pytest.mark.parametrize("data, says", [
    ([], "must be an object"),
    ({"specialities": [], "assignments": [], "covers": []}, "non-empty"),
    ({"specialities": ["a"], "assignments": [{"speciality": "a"}], "covers": []}, "needs `case`"),
    ({"specialities": ["a"], "assignments": "x", "covers": []}, "must be a list"),
])
def test_worklist_names_a_malformed_map(tmp_path, capsys, data, says):
    paths = _files(tmp_path)
    paths["map"].write_text(json.dumps(data), encoding="utf-8")
    msg = _fails(tmp_path, capsys, paths)
    assert _has(msg, str(paths["map"])) and _has(msg, says)


def test_worklist_refuses_a_speciality_on_no_topic(tmp_path, capsys):
    _guideline(tmp_path / "cookbook", "implementing/security/cors")
    msg = _fails(tmp_path, capsys, assignments=[_a("security/cors", "implementing/security/cors")],
                 specialities=["security/cors", "security/orphan", "security/also-orphan"])
    assert _has(msg, "assigned to no topic or new row: security/also-orphan, security/orphan")


def test_worklist_refuses_a_checklist_no_new_row_claims(tmp_path, capsys):
    msg = _fails(tmp_path, capsys, assignments=[_a("security/security-compliance", None, "checklist")])
    assert _has(msg, "assigned to no topic or new row: security/security-compliance")


def test_worklist_refuses_a_topic_the_cookbook_does_not_hold(tmp_path, capsys):
    _guideline(tmp_path / "cookbook", "implementing/security/cors")
    msg = _fails(tmp_path, capsys, assignments=[_a("security/cors", "implementing/security/cors"),
                                                _a("security/gone", "implementing/security/gone")])
    assert _has(msg, "topics in neither the cookbook nor --new-rows: guidelines/implementing/security/gone")


def test_worklist_refuses_an_undeclared_speciality(tmp_path, capsys):
    _guideline(tmp_path / "cookbook", "implementing/security/cors")
    msg = _fails(tmp_path, capsys, assignments=[_a("security/cors", "implementing/security/cors"),
                                                _a("security/extra", "implementing/security/cors")],
                 specialities=["security/cors"])
    assert _has(msg, "specialities not declared: security/extra")


def test_worklist_refuses_an_unknown_batch_key(tmp_path, capsys):
    msg = _fails(tmp_path, capsys, batches={**BATCHES, "areas": {"security": "nope"}})
    assert _has(msg, "batch keys not in `labels`: nope")


def test_worklist_refuses_a_fold_check_folder_that_is_no_copy(tmp_path, capsys):
    _guideline(tmp_path / "cookbook", "implementing/ui/color")
    msg = _fails(tmp_path, capsys, batches={**BATCHES, "fold_check": ["guidelines/cookbook/ui/color"]})
    assert _has(msg, "fold_check folders that are no copy: guidelines/cookbook/ui/color")


def test_worklist_refuses_out_into_a_missing_directory(tmp_path, capsys):
    (tmp_path / "cookbook").mkdir()
    paths = _files(tmp_path)
    capsys.readouterr()
    assert main(_argv(tmp_path, paths, "--out", str(tmp_path / "nowhere" / "w.json"))) == 2
    captured = capsys.readouterr()
    assert "Traceback" not in captured.err
    assert _has("".join((captured.out + captured.err).split()), "nowhere/w.json: no directory")
