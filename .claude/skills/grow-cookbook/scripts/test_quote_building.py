"""quote_building.py: a building speciality's text quoted once, each sentence
marked this area's or another named area's, nothing dropped (E3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import quote_building as qb  # noqa: E402

TEXT = Path(__file__).resolve().parent / "fixtures" / "building" / "building--devops-observability.txt"
AREA = "implementing/feature-management"
FAIL_FAST = 7  # "Read every value that varies per deploy …"


def repo(tmp: Path) -> Path:
    for a in (AREA, "implementing/observability", "shipping/deployment"):
        (tmp / "cookbook" / "guidelines" / a).mkdir(parents=True, exist_ok=True)
    return tmp


def test_sentences_keep_every_word_and_drop_only_blank_lines():
    text = TEXT.read_text(encoding="utf-8")
    sentences = qb.sentences(text)
    assert len(sentences) == 10
    assert " ".join(sentences).split() == text.split()
    assert sentences[FAIL_FAST - 1].startswith("Read every value that varies per deploy")


def marks(**overrides) -> dict:
    m = {str(n): "implementing/observability" for n in range(1, 11)}
    m[str(FAIL_FAST)] = AREA
    m.update(overrides)
    return m


def test_render_marks_each_sentence_and_lists_this_areas(tmp_path):
    out = qb.render(AREA, "building/devops-observability", TEXT, marks(**{"9": "shipping/deployment"}),
                    repo(tmp_path))
    assert out["problems"] == []
    assert [s["n"] for s in out["this_area"]] == [FAIL_FAST]
    md = out["markdown"]
    assert md.count("\n> ") == 10
    assert "[this area's]" in md and md.count("[this area's]") == 1
    assert "[implementing/observability's]" in md and "[shipping/deployment's]" in md
    assert "\n> \n" not in md


def test_an_unmarked_or_unknown_area_is_a_problem(tmp_path):
    m = marks()
    del m["3"]
    m["4"] = "nowhere/at-all"
    out = qb.render(AREA, "building/devops-observability", TEXT, m, repo(tmp_path))
    assert {p["n"] for p in out["problems"]} == {3, 4}


def test_cli_without_marks_prints_a_template_and_with_bad_marks_exits_2(tmp_path, capsys):
    r = repo(tmp_path)
    assert qb.main([AREA, "--speciality", "building/devops-observability", "--file", str(TEXT),
                    "--repo", str(r)]) == 0
    template = json.loads(capsys.readouterr().out)
    assert len(template["marks"]) == 10 and set(template["marks"].values()) == {None}
    bad = tmp_path / "marks.json"
    bad.write_text(json.dumps({"1": AREA}), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/devops-observability", "--file", str(TEXT),
                    "--repo", str(r), "--marks", str(bad)]) == 2


def test_each_list_item_is_its_own_unit():
    # m2: a list with no closing punctuation was one "sentence".
    text = ("Covers:\n- feature flags\n- kill switches. Both kinds\n* remote config\n1. rollout\n"
            "12) staged rollout\n  continued here\n\nA closing line.")
    got = qb.sentences(text)
    assert got == ["Covers:", "- feature flags", "- kill switches.", "Both kinds", "* remote config",
                   "1. rollout", "12) staged rollout continued here", "A closing line."]
    assert " ".join(got).split() == text.split()


def _template(tmp_path, capsys, *extra) -> tuple[int, dict | None, str, str]:
    capsys.readouterr()
    code = qb.main([AREA, "--speciality", "building/devops-observability", "--file", str(TEXT),
                    "--repo", str(repo(tmp_path)), *extra])
    cap = capsys.readouterr()
    return code, (json.loads(cap.out) if code == 0 else None), cap.out, cap.err


def test_a_rerun_never_wipes_marks(tmp_path, capsys):
    # 1.4.16, G22: re-running the template command rewrote A/building-<name>.json
    # with null marks. With --keep naming that file, a file holding a mark for
    # the same sentences is printed as it is (1.4.18, G38: exit 0, "marks kept"),
    # so write_on_success.py leaves it untouched.
    saved = tmp_path / "A" / "building-devops-observability.json"
    code, template, _, _ = _template(tmp_path, capsys, "--keep", str(saved))
    assert code == 0 and set(template["marks"].values()) == {None}   # no file yet
    saved.parent.mkdir()
    saved.write_text(json.dumps(template), encoding="utf-8")
    code, again, _, _ = _template(tmp_path, capsys, "--keep", str(saved))
    assert code == 0 and again == template                            # only null marks: nothing to lose
    template["marks"] = marks()
    kept = json.dumps(template, indent=1) + "\n"
    saved.write_text(kept, encoding="utf-8")
    # 1.4.18, G38: a re-run on unchanged sentences is idempotent: exit 0, and
    # stdout is the marks file byte for byte, so write_on_success.py leaves it.
    code, out, printed, said = _template(tmp_path, capsys, "--keep", str(saved))
    assert code == 0 and printed == kept and out == template
    assert "marks kept (sentences unchanged)" in said and str(saved) in said


def test_a_rerun_through_write_on_success_leaves_the_marks_file_untouched(tmp_path):
    # G38, end to end: the step-1.2 template command, run again with marks
    # present and the text unchanged, exits 0 and the file is not rewritten.
    import os
    import subprocess
    here = Path(__file__).resolve().parent
    saved = tmp_path / "A" / "building-devops-observability.json"
    saved.parent.mkdir()
    found = qb.sentences(TEXT.read_text(encoding="utf-8"))
    data = {"speciality": "building/devops-observability",
            "sentences": [{"n": n, "text": s} for n, s in enumerate(found, start=1)], "marks": marks()}
    saved.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    before = saved.read_bytes()
    os.utime(saved, (1_000_000_000, 1_000_000_000))
    r = subprocess.run([sys.executable, str(here / "write_on_success.py"), str(saved), "--",
                        sys.executable, str(here / "quote_building.py"), AREA,
                        "--speciality", "building/devops-observability", "--file", str(TEXT),
                        "--repo", str(repo(tmp_path)), "--keep", str(saved)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "marks kept (sentences unchanged)" in r.stderr
    assert saved.read_bytes() == before and saved.stat().st_mtime == 1_000_000_000
    assert sorted(p.name for p in saved.parent.iterdir()) == [saved.name]


def test_a_rerun_on_changed_text_keeps_each_unchanged_sentences_mark(tmp_path, capsys):
    saved = tmp_path / "building-devops-observability.json"
    sentences = [{"n": n, "text": s} for n, s in enumerate(qb.sentences(TEXT.read_text(encoding="utf-8")), 1)]
    old = sentences[:2] + [{"n": 3, "text": "A sentence the speciality no longer has."}] + [
        {**s, "n": s["n"] + 1} for s in sentences[2:]]
    m = {str(s["n"]): "implementing/observability" for s in old}
    m["3"] = "shipping/deployment"
    m[str(FAIL_FAST + 1)] = AREA
    saved.write_text(json.dumps({"speciality": "building/devops-observability", "sentences": old, "marks": m}),
                     encoding="utf-8")
    code, out, _, err = _template(tmp_path, capsys, "--keep", str(saved))
    assert code == 0
    assert out["sentences"] == sentences
    want = {str(n): "implementing/observability" for n in range(1, 11)}
    want[str(FAIL_FAST)] = AREA
    assert out["marks"] == want
    assert out["dropped"] == [{"n": 3, "text": "A sentence the speciality no longer has.",
                               "mark": "shipping/deployment"}]
    # 1.4.17, N3: on stderr itself (stdout's JSON holds both words too)
    assert "dropped" in err and "no longer has" in err and "old sentence 3" in err


def test_a_dropped_duplicate_is_named_as_one_occurrence(tmp_path, capsys):
    # 1.4.17, N1: the old text held a sentence twice, the new one once; the
    # text still has it, so the message must not say it is gone.
    saved = tmp_path / "building-devops-observability.json"
    found = qb.sentences(TEXT.read_text(encoding="utf-8"))
    old = [{"n": n, "text": s} for n, s in enumerate([found[0], *found], 1)]
    m = {str(s["n"]): "implementing/observability" for s in old}
    saved.write_text(json.dumps({"speciality": "building/devops-observability", "sentences": old, "marks": m}),
                     encoding="utf-8")
    code, out, _, err = _template(tmp_path, capsys, "--keep", str(saved))
    assert code == 0 and [d["n"] for d in out["dropped"]] == [2]
    assert "one occurrence of" in err and "no longer has" not in err


def test_a_corrupt_keep_file_exits_2_naming_it(tmp_path, capsys):
    # 1.4.17, N2: a corrupt --keep file gave a traceback (exit 1).
    saved = tmp_path / "building-devops-observability.json"
    for bad in ("{not json", json.dumps({"sentences": [{"n": 1, "text": "x"}]}), json.dumps([1, 2])):
        saved.write_text(bad, encoding="utf-8")
        code, out, said, err = _template(tmp_path, capsys, "--keep", str(saved))
        assert code == 2 and str(saved) in said + err and out is None


def test_no_split_after_an_abbreviation_or_inside_parentheses():
    # 1.4.24, G54: platform-android's first rule split at "(e.g." into a fragment.
    text = ("Use the platform's own controls (e.g. Material buttons). Match its back gesture, i.e. "
            "Predictive back. Cover files, keys, etc. Before release. Prefer A vs. B. Compare cf. "
            "The guide. Keep (a note. Inside parentheses) whole. Then end.")
    assert qb.sentences(text) == [
        "Use the platform's own controls (e.g. Material buttons).",
        "Match its back gesture, i.e. Predictive back.",
        "Cover files, keys, etc.",
        "Before release.",
        "Prefer A vs. B.",
        "Compare cf. The guide.",
        "Keep (a note. Inside parentheses) whole.",
        "Then end."]
    assert qb.sentences("E.g. First one. Second one.") == ["E.g. First one.", "Second one."]


def _old_split(text: str) -> list[str]:
    return [s for s in qb._END.split(" ".join(text.split())) if s]


def test_a_requote_carries_marks_across_a_rejoined_sentence_and_check_writes_nothing(tmp_path, capsys):
    # 1.4.24, G54: the new splitter renumbers marked files; marks travel by
    # text, a sentence the old splitter cut in two takes its parts' marks, and
    # --check reports every renumbering and every mark it cannot carry.
    text = ("First rule (e.g. Like this). Second rule stays. Gone soon (i.e. Both). Last one.")
    src = tmp_path / "s.md"
    src.write_text(text, encoding="utf-8")
    old = _old_split(text)
    assert len(old) == 6 and len(qb.sentences(text)) == 4
    marks = {"1": AREA, "2": AREA, "3": "implementing/observability",
             "4": AREA, "5": "shipping/deployment", "6": None}
    saved = tmp_path / "building-s.json"
    body = json.dumps({"speciality": "building/s", "sentences": [{"n": n, "text": t} for n, t in
                                                                 enumerate(old, 1)], "marks": marks})
    saved.write_text(body, encoding="utf-8")
    code = qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--repo", str(repo(tmp_path)),
                    "--keep", str(saved), "--check"])
    out = json.loads(capsys.readouterr().out)
    assert code == 1 and saved.read_text(encoding="utf-8") == body
    assert out["renumbered"] is True and out["old_count"] == 6 and out["new_count"] == 4
    assert out["marks"] == {"1": AREA, "2": "implementing/observability",
                            "3": [AREA, "shipping/deployment"], "4": None}
    assert out["joined"] == [{"n": 1, "from": [1, 2], "mark": AREA},
                             {"n": 3, "from": [4, 5], "mark": [AREA, "shipping/deployment"]}]
    assert out["lost"] == []
    # unchanged sentences: nothing to report, exit 0
    same = tmp_path / "building-t.json"
    found = qb.sentences(text)
    same.write_text(json.dumps({"speciality": "building/s", "sentences": [{"n": n, "text": t} for n, t in
                                                                          enumerate(found, 1)],
                                "marks": {"1": AREA}}), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(same), "--check"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["renumbered"] is False and out["lost"] == [] and out["joined"] == []


def test_check_reports_a_mark_it_cannot_carry(tmp_path, capsys):
    src = tmp_path / "s.md"
    src.write_text("Only this now.", encoding="utf-8")
    saved = tmp_path / "building-s.json"
    saved.write_text(json.dumps({"speciality": "building/s", "sentences": [{"n": 1, "text": "Gone."},
                                                                           {"n": 2, "text": "Only this now."}],
                                 "marks": {"1": AREA, "2": AREA}}), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(saved), "--check"]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["lost"] == [{"n": 1, "text": "Gone.", "mark": AREA}]


def test_a_mark_may_name_several_areas(tmp_path):
    # 1.4.24, G55: platform-windows 1 holds a UI clause and MSIX packaging.
    src = tmp_path / "s.md"
    src.write_text("One sentence. Two sentence.", encoding="utf-8")
    out = qb.render(AREA, "building/s", src, {"1": [AREA, "shipping/deployment"], "2": ["nowhere/x"]},
                    repo(tmp_path))
    assert out["this_area"] == [{"n": 1, "text": "One sentence."}]
    assert "> 1. One sentence. [this area's, shipping/deployment's]" in out["markdown"]
    assert out["problems"] == [{"n": 2, "why": "nowhere/x is no area of cookbook/guidelines/"}]


def test_etc_ends_a_sentence_unless_the_next_starts_lowercase_or_closes():
    # fix round 1, I2: `etc.` can end a sentence; joining after it always hid
    # the next sentence inside this one.
    assert qb.sentences("Use A, B, etc. Then run C.") == ["Use A, B, etc.", "Then run C."]
    # fix round 2, N-C: no cut is ever made before lowercase or a closing
    # mark, so `etc.` never joins: a cut after it always stands.
    assert qb.sentences("Use A, B, etc. and C.") == ["Use A, B, etc. and C."]
    assert qb._rejoin(["Use A, B, etc.", "and C."]) == ["Use A, B, etc.", "and C."]
    assert qb._rejoin(["Use A (e.g.", "B, etc.", "Then C)."]) == ["Use A (e.g. B, etc. Then C)."]


def test_a_parenthesis_never_closed_in_its_unit_joins_nothing():
    # fix round 1, I2: an open parenthesis closes at the end of its unit, so an
    # unbalanced one never swallows the sentences after it.
    assert qb.sentences("Keep it short (see A. Then B. Done.") == ["Keep it short (see A.", "Then B.", "Done."]
    assert qb.sentences("Keep (a note. Inside) whole. Then (one. Two. Three.") == [
        "Keep (a note. Inside) whole.", "Then (one.", "Two.", "Three."]


def test_a_requote_carries_each_copy_of_a_repeated_sentence_in_order(tmp_path):
    # fix round 1, M3: two sentences of one text each keep their own mark, in
    # order; a copy the new text no longer has is dropped, named as such.
    keep = tmp_path / "building-s.json"
    old = ["Same rule here.", "Middle one.", "Same rule here.", "Tail."]
    keep.write_text(json.dumps({"speciality": "building/s",
                                "sentences": [{"n": n, "text": s} for n, s in enumerate(old, 1)],
                                "marks": {"1": AREA, "2": "shipping/deployment", "3": "implementing/observability",
                                          "4": AREA}}), encoding="utf-8")
    out, said = qb.template("building/s", ["Same rule here.", "New one.", "Same rule here.", "Tail."], keep)
    assert out["marks"] == {"1": AREA, "2": None, "3": "implementing/observability", "4": AREA}
    assert out["dropped"] == [{"n": 2, "text": "Middle one.", "mark": "shipping/deployment"}]
    out, said = qb.template("building/s", ["Same rule here.", "Middle one.", "Tail."], keep)
    assert out["marks"] == {"1": AREA, "2": "shipping/deployment", "3": AREA}
    assert out["dropped"] == [{"n": 3, "text": "Same rule here.", "mark": "implementing/observability"}]
    assert "one occurrence of a sentence the text now has fewer times" in said


def test_check_says_a_text_change_without_renumbering_is_no_renumbering(tmp_path, capsys):
    # fix round 1, N1: same count, every carried sentence at its old number,
    # one text changed: `renumbered` false, the change in `changed`, exit 1.
    src = tmp_path / "s.md"
    src.write_text("First stays. Second is new. Third stays.", encoding="utf-8")
    saved = tmp_path / "building-s.json"
    saved.write_text(json.dumps({"speciality": "building/s", "sentences": [
        {"n": 1, "text": "First stays."}, {"n": 2, "text": "Second was old."}, {"n": 3, "text": "Third stays."}],
        "marks": {"1": AREA, "2": None, "3": AREA}}), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(saved), "--check"]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["renumbered"] is False and out["changed"] == [2] and out["lost"] == []
    src.write_text("Zero is new. First stays. Second was old. Third stays.", encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(saved), "--check"]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["renumbered"] is True and out["changed"] == [1]


def test_check_says_a_reorder_of_the_same_count_is_a_renumbering(tmp_path, capsys):
    # fix round 1, N1: an old sentence at another number is a renumbering even
    # when the count and every text stay.
    src = tmp_path / "s.md"
    src.write_text("Two. One.", encoding="utf-8")
    saved = tmp_path / "building-s.json"
    saved.write_text(json.dumps({"speciality": "building/s", "sentences": [
        {"n": 1, "text": "One."}, {"n": 2, "text": "Two."}], "marks": {"1": AREA, "2": None}}), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(saved), "--check"]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["renumbered"] is True and out["changed"] == []


def _ws_marks(tmp_path) -> tuple[Path, Path, Path]:
    """A workspace with this area's marks file for a two-sentence text, a
    worklist with a building entry for it, and a planned new area."""
    r = repo(tmp_path / "repo")
    ws = tmp_path / "ws"
    src = tmp_path / "s.md"
    src.write_text("One sentence. Two sentence.", encoding="utf-8")
    f = ws / "areas" / AREA / "building-s.json"
    f.parent.mkdir(parents=True)
    f.write_text(json.dumps({"speciality": "building/s", "sentences": [{"n": 1, "text": "One sentence."},
                                                                       {"n": 2, "text": "Two sentence."}],
                             "marks": {"1": AREA, "2": "shipping/release"}}), encoding="utf-8")
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": [], "building": [
        {"speciality": "building/s", "topic": f"guidelines/{AREA}/flags"},
        {"speciality": "building/s", "topic": "guidelines/shipping/deployment/rollout"}]}]}), encoding="utf-8")
    return r, ws, src


def test_a_planned_new_area_is_a_known_area(tmp_path, capsys):
    # G65 (1.4.25): an area with W/areas/<area>/area-plan.md and no cookbook
    # folder is a planned new area: no problem. The workspace is taken from
    # the marks file's path (W/areas/<area>/building-*.json) or --workspace.
    r, ws, src = _ws_marks(tmp_path)
    args = [AREA, "--speciality", "building/s", "--file", str(src), "--repo", str(r),
            "--marks", str(ws / "areas" / AREA / "building-s.json")]
    assert qb.main(args) == 2                                   # no plan yet: still a problem
    assert "shipping/release is no area" in capsys.readouterr().out
    plan = ws / "areas" / "shipping" / "release" / "area-plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# plan\n", encoding="utf-8")
    assert qb.main(args) == 0, capsys.readouterr()
    assert json.loads(capsys.readouterr().out)["problems"] == []
    out = qb.render(AREA, "building/s", src, {"1": AREA, "2": "shipping/release"}, r, workspace=ws)
    assert out["problems"] == []


def test_marks_output_names_the_topics_unmeasured_names(tmp_path, capsys):
    # G77 (1.4.25): --marks prints `topics`, this area's topics the worklist's
    # building entries reach for this speciality, as unmeasured.json's row.
    r, ws, src = _ws_marks(tmp_path)
    m = ws / "areas" / AREA / "building-s.json"
    data = json.loads(m.read_text())
    data["marks"]["2"] = AREA
    m.write_text(json.dumps(data), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--repo", str(r),
                    "--marks", str(m)]) == 0
    assert json.loads(capsys.readouterr().out)["topics"] == [f"guidelines/{AREA}/flags"]
    import unmeasured
    row = unmeasured.place(AREA, json.loads((ws / "worklist.json").read_text()),
                           [{"speciality": "building/s", "topic": None, "case": "building-split"}],
                           [{"speciality": "building/s", "topic": None, "file": None}])["building"][0]
    assert row["topics"] == [f"guidelines/{AREA}/flags"]


# 1.4.33: G111 `kept` on --check, G117 a reference not yet written.

def test_check_says_whether_every_mark_is_kept(tmp_path, capsys):
    # G111: `kept` is true when the re-quote carries every mark (nothing
    # in `lost`), an appended sentence included; false when one is lost.
    src = tmp_path / "s.md"
    src.write_text("Only this now. And a new one.", encoding="utf-8")
    saved = tmp_path / "building-s.json"
    saved.write_text(json.dumps({"speciality": "building/s", "sentences": [{"n": 1, "text": "Only this now."}],
                                 "marks": {"1": AREA}}), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(saved), "--check"]) == 1
    out = json.loads(capsys.readouterr().out)
    assert (out["kept"], out["renumbered"], out["changed"]) == (True, True, [2])
    src.write_text("And a new one.", encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(saved), "--check"]) == 1
    assert json.loads(capsys.readouterr().out)["kept"] is False


@pytest.mark.parametrize("extra", [[], ["--check", "--keep", "building-s.json"], ["--marks", "building-s.json"]])
def test_a_reference_not_yet_written_exits_2_naming_how_to_write_it(tmp_path, capsys, extra):
    # G117: --file naming a reference step 1.3 has not written yet is a clear
    # exit 2 naming speciality_reference.py, never a traceback.
    (tmp_path / "building-s.json").write_text(json.dumps({"speciality": "building/s", "sentences": [],
                                                          "marks": {}}), encoding="utf-8")
    extra = [str(tmp_path / e) if e.endswith(".json") else e for e in extra]
    code = qb.main([AREA, "--speciality", "building/s", "--file", str(tmp_path / "A/reference/s.md"),
                    "--repo", str(repo(tmp_path)), *extra])
    err = capsys.readouterr().err
    assert code == 2 and "not written yet" in err and "speciality_reference.py building/s" in err, err


# 1.4.37: G158 --speciality checked against the speciality map, G168 the KEPT
# message, the -quoted line and --quiet.

def test_an_unknown_speciality_exits_2_and_the_right_form_keeps_topics(tmp_path, capsys):
    # G158 (N9): with the workspace's speciality-map.json readable, a
    # --speciality it does not name exits 2 (`ui` for `implementing/ui` once
    # dropped `topics` silently); the mapped form prints `topics`.
    r, ws, src = _ws_marks(tmp_path)
    m = ws / "areas" / AREA / "building-s.json"
    data = json.loads(m.read_text())
    data["marks"]["2"] = AREA
    m.write_text(json.dumps(data), encoding="utf-8")
    (ws / "speciality-map.json").write_text(json.dumps([{"speciality": "building/s", "topic": None}]),
                                           encoding="utf-8")
    base = ["--file", str(src), "--repo", str(r)]
    for bad in ("nosuch", "s"):
        assert qb.main([AREA, "--speciality", bad, *base, "--marks", str(m)]) == 2
        said = capsys.readouterr()
        assert bad in said.err and "speciality-map.json" in said.err and said.out == ""
        assert qb.main([AREA, "--speciality", bad, *base, "--keep", str(m)]) == 2
        assert "speciality-map.json" in capsys.readouterr().err
    assert qb.main([AREA, "--speciality", "building/s", *base, "--marks", str(m)]) == 0
    assert json.loads(capsys.readouterr().out)["topics"] == [f"guidelines/{AREA}/flags"]


def test_the_kept_path_says_nothing_to_run(tmp_path, capsys):
    # G168 (N19): the KEPT message names no step to run.
    src = tmp_path / "s.md"
    src.write_text("One. Two.", encoding="utf-8")
    saved = tmp_path / "building-s.json"
    saved.write_text(json.dumps({"speciality": "building/s", "sentences": [{"n": 1, "text": "One."},
                                 {"n": 2, "text": "Two."}], "marks": {"1": AREA, "2": None}}), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(saved)]) == 0
    err = capsys.readouterr().err
    assert "marks kept (sentences unchanged)" in err and "nothing to run" in err and "Run" not in err, err


def test_marks_says_one_line_on_stderr_and_quiet_drops_the_markdown(tmp_path, capsys):
    # G168 (N19): the --marks run (written to A/building-<name>-quoted.json)
    # says one line on stderr; --quiet leaves the markdown out of stdout.
    r, ws, src = _ws_marks(tmp_path)
    m = ws / "areas" / AREA / "building-s.json"
    args = [AREA, "--speciality", "building/s", "--file", str(src), "--repo", str(r), "--marks", str(m)]
    (ws / "areas" / "shipping" / "release").mkdir(parents=True)
    (ws / "areas" / "shipping" / "release" / "area-plan.md").write_text("# plan\n", encoding="utf-8")
    assert qb.main(args) == 0
    said = capsys.readouterr()
    assert "markdown" in json.loads(said.out)
    assert len(said.err.strip().splitlines()) == 1 and "2 sentences" in said.err, said.err
    assert qb.main([*args, "--quiet"]) == 0
    said = capsys.readouterr()
    out = json.loads(said.out)
    assert "markdown" not in out and out["this_area"] == [{"n": 1, "text": "One sentence."}]
    assert len(said.err.strip().splitlines()) == 1


# --- gapfix11 (1.4.39) ---------------------------------------------------------------------------


def test_quiet_is_refused_when_the_quoted_file_holds_markdown(tmp_path, capsys):
    # G196 (L11): --quiet --marks would write a quoted file without the
    # `markdown` the saved A/building-<name>-quoted.json holds: refused.
    r, ws, src = _ws_marks(tmp_path)
    m = ws / "areas" / AREA / "building-s.json"
    args = [AREA, "--speciality", "building/s", "--file", str(src), "--repo", str(r), "--marks", str(m)]
    (ws / "areas" / "shipping" / "release").mkdir(parents=True)
    (ws / "areas" / "shipping" / "release" / "area-plan.md").write_text("# plan\n", encoding="utf-8")
    assert qb.main(args) == 0
    (ws / "areas" / AREA / "building-s-quoted.json").write_text(capsys.readouterr().out, encoding="utf-8")
    assert qb.main([*args, "--quiet"]) == 2
    said = capsys.readouterr()
    assert said.out == "" and "--quiet" in said.err and "markdown" in said.err, said.err


def test_a_stale_home_in_the_kept_marks_file_is_named_on_stderr(tmp_path, capsys):
    # G205 (L20): a `homes` value naming no topic of this plan is named.
    r, ws, src = _ws_marks(tmp_path)
    m = ws / "areas" / AREA / "building-s.json"
    d = json.loads(m.read_text())
    d["homes"] = {"1": "api-design"}
    m.write_text(json.dumps(d), encoding="utf-8")
    assert qb.main([AREA, "--speciality", "building/s", "--file", str(src), "--keep", str(m),
                    "--repo", str(r)]) == 0
    err = capsys.readouterr().err
    assert "stale_home" in err and "api-design" in err, err
