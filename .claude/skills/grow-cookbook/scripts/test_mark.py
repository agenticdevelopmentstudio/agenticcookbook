"""mark.py: set one building sentence's mark, validated (G55, 1.4.24)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mark  # noqa: E402

AREA = "implementing/ui"


def setup(tmp: Path) -> tuple[Path, Path, Path]:
    repo = tmp / "repo"
    for a in (AREA, "shipping/packaging"):
        (repo / "cookbook" / "guidelines" / a).mkdir(parents=True)
    ws = tmp / "ws"
    f = ws / "areas" / AREA / "building-platform-windows.json"
    f.parent.mkdir(parents=True)
    f.write_text(json.dumps({"speciality": "building/platform-windows",
                             "sentences": [{"n": 1, "text": "Use WinUI and ship MSIX."}, {"n": 2, "text": "Two."}],
                             "marks": {"1": None, "2": None}}), encoding="utf-8")
    return repo, ws, f


def call(repo, ws, *extra) -> list[str]:
    return [AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/platform-windows", *extra]


def test_one_area_is_a_path_and_several_a_list(tmp_path, capsys):
    repo, ws, f = setup(tmp_path)
    assert mark.main(call(repo, ws, "--n", "2", "--to", AREA)) == 0
    assert json.loads(f.read_text())["marks"] == {"1": None, "2": AREA}
    assert mark.main(call(repo, ws, "--n", "1", "--to", "shipping/packaging", AREA)) == 0
    data = json.loads(f.read_text())
    assert data["marks"]["1"] == [AREA, "shipping/packaging"]
    assert data["sentences"][0]["text"] == "Use WinUI and ship MSIX."
    assert mark.main(call(repo, ws, "--n", "1", "--clear")) == 0
    assert json.loads(f.read_text())["marks"]["1"] is None


def test_it_prints_what_it_changed(tmp_path, capsys):
    repo, ws, f = setup(tmp_path)
    assert mark.main(call(repo, ws, "--n", "1", "--to", AREA)) == 0
    assert json.loads(capsys.readouterr().out) == {"file": str(f), "n": 1, "text": "Use WinUI and ship MSIX.",
                                                   "was": None, "now": AREA}


def test_bad_input_exits_2_and_writes_nothing(tmp_path, capsys):
    repo, ws, f = setup(tmp_path)
    before = f.read_text()
    assert mark.main(call(repo, ws, "--n", "3", "--to", AREA)) == 2
    assert "no sentence 3" in capsys.readouterr().err
    assert mark.main(call(repo, ws, "--n", "1", "--to", "nowhere/x")) == 2
    assert "nowhere/x" in capsys.readouterr().err
    other = [AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/missing",
             "--n", "1", "--to", AREA]
    assert mark.main(other) == 2
    assert "building-missing.json" in capsys.readouterr().err
    f2 = ws / "areas" / AREA / "building-x.json"
    f2.write_text(json.dumps({"speciality": "building/other", "sentences": [], "marks": {}}), encoding="utf-8")
    bad = [AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/x", "--n", "1", "--to", AREA]
    assert mark.main(bad) == 2
    assert "building/other" in capsys.readouterr().err
    assert f.read_text() == before


def test_it_runs_from_any_directory(tmp_path):
    repo, ws, f = setup(tmp_path)
    r = subprocess.run([sys.executable, "-I", str(HERE / "mark.py"), *call(repo, ws, "--n", "2", "--to", AREA)],
                       capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert json.loads(f.read_text())["marks"]["2"] == AREA


def test_a_planned_new_area_is_accepted_and_an_unknown_one_refused(tmp_path, capsys):
    # G65 (1.4.25): an area with no cookbook folder but a plan at
    # W/areas/<area>/area-plan.md is a planned new area: accepted. One with
    # neither is still refused.
    repo, ws, f = setup(tmp_path)
    plan = ws / "areas" / "shipping" / "release" / "area-plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# plan\n", encoding="utf-8")
    assert mark.main(call(repo, ws, "--n", "1", "--to", "shipping/release")) == 0
    assert json.loads(f.read_text())["marks"]["1"] == "shipping/release"
    before = f.read_text()
    assert mark.main(call(repo, ws, "--n", "2", "--to", "shipping/nowhere")) == 2
    assert "shipping/nowhere" in capsys.readouterr().err and f.read_text() == before


def test_many_marks_in_one_call_are_all_validated_before_any_write(tmp_path, capsys):
    # G70 (1.4.25): repeatable `--mark n=area[,area]` (empty after `=`
    # clears); every mark is checked before the file is written.
    repo, ws, f = setup(tmp_path)
    assert mark.main(call(repo, ws, "--mark", f"1={AREA},shipping/packaging", "--mark", f"2={AREA}")) == 0
    assert json.loads(f.read_text())["marks"] == {"1": [AREA, "shipping/packaging"], "2": AREA}
    out = json.loads(capsys.readouterr().out)
    assert out["file"] == str(f)
    assert out["marks"] == [{"n": 1, "text": "Use WinUI and ship MSIX.", "was": None, "now": [AREA, "shipping/packaging"]},
                            {"n": 2, "text": "Two.", "was": None, "now": AREA}]
    before = f.read_text()
    for bad, why in ((["--mark", "1=", "--mark", "3=" + AREA], "no sentence 3"),
                     (["--mark", "1=", "--mark", "2=nowhere/x"], "nowhere/x"),
                     (["--mark", "x=" + AREA], "x="),
                     (["--mark", "1=", "--mark", "1=" + AREA], "twice")):
        assert mark.main(call(repo, ws, *bad)) == 2, bad
        assert why in capsys.readouterr().err
        assert f.read_text() == before, bad
    assert mark.main(call(repo, ws, "--mark", "1=", "--mark", "2=")) == 0
    assert json.loads(f.read_text())["marks"] == {"1": None, "2": None}


def test_a_home_is_recorded_cleared_and_checked_before_any_write(tmp_path, capsys):
    # G145 (1.4.36): --home N=TOPIC records the plan's chosen home in `homes`;
    # G156 (1.4.37): TOPIC is a topic of this plan (here: a folder holding artifact.json).
    repo, ws, f = setup(tmp_path)
    for t in ("windows-ui", "packaging"):
        (repo / "cookbook" / "guidelines" / AREA / t).mkdir()
        (repo / "cookbook" / "guidelines" / AREA / t / "artifact.json").write_text("{}")
    _report(ws, home_unguessed=[{"speciality": "building/platform-windows", "n": n} for n in (1, 2)])   # G203
    assert mark.main(call(repo, ws, "--home", "1=windows-ui", "--home", "2=packaging")) == 0
    assert json.loads(f.read_text())["homes"] == {"1": "windows-ui", "2": "packaging"}
    assert json.loads(f.read_text())["marks"] == {"1": None, "2": None}
    before = f.read_bytes()
    for bad in (["--home", "3=x"], ["--home", "1=a/b"], ["--home", "x=t"], ["--home", "1=windows-ui", "--home", "1=packaging"],
                ["--home", "1=nosuch"], ["--home", "1=shipping/packaging:nosuch"]):
        assert mark.main(call(repo, ws, *bad)) == 2 and f.read_bytes() == before, bad
    assert mark.main(call(repo, ws, "--home", "1=")) == 0
    assert json.loads(f.read_text())["homes"] == {"2": "packaging"}
    before = f.read_bytes()
    for mixed in (["--mark", "1=implementing/ui"], ["--n", "1", "--clear"]):      # --home goes alone
        with pytest.raises(SystemExit) as e:
            mark.main(call(repo, ws, "--home", "1=windows-ui", *mixed))
        assert e.value.code == 2 and f.read_bytes() == before, mixed


def test_a_home_in_another_area_needs_no_marks_file_here(tmp_path, capsys):
    # G156 (N7): N=AREA:TOPIC goes in A/homes.json, checked against that area's
    # topics and, with no marks file here, against the saved report's sentences.
    repo, ws, f = setup(tmp_path)
    (repo / "cookbook" / "guidelines" / "shipping" / "packaging" / "msix").mkdir()
    (repo / "cookbook" / "guidelines" / "shipping" / "packaging" / "msix" / "artifact.json").write_text("{}")
    (ws / "areas" / AREA / "run_gaps.json").write_text(json.dumps(
        {"home_unguessed": [{"speciality": "building/ops", "n": 4}]}), encoding="utf-8")
    ops = [AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/ops"]
    hf = ws / "areas" / AREA / "homes.json"
    for bad in ("4=shipping/packaging:nosuch", "4=nosuch/area:msix", "5=shipping/packaging:msix", "4=msix"):
        assert mark.main([*ops, "--home", bad]) == 2 and not hf.exists(), bad
    assert mark.main([*ops, "--home", "4=shipping/packaging:msix"]) == 0
    assert json.loads(hf.read_text()) == {"building/ops": {"4": "shipping/packaging:msix"}}
    assert mark.main([*ops, "--home", "4="]) == 0
    assert json.loads(hf.read_text()) == {}


# --- gapfix11 (1.4.39) ---------------------------------------------------------------------------


def _report(ws: Path, **rows) -> Path:
    rp = ws / "areas" / AREA / "run_gaps.json"
    rp.write_text(json.dumps({"home_unguessed": [], "held_by_wording": [], "building": [], **rows}))
    return rp


def test_home_needs_speciality_and_says_give_speciality(tmp_path, capsys):
    # G204 (L19): the exit-2 message names the missing flag.
    repo, ws, f = setup(tmp_path)
    with pytest.raises(SystemExit) as e:
        mark.main([AREA, "--workspace", str(ws), "--repo", str(repo), "--home", "1=x"])
    assert e.value.code == 2 and "give --speciality" in capsys.readouterr().err


def test_home_takes_any_building_sentence_of_the_report_and_refuses_one_it_does_not_list(tmp_path, capsys):
    # G203 (L18), L8 (1.4.40): a home is recorded for a home_unguessed row, a home_measures sentence or a
    # sentence with a home_guess (run_gaps.py reads it for each); a sentence the report does not list, or lists
    # with none of those, is still refused, naming the report.
    repo, ws, f = setup(tmp_path)
    (repo / "cookbook" / "guidelines" / AREA / "lists").mkdir()
    (repo / "cookbook" / "guidelines" / AREA / "lists" / "artifact.json").write_text("{}")
    d = json.loads(f.read_text())
    d["sentences"] += [{"n": 3, "text": "Three."}, {"n": 4, "text": "Four."}]
    d["marks"].update({"3": None, "4": None})
    f.write_text(json.dumps(d))
    before = f.read_bytes()
    assert mark.main(call(repo, ws, "--home", "1=lists")) == 2      # no saved report: nothing to check against
    assert "run_gaps" in capsys.readouterr().err and f.read_bytes() == before
    _report(ws, home_unguessed=[{"speciality": "building/platform-windows", "n": 2, "text": "Two."}],
            home_measures=[{"topic": "lists", "sentences": [{"speciality": "building/platform-windows", "n": 1}]}],
            building=[{"speciality": "building/platform-windows",
                       "sentences": [{"n": 3, "home_guess": "lists"}, {"n": 4, "home_guess": None}]}])
    for n in (1, 2, 3):
        assert mark.main(call(repo, ws, "--home", f"{n}=lists")) == 0, n
    assert json.loads(f.read_text())["homes"] == {"1": "lists", "2": "lists", "3": "lists"}
    capsys.readouterr()
    assert mark.main(call(repo, ws, "--home", "4=lists")) == 2      # listed with no home_guess: nothing to change
    assert "home_unguessed or home_measures" in capsys.readouterr().err
    assert mark.main(call(repo, ws, "--home", "1=")) == 0          # clearing is never refused


def test_held_file_records_many_verdicts_in_one_call(tmp_path, capsys):
    # G199 (L14): `--held-file FILE` ({id: held|not}) writes every verdict at
    # once; an unknown id or verdict refuses the whole file.
    repo, ws, f = setup(tmp_path)
    rows = [{"id": f"s:{n}@t", "text": f"piece {n}", "topic_sentence": "x", "rule_sentence": "x",
             "topic_hash": "abc"} for n in (1, 2, 3)]
    _report(ws, held_by_wording=rows)
    held = ws / "areas" / AREA / "held.json"
    v = tmp_path / "verdicts.json"
    v.write_text(json.dumps({"s:1@t": "held", "s:9@t": "not"}))
    base = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*base, "--held-file", str(v)]) == 2
    assert "s:9@t" in capsys.readouterr().err and not held.exists()
    v.write_text(json.dumps({"s:1@t": "held", "s:2@t": "maybe"}))
    assert mark.main([*base, "--held-file", str(v)]) == 2 and not held.exists()
    # gapfix14 (G288): a `not` gives its why
    v.write_text(json.dumps({"s:1@t": "held", "s:2@t": {"verdict": "not", "why": "x"}, "s:3@t": "held"}))
    capsys.readouterr()
    assert mark.main([*base, "--held-file", str(v)]) == 0
    saved = json.loads(held.read_text())
    assert {k: x["verdict"] for k, x in saved.items()} == {"s:1@t": "held", "s:2@t": "not", "s:3@t": "held"}
    assert saved["s:2@t"]["topic_hash"] == "abc" and saved["s:2@t"]["text"] == "piece 2"
    assert json.loads(capsys.readouterr().out)["verdicts"] == 3


def test_a_lacking_piece_takes_held_or_a_confirming_not_and_each_needs_a_reason(tmp_path, capsys):
    # G225/G233 (1.4.40): a `held` or short `not` that moves the total needs --why; each refusal writes nothing.
    # gapfix13 (G255, 1.4.42): a `lacking:` id takes `not` too, with a why: the lack is confirmed, still counted.
    repo, ws, f = setup(tmp_path)
    _report(ws, held_by_wording=[], lacking_pieces=[{"id": "lacking:s:1@t", "text": "p"}],
            short_sentences=[{"id": "short:s:2", "text": "q"}])
    held = ws / "areas" / AREA / "held.json"
    base = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*base, "--held", "lacking:s:1@t", "not"]) == 2      # no --why
    assert "give --why" in capsys.readouterr().err
    assert not held.exists()
    assert mark.main([*base, "--held", "lacking:s:1@t", "not", "--why", "homed here, lacking"]) == 0
    assert json.loads(held.read_text())["lacking:s:1@t"] == {"verdict": "not", "text": "p", "why": "homed here, lacking"}
    held.unlink()
    assert mark.main([*base, "--held", "lacking:s:1@t", "held"]) == 2 and not held.exists()      # no --why
    assert mark.main([*base, "--held", "short:s:2", "not"]) == 2 and not held.exists()
    assert mark.main([*base, "--held", "lacking:s:1@t", "held", "--why", "in the plan"]) == 0
    assert json.loads(held.read_text())["lacking:s:1@t"]["why"] == "in the plan"


def test_help_names_every_id_form_and_verdict(capsys):
    # gapfix13 (G268, 1.4.42)
    with pytest.raises(SystemExit):
        mark.main(["--help"])
    out = " ".join(capsys.readouterr().out.split())
    for word in ("lacking:", "short:", "hand:", "home:", "r9:", "<speciality>:<n>@<topic>", "{verdict, why}",
                 "--why", "--lack", "held", "not"):
        assert word in out, word


def test_a_verdict_file_counts_changed_refreshed_and_unchanged(tmp_path, capsys):
    # gapfix13 (G270, 1.4.42): a why or pin updated under the same verdict is `refreshed`, not hidden.
    repo, ws, f = setup(tmp_path)
    _report(ws, held_by_wording=[], lacking_pieces=[{"id": "lacking:s:1@t", "text": "p"},
                                                    {"id": "lacking:s:2@t", "text": "q"},
                                                    {"id": "lacking:s:3@t", "text": "r"}])
    base = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    v = tmp_path / "v.json"
    v.write_text(json.dumps({k: {"verdict": "held", "why": "w"} for k in ("lacking:s:1@t", "lacking:s:2@t")}))
    assert mark.main([*base, "--held-file", str(v)]) == 0
    capsys.readouterr()
    v.write_text(json.dumps({"lacking:s:1@t": {"verdict": "held", "why": "w"},
                             "lacking:s:2@t": {"verdict": "held", "why": "a better why"},
                             "lacking:s:3@t": {"verdict": "not", "why": "x"}}))
    assert mark.main([*base, "--held-file", str(v)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert (out["changed"], out["refreshed"], out["unchanged"]) == (1, 1, 1)


def test_help_gives_a_source_example_and_the_quote_building_recipe_for_sentence_numbers(capsys):
    # gapfix14 (G287, implementing-concurrency#3, implementing-performance#4): --source's relpath form and the way
    # to learn a sentence number were found only by trying.
    with pytest.raises(SystemExit):
        mark.main(["--help"])
    out = " ".join(capsys.readouterr().out.split())
    for words in ("reference/building--platform-windows.txt#10", "quote_building.py", "--keep /dev/null",
                  "A/homes.json"):
        assert words in out, words
