"""run_gaps.py: step 1.3's `cookr roles gaps` commands built from the area's
reference and unmeasured files, run, numbered as quote_building numbers the
building text, and summed per topic (1.4.18, G32-G37; 1.4.19 fix round 1;
1.4.20 fix round 2; 1.4.21 fix round 3; 1.4.22 fix round 4; 1.4.23 fix round 5).

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import quote_building as qb  # noqa: E402
import run_gaps  # noqa: E402
from reference_format import REFERENCE_FORMAT as FORMAT  # noqa: E402
import stage_status  # noqa: E402

CLI = HERE.parents[3] / "skills" / "cookr" / "cli"
AREA = "implementing/sec"

pytestmark = pytest.mark.skipif(
    subprocess.run([sys.executable, "-c", "import cookr"], env={**os.environ, "PYTHONPATH": str(CLI)},
                   capture_output=True).returncode != 0,
    reason="cookr does not import under this python (run the suite with $COOKR_PY)")

# Sentence 1 holds `:`, `;` and `—`: cookr cuts it in three pieces at `:` and
# `;`, quote_building keeps it whole; every piece must carry number 1.
# Sentence 6 is under six words: cookr measures no piece of it (I2).
# Sentence 7 has no mark; sentence 8 is marked here only by another plan's
# `marked_here`; sentence 9 shares half its words with authn and half with
# authz, a tie (I1). Sentence 10's first clause is held at authz, but cookr
# drops its short `; never float it.` clause: measured only in part (1.4.20).
BUILDING = (
    "Every session MUST have an absolute timeout enforced by the server side code: "
    "idle timeouts alone are never enough for any session; rotate the session identifier "
    "after every login — never reuse it across a privilege change.\n\n"
    "Deny every request by default unless a role explicitly grants the action.\n\n"
    "Rank every vulnerability by exploitability before its severity score alone.\n\n"
    "Keep an audit log of every compliance control and the evidence that it was verified.\n\n"
    "Talk only to immediate collaborators in every method you write.\n\n"
    "Never log a secret.\n\n"
    "Write every audit entry before the response is sent to the client.\n\n"
    "Encrypt every backup file with a key held outside the backup store.\n\n"
    "Sign webhook payloads, then verify signatures with constant time comparison.\n\n"
    "Pin every dependency to an exact version in the lockfile; never float it.\n")
TOPICS = {
    "implementing/sec/authn": "- Every session MUST have an absolute timeout enforced by the server side code.\n",
    "implementing/sec/authz": "- Deny every request by default unless a role explicitly grants the action.\n",
    "reviewing/sec/vp": "- Rank every vulnerability by exploitability before its severity score alone.\n",
    "reviewing/sec/lod": "- Talk only to immediate collaborators in every method you write.\n",
}
EXTRA = {   # topic text beyond the line its own speciality quotes
    "implementing/sec/authn": "- Sign webhook payloads with constant keys.\n- Rotate each identifier yearly.\n"
                              "- Keep rotating credentials under the documented operational schedule always.\n",
    # one word ("keep") of sentence 4, scored below vp's "audit" line: the
    # top 3 are ranked over all topics, not in topic order (1.4.20 Minor 1)
    "implementing/sec/authz": "- Verify signatures in time comparison.\n"
                              "- Pin every dependency to an exact version in the lockfile.\n",
    "reviewing/sec/vp": "- Audit findings weekly with evidence.\n",   # two words of sentence 4: too few to guess vp
}
PLAN = """# Plan

## Proposed topics

| Topic | Action | Artifact | Why |
|---|---|---|---|
| authn | kept | `cookbook/guidelines/implementing/sec/authn` | x |
| authz | kept | `cookbook/guidelines/implementing/sec/authz` | x |
| vp | kept | `cookbook/guidelines/reviewing/sec/vp` | written where it lives |
| lod | merged | `cookbook/guidelines/reviewing/sec/lod` | runs under reviewing/sec |
| compliance | new | `cookbook/guidelines/implementing/sec/compliance` | x |
| controls | new | `cookbook/guidelines/implementing/sec/controls` | x |
"""


def build(tmp: Path, plan: bool = True) -> tuple[Path, Path]:
    repo, ws = tmp / "repo", tmp / "ws"
    (repo / "cookbook").mkdir(parents=True)
    (repo / "cookbook" / "cookbook.json").write_text(
        '{"format": 2, "id": "00000000-0000-4000-8000-000000000001", "rdid": "tst"}\n')
    for t, text in TOPICS.items():
        f = repo / "cookbook" / "guidelines" / t
        f.mkdir(parents=True)
        (f / "artifact.json").write_text('{"meta": {}, "parts": [{"part": "rules", "role": "rules"}]}\n')
        (f / "rules.md").write_text(text + EXTRA.get(t, ""))
    a = ws / "areas" / AREA
    (a / "reference").mkdir(parents=True)
    files = {"security/authn": TOPICS["implementing/sec/authn"][2:],
             "security/authz": TOPICS["implementing/sec/authz"][2:],
             "security/vp": TOPICS["reviewing/sec/vp"][2:],
             "cq/lod": TOPICS["reviewing/sec/lod"][2:],
             "privacy/gone": "Some text another area measures against its own survivor topic.\n",
             "security/shared": "Log every authorization decision with the subject and the resource named.\n",
             "building/audit": "Keep every audit record for seven years at least.\n\nShip logs off the host.\n",
             "building/security": BUILDING}
    path = {}
    for s, text in files.items():
        path[s] = a / "reference" / (s.replace("/", "--") + ".txt")
        path[s].write_text(text)
    rows = [{"speciality": "security/authn", "topic": "cookbook/guidelines/reviewing/sec/authn", "file": str(path["security/authn"])},
            {"speciality": "security/authz", "topic": "cookbook/guidelines/implementing/sec/authz", "file": str(path["security/authz"])},
            {"speciality": "security/vp", "topic": "cookbook/guidelines/reviewing/sec/vp", "file": str(path["security/vp"])},
            {"speciality": "cq/lod", "topic": "cookbook/guidelines/reviewing/sec/lod", "file": str(path["cq/lod"])},
            {"speciality": "privacy/gone", "topic": "cookbook/guidelines/reviewing/sec/gone", "file": str(path["privacy/gone"])},
            {"speciality": "security/shared", "topic": "cookbook/guidelines/implementing/sec/authz", "file": str(path["security/shared"])},
            {"speciality": "building/security", "topic": None, "file": str(path["building/security"])},
            {"speciality": "building/ops", "topic": None, "file": None},
            {"speciality": "building/audit", "topic": None, "file": str(path["building/audit"])},
            {"speciality": "building/bare", "topic": None, "file": None}]
    rows = [{**r, "format": FORMAT} for r in rows]      # written by today's speciality_reference.py
    (a / "reference.json").write_text(json.dumps(rows))
    via = [{"speciality": f"security/{t}", "topic": f"guidelines/implementing/sec/{t}"}
           for t in ("authn", "authz", "vp", "lod", "compliance")]
    (a / "unmeasured.json").write_text(json.dumps({
        "area": AREA, "new_topics": [], "unplaced": [], "mark_conflicts": [], "unread_marks": [],
        "building": [{"speciality": "building/security", "topics": [v["topic"] for v in via],
                      "by_new_home": [], "measured_by": [], "via": via, "file": str(path["building/security"])},
                     {"speciality": "building/ops", "topics": [], "by_new_home": [], "measured_by": [],
                      "via": [{"speciality": "building/ops", "topic": "guidelines/implementing/sec/authz"}], "file": None},
                     {"speciality": "building/audit", "topics": [], "by_new_home": [], "measured_by": [],
                      "via": [{"speciality": "building/audit", "topic": "guidelines/implementing/sec/compliance"}],
                      "file": str(path["building/audit"])},
                     {"speciality": "building/bare", "topics": [], "by_new_home": [], "measured_by": [],
                      "via": [], "file": None}],
        "marked_here": [{"speciality": "building/security", "n": 8, "text": "Encrypt every backup file.",
                         "plan": "reviewing/sec"}],
        "against_survivor": [{"speciality": "security/authn", "copy": "cookbook/guidelines/reviewing/sec/authn",
                              "survivor": "cookbook/guidelines/implementing/sec/authn", "file": str(path["security/authn"])}],
        "survivor_elsewhere": [{"speciality": "privacy/gone", "copy": "cookbook/guidelines/implementing/sec/gone",
                                "survivor": "cookbook/guidelines/reviewing/sec/gone", "file": str(path["privacy/gone"])}]}))
    found = qb.sentences(BUILDING)
    (a / "building-security.json").write_text(json.dumps({
        "speciality": "building/security",
        "sentences": [{"n": n, "text": s} for n, s in enumerate(found, start=1)],
        "marks": {"1": AREA, "2": AREA, "3": AREA, "4": AREA, "5": "reviewing/sec", "6": AREA, "7": None,
                  "8": None, "9": AREA, "10": AREA}}))
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": [
        {"topic": t, "survivor": f"guidelines/reviewing/sec/{t}", "new_home": f"guidelines/implementing/sec/{t}",
         "copies": [], "devteam": [{"speciality": s} for s in sps]}
        for t, sps in (("vp", ["security/vp", "security/shared"]), ("lod", ["cq/lod"]))] + [
        # R9 is owed for a `shared-different` new topic (a candidate survivor
        # to measure against), never for a checklist one (1.4.20).
        {"topic": t, "survivor": f"guidelines/implementing/sec/{t}", "new": True, "kind": kind,
         "copies": [], "devteam": []}
        for t, kind in (("compliance", "shared-different"), ("controls", "checklist"))]}]}))
    if plan:
        (a / "area-plan.md").write_text(PLAN)
    return repo, ws


def run(repo: Path, ws: Path, capsys, *extra: str) -> tuple[int, dict | None, str]:
    capsys.readouterr()
    code = run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo),
                          "--cookr-cli", str(CLI), *extra])
    cap = capsys.readouterr()
    return code, (json.loads(cap.out) if cap.out.strip() else None), cap.err


def _ns(b: dict) -> list[int]:
    """The numbers of a building entry's `unmeasured_sentences` rows (G48)."""
    return [r["n"] for r in b["unmeasured_sentences"]]


def _norm(s: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s.lower()).split())


def test_each_piece_carries_its_quote_building_sentence_number(tmp_path, capsys):
    # G34: cookr cuts at `;` and `:` and quote_building does not; the gaps
    # file carries, beside each lacking piece, the number quote_building gives
    # the sentence that holds it, so the plan cites one numbering.
    repo, ws = build(tmp_path)
    code, out, err = run(repo, ws, capsys)
    assert code == 0, err
    gaps = json.loads((ws / "areas" / AREA / "gaps" / "authn.json").read_text())
    ref = next(r for r in gaps["references"] if r["file"].endswith("building--security.txt"))
    assert ref["lacking_numbers"] == [1, 1, 2, 3, 4, 5, 7, 8, 9, 10]
    found = qb.sentences(BUILDING)
    for piece, n in zip(ref["lacking_sentences"], ref["lacking_numbers"]):
        assert _norm(piece) in _norm(found[n - 1])
    assert len(ref["lacking_sentences"]) == len(ref["lacking_numbers"])
    assert sum(1 for p in ref["lacking_sentences"] if p.startswith(("idle", "rotate"))) == 2   # `:` and `;` cut


def test_against_files_follow_the_reference_unmeasured_and_plan(tmp_path, capsys):
    # G37: direct rows, an against_survivor row on its survivor, a
    # survivor_elsewhere row skipped, each `via` topic given the building file;
    # G36: a merged row whose folder is another area's is measured in that
    # plan, not here; G35: a `via` topic with no folder is listed, unmeasured.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    assert code == 0
    topics = {t["topic"]: t for t in out["topics"]}
    assert sorted(topics) == ["authn", "authz", "vp"]
    files = {t: [Path(r["file"]).name for r in topics[t]["references"]] for t in topics}
    assert files == {"authn": ["security--authn.txt", "building--security.txt"],
                     "authz": ["security--authz.txt", "security--shared.txt", "building--security.txt"],
                     "vp": ["security--vp.txt", "security--shared.txt", "building--security.txt"]}   # worklist devteam
    # Nit 5: a building row with no file is listed whether or not it has a `via`.
    assert [m["speciality"] for m in out["missing_files"]] == ["building/ops", "building/bare"]
    assert all("speciality_reference.py" in m["why"] for m in out["missing_files"])
    assert topics["vp"]["folder"] == "cookbook/guidelines/reviewing/sec/vp"
    assert out["measured_elsewhere"] == [{"topic": "lod", "folder": "cookbook/guidelines/reviewing/sec/lod",
                                          "plan": "reviewing/sec",
                                          "specialities": ["cq/lod", "building/security"]}]
    assert out["r9_missing"] == ["compliance"]          # owed; checklist `controls` is not
    assert out["unmeasurable"] == [{"topic": "compliance", "folder": "cookbook/guidelines/implementing/sec/compliance",
                                    "specialities": ["building/security", "building/audit"]}]
    assert sorted(p.name for p in (ws / "areas" / AREA / "gaps").iterdir()) == ["authn.json", "authz.json", "vp.json"]
    assert topics["authn"]["pieces"] == 1 + 11 and topics["authn"]["held"] == 2 and topics["authn"]["lacking"] == 10


def test_a_new_topic_the_worklist_does_not_name_is_owed_an_r9_measure(tmp_path, capsys):
    # 1.4.21 Nit 2: with no worklist entry its kind is unknown, so it is
    # owed one (over-reporting beats missing).
    repo, ws = build(tmp_path)
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(plan.read_text() + "| orphan | new | `cookbook/guidelines/implementing/sec/orphan` | x |\n")
    code, out, err = run(repo, ws, capsys)
    assert out["r9_missing"] == ["compliance", "orphan"] and "orphan" in err


def test_without_a_plan_a_new_home_resolves_to_the_worklist_survivor(tmp_path, capsys):
    repo, ws = build(tmp_path, plan=False)
    code, out, _ = run(repo, ws, capsys)
    assert code == 0
    topics = {t["topic"]: t["folder"] for t in out["topics"]}
    files = {t["topic"]: [Path(r["file"]).name for r in t["references"]] for t in out["topics"]}
    assert topics["vp"] == "cookbook/guidelines/reviewing/sec/vp"
    assert topics["lod"] == "cookbook/guidelines/reviewing/sec/lod"    # no merged row: measured here
    assert "building--security.txt" in files["lod"]                     # its `via` new_home -> survivor
    assert topics["authn"] == "cookbook/guidelines/implementing/sec/authn"   # against_survivor, no plan
    assert files["authn"] == ["security--authn.txt", "building--security.txt"]
    assert [u["topic"] for u in out["unmeasurable"]] == ["compliance"]
    assert out["measured_elsewhere"] == []


def test_each_building_sentence_is_judged_once_at_its_home_topic(tmp_path, capsys):
    # G33: a sentence is a candidate only when held at no measured topic, and
    # only when marked for this area (its own mark or another plan's
    # `marked_here`); a sentence marked for another area never is.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    assert code == 0
    b = out["building"][0]
    by_n = {s["n"]: s for s in b["sentences"]}
    assert by_n[1]["lacking_at"] == ["authn", "authz", "vp"]
    assert by_n[2]["home_guess"] == "authz" and by_n[2]["held_at"] == ["authz"]
    assert by_n[3]["home_guess"] == "vp" and by_n[3]["held_at"] == ["vp"]
    assert b["gap_candidates"] == [1, 4, 8, 9]          # 8: marked here by `marked_here` only
    assert b["other_area"] == [5] and b["unmarked"] == [7]
    authn = next(t for t in out["topics"] if t["topic"] == "authn")
    assert {"speciality": "building/security", "n": 2, "home_guess": "authz"} in authn["lacking_by_home_guess"]
    assert "advisory" in out["note"] and "home" not in by_n[1] and "gaps" not in b


def test_home_guess_is_null_where_no_measured_topic_can_be_the_home(tmp_path, capsys):
    # 1.4.19 I1: sentence 4's home is the new compliance topic, which is not
    # measured: no measured topic shares enough of its words, so no guess;
    # sentence 9 shares as much with authn as with authz: a tie, no guess.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    by_n = {s["n"]: s for s in out["building"][0]["sentences"]}
    assert by_n[4]["home_guess"] is None and by_n[4]["lacking_at"] == ["authn", "authz", "vp"]
    assert by_n[9]["home_guess"] is None and set(by_n[9]["lacking_at"]) >= {"authn", "authz"}
    assert by_n[1]["home_guess"] == "authn"


def test_a_sentence_cookr_never_measures_is_never_held(tmp_path, capsys):
    # 1.4.19 I2: every piece of sentence 6 is under six words, so cookr
    # measures none of it: it is not held anywhere, it is listed apart.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    b = out["building"][0]
    s6 = next(s for s in b["sentences"] if s["n"] == 6)
    assert s6["measured"] is False and s6["held_at"] == [] and s6["lacking_at"] == [] and s6["home_guess"] is None
    assert _ns(b) == [6, 10] and 6 not in b["gap_candidates"]
    assert all(s["measured"] for s in b["sentences"] if s["n"] not in (6, 10))


def test_a_sentence_measured_only_in_part_is_never_held(tmp_path, capsys):
    # 1.4.20 Minor 3: cookr drops sentence 10's `never float it.` (under six
    # words) and holds its first clause at authz; the dropped clause was never
    # measured, so the sentence is not held: it is listed for judging by hand,
    # the dropped clause named.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    b = out["building"][0]
    s10 = next(s for s in b["sentences"] if s["n"] == 10)
    assert s10["measured"] is False
    assert s10["unmeasured_parts"] == ["never float it."]
    assert 10 in _ns(b) and 10 not in b["gap_candidates"]
    # 1.4.21 Minor 1, 1.4.22 Minor 1: the verdicts of its measured pieces stay
    # beside the dropped piece, so the hand judge sees both, but under
    # `measured_pieces`: the sentence's own `held_at` stays empty, so it never
    # reads as held, and the entry says so itself.
    assert s10["held_at"] == [] and s10["lacking_at"] == []
    assert s10["measured_pieces"] == {"held_at": ["authz"], "lacking_at": ["authn", "vp"]}
    assert s10["home_guess"] == "authz"
    assert "judged by hand" in s10["by_hand"] and "not a verdict on the sentence" in s10["by_hand"]
    authn = next(r for r in out["topics"] if r["topic"] == "authn")
    assert {"speciality": "building/security", "n": 10, "home_guess": "authz",
            "measured": False} in authn["lacking_by_home_guess"]
    s1 = next(s for s in b["sentences"] if s["n"] == 1)
    assert "unmeasured_parts" not in s1 and "measured_pieces" not in s1 and "by_hand" not in s1
    assert all("measured" not in r for r in authn["lacking_by_home_guess"] if r["n"] != 10)
    assert "measured_pieces" in out["note"] and "not a verdict on the sentence" in out["note"]
    # no sentence with a piece not measured has a sentence-level verdict
    assert all(s["held_at"] == [] and s["lacking_at"] == []
               for x in out["building"] for s in x["sentences"] if not s["measured"])


def test_a_sentence_measured_in_part_and_held_nowhere_is_no_gap_candidate(tmp_path, capsys, monkeypatch):
    # 1.4.21 Minor 1: sentence 4 is lacking at every measured topic; with a
    # piece cookr did not measure it keeps its lacking verdicts but is listed
    # for a hand judgment, not as a gap candidate.
    repo, ws = build(tmp_path)
    real, s4 = run_gaps.cookr_pieces, qb.sentences(BUILDING)[3]
    head, tail = s4.split(" and the evidence ")

    def split_4(*a):
        out = []
        for piece, kept in real(*a):
            out += [[head, True], ["the evidence " + tail, False]] if piece == s4 else [[piece, kept]]
        return out
    monkeypatch.setattr(run_gaps, "cookr_pieces", split_4)
    code, out, _ = run(repo, ws, capsys)
    b = out["building"][0]
    s4 = next(s for s in b["sentences"] if s["n"] == 4)
    assert s4["measured"] is False and s4["held_at"] == [] and s4["lacking_at"] == []
    assert s4["measured_pieces"] == {"held_at": [], "lacking_at": ["authn", "authz", "vp"]}
    assert 4 in _ns(b) and 4 not in b["gap_candidates"]


def test_a_dropped_piece_no_sentence_holds_is_listed_unplaced(tmp_path, capsys, monkeypatch):
    # 1.4.21 Nit 3: a dropped piece numbers() cannot place is never ignored:
    # it is listed in `unplaced_pieces` for a hand judgment.
    repo, ws = build(tmp_path)
    real = run_gaps.numbers

    def lose(pieces, text):
        return [None if p == "never float it." else n for p, n in zip(pieces, real(pieces, text))]
    monkeypatch.setattr(run_gaps, "numbers", lose)
    code, out, _ = run(repo, ws, capsys)
    b = out["building"][0]
    # 1.4.22 Nit 1: an object, saying it was not measured (no verdict, no
    # topic); 1.4.22 Minor 2: sentence 10 could hold it, so it is named there.
    assert b["unplaced_pieces"] == [{"text": "never float it.", "measured": False, "verdict": None,
                                     "topic": None, "sentences": [10]}]
    s10 = next(s for s in b["sentences"] if s["n"] == 10)
    assert s10["measured"] is False and s10["unplaced_parts"] == ["never float it."] and s10["held_at"] == []
    # G56 (1.4.24): the key is always there, [] when nothing is unplaced.
    assert next(x for x in out["building"] if x["speciality"] == "building/audit")["unplaced_pieces"] == []


def test_a_measured_piece_no_sentence_holds_is_never_dropped(tmp_path, capsys, monkeypatch):
    # 1.4.22 Minor 2: sentence 1's first piece is held at authn, its other two
    # are lacking there. When numbers() cannot place those two, the sentence
    # must not read as held at authn from the one piece left: each lost piece
    # is listed with its verdict per topic, and the sentence is judged by hand.
    repo, ws = build(tmp_path)
    real = run_gaps.numbers
    lost = ("idle timeouts alone are never enough for any session;",
            "rotate the session identifier after every login — never reuse it across a privilege change.")

    def lose(pieces, text):
        return [None if p in lost else n for p, n in zip(pieces, real(pieces, text))]
    monkeypatch.setattr(run_gaps, "numbers", lose)
    code, out, _ = run(repo, ws, capsys)
    assert code == 0
    b = out["building"][0]
    s1 = next(s for s in b["sentences"] if s["n"] == 1)
    assert s1["measured"] is False and s1["held_at"] == [] and s1["lacking_at"] == []
    assert s1["unplaced_parts"] == list(lost)
    assert s1["measured_pieces"]["held_at"] == ["authn"]         # the one piece placed: not the sentence
    assert 1 in _ns(b) and 1 not in b["gap_candidates"]
    assert "not a verdict on the sentence" in s1["by_hand"]
    for text in lost:
        for topic in ("authn", "authz", "vp"):
            assert {"text": text, "measured": True, "verdict": "lacking", "topic": topic,
                    "sentences": [1]} in b["unplaced_pieces"], (text, topic)
    assert len(b["unplaced_pieces"]) == 6
    rows = {r["topic"]: r for r in out["topics"]}
    ref = next(r for r in rows["authn"]["references"] if r["speciality"] == "building/security")
    assert ref["lacking_numbers"].count(None) == 2 and ref["unplaced"] == 2
    assert rows["authn"]["unplaced"] == 2
    assert "unplaced_pieces" in out["note"]


def test_a_lacking_piece_numbered_nowhere_is_listed_even_when_the_piece_is_placed(tmp_path, capsys, monkeypatch):
    # 1.4.22 Minor 2: numbers() runs once per topic over its lacking pieces
    # and once over every piece; they can disagree. Here only authn's lacking
    # list loses sentence 1's second piece (a null in its `lacking_numbers`),
    # while the pass over every piece places it: the null is still listed,
    # and sentence 1 must not read as held at authn.
    repo, ws = build(tmp_path)
    real, first = run_gaps.numbers, "Every session MUST have an absolute timeout enforced by the server side code:"
    piece = "idle timeouts alone are never enough for any session;"

    def lose(pieces, text):
        return [None if p == piece and first not in pieces else n for p, n in zip(pieces, real(pieces, text))]
    monkeypatch.setattr(run_gaps, "numbers", lose)
    out = run(repo, ws, capsys)[1]
    b = out["building"][0]
    assert b["unplaced_pieces"] == [{"text": piece, "measured": True, "verdict": "lacking", "topic": "authn",
                                     "sentences": [1]}]
    s1 = next(s for s in b["sentences"] if s["n"] == 1)
    assert s1["measured"] is False and s1["held_at"] == [] and s1["unplaced_parts"] == [piece]
    assert 1 in _ns(b) and 1 not in b["gap_candidates"]
    assert {r["topic"]: r["unplaced"] for r in out["topics"]} == {"authn": 1, "authz": 0, "vp": 0}


def test_an_unplaced_piece_is_lacking_wherever_cookr_listed_it_lacking(tmp_path, capsys, monkeypatch):
    # 1.4.23 Minor 1: the passes disagree the other way round: the pass over
    # every piece (the only one holding the dropped "Never log a secret.")
    # cannot number sentence 1's second piece, while each topic's lacking
    # pass numbers it. cookr listed it lacking at all three topics, so its
    # rows say lacking there, never held.
    repo, ws = build(tmp_path)
    real, piece = run_gaps.numbers, "idle timeouts alone are never enough for any session;"

    def lose(pieces, text):
        full = "Never log a secret." in pieces
        return [None if p == piece and full else n for p, n in zip(pieces, real(pieces, text))]
    monkeypatch.setattr(run_gaps, "numbers", lose)
    out = run(repo, ws, capsys)[1]
    b = out["building"][0]
    assert b["unplaced_pieces"] == [{"text": piece, "measured": True, "verdict": "lacking", "topic": t,
                                     "sentences": [1]} for t in ("authn", "authz", "vp")]
    s1 = next(s for s in b["sentences"] if s["n"] == 1)
    assert s1["measured"] is False and s1["held_at"] == [] and s1["unplaced_parts"] == [piece]
    assert s1["measured_pieces"]["lacking_at"] == ["authn", "authz", "vp"]
    assert all(r["unplaced"] == 0 for r in out["topics"])      # each lacking pass numbered it


def test_an_unplaced_measured_piece_held_at_a_topic_says_so(tmp_path, capsys, monkeypatch):
    # 1.4.22 Minor 2: sentence 2 is one piece, held at authz and lacking at
    # authn and vp. Unplaced, it carries each verdict, and sentence 2 has no
    # verdict of its own.
    repo, ws = build(tmp_path)
    real, s2 = run_gaps.numbers, qb.sentences(BUILDING)[1]

    def lose(pieces, text):
        return [None if p == s2 else n for p, n in zip(pieces, real(pieces, text))]
    monkeypatch.setattr(run_gaps, "numbers", lose)
    b = run(repo, ws, capsys)[1]["building"][0]
    got = {u["topic"]: u["verdict"] for u in b["unplaced_pieces"] if u["text"] == s2}
    assert got == {"authn": "lacking", "authz": "held", "vp": "lacking"}
    by_n = {s["n"]: s for s in b["sentences"]}
    assert by_n[2]["measured"] is False and by_n[2]["held_at"] == [] and "measured_pieces" not in by_n[2]
    assert by_n[2]["unplaced_parts"] == [s2] and 2 in _ns(b)
    assert by_n[3]["measured"] is True and by_n[3]["held_at"] == ["vp"]      # untouched


def test_a_measured_piece_spanning_two_sentences_leaves_neither_held(tmp_path, capsys, monkeypatch):
    # 1.4.22 Minor 2, the real numbers(): cookr cuts one piece where
    # quote_building cuts two sentences (2 and 3), so no one sentence holds
    # it. Both sentences it could belong to are judged by hand.
    repo, ws = build(tmp_path)
    found = qb.sentences(BUILDING)
    real, span = run_gaps.cookr_pieces, found[1] + " " + found[2]

    def join(*a):
        pieces = real(*a)
        if a[0] != str(ws / "areas" / AREA / "reference" / "building--security.txt"):
            return pieces            # G72 cuts every speciality's file: only the building text is joined
        out = [[span, True] if p == found[1] else [p, kept] for p, kept in pieces if p != found[2]]
        assert [span, True] in out
        return out
    monkeypatch.setattr(run_gaps, "cookr_pieces", join)
    b = run(repo, ws, capsys)[1]["building"][0]
    assert {u["text"] for u in b["unplaced_pieces"]} == {span}
    assert all(u["measured"] is True and u["sentences"] == [2, 3] for u in b["unplaced_pieces"])
    for n in (2, 3):
        s = next(s for s in b["sentences"] if s["n"] == n)
        assert s["measured"] is False and s["held_at"] == [] and s["unplaced_parts"] == [span], n
        assert n in _ns(b) and n not in b["gap_candidates"]


def test_an_unplaced_piece_no_sentence_could_hold_stands_alone(tmp_path, capsys, monkeypatch):
    # 1.4.22 Minor 2: no sentence can be chosen: the piece is listed alone
    # (`sentences` []), for a hand judgment; no sentence changes.
    repo, ws = build(tmp_path)
    real, stray = run_gaps.cookr_pieces, "Words that appear in no sentence of the building text."
    monkeypatch.setattr(run_gaps, "cookr_pieces", lambda *a: real(*a) + [[stray, True]])
    b = run(repo, ws, capsys)[1]["building"][0]
    assert {u["text"] for u in b["unplaced_pieces"]} == {stray}
    assert all(u["sentences"] == [] and u["measured"] is True for u in b["unplaced_pieces"])
    assert _ns(b) == [6, 10]
    assert all("unplaced_parts" not in s for s in b["sentences"])


def test_could_hold_names_every_sentence_a_piece_overlaps():
    found = ["Alpha bravo charlie.", "Delta echo foxtrot.", "Golf hotel.", "Alpha bravo charlie."]
    assert run_gaps.could_hold("charlie. Delta echo", found) == [1, 2]
    assert run_gaps.could_hold("Alpha bravo charlie", found) == [1, 4]     # every place it may sit
    assert run_gaps.could_hold("foxtrot golf hotel alpha", found) == [2, 3, 4]
    assert run_gaps.could_hold("zulu", found) == [] and run_gaps.could_hold("—", found) == []


def test_a_building_file_measured_at_no_topic_lists_every_sentence_unmeasured(tmp_path, capsys):
    # 1.4.19 I2: building/audit's only `via` topic is new (no folder), so
    # cookr measures none of its text: its sentences are listed, never dropped.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    b = next(x for x in out["building"] if x["speciality"] == "building/audit")
    assert b["measured_at"] == [] and _ns(b) == [1, 2] and b["gap_candidates"] == []
    assert all(s["measured"] is False for s in b["sentences"])
    assert next(x for x in out["building"] if x["speciality"] == "building/security")["measured_at"] == ["authn", "authz", "vp"]


def test_numbers_follow_repeated_and_out_of_order_pieces():
    # G34: a piece repeated in the text maps to each sentence in turn; a piece
    # met after the cursor's sentence is still found before it.
    text = ("Alpha bravo charlie delta echo foxtrot.\n\nGolf hotel india juliet kilo lima.\n\n"
            "Alpha bravo charlie delta echo foxtrot.\n")
    a, g = "Alpha bravo charlie delta echo foxtrot.", "Golf hotel india juliet kilo lima."
    assert run_gaps.numbers([a, a], text) == [1, 3]
    assert run_gaps.numbers([g, a], text) == [2, 3]
    assert run_gaps.numbers([g, a, a], text) == [2, 3, 1]


def test_hints_rank_each_gap_against_its_home_topic(tmp_path, capsys):
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys, "--hints")
    assert code == 0
    by_n = {s["n"]: s for s in out["building"][0]["sentences"]}
    assert by_n[1]["hints"][0]["part"] == "rules" and by_n[1]["hints"][0]["score"] > 0
    assert by_n[1]["hints_at"] == "authn" and {h["topic"] for h in by_n[1]["hints"]} == {"authn"}
    assert "hints" not in by_n[2]                               # held at its home


def test_hints_without_a_home_guess_rank_every_measured_topic(tmp_path, capsys):
    # 1.4.20 Minor 1: no home guessed (sentence 4 below the share, 9 a tie, 6
    # never measured): the top 3 over every measured topic, labelled so.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys, "--hints")
    by_n = {s["n"]: s for s in out["building"][0]["sentences"]}
    for n in (4, 9, 6):
        assert by_n[n]["hints_at"] == "every measured topic", n
        assert len(by_n[n]["hints"]) <= 3 and len(by_n[n]["hints"]) > 0 or n == 6   # 6 shares no word
        assert {h["topic"] for h in by_n[n]["hints"]} <= {"authn", "authz", "vp"}
    assert {h["topic"] for h in by_n[4]["hints"]} >= {"vp"}               # "audit": vp's line
    assert {h["topic"] for h in by_n[9]["hints"]} >= {"authn", "authz"}   # both tied topics ranked
    # Sentence 4 shares one word with authn, measured first, and scores
    # higher at vp: the top 3 are ranked over all topics, not topic by topic.
    assert [h["topic"] for h in by_n[4]["hints"]] == ["vp", "authn"]
    assert by_n[10]["hints_at"] == "authz"       # partly measured: hinted at its home (1.4.21)
    assert by_n[10]["held_at"] == [] and by_n[10]["measured_pieces"]["held_at"] == ["authz"]   # 1.4.22


def test_hints_never_rank_a_topic_that_failed(tmp_path, capsys):
    # 1.4.21 Nit 1: "every measured topic" leaves out a topic whose cookr run
    # failed; sentence 9 otherwise ranks authz.
    repo, ws = build(tmp_path)
    (ws / "areas" / AREA / "reference" / "security--authz.txt").unlink()
    code, out, _ = run(repo, ws, capsys, "--hints")
    assert code == 2 and out["failed"][0]["topic"] == "authz"
    hinted = [s for s in out["building"][0]["sentences"] if "hints" in s]
    assert any(s["hints"] for s in hinted)
    assert all(h["topic"] != "authz" for s in hinted for h in s["hints"])


def test_the_note_names_the_home_share_in_force(tmp_path, capsys, monkeypatch):
    # 1.4.20 Nit 4: the note is built from HOME_SHARE, never a copy of it.
    repo, ws = build(tmp_path)
    monkeypatch.setattr(run_gaps, "HOME_SHARE", 0.55)
    out = run(repo, ws, capsys)[1]
    assert "55%" in out["note"] and "40%" not in out["note"]


def test_stale_gaps_files_are_listed_and_a_new_measure_file_is_not(tmp_path, capsys):
    # G32: a gaps file no topic of the current measurement set produces is
    # stale (an R9 `new-<name>.json` is written by its own step, never stale).
    repo, ws = build(tmp_path)
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    (gaps / "old-topic.json").write_text("{}")
    (gaps / "lod.json").write_text("{}")
    (gaps / "new-compliance.json").write_text("{}")
    code, out, _ = run(repo, ws, capsys)
    assert code == 0 and out["stale_gaps"] == ["lod.json", "old-topic.json"]
    assert stage_status.status(AREA, ws, repo)["stale_gaps"] == ["lod.json", "old-topic.json"]
    (gaps / "lod.json").unlink(), (gaps / "old-topic.json").unlink()
    assert stage_status.status(AREA, ws, repo)["stale_gaps"] == []
    out = run(repo, ws, capsys)[1]
    assert out["r9_missing"] == []                     # new-compliance.json is there


def test_out_writes_elsewhere_and_leaves_the_area_untouched(tmp_path, capsys):
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys, "--out", str(tmp_path / "scratch"))
    assert code == 0 and sorted(p.name for p in (tmp_path / "scratch").iterdir()) == [
        "authn.json", "authz.json", "run_gaps.json", "vp.json"]           # M4: its report saved inside --out
    assert not (ws / "areas" / AREA / "gaps").exists() and not (ws / "areas" / AREA / "run_gaps.json").exists()
    assert not (tmp_path / "run_gaps.json").exists()


def test_two_topics_with_one_basename_exit_2(tmp_path, capsys):
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    rows = json.loads((a / "reference.json").read_text())
    (repo / "cookbook" / "guidelines" / "reviewing" / "sec" / "authz").mkdir()
    rows.append({"speciality": "security/authz2", "topic": "cookbook/guidelines/reviewing/sec/authz", "file": rows[1]["file"]})
    (a / "reference.json").write_text(json.dumps(rows))
    (a / "area-plan.md").unlink()
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    (gaps / "old-topic.json").write_text("{}")
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and "authz" in err and out is None
    stale = stage_status.status(AREA, ws, repo)["stale_gaps"]
    assert isinstance(stale, dict) and "authz" in stale["refused"]   # M3: unknown, never "nothing stale"


def test_a_missing_input_exits_2_naming_it(tmp_path, capsys):
    repo, ws = build(tmp_path)
    (ws / "areas" / AREA / "unmeasured.json").unlink()
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and "unmeasured.json" in err


def test_a_failed_cookr_run_exits_2_and_keeps_the_previous_file(tmp_path, capsys):
    repo, ws = build(tmp_path)
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    (gaps / "authz.json").write_text("old\n")
    (ws / "areas" / AREA / "reference" / "security--authz.txt").unlink()   # cookr names the path, exit 2
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and out["failed"][0]["topic"] == "authz"
    assert (gaps / "authz.json").read_text() == "old\n"
    assert out["building"][0]["partial"] == ["authz"]     # M2: figures without authz are not the area's


def test_cookr_pieces_raises_when_cookr_cannot_cut(tmp_path):
    # 1.4.20 Nit 3: a cli without cookr is a failure, never "no pieces".
    f = tmp_path / "x.txt"
    f.write_text("One sentence long enough to be measured by cookr here.\n")
    (tmp_path / "empty-cli").mkdir()
    with pytest.raises(ValueError):
        run_gaps.cookr_pieces(str(f), sys.executable, tmp_path / "empty-cli")
    assert run_gaps.cookr_pieces(str(f), sys.executable, CLI) == [
        ["One sentence long enough to be measured by cookr here.", True]]


def test_a_building_file_cookr_cannot_cut_is_a_failed_speciality(tmp_path, capsys, monkeypatch):
    # 1.4.20 Nit 3: the failure names the speciality under `speciality`, not
    # `topic`, and exits 2.
    repo, ws = build(tmp_path)

    def broken(*_):
        raise ValueError("cookr could not cut it")
    monkeypatch.setattr(run_gaps, "cookr_pieces", broken)
    code, out, _ = run(repo, ws, capsys)
    assert code == 2
    assert {"speciality": "building/security", "why": "cookr could not cut it"} in out["failed"]
    assert all("topic" not in f for f in out["failed"] if f.get("speciality"))


def test_a_cookr_run_printing_no_json_exits_2_and_keeps_the_previous_file(tmp_path, capsys):
    # M1: exit 0 with stdout that is not JSON is a failed run, not a traceback;
    # the previous file stays and no scratch file is left behind.
    repo, ws = build(tmp_path)
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    (gaps / "authn.json").write_text("old\n")
    fake = tmp_path / "fake-cli"
    (fake / "cookr").mkdir(parents=True)
    (fake / "cookr" / "__init__.py").write_text("")
    (fake / "cookr" / "__main__.py").write_text("print('not json')\n")
    capsys.readouterr()
    code = run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(fake)])
    out = json.loads(capsys.readouterr().out)
    assert code == 2 and sorted(f["topic"] for f in out["failed"] if "topic" in f) == ["authn", "authz", "vp"]
    assert (gaps / "authn.json").read_text() == "old\n"
    assert sorted(p.name for p in gaps.iterdir()) == ["authn.json"]


def _shadow(tmp: Path) -> Path:
    """A folder holding a `cookr` package that only says it was imported."""
    evil = tmp / "evil"
    (evil / "cookr").mkdir(parents=True)
    (evil / "cookr" / "__init__.py").write_text("raise SystemExit('shadowed cookr imported')\n")
    return evil


def test_a_cookr_package_in_the_working_directory_never_shadows_cookr(tmp_path, capsys, monkeypatch):
    # G44 (1.4.24): every subprocess the skill starts is isolated from the
    # working directory, so a `cookr` folder there is never imported.
    repo, ws = build(tmp_path)
    monkeypatch.chdir(_shadow(tmp_path))
    code, out, err = run(repo, ws, capsys)
    assert out["failed"] == [], out["failed"]
    assert "shadowed" not in err
    f = tmp_path / "x.txt"
    f.write_text("One sentence long enough to be measured by cookr here.\n")
    assert run_gaps.cookr_pieces(str(f), sys.executable, CLI) == [
        ["One sentence long enough to be measured by cookr here.", True]]


def _snapshot(folder: Path) -> dict:
    return {p.relative_to(folder).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in sorted(folder.rglob("*")) if p.is_file()}


def test_check_writes_nothing_and_reports_no_change_after_a_run(tmp_path, capsys):
    # G45 (1.4.24): --check measures into a scratch folder, compares the fresh
    # result with the saved gaps files and writes nothing.
    repo, ws = build(tmp_path)
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    import r9_stamp      # G94 (1.4.33): an R9 file is stamped with its reference's hash, else r9_stale
    assert r9_stamp.main([str(_r9_file(ws / "areas" / AREA))]) == 0     # before the run: its report knows it (G67)
    run(repo, ws, capsys)
    before = _snapshot(ws)
    code, out, _ = run(repo, ws, capsys, "--check")
    assert code == 0, out["changes"]
    assert out["check"] == "unchanged" and out["changes"] == []
    assert _snapshot(ws) == before


def test_check_reports_a_topic_whose_measure_changed(tmp_path, capsys):
    # G45: a topic that now holds a sentence it lacked is a change; the saved
    # file stays as it was.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    saved = (ws / "areas" / AREA / "gaps" / "authz.json").read_bytes()
    with (repo / "cookbook/guidelines/implementing/sec/authz/rules.md").open("a") as f:
        f.write("- Encrypt every backup file with a key held outside the backup store.\n")
    code, out, _ = run(repo, ws, capsys, "--check")
    assert code == 1 and out["check"] == "changed"
    assert any(c["path"].startswith("topics[authz]") for c in out["changes"]), out["changes"]
    assert any(c["path"].startswith("building[building/security].gap_candidates") for c in out["changes"])
    assert (ws / "areas" / AREA / "gaps" / "authz.json").read_bytes() == saved


def test_a_run_clears_only_the_stale_files_it_wrote(tmp_path, capsys):
    # G45: the clear is the script's job: a stale file run_gaps wrote (its
    # references carry `lacking_numbers`) is removed; a hand file and an R9
    # `new-<name>.json` never are. --check removes nothing.
    repo, ws = build(tmp_path)
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    ours = json.dumps({"references": [{"file": "x", "lacking_sentences": [], "lacking_numbers": []}]})
    (gaps / "old-topic.json").write_text(ours)
    (gaps / "hand.json").write_text("{}")
    (gaps / "new-compliance.json").write_text(ours)
    code, out, _ = run(repo, ws, capsys, "--check")
    assert out["would_clear"] == ["old-topic.json"] and (gaps / "old-topic.json").is_file()
    code, out, _ = run(repo, ws, capsys)
    assert out["cleared"] == ["old-topic.json"] and not (gaps / "old-topic.json").exists()
    assert out["stale_gaps"] == ["hand.json"]
    assert (gaps / "hand.json").is_file() and (gaps / "new-compliance.json").is_file()


def test_every_merged_row_elsewhere_is_listed_whatever_its_speciality(tmp_path, capsys):
    # G46 (1.4.24): a merged plan row whose Artifact is in another area is
    # in `measured_elsewhere` even when no speciality of this area names it.
    repo, ws = build(tmp_path)
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(PLAN + "| gone2 | merged | `cookbook/guidelines/reviewing/sec/gone2` | x |\n")
    code, out, _ = run(repo, ws, capsys)
    row = next(r for r in out["measured_elsewhere"] if r["topic"] == "gone2")
    assert row == {"topic": "gone2", "folder": "cookbook/guidelines/reviewing/sec/gone2",
                   "plan": "reviewing/sec", "specialities": []}
    assert out["why_empty"] is None


def test_an_area_with_no_topic_to_measure_says_why(tmp_path, capsys):
    # G46: `topics` empty carries `why_empty`.
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    (a / "reference.json").write_text("[]")
    u = json.loads((a / "unmeasured.json").read_text())
    u.update(building=[], against_survivor=[], survivor_elsewhere=[])
    (a / "unmeasured.json").write_text(json.dumps(u))
    (ws / "worklist.json").write_text(json.dumps({"batches": []}))
    (a / "area-plan.md").write_text(PLAN.split("| authn")[0])
    code, out, _ = run(repo, ws, capsys)
    assert out["topics"] == [] and out["why_empty"] == "area has no speciality"


def test_every_sentence_not_fully_measured_is_listed_with_its_mark(tmp_path, capsys):
    # G48 (1.4.24): every not-fully-measured sentence is listed, whatever its
    # mark, each row naming `marked_for`.
    repo, ws = build(tmp_path)
    b = run(repo, ws, capsys)[1]["building"][0]
    assert b["unmeasured_sentences"] == [{"n": 6, "marked_for": AREA}, {"n": 10, "marked_for": AREA}]


def test_a_sentence_not_measured_and_marked_elsewhere_names_that_area(tmp_path, capsys):
    # G64 (1.4.24): a sentence cookr did not fully measure, marked for another
    # area, is still listed, and `marked_for` says whose it is.
    repo, ws = build(tmp_path)
    f = ws / "areas" / AREA / "building-security.json"
    data = json.loads(f.read_text())
    data["marks"]["6"] = "reviewing/sec"
    f.write_text(json.dumps(data))
    b = run(repo, ws, capsys)[1]["building"][0]
    assert {"n": 6, "marked_for": "reviewing/sec"} in b["unmeasured_sentences"]
    assert 6 in b["other_area"] and 6 not in b["gap_candidates"]


def test_a_mark_naming_several_areas_counts_for_each(tmp_path, capsys):
    # G55 (1.4.24): a mark may be a list of areas; this area in it makes the
    # sentence this area's.
    repo, ws = build(tmp_path)
    f = ws / "areas" / AREA / "building-security.json"
    data = json.loads(f.read_text())
    data["marks"]["4"] = ["reviewing/sec", AREA]
    data["marks"]["9"] = ["reviewing/sec", "shipping"]
    f.write_text(json.dumps(data))
    b = run(repo, ws, capsys)[1]["building"][0]
    assert 4 in b["gap_candidates"] and 9 not in b["gap_candidates"] and 9 in b["other_area"]


def test_a_lacking_sentence_finds_its_home_in_any_topic_of_the_area(tmp_path, capsys):
    # G50 (1.4.24): a topic folder of the area that no speciality names is
    # searched too, for home_guess and `lacking_candidates`; never measured.
    repo, ws = build(tmp_path)
    f = repo / "cookbook/guidelines/implementing/sec/backups"
    f.mkdir()
    (f / "artifact.json").write_text('{"meta": {}, "parts": [{"part": "rules", "role": "rules"}]}\n')
    (f / "rules.md").write_text("- Encrypt every backup file with a key held outside the backup store.\n")
    out = run(repo, ws, capsys)[1]
    by_n = {s["n"]: s for s in out["building"][0]["sentences"]}
    assert by_n[8]["home_guess"] == "backups"
    assert by_n[8]["lacking_candidates"][0]["topic"] == "backups"
    assert "backups" not in [t["topic"] for t in out["topics"]]


def test_one_lacking_text_in_several_specialities_is_grouped(tmp_path, capsys):
    # G51 (1.4.24): identical lacking text across specialities is grouped in
    # `same_text`; each speciality still lists it.
    repo, ws = build(tmp_path)
    line = "Log every authorization decision with the subject and the resource named.\n"
    with (ws / "areas" / AREA / "reference" / "security--vp.txt").open("a") as fh:
        fh.write(line)
    out = run(repo, ws, capsys)[1]
    row = next(r for r in out["same_text"] if r["text"] == line.strip())
    assert row["specialities"] == ["security/shared", "security/vp"]
    vp = next(t for t in out["topics"] if t["topic"] == "vp")
    assert all(r["lacking"] >= 1 for r in vp["references"] if r["speciality"] in row["specialities"])


def test_topic_counts_split_own_and_building_marked_elsewhere(tmp_path, capsys):
    # G52 (1.4.24): each topic's counts split into `own` and
    # `building_marked_elsewhere` (building pieces whose sentence is marked
    # for another area), the totals kept.
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    for t in out["topics"]:
        for k in ("pieces", "held", "lacking"):
            assert t["own"][k] + t["building_marked_elsewhere"][k] == t[k], (t["topic"], k)
    authn = next(t for t in out["topics"] if t["topic"] == "authn")
    assert authn["building_marked_elsewhere"]["pieces"] >= 1      # sentence 5 is reviewing/sec's


def test_a_new_topic_candidate_outside_the_area_is_its_r9_target(tmp_path, capsys):
    # G53 (1.4.24): a speciality a `new` worklist topic of this area claims,
    # whose reference topic lies outside the area, is that topic's R9 target
    # (`new-<name>.json`), never measured as an existing topic.
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    f = repo / "cookbook/principles/lae"
    f.mkdir(parents=True)
    (f / "artifact.json").write_text('{"meta": {}, "parts": [{"part": "rules", "role": "rules"}]}\n')
    (f / "rules.md").write_text("- Surprise no reader of the code.\n")
    (a / "reference" / "security--lae.txt").write_text("Never surprise a reader of the code you write.\n")
    rows = json.loads((a / "reference.json").read_text())
    rows.append({"speciality": "security/lae", "topic": "cookbook/principles/lae",
                 "file": str(a / "reference" / "security--lae.txt")})
    (a / "reference.json").write_text(json.dumps(rows))
    wl = json.loads((ws / "worklist.json").read_text())
    for t in wl["batches"][0]["topics"]:
        if t["topic"] == "compliance":
            t["devteam"] = [{"speciality": "security/lae"}]
    (ws / "worklist.json").write_text(json.dumps(wl))
    out = run(repo, ws, capsys)[1]
    assert "lae" not in [t["topic"] for t in out["topics"]]
    assert not (a / "gaps" / "lae.json").exists()
    assert out["r9_targets"] == [{"topic": "compliance", "candidate": "cookbook/principles/lae",
                                  "speciality": "security/lae", "file": str(a / "reference" / "security--lae.txt"),
                                  "out": "new-compliance.json"}]
    assert "compliance" in out["r9_missing"]


def test_unplaced_pieces_is_always_there(tmp_path, capsys):
    # G56 (1.4.24): every building entry carries `unplaced_pieces`, [] or not.
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    assert all(isinstance(b["unplaced_pieces"], list) for b in out["building"])


def test_a_cookr_package_beside_the_scripts_never_shadows_cookr(tmp_path, capsys, monkeypatch):
    # G44 (1.4.24): cookr runs with `-P` from the scripts' own folder, so not
    # even a `cookr` package there is imported in place of the real one.
    repo, ws = build(tmp_path)
    here = tmp_path / "here"
    here.mkdir()
    for f in run_gaps.HERE.glob("*.py"):
        (here / f.name).write_bytes(f.read_bytes())
    (here / "cookr").mkdir()
    (here / "cookr" / "__init__.py").write_text("raise SystemExit('shadowed cookr imported')\n")
    monkeypatch.setattr(run_gaps, "HERE", here)
    code, out, err = run(repo, ws, capsys)
    assert out["failed"] == [], out["failed"]
    assert "shadowed" not in err


def test_ours_never_claims_an_r9_file_or_a_hand_file(tmp_path, capsys):
    # G45 (1.4.24): only a file whose every reference carries `lacking_numbers`
    # is run_gaps' own; an R9 `new-<name>.json` never is, whatever it holds,
    # and a hand file with references of its own shape is kept by a run.
    wrote = {"references": [{"file": "x", "lacking_numbers": []}]}
    hand = {"references": [{"file": "x", "lacking_sentences": ["Kept by hand."]}]}
    for name, data in (("new-r9.json", wrote), ("hand-refs.json", hand), ("ours.json", wrote)):
        (tmp_path / name).write_text(json.dumps(data))
    assert not run_gaps.ours(tmp_path / "new-r9.json")
    assert not run_gaps.ours(tmp_path / "hand-refs.json")
    assert run_gaps.ours(tmp_path / "ours.json")
    repo, ws = build(tmp_path / "t")
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    (gaps / "hand-refs.json").write_text(json.dumps(hand))
    code, out, _ = run(repo, ws, capsys)
    assert out["cleared"] == [] and (gaps / "hand-refs.json").is_file()
    assert "hand-refs.json" in out["stale_gaps"]


def test_lacking_candidates_are_the_top_three_topics_by_share():
    # G50 (1.4.24): up to three of the area's topic folders, best share first.
    area_words = {name: (run_gaps.words(text), None) for name, text in (
        ("a", "retry backoff jitter budget"), ("b", "retry backoff"), ("c", "retry"),
        ("d", "jitter"), ("e", "unrelated words only"))}
    s = {"home_guess": None}
    run_gaps._candidates(s, "Retry with backoff and jitter within a budget.", area_words)
    assert [c["topic"] for c in s["lacking_candidates"]] == ["a", "b", "c"]
    assert s["lacking_candidates"][0]["share"] > s["lacking_candidates"][1]["share"]


def test_a_sentence_marked_here_or_for_here_among_others_is_own():
    # G52 (1.4.24): only a sentence marked for other areas alone counts as
    # building_marked_elsewhere; one marked here, or for a list naming this
    # area, stays `own`.
    topics = [{"topic": "t", "pieces": 3, "held": 1, "lacking": 2,
               "references": [{"file": "f", "lacking_numbers": [2, 3]}]}]
    pieces_of = {"f": ([1, 2, 3], {1: AREA, 2: [AREA, "implementing/ui"], 3: "implementing/ui"})}
    run_gaps._split(topics, pieces_of, AREA)
    assert topics[0]["building_marked_elsewhere"] == {"pieces": 1, "held": 0, "lacking": 1}
    assert topics[0]["own"] == {"pieces": 2, "held": 1, "lacking": 1}


def test_a_topic_folder_that_cannot_be_read_is_listed_unplaced(tmp_path, capsys):
    # fix round 1, I3: a folder of the area whose artifact.json cannot be read
    # is a row in `unplaced` with its error, never silently left out.
    repo, ws = build(tmp_path)
    broken = repo / "cookbook" / "guidelines" / AREA / "broken"
    broken.mkdir()
    (broken / "artifact.json").write_text("{not json")
    code, out, err = run(repo, ws, capsys)
    assert code == 2     # fix round 2, N-A: an unplaced topic stops the run
    assert [(u["topic"], u["folder"]) for u in out["unplaced"]] == [
        ("broken", f"cookbook/guidelines/{AREA}/broken")]
    assert "cannot read" in out["unplaced"][0]["why"] and "broken" in err


def test_a_write_run_that_exits_2_on_an_unplaced_topic_still_writes_every_gaps_file(tmp_path, capsys):
    # fix round 3, T-1: exit 2 on an `unplaced` row is only the return value;
    # every other topic's gaps file and the full JSON are written first.
    repo, ws = build(tmp_path)
    broken = repo / "cookbook" / "guidelines" / AREA / "broken"
    broken.mkdir()
    (broken / "artifact.json").write_text("{not json")
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and [u["topic"] for u in out["unplaced"]] == ["broken"]
    gaps = ws / "areas" / AREA / "gaps"
    assert sorted(p.name for p in gaps.iterdir()) == ["authn.json", "authz.json", "vp.json"]
    assert all(json.loads((gaps / n).read_text())["written_by"] == "run_gaps.py" for n in ("authn.json", "authz.json", "vp.json"))
    assert sorted(r["topic"] for r in out["topics"]) == ["authn", "authz", "vp"] and out["building"]


def test_a_relative_speciality_file_is_refused_naming_it(tmp_path, capsys):
    # fix round 1, M2: cookr runs from the scripts folder, so a relative
    # `--against`/file path would resolve there; it is refused at read time.
    repo, ws = build(tmp_path)
    ref = ws / "areas" / AREA / "reference.json"
    rows = json.loads(ref.read_text())
    rows[1]["file"] = "areas/implementing/sec/reference/security--authz.txt"
    ref.write_text(json.dumps(rows))
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and out is None and "areas/implementing/sec/reference/security--authz.txt" in err
    assert "relative" in err
    repo, ws = build(tmp_path / "b")
    um = ws / "areas" / AREA / "unmeasured.json"
    data = json.loads(um.read_text())
    data["building"][0]["file"] = "reference/building--security.txt"
    um.write_text(json.dumps(data))
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and out is None and "reference/building--security.txt" in err and "relative" in err


def test_a_run_clears_its_own_file_with_no_references_never_a_hand_one(tmp_path, capsys):
    # fix round 1, M6: every file run_gaps writes says so (`written_by`), so
    # one with no references is cleared too; a hand file or R9 file never is.
    mine = {"folder": "x", "references": [], "written_by": "run_gaps.py"}
    (tmp_path / "old.json").write_text(json.dumps(mine))
    (tmp_path / "new-x.json").write_text(json.dumps(mine))
    (tmp_path / "hand.json").write_text(json.dumps({"folder": "x", "references": []}))
    assert run_gaps.ours(tmp_path / "old.json")
    assert not run_gaps.ours(tmp_path / "new-x.json") and not run_gaps.ours(tmp_path / "hand.json")
    repo, ws = build(tmp_path / "t")
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    for name in ("old.json", "new-x.json", "hand.json"):
        (gaps / name).write_bytes((tmp_path / name).read_bytes())
    code, out, _ = run(repo, ws, capsys)
    assert out["cleared"] == ["old.json"] and not (gaps / "old.json").exists()
    assert (gaps / "new-x.json").is_file() and (gaps / "hand.json").is_file()
    written = [json.loads(p.read_text()) for p in gaps.glob("*.json") if p.name not in ("new-x.json", "hand.json")]
    assert written and all(d.get("written_by") == "run_gaps.py" for d in written)


def test_a_measured_topic_its_sentences_cannot_be_read_from_is_listed_unplaced(tmp_path, capsys, monkeypatch):
    # fix round 1, I3: a measured topic cookr read but whose sentences cannot
    # be read for hints is listed once in `unplaced`, never silently empty;
    # one outside the area too, which no walk of the area's folders sees.
    for broken_name, folder in (("authz", f"cookbook/guidelines/{AREA}/authz"),
                                ("vp", "cookbook/guidelines/reviewing/sec/vp")):
        repo, ws = build(tmp_path / broken_name)
        real = run_gaps.topic_sentences

        def broken(f, real=real, broken_name=broken_name):
            if Path(f).name == broken_name:
                raise SystemExit(f"paraphrase_hints.py: cannot read {f}/artifact.json (test)")
            return real(f)
        monkeypatch.setattr(run_gaps, "topic_sentences", broken)
        code, out, err = run(repo, ws, capsys)
        monkeypatch.setattr(run_gaps, "topic_sentences", real)
        assert [u["folder"] for u in out["unplaced"]] == [folder], broken_name
        assert "(test)" in out["unplaced"][0]["why"]


def test_a_file_a_run_would_clear_is_never_also_stale(tmp_path):
    # fix round 1, N2: `stale_gaps` leaves out what a run clears, whatever the
    # mode; a run that writes nothing names it in `would_clear` only.
    repo, ws = build(tmp_path)
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    (gaps / "old.json").write_text(json.dumps({"folder": "x", "references": [], "written_by": "run_gaps.py"}))
    (gaps / "hand.json").write_text(json.dumps({"folder": "x", "references": []}))
    with tempfile.TemporaryDirectory() as scratch:
        result, _ = run_gaps.run(AREA, ws, repo, gaps, sys.executable, CLI, mode="fresh", scratch=Path(scratch))
    assert result["would_clear"] == ["old.json"]
    assert "old.json" not in result["stale_gaps"] and "hand.json" in result["stale_gaps"]
    assert (gaps / "old.json").is_file()


def test_check_lists_an_unplaced_topic_and_exits_2_even_unchanged(tmp_path, capsys):
    # fix round 2, N-A: a topic unreadable in both the saved and the fresh pass
    # is no change, yet `--check` names it in `unplaced` and exits 2.
    repo, ws = build(tmp_path)
    broken = repo / "cookbook" / "guidelines" / AREA / "broken"
    broken.mkdir()
    (broken / "artifact.json").write_text("{not json")
    run(repo, ws, capsys)
    code, out, err = run(repo, ws, capsys, "--check")
    assert code == 2 and out["check"] == "unchanged"
    assert [u["folder"] for u in out["unplaced"]] == [f"cookbook/guidelines/{AREA}/broken"]
    assert "cannot read" in out["unplaced"][0]["why"]


# 1.4.25: G66 hints at an authored home, G67 --check, G68 home measures,
# G72 short sentences, G90 the saved report.

def _backups(repo: Path) -> None:
    """A topic folder of the area no speciality names, holding sentence 8."""
    f = repo / "cookbook/guidelines/implementing/sec/backups"
    f.mkdir()
    (f / "artifact.json").write_text('{"meta": {}, "parts": [{"part": "rules", "role": "rules"}]}\n')
    (f / "rules.md").write_text("- Encrypt every backup file with a key held outside the backup store.\n")


def test_hints_at_a_home_no_speciality_names_never_crash(tmp_path, capsys):
    # G66: sentence 8's home_guess is `backups`, a folder of the area no
    # speciality names (from the area's words): --hints ranks it there.
    repo, ws = build(tmp_path)
    _backups(repo)
    code, out, err = run(repo, ws, capsys, "--hints")
    assert code == 0, err
    by_n = {s["n"]: s for s in out["building"][0]["sentences"]}
    assert by_n[8]["home_guess"] == "backups" and by_n[8]["hints_at"] == "backups"
    assert by_n[8]["hints"] and {h["topic"] for h in by_n[8]["hints"]} == {"backups"}
    assert out["advisory_failed"] == []


def test_an_advisory_failure_finishes_the_run_and_is_named(tmp_path, capsys, monkeypatch):
    # G66, G82: a failing advisory part never stops the run after its writes:
    # every gaps file and the report are written, the failure is listed in
    # `advisory_failed`, named on stderr, and the exit is not 1.
    repo, ws = build(tmp_path)

    def boom(*_a, **_k):
        raise RuntimeError("rank broke")
    monkeypatch.setattr(run_gaps, "rank", boom)
    code, out, err = run(repo, ws, capsys, "--hints")
    assert code == 0 and "rank broke" in err
    assert out["advisory_failed"] and all(x["part"] == "hints" and "rank broke" in x["why"]
                                          for x in out["advisory_failed"])
    assert sorted(p.name for p in (ws / "areas" / AREA / "gaps").iterdir()) == ["authn.json", "authz.json", "vp.json"]
    assert json.loads((ws / "areas" / AREA / "run_gaps.json").read_text())["advisory_failed"] == out["advisory_failed"]


def test_short_sentences_cookr_leaves_out_are_listed_for_every_speciality(tmp_path, capsys):
    # G72: a sentence under six words is never measured; each one of every
    # speciality, direct or building, measured at a topic or not, is listed.
    repo, ws = build(tmp_path)
    with (ws / "areas" / AREA / "reference" / "security--authz.txt").open("a") as fh:
        fh.write("\nDeny by default.\n")
    out = run(repo, ws, capsys)[1]
    rows = [{k: r[k] for k in ("speciality", "n", "text")} for r in out["short_sentences"]]   # G101: more keys
    assert {"speciality": "security/authz", "n": 2, "text": "Deny by default."} in rows
    assert {"speciality": "building/security", "n": 6, "text": "Never log a secret."} in rows
    assert {"speciality": "building/security", "n": 10, "text": "never float it."} in rows
    assert {"speciality": "building/audit", "n": 2, "text": "Ship logs off the host."} in rows   # measured at no topic
    assert len(rows) == len({(r["speciality"], r["n"], r["text"]) for r in rows})


def test_the_report_is_saved_beside_the_gaps_folder(tmp_path, capsys):
    # G90: a run writes its JSON to A/run_gaps.json itself (exit 2 too); --check never.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    report = ws / "areas" / AREA / "run_gaps.json"
    assert json.loads(report.read_text()) == out
    before = report.read_bytes()
    run(repo, ws, capsys, "--check")
    assert report.read_bytes() == before
    (ws / "areas" / AREA / "reference" / "security--authz.txt").unlink()
    code, out, _ = run(repo, ws, capsys)
    assert code == 2 and json.loads(report.read_text())["failed"] == out["failed"]


def test_check_counts_a_file_it_would_clear_as_a_change(tmp_path, capsys):
    # G67: `would_clear` not empty is a change, never `unchanged`.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    ours = json.dumps({"written_by": "run_gaps.py", "references": []})
    (ws / "areas" / AREA / "gaps" / "old-topic.json").write_text(ours)
    code, out, _ = run(repo, ws, capsys, "--check")
    assert code == 1 and out["check"] == "changed" and out["would_clear"] == ["old-topic.json"]
    assert any(c["path"] == "would_clear" for c in out["changes"])


def test_check_compares_every_key_of_the_saved_report(tmp_path, capsys):
    # G67: measured_elsewhere, why_empty, r9_missing and unmeasured_sentences
    # are compared with the saved A/run_gaps.json, so no --out run is needed.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    a = ws / "areas" / AREA
    (a / "gaps" / "new-compliance.json").write_text("{}")                       # r9_missing
    (a / "area-plan.md").write_text(PLAN + "| gone2 | merged | `cookbook/guidelines/reviewing/sec/gone2` | x |\n")
    f = a / "building-security.json"                                            # unmeasured_sentences
    data = json.loads(f.read_text())
    data["marks"]["6"] = "reviewing/sec"
    f.write_text(json.dumps(data))
    code, out, _ = run(repo, ws, capsys, "--check")
    paths = [c["path"] for c in out["changes"]]
    assert code == 1
    assert "r9_missing" in paths and "measured_elsewhere" in paths
    assert any(p.startswith("building[building/security].unmeasured_sentences") for p in paths), paths


def test_check_without_a_saved_report_is_a_change(tmp_path, capsys):
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    (ws / "areas" / AREA / "run_gaps.json").unlink()
    code, out, _ = run(repo, ws, capsys, "--check")
    assert code == 1 and {"path": "run_gaps.json", "was": None, "now": "missing"} in out["changes"]


def _devteam(tmp: Path) -> Path:
    """A stand-in devteam whose speciality_reference.py writes building/extra."""
    d = tmp / "devteam"
    d.mkdir(exist_ok=True)
    (d / "speciality_reference.py").write_text(
        "import json, sys, pathlib\n"
        "out = pathlib.Path(sys.argv[sys.argv.index('--out') + 1]); out.mkdir(parents=True, exist_ok=True)\n"
        "f = out / (sys.argv[1].replace('/', '--') + '.txt')\n"
        "f.write_text('Encrypt every backup file with a key held outside the backup store.\\n')\n"
        "print(json.dumps([{'speciality': sys.argv[1], 'topic': None, 'file': str(f)}]))\n")
    return d


def test_a_sentence_homed_at_a_topic_no_speciality_names_is_measured_there(tmp_path, capsys):
    # G68: sentence 8's home is `backups`, which no speciality names: it is
    # measured there into gaps/home--backups.json (run_gaps' own file), with a
    # verdict per sentence in `home_measures`. A `marked_here` speciality
    # with no building row gets its reference written into A/reference/.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = ws / "areas" / AREA
    u = json.loads((a / "unmeasured.json").read_text())
    u["marked_here"].append({"speciality": "building/extra", "n": 1, "marked_by": ["reviewing/sec"],
                             "text": "Encrypt every backup file with a key held outside the backup store."})
    (a / "unmeasured.json").write_text(json.dumps(u))
    code, out, err = run(repo, ws, capsys, "--devteam", str(_devteam(tmp_path)))
    assert code == 0, err
    assert (a / "reference" / "building--extra.txt").is_file()
    home = json.loads((a / "gaps" / "home--backups.json").read_text())
    assert home["written_by"] == "run_gaps.py"
    row = out["home_measures"][0]
    assert row["topic"] == "backups" and row["gaps_file"] == "home--backups.json"
    assert row["folder"] == "cookbook/guidelines/implementing/sec/backups"
    assert row["specialities"] == ["building/extra", "building/security"]
    assert {"speciality": "building/security", "n": 8, "verdict": "held", "marked_for": AREA} in row["sentences"]
    assert {"speciality": "building/extra", "n": 1, "verdict": "held", "marked_for": AREA} in row["sentences"]
    assert "home--backups.json" not in out["stale_gaps"]
    assert stage_status.status(AREA, ws, repo)["stale_gaps"] == []
    code, chk, _ = run(repo, ws, capsys, "--check", "--devteam", str(_devteam(tmp_path)))
    assert code == 0, chk["changes"]
    import shutil
    shutil.rmtree(repo / "cookbook/guidelines/implementing/sec/backups")
    code, out, _ = run(repo, ws, capsys, "--devteam", str(_devteam(tmp_path)))
    assert out["home_measures"] == [] and out["cleared"] == ["home--backups.json"]
    assert not (a / "gaps" / "home--backups.json").exists()


def test_a_marked_here_speciality_with_no_devteam_is_a_missing_file(tmp_path, capsys):
    # G68: with no speciality_reference.py to write it, the speciality is
    # listed in missing_files, never dropped.
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    u = json.loads((a / "unmeasured.json").read_text())
    u["marked_here"].append({"speciality": "building/extra", "n": 1, "marked_by": ["reviewing/sec"], "text": "X."})
    (a / "unmeasured.json").write_text(json.dumps(u))
    code, out, _ = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))
    assert any(m["speciality"] == "building/extra" and "speciality_reference.py" in m["why"]
               for m in out["missing_files"])


# 1.4.26 (gapfix7 fix round 1): I2 marked_here text checked, M1 home file
# names, M2 a home file without the reference, M3 advisory_failed compared,
# M4 a --out run's report, N1 OSError recorded, N3 R9 survives the clear.

BACKUP = "Encrypt every backup file with a key held outside the backup store."


def _marked_extra(ws: Path, n: int, text: str | None) -> Path:
    a = ws / "areas" / AREA
    u = json.loads((a / "unmeasured.json").read_text())
    row = {"speciality": "building/extra", "n": n, "marked_by": ["reviewing/sec"]}
    if text is not None:
        row["text"] = text
    u["marked_here"].append(row)
    (a / "unmeasured.json").write_text(json.dumps(u))
    return a


def _two_sentence_reference(a: Path) -> None:
    """building/extra's reference renumbered: a sentence inserted before it."""
    (a / "reference").mkdir(exist_ok=True)
    (a / "reference" / "building--extra.txt").write_text(
        "Rotate every signing key on a fixed schedule written down in advance.\n\n" + BACKUP + "\n")


def test_a_marked_here_row_whose_text_moved_is_carried_by_its_text(tmp_path, capsys):
    # I2: the marks numbered sentence 1 against an older reference; the
    # reference now has another sentence at 1. The row is never measured as
    # that other sentence: it is listed in `numbering_differs` and measured
    # as the sentence its text names (now 2).
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 1, BACKUP)
    _two_sentence_reference(a)
    code, out, err = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))
    # R2-M-4 (1.4.28): with no writer the old file is used, stale: exit 1.
    assert code == 1 and [r["speciality"] for r in out["stale_reference"]] == ["building/extra"], err
    assert out["numbering_differs"] == [{"speciality": "building/extra", "n": 1, "text": BACKUP,
                                         "now": "Rotate every signing key on a fixed schedule written down in advance.",
                                         "found_at": [2], "measured_as": 2}]
    rows = [s for h in out["home_measures"] for s in h["sentences"] if s["speciality"] == "building/extra"]
    assert rows == [{"speciality": "building/extra", "n": 2, "verdict": "held", "marked_for": AREA}]


def test_a_marked_here_row_whose_text_is_gone_is_listed_never_measured(tmp_path, capsys):
    # I2: the text at n differs and is nowhere in the reference: listed with
    # `measured_as` null, and no sentence of building/extra is measured.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 2, "Hash every password with a slow memory hard function always.")
    _two_sentence_reference(a)
    out = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))[1]
    assert out["numbering_differs"] == [{"speciality": "building/extra", "n": 2,
                                         "text": "Hash every password with a slow memory hard function always.",
                                         "now": BACKUP, "found_at": [], "measured_as": None}]
    assert not any(s["speciality"] == "building/extra" for h in out["home_measures"] for s in h["sentences"])


def test_a_marked_here_row_with_no_text_is_listed_as_unchecked(tmp_path, capsys):
    # I2: a row with no text cannot be checked: measured by its n, and listed.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 1, None)
    (a / "reference").mkdir(exist_ok=True)
    (a / "reference" / "building--extra.txt").write_text(BACKUP + "\n")
    out = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))[1]
    assert out["numbering_differs"] == [{"speciality": "building/extra", "n": 1, "text": None, "now": BACKUP,
                                         "found_at": [], "measured_as": 1}]


def test_a_matching_marked_here_row_is_not_listed(tmp_path, capsys):
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 2, BACKUP.upper())          # normalised as quote_building compares
    _two_sentence_reference(a)
    out = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))[1]
    assert out["numbering_differs"] == []


def test_home_files_take_a_name_no_topic_file_can_take(tmp_path, capsys):
    # M1: a home file is `home--<topic>.json`; a topic's own gaps file named
    # `home-x.json` (a topic folder `home-x`) is never cleared as a home file
    # nor hidden from `stale_gaps`.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = ws / "areas" / AREA
    (a / "gaps").mkdir(exist_ok=True)
    topic_file = json.dumps({"written_by": "run_gaps.py", "references": []})
    (a / "gaps" / "home-x.json").write_text(topic_file)      # another set's topic `home-x`
    code, out, err = run(repo, ws, capsys)
    assert code == 0, err
    assert [h["gaps_file"] for h in out["home_measures"]] == ["home--backups.json"]
    assert (a / "gaps" / "home--backups.json").is_file()
    assert "home-x.json" in out["cleared"]                    # cleared as the topic file it is, by stale()
    (a / "gaps" / "home-x.json").write_text(json.dumps({"references": []}))   # not ours: kept, and stale
    out = run(repo, ws, capsys)[1]
    assert "home-x.json" in out["stale_gaps"] and (a / "gaps" / "home-x.json").is_file()


def test_a_home_file_without_the_reference_reads_not_measured(tmp_path, capsys):
    # M2: a saved home file that never measured this reference gives no
    # verdict: "not measured", never "held", and the row names the file.
    repo, ws = build(tmp_path)
    _backups(repo)
    run(repo, ws, capsys)
    a = ws / "areas" / AREA
    f = a / "gaps" / "home--backups.json"
    data = json.loads(f.read_text())
    data["references"] = []
    f.write_text(json.dumps(data))
    saved, _ = run_gaps.run(AREA, ws, repo, a / "gaps", sys.executable, CLI, mode="saved")
    row = saved["home_measures"][0]
    assert {"speciality": "building/security", "n": 8, "verdict": "not measured", "marked_for": AREA} in row["sentences"]
    sec = next(b["file"] for b in saved["building"] if b["speciality"] == "building/security")
    assert row["unmeasured_references"] == [sec]


def test_check_compares_advisory_failed(tmp_path, capsys, monkeypatch):
    # M3: a hint that failed at the run and works now (or the reverse) is a change.
    repo, ws = build(tmp_path)

    def boom(*_a, **_k):
        raise RuntimeError("rank broke")
    with monkeypatch.context() as mp:
        mp.setattr(run_gaps, "rank", boom)
        run(repo, ws, capsys, "--hints")
    code, out, _ = run(repo, ws, capsys, "--check", "--hints")
    assert code == 1 and any(c["path"].startswith("advisory_failed") for c in out["changes"]), out["changes"]


def test_a_run_with_its_own_out_saves_its_report_there(tmp_path, capsys):
    # M4: `--out DIR` other than A/gaps saves DIR/run_gaps.json, never the
    # area's A/run_gaps.json; the report is never a stale gaps file.
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    run(repo, ws, capsys)
    real = (a / "run_gaps.json").read_bytes()
    scratch = tmp_path / "scratch"      # R2-M-1 (1.4.28): never a folder inside the area but A/gaps
    code, out, _ = run(repo, ws, capsys, "--out", str(scratch))
    assert (a / "run_gaps.json").read_bytes() == real
    assert json.loads((scratch / "run_gaps.json").read_text()) == out
    out = run(repo, ws, capsys, "--out", str(scratch))[1]
    assert "run_gaps.json" not in out["stale_gaps"] and "run_gaps.json" not in out["cleared"]
    code, chk, _ = run(repo, ws, capsys, "--check", "--out", str(scratch))
    assert code == 0, chk["changes"]


def test_a_reference_writer_that_cannot_start_is_a_missing_file(tmp_path):
    # N1: speciality_reference.py run by a python that does not exist: listed, never a traceback.
    a = tmp_path / "a"
    a.mkdir()
    f, why, stale = run_gaps._reference("building/extra", a, "write", None, _devteam(tmp_path),
                                        str(tmp_path / "no-python"))
    assert f is None and "speciality_reference.py" in why and stale is False


def test_a_home_sentence_cookr_cannot_cut_is_failed_not_a_traceback(tmp_path, capsys, monkeypatch):
    # N1: an OSError cutting a home-measured file is recorded in `failed`.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 1, BACKUP)
    (a / "reference").mkdir(exist_ok=True)
    (a / "reference" / "building--extra.txt").write_text(BACKUP + "\n")
    real = run_gaps.cookr_pieces

    def flaky(file, *rest):
        if file.endswith("building--extra.txt"):
            raise OSError("cookr went away")
        return real(file, *rest)
    monkeypatch.setattr(run_gaps, "cookr_pieces", flaky)
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and any(x.get("speciality") == "building/extra" and "cookr went away" in x["why"]
                             for x in out["failed"]), err


def test_an_r9_file_survives_the_home_clear(tmp_path, capsys):
    # N3 (G68 regression): clearing home files never touches an R9 `new-*`.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = ws / "areas" / AREA
    run(repo, ws, capsys)
    r9 = json.dumps({"references": [{"file": "x", "lacking_numbers": []}]})
    (a / "gaps" / "new-backups.json").write_text(r9)
    import shutil
    shutil.rmtree(repo / "cookbook/guidelines/implementing/sec/backups")
    out = run(repo, ws, capsys)[1]
    assert "home--backups.json" in out["cleared"]
    assert (a / "gaps" / "new-backups.json").read_text() == r9


def test_a_refused_input_leaves_the_saved_report_as_it_was(tmp_path, capsys):
    # N2: exit 2 from a refusal (before any run) writes no report; only a
    # run that exits 2 saves one. The saved report stays the last run's.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    report = ws / "areas" / AREA / "run_gaps.json"
    before = report.read_bytes()
    (ws / "areas" / AREA / "unmeasured.json").unlink()
    code, out, err = run(repo, ws, capsys)
    assert code == 2 and out is None and report.read_bytes() == before


def test_a_run_with_its_own_out_writes_a_missing_reference_there(tmp_path, capsys):
    # M4 (writes): a `--out DIR` run writes a `marked_here` speciality's
    # missing reference into DIR/reference, never into the area's
    # A/reference; `--check --out DIR` reads it back there.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = ws / "areas" / AREA
    _marked_extra(ws, 1, BACKUP)
    scratch = tmp_path / "scratch"
    dt = str(_devteam(tmp_path))
    code, out, err = run(repo, ws, capsys, "--out", str(scratch), "--devteam", dt)
    assert code == 0, err
    assert not (a / "reference" / "building--extra.txt").exists()
    assert (scratch / "reference" / "building--extra.txt").is_file()
    assert {"speciality": "building/extra", "n": 1, "verdict": "held", "marked_for": AREA} in out["home_measures"][0]["sentences"]
    code, chk, _ = run(repo, ws, capsys, "--check", "--out", str(scratch), "--devteam", dt)
    assert code == 0, chk["changes"]



# 1.4.27 (gapfix7 fix round 2): R-I-1 stale references, R-I-2 unmeasured
# numbering rows judged by hand, R-M-1 --out the area refused, R-M-2 hints
# recorded, R-M-3 scratch references rewritten, R-M-4 --check --out, R-N-1.

def _unstamp(ws: Path, *specialities: str) -> None:
    """Those rows as a pre-1.4.26 speciality_reference.py wrote them: no `format`."""
    ref = ws / "areas" / AREA / "reference.json"
    rows = json.loads(ref.read_text())
    for r in rows:
        if r["speciality"] in specialities:
            r.pop("format", None)
    ref.write_text(json.dumps(rows))


def test_a_reference_written_before_1426_is_listed_stale(tmp_path, capsys):
    # R-I-1: a row with no format stamp (or an older one) is never measured
    # as if it were current: it is listed in `stale_reference`, and
    # `--check` counts it as a change.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 0, chk["changes"]
    _unstamp(ws, "security/authn")
    ref = ws / "areas" / AREA / "reference.json"
    rows = json.loads(ref.read_text())
    rows[1]["format"] = FORMAT - 1
    ref.write_text(json.dumps(rows))
    code, out, _ = run(repo, ws, capsys)
    stale = {r["speciality"]: r for r in out["stale_reference"]}
    assert set(stale) == {"security/authn", "security/authz"}
    assert stale["security/authn"]["format"] is None and stale["security/authz"]["format"] == FORMAT - 1
    # R2-M-3: the reference files are step 1.1; 1.2 and 1.3 re-measure.
    assert all(r["want"] == FORMAT and "step 1.1, then steps 1.2 and 1.3" in r["why"] for r in stale.values())
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 1 and any(c["path"] == "stale_reference" for c in chk["changes"]), chk["changes"]
    assert [r["speciality"] for r in chk["stale_reference"]] == ["security/authn", "security/authz"]


def test_a_marked_here_reference_is_rewritten_on_every_run(tmp_path, capsys):
    # R-I-1: a marked_here speciality's reference has no reference.json row
    # to stamp; a run rewrites it with today's speciality_reference.py, so an
    # old A/reference file is never measured as current.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 1, BACKUP)
    (a / "reference").mkdir(exist_ok=True)
    (a / "reference" / "building--extra.txt").write_text("An old text written by an older generator.\n")
    code, out, err = run(repo, ws, capsys, "--devteam", str(_devteam(tmp_path)))
    assert code == 0, err
    assert (a / "reference" / "building--extra.txt").read_text().strip() == BACKUP
    assert out["numbering_differs"] == [] and out["stale_reference"] == []


def test_a_marked_here_reference_no_devteam_can_rewrite_is_stale(tmp_path, capsys):
    # R-I-1: with no speciality_reference.py, an A/reference file is used as
    # it is, its format unknown: listed in `stale_reference`.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 1, BACKUP)
    (a / "reference").mkdir(exist_ok=True)
    (a / "reference" / "building--extra.txt").write_text(BACKUP + "\n")
    out = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))[1]
    assert [(r["speciality"], r["format"]) for r in out["stale_reference"]] == [("building/extra", None)]


def test_an_unmeasured_numbering_row_is_judged_by_hand(tmp_path, capsys):
    # R-I-2: a numbering_differs row not measured (`measured_as` null) is in
    # `home_unguessed` too, the list judged by hand.
    repo, ws = build(tmp_path)
    _backups(repo)
    gone = "Hash every password with a slow memory hard function always."
    a = _marked_extra(ws, 2, gone)
    _two_sentence_reference(a)
    out = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))[1]
    rows = [r for r in out["home_unguessed"] if r["speciality"] == "building/extra"]
    assert rows == [{"speciality": "building/extra", "n": 2, "text": gone, "marked_for": AREA,
                     "why": "numbering differs: its text is not found once in the reference; judge it by hand "
                            "or re-mark it"}]


def test_a_numbering_row_marked_twice_is_listed_and_measured_once(tmp_path, capsys):
    # R-N-1: the same marked_here row twice (two marking plans) gives one
    # numbering_differs row and one sentence at its home.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 1, BACKUP)
    _marked_extra(ws, 1, BACKUP)
    _two_sentence_reference(a)
    out = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))[1]
    assert len(out["numbering_differs"]) == 1
    rows = [s for h in out["home_measures"] for s in h["sentences"] if s["speciality"] == "building/extra"]
    assert rows == [{"speciality": "building/extra", "n": 2, "verdict": "held", "marked_for": AREA}]


def test_two_rows_that_resolve_to_one_sentence_measure_it_once(tmp_path, capsys):
    # R-N-1: two distinct marked_here rows (one by its number, one by its
    # moved text) both name sentence 2: it is measured once at its home.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 2, BACKUP)
    _marked_extra(ws, 7, BACKUP)
    _two_sentence_reference(a)
    out = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))[1]
    rows = [s for h in out["home_measures"] for s in h["sentences"] if s["speciality"] == "building/extra"]
    assert rows == [{"speciality": "building/extra", "n": 2, "verdict": "held", "marked_for": AREA}], rows


def test_out_at_the_area_itself_is_refused(tmp_path, capsys):
    # R-M-1: `--out A` (or a symlink to it, or a folder holding it) would
    # write into the area's own files: refused, exit 2, nothing written.
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    link = tmp_path / "link"
    link.symlink_to(a)
    for out in (a, link, ws / "areas", a / "." ):
        code, res, err = run(repo, ws, capsys, "--out", str(out))
        assert code == 2 and res is None and "--out" in err, (out, err)
    assert not (a / "run_gaps.json").exists() and not (a / "authn.json").exists()


def test_the_default_folder_by_another_spelling_is_the_default(tmp_path, capsys):
    # R-M-1: A/gaps reached through a symlink is the default folder: the
    # report is A/run_gaps.json.
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    (a / "gaps").mkdir(exist_ok=True)
    link = tmp_path / "g"
    link.symlink_to(a / "gaps")
    code, out, err = run(repo, ws, capsys, "--out", str(link))
    assert code == 0, err
    assert (a / "run_gaps.json").is_file() and not (a / "gaps" / "run_gaps.json").exists()


def test_the_report_records_hints_and_check_compares_advisories_only_alike(tmp_path, capsys, monkeypatch):
    # R-M-2: run_gaps.json records whether --hints ran; --check compares
    # `advisory_failed` only when both ran with the same setting, and else
    # says the hints were not compared.
    repo, ws = build(tmp_path)

    def boom(*_a, **_k):
        raise RuntimeError("rank broke")
    with monkeypatch.context() as mp:
        mp.setattr(run_gaps, "rank", boom)
        out = run(repo, ws, capsys, "--hints")[1]
    assert out["hints"] is True and out["advisory_failed"]
    code, chk, _ = run(repo, ws, capsys, "--check", "--no-hints")
    assert code == 0, chk["changes"]
    assert chk["not_compared"] == ["advisory_failed: the saved report ran with --hints, this check without"]
    assert (chk["hints"], chk["hints_from"]) == (False, "flag")
    code, chk, _ = run(repo, ws, capsys, "--check", "--hints")
    assert code == 1 and "not_compared" not in chk


def test_check_without_the_hints_flag_runs_as_the_saved_report_ran(tmp_path, capsys, monkeypatch):
    # G96 (1.4.33): with no --hints/--no-hints, --check takes `hints` from the
    # saved report, so the prescribed pair always compares advisory_failed.
    repo, ws = build(tmp_path)

    def boom(*_a, **_k):
        raise RuntimeError("rank broke")
    with monkeypatch.context() as mp:
        mp.setattr(run_gaps, "rank", boom)
        run(repo, ws, capsys, "--hints")
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert "not_compared" not in chk and (chk["hints"], chk["hints_from"]) == (True, "report"), chk
    assert code == 1 and any(c["path"].startswith("advisory_failed") for c in chk["changes"]), chk["changes"]
    run(repo, ws, capsys, "--no-hints")         # saved without hints (G122: a bare run keeps the saved hints)
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 0 and "not_compared" not in chk and (chk["hints"], chk["hints_from"]) == (False, "report")


def test_a_scratch_reference_is_rewritten_on_every_run(tmp_path, capsys):
    # R-M-3: DIR/reference/<name>.txt left by an earlier --out run is never reused.
    repo, ws = build(tmp_path)
    _backups(repo)
    _marked_extra(ws, 1, BACKUP)
    scratch = tmp_path / "scratch"
    (scratch / "reference").mkdir(parents=True)
    (scratch / "reference" / "building--extra.txt").write_text("An old scratch text.\n")
    code, out, err = run(repo, ws, capsys, "--out", str(scratch), "--devteam", str(_devteam(tmp_path)))
    assert code == 0, err
    assert (scratch / "reference" / "building--extra.txt").read_text().strip() == BACKUP


def test_check_with_its_own_out_compares_that_folders_report(tmp_path, capsys):
    # R-M-4: `--check --out DIR` compares DIR/run_gaps.json (the report a
    # `--out DIR` run saves), never A/run_gaps.json. G172 (1.4.37): with none
    # in DIR it is refused, exit 2 (it once ran and called the report missing).
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    scratch = tmp_path / "scratch"
    code, chk, err = run(repo, ws, capsys, "--check", "--out", str(scratch))
    assert code == 2 and chk is None and str(scratch / "run_gaps.json") in err
    run(repo, ws, capsys, "--out", str(scratch))
    code, chk, _ = run(repo, ws, capsys, "--check", "--out", str(scratch))
    assert chk["report"] == str(scratch / "run_gaps.json") and chk["changes"] == []


def test_a_write_run_with_a_stale_reference_saves_its_report_and_exits_1(tmp_path, capsys):
    # Fix round 3, R2-M-4: a run measured on a stale reference still saves
    # A/run_gaps.json, but exits 1 and says so on stderr, so a script gating
    # on the exit code never takes its figures as current.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    assert code == 0 and out["stale_reference"] == []
    _unstamp(ws, "security/authn")
    report = ws / "areas" / AREA / "run_gaps.json"
    report.unlink()
    code, out, err = run(repo, ws, capsys)
    assert code == 1, err
    assert json.loads(report.read_text())["stale_reference"] == out["stale_reference"]
    assert "stale_reference" in err and "security/authn" in err


def test_out_inside_the_area_other_than_gaps_is_refused(tmp_path, capsys):
    # Fix round 3, R2-M-1: an --out inside the area is A/gaps or below it;
    # A/reference, A/topics or any other folder there is refused, exit 2.
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    before = sorted(p.relative_to(a) for p in a.rglob("*"))
    for out in (a / "reference", a / "topics", a / "gapsx"):
        code, res, err = run(repo, ws, capsys, "--out", str(out))
        assert code == 2 and res is None and "--out" in err, (out, err)
    assert sorted(p.relative_to(a) for p in a.rglob("*")) == before
    code, res, err = run(repo, ws, capsys, "--out", str(a / "gaps" / "scratch"))
    assert code == 0, err
    assert (a / "gaps" / "scratch" / "run_gaps.json").is_file()


def test_check_lists_a_stale_reference_change_once(tmp_path, capsys):
    # Fix round 3, R2-N-2: when the saved report's stale_reference differs,
    # changes() already names it; check adds no second stale_reference entry.
    repo, ws = build(tmp_path)
    _unstamp(ws, "security/authn")
    run(repo, ws, capsys)      # saved: authn stale with no stamp
    ref = ws / "areas" / AREA / "reference.json"
    rows = json.loads(ref.read_text())
    for r in rows:
        if r["speciality"] == "security/authn":
            r["format"] = FORMAT - 1
    ref.write_text(json.dumps(rows))
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 1
    stale = [c["path"] for c in chk["changes"] if c["path"].split("[")[0].split(".")[0] == "stale_reference"]
    assert stale == ["stale_reference[security/authn].format"], chk["changes"]


def test_every_report_records_its_reference_format(tmp_path, capsys):
    # N3-I-1 (1.4.29): a run saves the reference format it measured under,
    # in A/run_gaps.json and in an --out report alike; --check compares it.
    repo, ws = build(tmp_path)
    report = ws / "areas" / AREA / "run_gaps.json"
    code, out, err = run(repo, ws, capsys)
    assert code == 0 and out["reference_format"] == FORMAT, err
    assert json.loads(report.read_text())["reference_format"] == FORMAT
    scratch = tmp_path / "scratch"
    run(repo, ws, capsys, "--out", str(scratch))
    assert json.loads((scratch / "run_gaps.json").read_text())["reference_format"] == FORMAT
    assert run(repo, ws, capsys, "--check")[0] == 0
    for was in (None, FORMAT - 1):          # a report saved before 1.4.29; one a format lower
        saved = json.loads(report.read_text())
        saved.pop("reference_format", None)
        if was is not None:
            saved["reference_format"] = was
        report.write_text(json.dumps(saved))
        code, chk, _ = run(repo, ws, capsys, "--check")
        assert code == 1 and {"path": "reference_format", "was": was, "now": FORMAT} in chk["changes"], chk["changes"]


def test_a_fresh_run_clears_a_report_stage_status_lists_as_old(tmp_path, capsys):
    # N3-I-1: stage_status lists a report with no reference format, or one
    # a format lower, in `stale_reference`; a fresh run_gaps run clears it.
    repo, ws = build(tmp_path)
    report = ws / "areas" / AREA / "run_gaps.json"

    def listed():
        return [(r["speciality"], r["reason"]) for r in stage_status.status(AREA, ws, repo)["stale_reference"]]
    assert listed() == [(None, "old_report")]     # G99 (1.4.33): a plan with no saved report
    assert run(repo, ws, capsys)[0] == 0
    assert listed() == []
    for saved in ({"area": AREA, "topics": []}, {"topics": [], "stale_reference": [], "reference_format": FORMAT - 1}):
        report.write_text(json.dumps(saved))
        assert listed() == [(None, "old_report")]
        assert run(repo, ws, capsys)[0] == 0
        assert listed() == []


def test_a_report_saved_over_a_stale_row_stays_stale_until_the_next_run(tmp_path, capsys):
    # N4-I-1 (1.4.30): a run that lists an old_format row saves its report
    # (exit 1). Stamping the row without a re-run leaves that report in
    # place: stage_status lists it, and a fresh run clears it.
    repo, ws = build(tmp_path)
    ref = ws / "areas" / AREA / "reference.json"
    current = ref.read_text()
    _unstamp(ws, "security/authn")

    def listed():
        return [(r["speciality"], r["reason"]) for r in stage_status.status(AREA, ws, repo)["stale_reference"]]
    assert run(repo, ws, capsys)[0] == 1
    assert listed() == [("security/authn", "old_format"), (None, "old_report")]
    ref.write_text(current)                          # the rows rewritten, run_gaps not re-run
    assert listed() == [(None, "old_report")]
    assert stage_status.status(AREA, ws, repo)["next"] == "plan"
    assert run(repo, ws, capsys)[0] == 0
    assert listed() == []


def test_stage_status_sees_run_gaps_no_writer_row_whatever_its_wording(tmp_path, capsys, monkeypatch):
    # N3-M-2 (1.4.29): run_gaps marks the row `reason: "no_writer"`, and
    # stage_status reads that field, so rewording `why` loses nothing.
    repo, ws = build(tmp_path)
    _backups(repo)
    a = _marked_extra(ws, 1, BACKUP)
    (a / "reference").mkdir(exist_ok=True)
    (a / "reference" / "building--extra.txt").write_text(BACKUP + "\n")
    for wording in (None, "reworded: rewrite the file and measure again"):
        if wording:
            monkeypatch.setattr(run_gaps, "STALE_WHY", wording)
            monkeypatch.setattr(run_gaps, "NO_WRITER_WHY", "nothing here can write it again")
        code, out, _ = run(repo, ws, capsys, "--devteam", str(tmp_path / "nowhere"))
        assert code == 1
        assert [(r["speciality"], r["reason"]) for r in out["stale_reference"]] == [("building/extra", "no_writer")]
        if wording:
            assert "speciality_reference.py" not in out["stale_reference"][0]["why"]
        got = stage_status.status(AREA, ws, repo)["stale_reference"]
        assert [(r["speciality"], r["reason"]) for r in got] == [("building/extra", "no_writer")], got


def test_a_reference_json_stale_row_names_its_reason(tmp_path, capsys):
    # N3-M-2: every stale row carries a structured `reason`.
    repo, ws = build(tmp_path)
    _unstamp(ws, "security/authn")
    out = run(repo, ws, capsys)[1]
    assert [(r["speciality"], r["reason"]) for r in out["stale_reference"]] == [("security/authn", "old_format")]


# ---- 1.4.33 (gap-fix round 8: G94-G121) ----

def _r9_file(a: Path, name: str = "compliance") -> Path:
    """A hand-built R9 measure of building/audit, unstamped."""
    ref = a / "reference" / "building--audit.txt"
    f = a / "gaps" / f"new-{name}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    (a / "survivor").mkdir(parents=True, exist_ok=True)
    (a / "survivor" / "artifact.json").write_text('{"name": "survivor"}')
    f.write_text(json.dumps({"folder": str(a / "survivor"), "references": [
        {"file": str(ref), "sentences": 2, "held": 0, "lacking": 2,
         "lacking_sentences": ["Keep every audit record for seven years at least.", "Ship logs off the host."]}]}))
    return f


def test_an_r9_file_with_no_hash_or_a_changed_reference_is_r9_stale(tmp_path, capsys):
    # G94 (Critical): an R9 measure taken on an older reference is stale; a run
    # lists it, --check counts it as a change, a stamp clears it, an edit re-raises it.
    import r9_stamp
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    f = _r9_file(a)
    code, out, err = run(repo, ws, capsys)
    assert [(r["file"], r["reason"]) for r in out["r9_stale"]] == [
        ("new-compliance.json", "no_hash"), ("new-compliance.json", "folder_no_hash")], out["r9_stale"]
    assert "r9_stale new-compliance.json" in err
    code, out, err = run(repo, ws, capsys, "--check")
    assert code == 1 and out["r9_stale"] and any(c["path"] == "r9_stale" for c in out["changes"]), out
    assert r9_stamp.main([str(f)]) == 0
    code, out, err = run(repo, ws, capsys)
    assert out["r9_stale"] == [], out["r9_stale"]
    code, out, err = run(repo, ws, capsys, "--check")
    assert out["r9_stale"] == [] and not any(c["path"].startswith("r9_stale") for c in out["changes"]), out
    (a / "reference" / "building--audit.txt").write_text("Keep every audit record for ten years.\n")
    code, out, err = run(repo, ws, capsys, "--check")
    assert code == 1 and [r["reason"] for r in out["r9_stale"]] == ["changed"], out
    assert any(c["path"].startswith("r9_stale") for c in out["changes"]), out["changes"]
    assert r9_stamp.main([str(f)]) == 0
    code, out, err = run(repo, ws, capsys, "--check")
    assert out["r9_stale"] == [], out["r9_stale"]
    (a / "survivor" / "artifact.json").write_text('{"name": "survivor", "summary": "edited"}')   # review I2
    code, out, err = run(repo, ws, capsys, "--check")
    assert code == 1 and [r["reason"] for r in out["r9_stale"]] == ["folder_changed"], out
    code, out, err = run(repo, ws, capsys)
    assert [r["reason"] for r in out["r9_stale"]] == ["folder_changed"] and "r9_stale new-compliance.json" in err


def test_an_r9_file_written_relative_to_the_repo_is_read_there(tmp_path, capsys):
    # review I2/M6 (fix round 1): run_gaps passes --repo to r9_stale, so a
    # survivor folder written relative to the repo is found, not "missing".
    import r9_stamp
    repo, ws = build(tmp_path)
    a = ws / "areas" / AREA
    f = _r9_file(a)
    topic = "cookbook/guidelines/" + next(iter(TOPICS))
    data = json.loads(f.read_text())
    data["folder"] = topic
    f.write_text(json.dumps(data))
    assert r9_stamp.main([str(f), "--repo", str(repo)]) == 0
    assert run(repo, ws, capsys)[1]["r9_stale"] == []
    (repo / topic / "rules.md").write_text("Edited.\n")
    assert [r["reason"] for r in run(repo, ws, capsys)[1]["r9_stale"]] == ["folder_changed"]


def test_every_building_sentence_with_no_home_is_in_home_unguessed(tmp_path, capsys):
    # G95: a building sentence whose home_guess is null and that no measured
    # topic holds is listed in home_unguessed, whatever its mark (G91: rows
    # marked elsewhere are listed, counted, never judged), with `marked_for`.
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    no_home = {(b["speciality"], s["n"]) for b in out["building"] for s in b["sentences"]
               if s["home_guess"] is None and not s["held_at"]}
    assert no_home and {(r["speciality"], r["n"]) for r in out["home_unguessed"]} == no_home, out["home_unguessed"]
    by = {(r["speciality"], r["n"]): r for r in out["home_unguessed"]}
    assert by[("building/security", 5)]["marked_for"] == "reviewing/sec"
    assert by[("building/security", 7)]["marked_for"] == "unmarked"   # G124 (1.4.36): never null
    assert by[("building/security", 4)]["text"] == qb.sentences(BUILDING)[3]
    assert all(r["why"] for r in out["home_unguessed"])


def test_home_measures_rows_say_whose_mark_each_sentence_carries(tmp_path, capsys):
    # G100: every sentence measured at its home carries `marked_for`, never filtered.
    repo, ws = build(tmp_path)
    _backups(repo)
    out = run(repo, ws, capsys)[1]
    rows = [s for h in out["home_measures"] for s in h["sentences"]]
    assert rows and all("marked_for" in s for s in rows), rows
    assert {"speciality": "building/security", "n": 8, "verdict": "held",
            "marked_for": AREA} in rows      # marked here only by another plan's marked_here


def test_short_sentences_rows_carry_their_mark_and_topic(tmp_path, capsys):
    # G101: a short piece says whose mark its sentence carries and the topic it stands at.
    repo, ws = build(tmp_path)
    with (ws / "areas" / AREA / "reference" / "security--authz.txt").open("a") as fh:
        fh.write("\nDeny by default.\n")
    out = run(repo, ws, capsys)[1]
    by = {(r["speciality"], r["n"]): r for r in out["short_sentences"]}
    assert by[("security/authz", 2)]["topic"] == "authz" and by[("security/authz", 2)]["marked_for"] == AREA
    assert by[("building/security", 6)]["marked_for"] == AREA and by[("building/security", 6)]["topic"] is None
    assert by[("building/security", 10)]["topic"] == "authz"         # its home_guess
    assert all({"marked_for", "topic", "fragment", "kind"} <= set(r) for r in out["short_sentences"])


def test_cut_fragments_labels_and_markers_are_tagged_never_dropped(tmp_path, capsys):
    # G102, G103: cookr cuts inside a backtick span and after `vs.`, and keeps a
    # heading label as a piece; each is tagged, listed and counted. A pure list
    # marker is listed under `markers`.
    repo, ws = build(tmp_path)
    with (ws / "areas" / AREA / "reference" / "security--authz.txt").open("a") as fh:
        fh.write("\nStructure:\n\nSet the header `context: strict` on every response you send back.\n\n"
                 "Prefer a `<button>` vs. a link for actions.\n")
    out = run(repo, ws, capsys)[1]
    rows = [r for r in out["short_sentences"] if r["speciality"] == "security/authz"]
    texts = {r["text"]: r for r in rows}
    label = next(r for t, r in texts.items() if t.startswith("Structure"))
    assert label["kind"] == "label" and label["fragment"] is True, rows
    tick = [r for t, r in texts.items() if t.count("`") % 2 == 1]
    assert tick and all(r["fragment"] for r in tick), rows
    vs = [r for t, r in texts.items() if t.rstrip().lower().endswith("vs.")]
    assert vs and all(r["fragment"] for r in vs), rows
    assert all(r["kind"] in ("label", "piece", "cut", "opener", "heading") for r in out["short_sentences"])
    assert run_gaps.piece_kind("1.") == "marker" and run_gaps.piece_kind("-") == "marker"
    assert run_gaps.piece_kind("Scan + gate:") == "label"
    assert run_gaps.piece_kind("Never log a secret.") == "piece"
    assert run_gaps.piece_kind("Keys must rotate:") == "piece"            # a verb: a rule, not a label
    assert isinstance(out["markers"], list)


def test_markers_are_listed_apart_from_short_sentences(tmp_path, capsys, monkeypatch):
    # G103: a piece that is only a list marker is under `markers`, never dropped silently.
    repo, ws = build(tmp_path)
    real = run_gaps.cookr_pieces

    def with_marker(f, *rest):
        pieces = real(f, *rest)
        return pieces + [["2.", False]] if f.endswith("security--authz.txt") else pieces
    monkeypatch.setattr(run_gaps, "cookr_pieces", with_marker)
    out = run(repo, ws, capsys)[1]
    assert {"speciality": "security/authz", "text": "2."} in [
        {k: r[k] for k in ("speciality", "text")} for r in out["markers"]]
    assert not any(r["text"] == "2." for r in out["short_sentences"])


def test_a_restatement_inside_one_speciality_is_flagged_repeat_of_and_still_counted(tmp_path, capsys):
    # G104: each lacking piece counts where it stands; a later sentence of the
    # same speciality restating an earlier one is listed in `repeat_of`.
    repo, ws = build(tmp_path)
    ref = ws / "areas" / AREA / "reference" / "security--authz.txt"
    ref.write_text(ref.read_text() + "\nRecord every privileged action in the audit trail promptly.\n\n"
                   "A complete review must establish that every privileged action is recorded in the audit trail promptly.\n")
    out = run(repo, ws, capsys)[1]
    rows = [r for r in out["repeat_of"] if r["speciality"] == "security/authz"]
    assert len(rows) == 1 and rows[0]["sentences"] == [2, 3], out["repeat_of"]
    assert set(rows[0]) >= {"speciality", "text", "sentences", "topics"}
    authz = next(t for t in out["topics"] if t["topic"] == "authz")
    ref_row = next(r for r in authz["references"] if r["speciality"] == "security/authz")
    assert 2 in ref_row["lacking_numbers"] and 3 in ref_row["lacking_numbers"]       # both still counted


def test_a_home_guess_names_the_words_it_rests_on(tmp_path, capsys):
    # G121: every home_guess prints the shared words behind it.
    repo, ws = build(tmp_path)
    _backups(repo)
    out = run(repo, ws, capsys)[1]
    by = {s["n"]: s for s in out["building"][0]["sentences"]}
    for s in by.values():
        if s["home_guess"]:
            assert s["home_shared_words"], s
        else:
            assert "home_shared_words" not in s or s["home_shared_words"] == []
    assert "backup" in " ".join(by[8]["home_shared_words"]), by[8]


def test_an_old_shape_gaps_file_no_topic_writes_is_cleared(tmp_path, capsys):
    # G110 (1.4.33): a gaps file cookr wrote before `lacking_numbers` (no
    # `written_by`, cookr's own shape) for no topic of this set is cleared by
    # a run (`cleared`) and named by --check (`would_clear`); a hand file, an R9
    # file and a topic's own file are never cleared.
    repo, ws = build(tmp_path)
    gaps = ws / "areas" / AREA / "gaps"
    gaps.mkdir()
    old = {"folder": "/repo/cookbook/guidelines/implementing/sec/gone",
           "references": [{"file": "/x.txt", "sentences": 2, "held": 1, "lacking": 1,
                           "lacking_sentences": ["Rotate keys yearly at the least."]}]}
    hand = {"references": [{"file": "x", "lacking_sentences": ["Kept by hand."]}]}
    (gaps / "gone.json").write_text(json.dumps(old))
    (gaps / "hand-refs.json").write_text(json.dumps(hand))
    assert run_gaps.ours(gaps / "gone.json") and not run_gaps.ours(gaps / "hand-refs.json")
    (gaps / "new-gone.json").write_text(json.dumps(old))
    assert not run_gaps.ours(gaps / "new-gone.json")
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert "gone.json" in chk["would_clear"] and (gaps / "gone.json").is_file()
    out = run(repo, ws, capsys)[1]
    assert "gone.json" in out["cleared"] and not (gaps / "gone.json").exists()
    assert (gaps / "hand-refs.json").is_file() and (gaps / "new-gone.json").is_file()
    assert "hand-refs.json" in out["stale_gaps"]


def test_keys_prints_every_key_of_a_run_and_of_a_check(tmp_path, capsys):
    # G119 (1.4.33): --keys/--summary prints each output key, an empty list as [].
    import json_keys
    repo, ws = build(tmp_path)
    full = run(repo, ws, capsys)[1]
    for flag in ("--keys", "--summary"):
        code, short, _ = run(repo, ws, capsys, flag)
        assert code == 0 and list(short) == list(full) and short == json_keys.keys(full)
    code, chk, _ = run(repo, ws, capsys, "--check")
    code2, short, _ = run(repo, ws, capsys, "--check", "--keys")
    assert code2 == code and short == json_keys.keys(chk)


def test_digest_is_one_line_the_plan_records(tmp_path, capsys):
    # G120 (1.4.33): --digest prints one line, the check's result summary for
    # the plan's Step-4 re-check: verdict, exit, every count, the hints setting
    # and the saved report's git blob hash, so a second check is comparable.
    from reference_format import blob_hash
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    rp = ws / "areas" / AREA / "run_gaps.json"
    capsys.readouterr()
    code = run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI),
                          "--check", "--digest"])
    line = capsys.readouterr().out
    assert line.count("\n") == 1 and code == 0
    assert line.startswith(f"run_gaps.py --check {AREA}: unchanged, exit 0; ")
    for part in ("changes 0", "not_compared 0", "would_clear 0", "r9_stale 0", "stale_reference 0",
                 "unplaced 0", "failed 0", "hints off (report)", f"report {blob_hash(rp)}"):
        assert part in line, (part, line)
    code = run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI),
                          "--digest"])
    lines = capsys.readouterr().out.splitlines()
    # G122 (1.4.36): without --check, the saved report's digest, never a run
    assert lines[0].startswith(f"run_gaps.py {AREA}: saved report; ") and f"report {blob_hash(rp)}" in lines[0]
    # L27: a run's digest adds one line per topic named by short_sentences,
    # home_measures or a sentence's first lacking candidate, with each count.
    full = json.loads(rp.read_text())
    named = ({r["topic"] for r in full["short_sentences"] if r.get("topic")}
             | {r["topic"] for r in full["home_measures"]}
             | {s["lacking_candidates"][0]["topic"] for b in full["building"] for s in b["sentences"]
                if s.get("lacking_candidates")})
    assert named and [x.split(":")[0].strip() for x in lines[1:]] == sorted(named), lines
    for x in lines[1:]:
        assert x.startswith("  ") and "short_sentences " in x and "home_measures " in x and "first_candidate " in x


# ---- fix round 1 (1.4.34) ----

def test_check_counts_a_key_the_saved_report_lacks_as_no_change_when_empty(tmp_path, capsys):
    # review M3: an additive release does not flip every --check; a non-empty new key still does
    repo, ws = build(tmp_path)
    code, out, err = run(repo, ws, capsys)
    rp = ws / "areas" / AREA / "run_gaps.json"
    report = json.loads(rp.read_text())
    assert report["repeat_of"] == [] and report["markers"] == []
    del report["repeat_of"], report["markers"]
    rp.write_text(json.dumps(report))
    code, out, err = run(repo, ws, capsys, "--check")
    assert code == 0 and out["check"] == "unchanged" and out["changes"] == [], out
    assert sorted(out["new_keys"]) == ["markers", "repeat_of"]
    report["markers"] = [{"speciality": "x", "n": 1, "text": "1."}]
    del report["home_unguessed"]
    rp.write_text(json.dumps(report))
    code, out, err = run(repo, ws, capsys, "--check")
    assert code == 1 and "markers" in [c["path"].split("[")[0] for c in out["changes"]], out["changes"]


# ---- gapfix9 (1.4.36) ----

def test_keys_summary_and_digest_without_check_read_the_saved_report_and_write_nothing(tmp_path, capsys):
    # G122 (N1): without --check these flags print the saved A/run_gaps.json,
    # never a run; with no saved report they exit 2 naming the step-1.3 run.
    import json_keys
    repo, ws = build(tmp_path)
    rp = ws / "areas" / AREA / "run_gaps.json"
    for flag in ("--keys", "--summary", "--digest"):
        code, out, err = run(repo, ws, capsys, flag)
        assert code == 2 and out is None and not rp.exists(), (flag, err)
        assert f"run_gaps.py --area {AREA} --hints" in err and "step 1.3" in err, err
    run(repo, ws, capsys, "--hints")
    before = rp.read_bytes()
    saved = json.loads(before)
    assert saved["hints"] is True
    for flag in ("--keys", "--summary"):
        code, out, _ = run(repo, ws, capsys, flag)
        assert code == 0 and out == json_keys.keys(saved) and rp.read_bytes() == before
    capsys.readouterr()
    code = run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI),
                          "--digest"])
    line = capsys.readouterr().out.splitlines()[0]
    assert code == 0 and line.startswith(f"run_gaps.py {AREA}: saved report; ") and "hints on" in line, line
    assert rp.read_bytes() == before


def test_a_run_without_a_hints_flag_keeps_the_saved_reports_hints(tmp_path, capsys):
    # G122 (N1): a write run with neither --hints nor --no-hints runs as the saved report ran.
    repo, ws = build(tmp_path)
    rp = ws / "areas" / AREA / "run_gaps.json"
    run(repo, ws, capsys, "--hints")
    code, out, _ = run(repo, ws, capsys)
    assert out["hints"] is True and json.loads(rp.read_text())["hints"] is True
    assert any("hints" in s for b in out["building"] for s in b["sentences"])
    code, out, _ = run(repo, ws, capsys, "--no-hints")
    assert out["hints"] is False and json.loads(rp.read_text())["hints"] is False


def test_home_unguessed_rows_marked_elsewhere_are_tagged_count_only_never_dropped(tmp_path, capsys):
    # G123 (N2): every row stays listed; a row marked for other areas only is
    # tagged count_only, its why saying it is counted, never judged here (G91).
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    no_home = {(b["speciality"], s["n"]) for b in out["building"] for s in b["sentences"]
               if s["home_guess"] is None and not s["held_at"]}
    by = {(r["speciality"], r["n"]): r for r in out["home_unguessed"]}
    assert set(by) == no_home
    assert by[("building/security", 5)]["count_only"] is True
    assert "counted, never judged here" in by[("building/security", 5)]["why"]
    assert "count_only" not in by[("building/security", 4)]


def test_a_null_mark_is_resolved_from_every_plans_marks_and_never_left_null(tmp_path, capsys):
    # G124 (N3): a sentence this area's marks leave null takes the areas any
    # plan's marks file gives it; "unmarked" when a marks file holds it unmarked,
    # "unknown" when no plan has a marks file for its speciality.
    repo, ws = build(tmp_path)

    def rows(out):
        every = [*out["home_unguessed"], *out["short_sentences"], *out["held_by_wording"],
                 *(s for h in out["home_measures"] for s in h["sentences"]),
                 *(s for b in out["building"] for s in b["unmeasured_sentences"])]
        assert every and all(r["marked_for"] is not None for r in every), every
        return every
    out = run(repo, ws, capsys)[1]
    rows(out)
    by = {(r["speciality"], r["n"]): r["marked_for"] for r in out["home_unguessed"]}
    assert by[("building/security", 7)] == "unmarked"
    assert by[("building/audit", 1)] == "unknown" and by[("building/audit", 2)] == "unknown"
    assert {(r["speciality"], r["n"]): r["marked_for"] for r in out["short_sentences"]}[("building/audit", 2)] == "unknown"
    other = ws / "areas" / "reviewing" / "sec"
    other.mkdir(parents=True)
    (other / "area-plan.md").write_text("# Plan\n")
    audit = qb.sentences("Keep every audit record for seven years at least.\n\nShip logs off the host.\n")
    (other / "building-audit.json").write_text(json.dumps({
        "speciality": "building/audit", "sentences": [{"n": n, "text": s} for n, s in enumerate(audit, start=1)],
        "marks": {"1": "reviewing/sec", "2": None}}))
    found = qb.sentences(BUILDING)
    (other / "building-security.json").write_text(json.dumps({
        "speciality": "building/security", "sentences": [{"n": n, "text": s} for n, s in enumerate(found, start=1)],
        "marks": {"7": ["reviewing/sec", "shipping"]}}))
    out = run(repo, ws, capsys)[1]
    rows(out)
    by = {(r["speciality"], r["n"]): r for r in out["home_unguessed"]}
    assert by[("building/security", 7)]["marked_for"] == ["reviewing/sec", "shipping"]
    assert by[("building/security", 7)]["count_only"] is True
    assert by[("building/audit", 1)]["marked_for"] == "reviewing/sec" and by[("building/audit", 1)]["count_only"]
    assert by[("building/audit", 2)]["marked_for"] == "unmarked" and "count_only" not in by[("building/audit", 2)]
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 0 and chk["check"] == "unchanged", chk["changes"]


def test_each_short_piece_kind_is_told_apart(tmp_path, capsys):
    # G125 (N4): label (a heading label or `- **name**:`), opener (Review /
    # Closing / a procedure lead ending in `:`, G161), cut (inside a backtick span, at `vs.`, or a code
    # token before `:`), heading (a `#` line); an uncertain piece is "piece".
    k = run_gaps.piece_kind
    assert k("1.") == "marker" and k("-") == "marker"
    assert k("Structure:") == "label" and k("Scan + gate:") == "label"
    assert k("- **Owner must sign off**:") == "label" and k("**Keys must rotate**:") == "label"
    assert k("Review changed shell scripts.") == "opener" and k("Review Codex configuration.") == "opener"
    assert k("Closing tidy pass for hygiene.") == "opener" and k("Final hygiene pass.") == "piece"
    assert k("Set the header `context:") == "cut" and k("Pin each image by sha256:") == "cut"
    assert k("frozen_string_literal:") == "cut" and k("# type:") == "cut"
    assert k("Prefer a `<button>` vs.") == "cut" and k("a link", after_vs=True) == "cut"
    assert k("#### Heading") == "heading" and k("## Rules") == "heading"
    assert k("Never log a secret.") == "piece" and k("Keys must rotate:") == "piece"
    assert k("Reviewers may skip it.") == "piece"
    for piece, frag in (("Structure:", True), ("Set the header `context:", True), ("#### Heading", False),
                        ("Review changed shell scripts.", False), ("Never log a secret.", False)):
        assert run_gaps.fragment(piece) is frag, piece
    repo, ws = build(tmp_path)
    with (ws / "areas" / AREA / "reference" / "security--authz.txt").open("a") as fh:
        fh.write("\nStructure:\n\nSet the header `context: strict` on every response you send back.\n")
    out = run(repo, ws, capsys)[1]
    texts = {r["text"]: r for r in out["short_sentences"] if r["speciality"] == "security/authz"}
    assert [r["kind"] for t, r in texts.items() if t.count("`") % 2 == 1] == ["cut"], texts


def test_a_colonless_bold_line_is_a_piece_never_a_label():
    # Fix round 1 (gapfix9 review I1): a bold label needs its colon; a whole
    # rule set as a bold line is a piece, counted, never held by its part.
    k = run_gaps.piece_kind
    assert k("- **Never commit secrets to git**") == "piece"
    assert k("**Always use TLS**") == "piece"
    assert k("- **Rule**:") == "label" and k("- **Rule:**") == "label" and k("**Keys must rotate**:") == "label"


def test_every_cookr_held_piece_is_listed_held_by_wording(tmp_path, capsys):
    # G132 (N11): each piece cookr holds on wording alone, with its sentence,
    # the topic that holds it and whose mark it is; a numeral the topic text
    # lacks is flagged number_differs.
    repo, ws = build(tmp_path)
    (ws / "areas" / AREA / "reference" / "security--authz.txt").write_text(
        "Deny every request by default unless a role explicitly grants the action within 5 seconds.\n")
    out = run(repo, ws, capsys)[1]
    rows = out["held_by_wording"]
    assert rows and all({"speciality", "n", "text", "topic", "marked_for", "number_differs"} <= set(r)
                        for r in rows), rows
    authz = [r for r in rows if r["speciality"] == "security/authz"]
    assert authz and authz[0]["n"] == 1 and authz[0]["topic"] == "authz" and authz[0]["marked_for"] == AREA
    assert authz[0]["number_differs"] is True, authz
    sec = [r for r in rows if r["speciality"] == "building/security" and r["n"] == 1]
    assert sec and sec[0]["topic"] == "authn" and sec[0]["marked_for"] == AREA, rows
    assert not any(r["number_differs"] for r in rows if r["speciality"] == "building/security" and r["n"] == 1)
    held = {(r["speciality"], r["n"], r["topic"]) for r in rows}
    for t in out["topics"]:
        for ref in t["references"]:
            if ref["held"]:
                assert any((ref["speciality"], t["topic"]) == (sp, tp) for sp, _, tp in held), (t["topic"], ref)


def test_the_review_focus_pair_is_tagged_and_each_sentence_named(tmp_path, capsys):
    # G146 (N25): the format-2 pair (sentence 2 restating sentence 1) is tagged
    # review_focus_pair, never dropped; each row names every sentence's text
    # and the topics it is counted at.
    repo, ws = build(tmp_path)
    ref = ws / "areas" / AREA / "reference" / "security--shared.txt"
    ref.write_text(ref.read_text() + "\nA complete review must establish that every authorization decision is "
                   "logged with the subject and the resource named.\n")
    out = run(repo, ws, capsys)[1]
    rows = [r for r in out["repeat_of"] if r["speciality"] == "security/shared"]
    assert len(rows) == 1 and rows[0]["sentences"] == [1, 2] and rows[0]["review_focus_pair"] is True, rows
    assert [p["n"] for p in rows[0]["pieces"]] == [1, 2] and all(p["text"] and p["topics"] for p in rows[0]["pieces"])
    ref = ws / "areas" / AREA / "reference" / "security--authz.txt"
    ref.write_text(ref.read_text() + "\nRecord every privileged action in the audit trail promptly.\n\n"
                   "A complete review must establish that every privileged action is recorded in the audit trail promptly.\n")
    out = run(repo, ws, capsys)[1]
    other = [r for r in out["repeat_of"] if r["speciality"] == "security/authz"]
    assert other and other[0]["review_focus_pair"] is False


def test_a_recorded_home_tags_the_row_and_a_sentence_lacking_everywhere_says_so(tmp_path, capsys):
    # G145 (N24): mark.py --home N=topic records the plan's chosen home; the
    # row stays listed, tagged home_recorded. A sentence measured and lacking
    # at every topic it was measured at says so, never "no measured topic holds it".
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    lack = {s["n"] for b in out["building"] if b["speciality"] == "building/security" for s in b["sentences"]
            if s["home_guess"] is None and not s["held_at"] and s["lacking_at"]}
    assert lack
    for r in out["home_unguessed"]:
        if r["speciality"] == "building/security" and r["n"] in lack:
            assert r["why"].startswith("measured, lacking at every topic it was measured at"), r
    n = min(lack)
    assert mark.main([AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/security",
                      "--home", f"{n}=authz"]) == 0
    assert json.loads((ws / "areas" / AREA / "building-security.json").read_text())["homes"] == {str(n): "authz"}
    out = run(repo, ws, capsys)[1]
    by = {(r["speciality"], r["n"]): r for r in out["home_unguessed"]}
    assert by[("building/security", n)]["home_recorded"] == "authz"


def test_a_check_prints_each_r9_stale_line_once(tmp_path, capsys):
    # G140 (N19): --check measures twice (saved, fresh); each r9_stale row is printed once.
    repo, ws = build(tmp_path)
    _r9_file(ws / "areas" / AREA)
    code, out, err = run(repo, ws, capsys, "--check")
    assert len(out["r9_stale"]) == 2 and err.count("run_gaps.py: r9_stale new-compliance.json") == 2, err
    assert all("r9_stamp.py" in r["why"] for r in out["r9_stale"])


def test_rows_prints_one_key_whole_and_keys_print_the_hold_rows(tmp_path, capsys):
    # G138 (N17, 1.4.36): --rows K prints key K of the saved report whole (or
    # of the check with --check); --keys prints stale_reference and r9_stale rows.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys, "--hints")
    rp = ws / "areas" / AREA / "run_gaps.json"
    before = rp.read_bytes()
    saved = json.loads(before)
    code, out, _ = run(repo, ws, capsys, "--rows", "building")
    assert code == 0 and out == {"building": saved["building"]} and rp.read_bytes() == before
    code, out, err = run(repo, ws, capsys, "--rows", "nope")
    assert code == 2 and out is None and "nope" in err
    code, out, _ = run(repo, ws, capsys, "--keys")
    assert out["stale_reference"] == saved["stale_reference"] and out["r9_stale"] == saved["r9_stale"]


# --- gapfix10 (1.4.37) ---------------------------------------------------------------------------


def test_a_home_in_another_area_is_recorded_in_homes_json_and_tags_the_row(tmp_path, capsys):
    # G156 (N7): `--home N=<area>:<topic>` needs no marks file here; it goes in
    # A/homes.json, checked against that area's topics; run_gaps tags the row
    # home_recorded and keeps its marked_for.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    rows = {(r["speciality"], r["n"]): r for r in out["home_unguessed"]}
    assert ("building/audit", 1) in rows
    was = rows[("building/audit", 1)]["marked_for"]
    a = ws / "areas" / AREA
    assert not (a / "building-audit.json").exists()
    call = [AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/audit"]
    assert mark.main([*call, "--home", "1=reviewing/sec:vp"]) == 0
    assert json.loads((a / "homes.json").read_text()) == {"building/audit": {"1": "reviewing/sec:vp"}}
    before = (a / "homes.json").read_bytes()
    for bad in ("1=reviewing/sec:nosuch", "1=nosuch/area:vp", "1=reviewing/sec:", "99=reviewing/sec:vp"):
        assert mark.main([*call, "--home", bad]) == 2 and (a / "homes.json").read_bytes() == before, bad
    out = run(repo, ws, capsys)[1]
    r = {(r["speciality"], r["n"]): r for r in out["home_unguessed"]}[("building/audit", 1)]
    assert r["home_recorded"] == "reviewing/sec:vp" and r["marked_for"] == was


def test_a_local_home_names_a_topic_of_this_plan(tmp_path, capsys):
    # G156 (N7): `--home N=TOPIC` is checked against this plan's topics.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]       # G203 (1.4.39): a home is recorded for a home_unguessed row only
    n = min(r["n"] for r in out["home_unguessed"] if r["speciality"] == "building/security")
    call = [AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/security"]
    f = ws / "areas" / AREA / "building-security.json"
    before = f.read_bytes()
    assert mark.main([*call, "--home", f"{n}=nosuch"]) == 2 and f.read_bytes() == before
    assert mark.main([*call, "--home", f"{n}=compliance"]) == 0          # a planned new topic


def test_held_rows_carry_the_topic_sentence_and_a_verdict_only_while_both_sentences_stand(tmp_path, capsys):
    # G159 (N10): each held_by_wording row names its topic sentence and an id;
    # `mark.py --held <id> held|not` records a verdict that a re-run carries
    # while the piece and the topic sentence are byte-identical; the row stays.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    rows = [r for r in out["held_by_wording"] if r["speciality"] == "security/authz"]
    assert rows and rows[0]["topic_sentence"] == "- Deny every request by default unless a role explicitly grants " \
                                                 "the action.", rows
    rid = rows[0]["id"]
    assert len({r["id"] for r in out["held_by_wording"]}) == len(out["held_by_wording"])
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", rid, "maybe"]) == 2
    assert mark.main([*call, "--held", "nosuch@x", "held"]) == 2
    assert mark.main([*call, "--held", rid, "held"]) == 0
    out = run(repo, ws, capsys)[1]
    r = next(r for r in out["held_by_wording"] if r["id"] == rid)
    assert r["verdict"] == "held" and "verdict_was" not in r
    t = repo / "cookbook" / "guidelines" / "implementing" / "sec" / "authz" / "rules.md"
    t.write_text(t.read_text().replace("grants the action.", "grants the action!"))
    out = run(repo, ws, capsys)[1]
    r = next(r for r in out["held_by_wording"] if r["id"] == rid)
    assert "verdict" not in r and r["verdict_was"] == "held" and "changed" in r["verdict_why"], r


def test_an_opener_is_review_closing_or_a_procedure_lead_ending_in_a_colon():
    # G161 (N12): a piece ending in "pass" is no opener; "Before merging:" is.
    k = run_gaps.piece_kind
    assert k("Run the security pass") == "piece" and k("Security pass.") == "piece"
    assert k("Before merging:") == "opener" and k("After the release:") == "opener"
    assert k("Review changed shell scripts.") == "opener" and k("Closing tidy pass for hygiene.") == "opener"


def test_keys_prints_held_by_wording_rows_whole(tmp_path, capsys):
    # G171 (N22): held_by_wording is in json_keys.ROW_KEYS.
    repo, ws = build(tmp_path)
    full = run(repo, ws, capsys)[1]
    keyed = run(repo, ws, capsys, "--keys")[1]
    assert full["held_by_wording"] and keyed["held_by_wording"] == full["held_by_wording"]


def test_check_with_an_out_holding_no_report_is_refused(tmp_path, capsys):
    # G172 (N23): `--check --out DIR` with no DIR/run_gaps.json exits 2.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    code, chk, err = run(repo, ws, capsys, "--check", "--out", str(tmp_path / "elsewhere"))
    assert code == 2 and chk is None and "--check --out" in err, err


def test_a_short_piece_whose_kind_changed_says_so_in_the_check(tmp_path, capsys):
    # G180 (N31): a changed short_sentences row carries kind_changed [old, new].
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    rp = ws / "areas" / AREA / "run_gaps.json"
    saved = json.loads(rp.read_text())
    row = saved["short_sentences"][0]
    new = row["kind"]
    row["kind"] = "label" if new != "label" else "piece"
    rp.write_text(json.dumps(saved))
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 1
    tagged = [x for c in chk["changes"] if c["path"].startswith("short_sentences")
              for x in ([c] if "kind_changed" in c else c.get("added", [])) if "kind_changed" in x]
    assert [x["kind_changed"] for x in tagged] == [[row["kind"], new]], chk["changes"]


# --- gapfix11 (1.4.39) ---------------------------------------------------------------------------


def _held_row(out: dict, sp: str = "security/authz") -> dict:
    return next(r for r in out["held_by_wording"] if r["speciality"] == sp)


def _topic(out: dict, name: str) -> dict:
    return next(t for t in out["topics"] if t["topic"] == name)


def test_a_not_verdict_moves_its_piece_to_lacking_and_the_check_says_so(tmp_path, capsys):
    # G189 (L4): a recorded `not` verdict counts the piece lacking in the saved
    # figures (`own` too), and --check before the re-run reports the change.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    row = _held_row(out)
    t0 = _topic(out, row["topic"])
    assert "not_held_by_verdict" not in t0
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", row["id"], "not", "--why", "x"]) == 0
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 1 and any(c["path"].startswith("topics") for c in chk["changes"]), chk["changes"]
    out = run(repo, ws, capsys)[1]
    t1 = _topic(out, row["topic"])
    assert (t1["held"], t1["lacking"]) == (t0["held"] - 1, t0["lacking"] + 1)
    assert (t1["own"]["held"], t1["own"]["lacking"]) == (t0["own"]["held"] - 1, t0["own"]["lacking"] + 1)
    assert t1["not_held_by_verdict"] == 1
    ref = next(r for r in t1["references"] if r["speciality"] == "security/authz")
    assert ref["not_held_by_verdict"] == [row["n"]]
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert chk["check"] == "unchanged", chk["changes"]
    assert mark.main([*call, "--held", row["id"], "held"]) == 0
    out = run(repo, ws, capsys)[1]
    assert (_topic(out, row["topic"])["held"], "not_held_by_verdict" in _topic(out, row["topic"])) == \
        (t0["held"], False)


def _reset_authz(repo):
    t = repo / "cookbook" / "guidelines" / "implementing" / "sec" / "authz" / "rules.md"
    t.write_text(t.read_text().replace("grants the action.", "grants the action!"))


def test_a_reset_verdict_never_lowers_the_total_a_saved_not_still_counts_lacking(tmp_path, capsys):
    # G251 (1.4.41): a recorded `not` whose topic sentence changed resets (`verdict_was` "not"), and the row keeps
    # counting lacking until re-judged; the total never falls because a verdict reset. Re-recording clears it.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    row = _held_row(out)
    base = out["measured_total"]
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", row["id"], "not", "--why", "x"]) == 0
    out = run(repo, ws, capsys)[1]
    with_not = out["measured_total"]
    assert with_not == base + 1
    _reset_authz(repo)
    out = run(repo, ws, capsys)[1]
    r = next(x for x in out["held_by_wording"] if x["id"] == row["id"])
    assert "verdict" not in r and r["verdict_was"] == "not", r
    assert out["measured_total"] == with_not, (out["measured_total"], with_not)
    assert _topic(out, row["topic"])["not_held_by_verdict"] == 1
    new = _held_row(out)
    assert mark.main([*call, "--held", new["id"], "held"]) == 0
    out = run(repo, ws, capsys)[1]
    assert "verdict_was" not in _held_row(out) and out["measured_total"] == base


def test_a_reset_held_verdict_counts_lacking_until_rejudged(tmp_path, capsys):
    # G251 (1.4.41): a saved `held` whose piece or topic sentence changed counts as `not` until re-judged.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    row = _held_row(out)
    base = out["measured_total"]
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", row["id"], "held"]) == 0
    assert run(repo, ws, capsys)[1]["measured_total"] == base
    _reset_authz(repo)
    out = run(repo, ws, capsys)[1]
    assert _held_row(out)["verdict_was"] == "held" and out["measured_total"] == base + 1
    # the topic's text changed elsewhere (the G202 reset, not the topic sentence): the same.
    assert mark.main([*call, "--held", _held_row(out)["id"], "held"]) == 0
    assert run(repo, ws, capsys)[1]["measured_total"] == base
    t = repo / "cookbook" / "guidelines" / "implementing" / "sec" / "authz" / "rules.md"
    t.write_text(t.read_text().replace("Pin every dependency", "Pin each dependency"))
    r = _held_row(run(repo, ws, capsys)[1])
    assert "verdict" not in r and r["verdict_was"] == "held" and "topic" in r["verdict_why"], r
    assert run(repo, ws, capsys)[1]["measured_total"] == base + 1


def test_check_reports_a_plan_whose_stated_gap_total_differs_from_the_count(tmp_path, capsys):
    # G189 (L4), G225/G226/G233 (1.4.40): the plan's `This area's gaps: N` is run_gaps' measured total in its
    # own unit (lacking pieces after every recorded verdict); a differing N, any other form of the line and a plan
    # with no line are each a row; advisory: the exit is unchanged.
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    counted = sum(t["own"]["lacking"] for t in out["topics"])
    assert out["measured_total"] == counted
    plan = ws / "areas" / AREA / "area-plan.md"
    code0, chk, _ = run(repo, ws, capsys, "--check")
    [g] = chk["gap_total"]                         # no stated total: a plan with lacking pieces and no line
    assert g["form"] == "missing" and g["stated"] is None and g["counted"] == counted, g
    plan.write_text(PLAN + f"\n## Gaps\n\nThis area's gaps: {counted + 3}\n")
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == code0
    [g] = chk["gap_total"]
    assert (g["stated"], g["counted"], g["saved"], g["form"]) == (counted + 3, counted, counted, "figure"), g
    assert "This area's gaps" in g["line"] and "run_gaps" in g["why"]
    for other in (f"**This area's gaps: {counted + 3}** (was 2)", f"This area's gaps: {counted} (run_gaps {counted}; 3 by hand)",
                  f"This area's gaps: {counted + 3} (run_gaps {counted}; 3 by hand)"):
        plan.write_text(PLAN + f"\n## Gaps\n\n{other}\n")
        [g] = run(repo, ws, capsys, "--check")[1]["gap_total"]
        assert g["form"] == "other" and "This area's gaps: N" in g["why"], g
    for ok in (f"This area's gaps: {counted}", f"**This area's gaps: {counted}**", f"**This area's gaps:** {counted}"):
        plan.write_text(PLAN + f"\n## Gaps\n\n{ok}\n")
        assert run(repo, ws, capsys, "--check")[1]["gap_total"] == [], ok
    plan.write_text(PLAN + f"\n## Gaps\n\nGap total for the area: {counted}\n")      # the old form matches nothing
    assert [g["form"] for g in run(repo, ws, capsys, "--check")[1]["gap_total"]] == ["missing"]


def test_a_quoted_gap_total_and_the_step_4_section_are_not_the_plans_statement(tmp_path, capsys):
    # G232 (L15): a backticked or quoted `This area's gaps: 9 (run_gaps ...)` and the Step-4 re-check section
    # are skipped; the plan's own line is still read.
    repo, ws = build(tmp_path)
    counted = sum(t["own"]["lacking"] for t in run(repo, ws, capsys)[1]["topics"])
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(PLAN + f"\n## Gaps\n\nThis area's gaps: {counted}\n\nThe form is `This area's gaps: 9 (run_gaps 4)`"
                    " and \"This area's gaps: 7 (by hand)\".\n\n> This area's gaps: 5\n\n## Step-4 re-check\n\n"
                    "This area's gaps: 12 (run_gaps 3)\n")
    assert run(repo, ws, capsys, "--check")[1]["gap_total"] == []


def test_every_lacking_piece_is_a_row_with_an_id_and_whether_it_is_counted(tmp_path, capsys):
    # G225 (L3): `lacking_pieces`, one row per lacking piece per topic, id `lacking:<speciality>:<n>@<topic>`
    # (`#k` from the second row sharing it); `counted` is the share `own` holds.
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    rows = out["lacking_pieces"]
    assert len(rows) == sum(t["lacking"] for t in out["topics"]), len(rows)
    assert sum(1 for r in rows if r["counted"]) == sum(t["own"]["lacking"] for t in out["topics"])
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == len(ids) and "lacking:building/security:1@authn" in ids and \
        "lacking:building/security:1@authn#2" in ids, ids
    assert all(r["text"] and r["topic"] and "verdict" not in r for r in rows)


def test_a_piece_held_in_other_words_by_hand_is_a_recorded_verdict_that_lowers_the_total(tmp_path, capsys):
    # G225/G226 (L3, L4): `mark.py --held <lacking id> held --why ...` is applied by run_gaps: the topic's
    # lacking falls and held rises by one, `measured_total` falls by one; --why is required.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    row = next(r for r in out["lacking_pieces"] if r["counted"])
    topic = _topic(out, row["topic"])
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", row["id"], "held"]) == 2
    assert "--why" in capsys.readouterr().err
    assert mark.main([*call, "--held", row["id"], "held", "--why", "held at the rule on timeouts"]) == 0
    capsys.readouterr()
    out2 = run(repo, ws, capsys)[1]
    again = next(r for r in out2["lacking_pieces"] if r["id"] == row["id"])
    assert again["verdict"] == "held" and again["why"] == "held at the rule on timeouts", again
    now = _topic(out2, row["topic"])
    assert (now["own"]["lacking"], now["own"]["held"]) == (topic["own"]["lacking"] - 1, topic["own"]["held"] + 1)
    assert (now["lacking"], now["held"]) == (topic["lacking"] - 1, topic["held"] + 1)
    assert out2["measured_total"] == out["measured_total"] - 1 == sum(t["own"]["lacking"] for t in out2["topics"])


def test_a_short_piece_judged_not_held_adds_one_and_a_changed_piece_resets_it(tmp_path, capsys):
    # G225 (L3): `short_sentences` rows carry `id` (`short:<speciality>:<n>`); `not` counts the piece lacking
    # (--why required), `held` changes nothing.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    short = next(r for r in out["short_sentences"] if r["speciality"] == "building/security" and r["n"] == 6)
    assert short["id"] == "short:building/security:6"
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", short["id"], "not"]) == 2
    assert mark.main([*call, "--held", short["id"], "not", "--why", "no topic says it"]) == 0
    out2 = run(repo, ws, capsys)[1]
    r = next(x for x in out2["short_sentences"] if x["id"] == short["id"])
    assert (r["verdict"], r["why"]) == ("not", "no topic says it")
    assert out2["measured_total"] == out["measured_total"] + 1
    assert mark.main([*call, "--held", short["id"], "held"]) == 0
    assert run(repo, ws, capsys)[1]["measured_total"] == out["measured_total"]


def test_held_file_takes_a_verdict_and_a_reason_and_prints_counts_not_ids(tmp_path, capsys):
    # G225 (L3), L21: a value is `held`, `not` or {"verdict", "why"}; the summary is {file, verdicts, changed: N},
    # the ids only under --verbose.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    rows = [r for r in out["lacking_pieces"] if r["counted"]][:2]
    f = tmp_path / "v.json"
    f.write_text(json.dumps({rows[0]["id"]: {"verdict": "held", "why": "r1"},
                             out["short_sentences"][0]["id"]: {"verdict": "not", "why": "r2"},
                             _held_row(out)["id"]: {"verdict": "not", "why": "r3"}}))   # gapfix14 (G288)
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    capsys.readouterr()
    assert mark.main([*call, "--held-file", str(f)]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["verdicts"] == 3 and printed["changed"] == 3 and "ids" not in printed, printed
    assert mark.main([*call, "--held-file", str(f), "--verbose"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["changed"] == 0 and printed["ids"] == [], printed
    f.write_text(json.dumps({rows[0]["id"]: "held"}))
    assert mark.main([*call, "--held-file", str(f)]) == 2          # a lacking piece held needs its why


def test_check_lists_a_verdict_changing_the_total_as_a_verdict_change_and_the_digest_says_the_total(tmp_path, capsys):
    # G247 (L25), L16: `verdict_changes` rows (id, was, now, total_delta); the digest prints
    # `gap_total_rows N; measured_total M`, and `--rows gap_total` reads the saved report.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    row = next(r for r in out["lacking_pieces"] if r["counted"])
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", row["id"], "held", "--why", "w"]) == 0
    chk = run(repo, ws, capsys, "--check")[1]
    [v] = chk["verdict_changes"]
    assert (v["id"], v["was"], v["now"], v["total_delta"]) == (row["id"], None, "held", -1), v
    assert chk["measured_total"] == out["measured_total"] - 1
    capsys.readouterr()
    run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI), "--check",
                   "--digest"])
    line = capsys.readouterr().out
    assert f"gap_total_rows 1; measured_total {out['measured_total'] - 1}" in line and "verdict_changes 1" in line, line
    run(repo, ws, capsys)
    capsys.readouterr()
    code = run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--rows", "gap_total"])
    shown = json.loads(capsys.readouterr().out)
    assert code == 0 and shown["gap_total"][0]["form"] == "missing", shown
    run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--digest"])
    assert f"measured_total {out['measured_total'] - 1}" in capsys.readouterr().out


def test_a_home_recorded_on_a_sentence_with_a_home_guess_changes_its_home_topic(tmp_path, capsys):
    # L8 (1.4.40): `recorded` is every sentence's recorded home, not only a home_unguessed row's.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    row = next(r for r in out["held_by_wording"] if (r["speciality"], r["n"]) == ("building/security", 2))
    assert (row["topic"], row["home_topic"], row["home"]) == ("authz", True, "authz")
    assert mark.main([AREA, "--workspace", str(ws), "--repo", str(repo), "--speciality", "building/security",
                      "--home", "2=authn"]) == 0
    capsys.readouterr()
    row = next(r for r in run(repo, ws, capsys)[1]["held_by_wording"] if (r["speciality"], r["n"]) == ("building/security", 2))
    assert (row["home_topic"], row["home"]) == (False, "authn"), row


def test_a_held_row_that_is_no_home_does_not_count_when_the_home_topic_holds_the_sentence():
    # L28 (1.4.40): `counted` false only for a row away from its home while the home topic holds the sentence.
    result = {"area": "a", "home_unguessed": [], "home_measures": [],
              "building": [{"speciality": "building/x", "file": "f",
                            "sentences": [{"n": 1, "home_guess": "t1", "held_at": ["t1", "t2"]},
                                          {"n": 2, "home_guess": "t1", "held_at": ["t2"]}]}],
              "held_by_wording": [{"speciality": "building/x", "n": n, "text": "Use it.", "topic": t}
                                  for n, t in ((1, "t1"), (1, "t2"), (2, "t2"))]}
    run_gaps._held_rule(result, {"t1": (set(), []), "t2": (set(), [])}, {"f": "One. Two."})
    assert [(r["n"], r["topic"], r["home_topic"], r["counted"]) for r in result["held_by_wording"]] == \
        [(1, "t1", True, True), (1, "t2", False, False), (2, "t2", False, True)]


def test_a_not_verdict_makes_the_sentence_lacking_in_its_home_measure(tmp_path, capsys):
    # L24 (1.4.40): one verdict per sentence at a topic: home_measures follows the recorded `not`.
    result = {"area": "a", "topics": [{"topic": "t", "references": [], "own": {"held": 1, "lacking": 0},
                                       "held": 1, "lacking": 0}],
              "home_measures": [{"topic": "t", "sentences": [{"speciality": "building/x", "n": 3, "verdict": "held"},
                                                              {"speciality": "building/x", "n": 4, "verdict": "held"}]}],
              "held_by_wording": [{"speciality": "building/x", "n": 3, "text": "Use it.", "topic": "t",
                                   "topic_sentence": "s", "rule_sentence": "s", "topic_hash": "h"}]}
    a = tmp_path
    (a / "held.json").write_text(json.dumps({"building/x:3@t": {"verdict": "not", "text": "Use it.",
                                                                  "topic_sentence": "s", "rule_sentence": "s",
                                                                  "topic_hash": "h"}}))
    run_gaps._held_verdicts(result, a)
    by = {x["n"]: x for x in result["home_measures"][0]["sentences"]}
    assert (by[3]["verdict"], by[3]["verdict_by"]) == ("lacking", "building/x:3@t") and by[4]["verdict"] == "held"


def test_rows_takes_a_comma_list_of_keys_as_stage_status_does(tmp_path, capsys):
    # L17 (1.4.40): `--rows a,b` prints both keys whole; an unknown one stops with exit 2 naming the keys.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    capsys.readouterr()
    call = ["--area", AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert run_gaps.main([*call, "--rows", "short_sentences,markers"]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert list(shown) == ["short_sentences", "markers"] and shown["short_sentences"], shown
    assert run_gaps.main([*call, "--rows", "markers,nope"]) == 2
    assert "no output key 'nope'" in capsys.readouterr().err


def test_modal_reads_the_strongest_rfc_2119_word():
    # G200 (L15, L16): MUST > SHOULD > MAY; none is None.
    m = run_gaps.modal
    assert m("Every session MUST have a timeout.") == ("MUST", 3)
    assert m("Clients MAY require If-Match.") == ("MAY", 1)
    assert m("You should not do this, but you must not do that.") == ("MUST NOT", 3)
    assert m("Prefer short names.") == ("PREFER", 2)
    assert m("Deny every request by default.") == (None, None)


def test_held_rows_name_the_modals_and_flag_a_weaker_topic_rule(tmp_path, capsys):
    # G201 (L16): a MUST piece held at a MAY topic sentence carries
    # modal_piece MUST, modal_topic MAY and modal_differs true; home_topic says
    # whether the topic is the sentence's home.
    repo, ws = build(tmp_path)
    t = repo / "cookbook" / "guidelines" / "implementing" / "sec" / "authn" / "rules.md"
    t.write_text(t.read_text().replace("Every session MUST have", "Every session MAY have"))
    out = run(repo, ws, capsys)[1]
    rows = [r for r in out["held_by_wording"] if r["speciality"] == "security/authn" and "MUST" in r["text"]]
    assert rows, out["held_by_wording"]
    r = rows[0]
    assert (r["modal_piece"], r["modal_topic"], r["modal_differs"]) == ("MUST", "MAY", True), r
    assert r["home_topic"] is True
    plain = _held_row(out)
    assert plain["modal_piece"] is None and plain["modal_differs"] is False


def test_a_verdict_is_pinned_to_the_topic_text_and_resets_when_any_rule_changes(tmp_path, capsys):
    # G202 (L17): each row names rule_sentence (the topic sentence with a
    # modal nearest the piece, else the nearest) and topic_hash; a verdict
    # recorded on one topic text resets when another sentence of it changes;
    # an older record without the hash keeps its verdict, `verdict_unpinned`.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    row = _held_row(out)
    assert row["rule_sentence"] and len(row["topic_hash"]) == 12
    call = [AREA, "--workspace", str(ws), "--repo", str(repo)]
    assert mark.main([*call, "--held", row["id"], "held"]) == 0
    saved = json.loads((ws / "areas" / AREA / "held.json").read_text())[row["id"]]
    assert saved["topic_hash"] == row["topic_hash"] and saved["rule_sentence"] == row["rule_sentence"]
    t = repo / "cookbook" / "guidelines" / "implementing" / "sec" / "authz" / "rules.md"
    t.write_text(t.read_text().replace("Pin every dependency", "Pin each dependency"))
    r = _held_row(run(repo, ws, capsys)[1])
    assert "verdict" not in r and r["verdict_was"] == "held" and "topic" in r["verdict_why"], r
    f = ws / "areas" / AREA / "held.json"
    old = json.loads(f.read_text())
    old[row["id"]] = {k: v for k, v in old[row["id"]].items() if k in ("verdict", "text", "topic_sentence")}
    f.write_text(json.dumps(old))
    r = _held_row(run(repo, ws, capsys)[1])
    assert r["verdict"] == "held" and r["verdict_unpinned"] is True, r


def test_a_rule_sentence_is_the_sentence_holding_the_piece_and_the_modal_neighbour_is_named():
    # G202 (1.4.39) chose the nearest sentence with a modal; G227 (1.4.40) makes the rule the sentence holding the
    # piece (an imperative with no modal reads as a MUST) and names the modal neighbour beside it.
    found = [("rules", "- Deny every request by default unless a role grants the action."),
             ("rules", "- A role MUST grant each action explicitly.")]
    pick = run_gaps.rule_pick("Deny every request unless a role grants the action.", found)
    assert pick["rule_sentence"] == found[0][1] and pick["nearest_modal_sentence"] == found[1][1], pick
    assert pick["implied"] is True
    assert run_gaps.rule_sentence("Deny every request.", found[:1]) == found[0][1]


def test_a_bare_home_naming_no_topic_of_the_plan_is_a_stale_home(tmp_path, capsys):
    # G205 (L20): a `homes` value naming no topic of this plan (an older
    # bare name for another area's topic) is listed in stale_home and on stderr.
    repo, ws = build(tmp_path)
    f = ws / "areas" / AREA / "building-security.json"
    d = json.loads(f.read_text())
    d["homes"] = {"3": "api-design", "4": "compliance"}
    f.write_text(json.dumps(d))
    (ws / "areas" / AREA / "homes.json").write_text(json.dumps({"building/audit": {"1": "vp"}}))
    code, out, err = run(repo, ws, capsys)
    assert sorted((r["speciality"], r["n"], r["home"]) for r in out["stale_home"]) == \
        [("building/audit", "1", "vp"), ("building/security", "3", "api-design")], out["stale_home"]
    assert "stale_home" in err and "api-design" in err


def test_a_saved_report_older_than_its_marks_says_it_was_not_re_run(tmp_path, capsys):
    # G207 (L22): --rows, --keys and --digest without --check read the saved
    # report; when a marks file is newer, stderr says so.
    import mark
    repo, ws = build(tmp_path)
    out = run(repo, ws, capsys)[1]
    def err_of(*flags) -> str:
        capsys.readouterr()
        run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI), *flags])
        return capsys.readouterr().err
    for flags in (("--rows", "held_by_wording"), ("--keys",), ("--digest",)):
        assert "not re-run" not in err_of(*flags)
    rp = ws / "areas" / AREA / "run_gaps.json"
    os.utime(rp, (rp.stat().st_mtime - 10, rp.stat().st_mtime - 10))
    assert mark.main([AREA, "--workspace", str(ws), "--repo", str(repo), "--held", _held_row(out)["id"], "not", "--why", "x"]) == 0
    for flags in (("--rows", "held_by_wording"), ("--keys",), ("--digest",)):
        err = err_of(*flags)
        assert "read saved report, not re-run" in err and "held.json" in err, (flags, err)


def test_a_no_modal_piece_is_read_at_its_strongest_against_a_weaker_topic_rule():
    # G200 (1.4.39): a piece with no modal word is judged as a MUST, so a
    # SHOULD rule of the topic flags modal_differs; a MUST rule does not.
    for rule, differs in (("Each request SHOULD be logged.", True), ("Each request MUST be logged.", False)):
        result = {"area": AREA, "building": [], "home_unguessed": [],
                  "held_by_wording": [{"speciality": "s/x", "n": 1, "text": "Log each request.", "topic": "t"}]}
        run_gaps._held_rule(result, {"t": (None, [("rules", rule)])})
        r = result["held_by_wording"][0]
        assert (r["modal_piece"], r["modal_differs"]) == (None, differs), r


def test_a_report_saved_before_the_rule_fields_lists_them_as_new_keys(tmp_path, capsys):
    # G202 (1.4.39): a saved report whose held_by_wording rows lack the 1.4.39
    # fields is compared on the fields it has; each one is a new key, no change.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    rp = ws / "areas" / AREA / "run_gaps.json"
    saved = json.loads(rp.read_text())
    assert saved["held_by_wording"]
    saved["held_by_wording"] = [{k: v for k, v in r.items() if k not in run_gaps.RULE_FIELDS}
                                for r in saved["held_by_wording"]]
    rp.write_text(json.dumps(saved))
    code, out, err = run(repo, ws, capsys, "--check")
    assert code == 0 and "held_by_wording.topic_hash" in out["new_keys"], (code, out.get("changes"), out["new_keys"])


def test_a_check_with_new_keys_names_them_on_stderr(tmp_path, capsys):
    # G218 (L33): `new_keys N` in the digest; stderr names each key.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    rp = ws / "areas" / AREA / "run_gaps.json"
    saved = json.loads(rp.read_text())
    assert saved["numbering_differs"] == []
    del saved["numbering_differs"]
    rp.write_text(json.dumps(saved))
    capsys.readouterr()
    run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI),
                   "--check", "--digest"])
    cap = capsys.readouterr()
    assert "new_keys 1" in cap.out and "run_gaps.py: new_keys: numbering_differs" in cap.err, cap


def test_rows_of_a_key_another_script_prints_names_that_script(tmp_path, capsys):
    # G220 (L35): `--rows plan_sections` is stage_status.py's; `piece` is a row's `text`.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    code, out, err = run(repo, ws, capsys, "--rows", "plan_sections")
    assert code == 2 and "stage_status.py" in err, err
    code, out, err = run(repo, ws, capsys, "--rows", "piece")
    assert code == 2 and "`text`" in err and "held_by_wording" in err, err


@pytest.mark.parametrize("bad", ["no/such", f"{AREA} --workspace x"])
def test_an_unknown_area_or_a_workspace_without_areas_exits_2(tmp_path, capsys, bad):
    # G198 (L13): never an empty run over an area that is not there.
    repo, ws = build(tmp_path)
    capsys.readouterr()
    code = run_gaps.main(["--area", bad, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI)])
    err = capsys.readouterr().err
    assert code == 2 and "unknown area" in err, err
    code = run_gaps.main(["--area", AREA, "--workspace", str(tmp_path), "--repo", str(repo), "--cookr-cli", str(CLI)])
    assert code == 2 and "no areas/" in capsys.readouterr().err


# --- gapfix12 (1.4.40) ---------------------------------------------------------------------------


def _rule_row(piece: str, sentence: str | None, topic_sentences: list[str], n: int = 1):
    """One held_by_wording row run through `_held_rule`: the piece cut from a building sentence (None: from a
    non-building speciality), against a topic holding `topic_sentences`."""
    row = {"speciality": "b/x" if sentence is not None else "s/x", "n": n, "text": piece, "topic": "t"}
    result = {"area": AREA, "home_unguessed": [], "held_by_wording": [row],
              "building": [{"speciality": "b/x", "file": "f.md", "sentences": [{"n": 1, "home_guess": "t"}]}]
              if sentence is not None else []}
    run_gaps._held_rule(result, {"t": (None, [("rules", s) for s in topic_sentences])},
                        {"f.md": sentence} if sentence is not None else {})
    return row


def test_a_no_modal_piece_takes_its_source_sentences_modal(tmp_path):
    # G223 (L1), G249 (L27): a piece cut from "Prefer ..." is a PREFER piece; held at a Prefer topic it is not
    # `modal_differs`. The same piece from a sentence with no modal still reads as a MUST (a SHOULD topic differs).
    topic = ["Prefer short names for sessions."]
    r = _rule_row("short names for sessions.", "Prefer short names for sessions. Log each one.", topic)
    assert (r["modal_piece"], r["modal_sentence"], r["modal_differs"]) == (None, "PREFER", False), r
    r = _rule_row("short names for sessions.", "Name sessions with short names.", ["Sessions SHOULD have short names."])
    assert (r["modal_piece"], r["modal_sentence"], r["modal_differs"]) == (None, None, True), r
    r = _rule_row("Sessions MUST be short.", "Prefer short sessions, and sessions MUST be short.",
                  ["Sessions SHOULD be short."])
    assert (r["modal_piece"], r["modal_sentence"], r["modal_differs"]) == ("MUST", "MUST", True), r
    r = _rule_row("sessions be short.", None, ["Sessions SHOULD be short."])      # a non-building piece: its own words
    assert r["modal_sentence"] is None and r["modal_differs"] is True, r


def test_an_imperative_topic_sentence_without_a_modal_reads_as_a_must_and_a_fragment_is_judged_by_its_scope():
    # G249 (L27): "Use real databases ... where practical." opens with a verb: a MUST (`modal_topic_implied`).
    # "Unit tests -- fast, isolated" has no sentence end: judged against the nearest sentence with a modal.
    imperative = _rule_row("Use real databases.", "Use real databases.", ["Use real databases where practical."])
    assert (imperative["modal_topic"], imperative["modal_topic_implied"], imperative["modal_differs"]) == \
        ("MUST", True, False), imperative
    frag = _rule_row("Unit tests are fast.", "Unit tests MUST be fast.",
                     ["Unit tests -- fast, isolated", "Tests SHOULD be isolated from one another."])
    assert frag["rule_sentence"] == "Tests SHOULD be isolated from one another.", frag
    assert (frag["modal_topic"], frag["modal_differs"], frag["rule_is_topic_sentence"]) == ("SHOULD", True, False), frag
    plain = _rule_row("Sessions expire.", "Sessions expire.", ["Sessions expire after thirty minutes of idling."])
    assert plain["modal_topic"] is None and plain["modal_differs"] is False, plain


def test_a_checklist_rows_severity_cell_is_its_modal():
    # G224 (L2): FAIL = MUST, WARN = SHOULD, INFO = MAY; no Severity cell: the row's words; prose unchanged.
    m = run_gaps.modal
    assert m("| Session timeout is set | FAIL |") == ("MUST", 3)
    assert m("| Logging is on | WARN |") == ("SHOULD", 2)
    assert m("| Docs exist | INFO |") == ("MAY", 1)
    assert m("| Sessions SHOULD expire | note |") == ("SHOULD", 2)
    assert m("A FAIL in prose is no severity; sessions MAY expire.") == ("MAY", 1)
    table = ("| Check | Severity | | --- | --- | | Session timeout is set | FAIL | | Logging is on | INFO | "
             "| Docs exist | WARN |")
    assert run_gaps.table_rows(table) == ["| Check | Severity |", "| Session timeout is set | FAIL |",
                                          "| Logging is on | INFO |", "| Docs exist | WARN |"]
    assert run_gaps.table_rows("Prose, not a table.") is None


def test_the_rule_sentence_of_a_checklist_is_the_row_holding_the_piece_never_the_table():
    # G224 (L2): the row's severity is the topic's modal.
    table = ("| Check | Severity | | --- | --- | | Session timeout is set | FAIL | | Logging is on | INFO |")
    for piece, rule, word, differs in (("Logging is on.", "| Logging is on | INFO |", "MAY", True),
                                       ("Session timeout is set.", "| Session timeout is set | FAIL |", "MUST", False)):
        r = _rule_row(piece, "Logging MUST be on. Session timeout MUST be set.", [table])
        assert (r["rule_sentence"], r["modal_topic"], r["modal_differs"]) == (rule, word, differs), r


def test_the_rule_is_the_sentence_holding_the_piece_and_a_neighbour_is_only_named():
    # G227 (L5): a SHOULD neighbour next to the holding sentence is `nearest_modal_sentence`, never the rule; a
    # holding sentence with no modal word gives `modal_topic` null.
    found = ["Sessions expire after thirty minutes of idling.", "Sessions SHOULD be logged for thirty minutes."]
    r = _rule_row("Sessions expire after thirty minutes.", "Sessions MUST expire after thirty minutes.", found)
    assert r["rule_sentence"] == found[0] and r["modal_topic"] is None and r["modal_differs"] is False, r
    assert r["nearest_modal_sentence"] == found[1] and r["rule_is_topic_sentence"] is True, r


def test_several_modals_read_the_pieces_strongest_and_the_topics_weakest():
    # G227 (L5): REQUIRED must not hide a SHOULD in the same piece; one MUST must not hide a MAY in the topic.
    piece = "Sessions are REQUIRED to expire, and tokens SHOULD rotate."
    r = _rule_row(piece, None, ["Sessions MUST expire, and tokens SHOULD rotate."])
    assert r["modal_piece"] == "REQUIRED" and r["modal_piece_all"] == ["REQUIRED", "SHOULD"], r
    assert (r["modal_topic"], r["modal_differs"]) == ("SHOULD", True), r          # strongest piece vs weakest topic
    r = _rule_row("Sessions MUST expire and tokens MUST rotate.", None,
                  ["Sessions MUST expire and tokens MAY rotate."])
    assert (r["modal_topic"], r["modal_differs"]) == ("MAY", True), r
    r = _rule_row("Sessions MUST expire.", None, ["Sessions MUST expire."])
    assert r["modal_differs"] is False, r


# gapfix13 (1.4.42): G253-G257, counting

def _g13_mark(repo, ws, capsys, *args):
    import mark
    capsys.readouterr()
    code = mark.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), *args])
    cap = capsys.readouterr()
    return code, (json.loads(cap.out) if cap.out.strip() else None), cap.err


AUDIT_1 = "Keep every audit record for seven years at least."


def test_a_hand_lack_on_a_no_folder_topic_raises_the_total_and_the_check_names_the_stated_line(tmp_path, capsys):
    # G253: a lack judged by hand gets a row (mark.py --lack), counted in measured_total and its topic's row.
    repo, ws = build(tmp_path)
    _, before, _ = run(repo, ws, capsys)
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(PLAN + f"\nThis area's gaps: {before['measured_total']}\n")
    code, out, err = _g13_mark(repo, ws, capsys, "--lack", "controls", "--source", "reference/building--audit.txt#1",
                           "--text", AUDIT_1, "--why", "no topic holds the retention period")
    assert code == 0, err
    assert out["id"] == "hand:building/audit:1@controls" and (ws / "areas" / AREA / "hand_lacks.json").is_file()
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert chk["measured_total"] == before["measured_total"] + 1
    assert [r["form"] for r in chk["gap_total"]] == ["figure"] and chk["gap_total"][0]["stated"] == before["measured_total"]
    _, after, _ = run(repo, ws, capsys)
    row = next(r for r in after["hand_lacks"] if r["id"] == "hand:building/audit:1@controls")
    assert row["counted"] and row["topic"] == "controls" and row["text"] == AUDIT_1
    t = next(t for t in after["topic_totals"] if t["topic"] == "controls")
    assert t["hand"] == 1 and t["total"] == 1
    assert sum(t["total"] for t in after["topic_totals"]) == after["measured_total"]


def test_withdrawing_a_hand_lack_lowers_the_total(tmp_path, capsys):
    repo, ws = build(tmp_path)
    _, before, _ = run(repo, ws, capsys)
    _g13_mark(repo, ws, capsys, "--lack", "controls", "--source", "reference/building--audit.txt#1",
          "--text", AUDIT_1, "--why", "x")
    _, up, _ = run(repo, ws, capsys)
    assert up["measured_total"] == before["measured_total"] + 1
    code, _, err = _g13_mark(repo, ws, capsys, "--held", "hand:building/audit:1@controls", "held",
                         "--why", "the plan's controls rule 3 keeps it")
    assert code == 0, err
    _, down, _ = run(repo, ws, capsys)
    assert down["measured_total"] == before["measured_total"]
    assert next(r for r in down["hand_lacks"])["counted"] is False


def test_a_hand_lack_of_a_measured_row_is_refused_naming_the_row(tmp_path, capsys):
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    found = qb.sentences(BUILDING)
    code, _, err = _g13_mark(repo, ws, capsys, "--lack", "authn", "--source", "reference/building--security.txt#1",
                         "--text", found[0], "--why", "x")
    assert code == 2 and "lacking:building/security:1@authn" in err
    assert not (ws / "areas" / AREA / "hand_lacks.json").exists()
    code, _, err = _g13_mark(repo, ws, capsys, "--lack", "controls", "--source", "reference/building--audit.txt#1",
                         "--text", "Some other sentence entirely here.", "--why", "x")
    assert code == 2 and AUDIT_1 in err      # the text must be the sentence at #n
    code, _, err = _g13_mark(repo, ws, capsys, "--lack", "nosuch", "--source", "reference/building--audit.txt#1",
                         "--text", AUDIT_1, "--why", "x")
    assert code == 2 and "nosuch" in err


def test_lacks_in_the_areas_own_r9_file_count_in_its_total(tmp_path, capsys):
    # G254 (a)
    repo, ws = build(tmp_path)
    _, before, _ = run(repo, ws, capsys)
    a = ws / "areas" / AREA
    (a / "gaps" / "new-compliance.json").write_text(json.dumps({
        "folder": "cookbook/guidelines/implementing/sec/compliance", "references": [
            {"file": str(a / "reference" / "building--audit.txt"), "sentences": 2, "held": 0, "lacking": 2,
             "lacking_sentences": [AUDIT_1, "Ship logs off the host."]}]}))
    _, after, _ = run(repo, ws, capsys)
    rows = after["r9_lacking"]
    assert [r["id"] for r in rows] == ["r9:compliance:building/audit:1", "r9:compliance:building/audit:2"]
    assert after["measured_total"] == before["measured_total"] + 2
    assert next(t for t in after["topic_totals"] if t["topic"] == "compliance")["r9"] == 2
    code, _, err = _g13_mark(repo, ws, capsys, "--held", "r9:compliance:building/audit:2", "held", "--why", "x")
    assert code == 0, err
    _, held, _ = run(repo, ws, capsys)
    assert held["measured_total"] == before["measured_total"] + 1


def _home_result(area="implementing/sec", topics=("authn",)):
    return {"area": area, "topics": [{"topic": t, "own": {"lacking": 0}} for t in topics],
            "short_sentences": [], "lacking_pieces": [], "held_by_wording": [], "home_unguessed": [],
            "home_measures": [{"topic": "authz", "sentences": [
                {"speciality": "building/x", "n": 1, "verdict": "lacking", "marked_for": None},
                {"speciality": "building/x", "n": 2, "verdict": "lacking", "marked_for": "reviewing/sec"},
                {"speciality": "building/x", "n": 3, "verdict": "held", "marked_for": None}]}]}


def test_a_lacking_home_measure_counts_at_the_area_owning_its_home(tmp_path):
    # G254 (b): counted here, unless the recorded home is another area's topic: then `counted at <area>`.
    r = _home_result()
    run_gaps._home_rows(r, {("building/x", 2): "reviewing/sec:lod"})
    s = r["home_lacking"]      # the lacking ones only; home_measures keeps its shape
    assert [x["id"] for x in s] == ["home:building/x:1@authz", "home:building/x:2@authz"]
    assert [x["counted"] for x in s] == [True, False]
    assert s[0]["counted_at"] == "implementing/sec" and s[1]["counted_at"] == "reviewing/sec"
    assert "counted at reviewing/sec" in s[1]["why_not_counted"]
    assert "id" not in r["home_measures"][0]["sentences"][0]
    assert run_gaps.measured_total(r) == 1


def test_a_piece_marked_for_another_area_says_where_it_is_counted():
    rows = run_gaps._lacking_rows([("building/x", "f", "authn", "p", 4)], {"f": (None, {4: "reviewing/sec"})},
                                  "implementing/sec")
    assert rows[0]["counted"] is False and rows[0]["counted_at"] == ["reviewing/sec"]


def _saved_area(ws, area, report, homes=None):
    d = ws / "areas" / area
    d.mkdir(parents=True, exist_ok=True)
    (d / "run_gaps.json").write_text(json.dumps({"area": area, "topics": [], "short_sentences": [],
                                                 "lacking_pieces": [], "held_by_wording": [], **report}))
    if homes:
        (d / "homes.json").write_text(json.dumps(homes))


def test_check_homes_lists_a_home_lack_counted_nowhere_or_twice(tmp_path, capsys):
    # G254 (c)
    repo, ws = build(tmp_path)
    home = lambda n: {"topic": "t", "sentences": [{"speciality": "building/x", "n": n, "verdict": "lacking"}]}
    _saved_area(ws, "a/one", {"home_measures": [home(1), home(2), home(3)]},
                homes={"building/x": {"1": "a/two:u"}})
    _saved_area(ws, "a/two", {"lacking_pieces": [
        {"id": "lacking:building/x:2@u", "speciality": "building/x", "n": 2, "topic": "u", "counted": True}]})
    capsys.readouterr()
    code = run_gaps.main(["--check-homes", "--workspace", str(ws), "--repo", str(repo)])
    out = json.loads(capsys.readouterr().out)
    assert code == 1
    rows = {(r["speciality"], r["n"]): r for r in out["check_homes"]}
    # gapfix14 (G273): a row names its kind, owner, home topic and every counting area's ids
    assert rows[("building/x", 1)]["kind"] == "counted_nowhere" and rows[("building/x", 1)]["owner"] == "a/two"
    assert rows[("building/x", 1)]["counting"] == {}
    assert rows[("building/x", 2)]["kind"] == "counted_twice"
    assert sorted(rows[("building/x", 2)]["counting"]) == ["a/one", "a/two"]
    assert ("building/x", 3) not in rows
    (ws / "areas" / "a" / "two" / "hand_lacks.json").write_text(json.dumps({"hand:building/x:1@u": {
        "topic": "u", "speciality": "building/x", "n": 1, "text": "x", "source": "r#1", "why": "w"}}))
    (ws / "areas" / "a" / "two" / "run_gaps.json").write_text(json.dumps({"area": "a/two", "topics": []}))
    capsys.readouterr()
    assert run_gaps.main(["--check-homes", "--workspace", str(ws), "--repo", str(repo)]) == 0
    assert json.loads(capsys.readouterr().out)["check_homes"] == []


def test_a_non_home_lacking_piece_is_listed_as_its_own_key(tmp_path, capsys):
    # G256: counted per topic row until each has a verdict; the rows not at the sentence's home are listed.
    repo, ws = build(tmp_path)
    _, out, _ = run(repo, ws, capsys)
    ids = {r["id"] for r in out["non_home_lacking"]}
    rows = {r["id"]: r for r in out["lacking_pieces"]}
    assert ids and all(rows[i]["counted"] and not rows[i].get("verdict") for i in ids)
    assert all(r["home"] != r["topic"] for r in out["non_home_lacking"])


def test_the_first_check_lists_each_counted_rows_last_verdict(tmp_path, capsys):
    # G257: per counted row its last recorded verdict and verdict_was (or none); the digest counts both kinds.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    _g13_mark(repo, ws, capsys, "--held", "short:building/security:6", "not", "--why", "lacking")
    code, chk, _ = run(repo, ws, capsys, "--check")
    rows = {r["id"]: r for r in chk["counted_rows"]}
    assert rows["short:building/security:6"]["last_verdict"] == "not"
    assert rows["lacking:building/security:1@authn"] == {"id": "lacking:building/security:1@authn",
                                                          "last_verdict": "none", "verdict_was": "none"}
    capsys.readouterr()
    run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI),
                   "--check", "--digest"])
    line = capsys.readouterr().out.strip().splitlines()[-1]
    assert "counted_with_prior_verdict 1" in line and re.search(r"counted_never_judged \d+", line)


def test_check_prints_at_most_forty_rows_a_key_naming_the_rest(tmp_path, capsys, monkeypatch):
    # G271: a --check shows at most 40 rows per key plus `(N more: --rows <key>)`; --rows prints them whole.
    repo, ws = build(tmp_path)
    big = {"check": "changed", "changes": [{"path": f"p{i}"} for i in range(55)], "new_keys": []}
    monkeypatch.setattr(run_gaps, "check", lambda *a, **k: (dict(big), 1))
    code, out, _ = run(repo, ws, capsys, "--check")
    assert code == 1 and len(out["changes"]) == 41 and out["changes"][-1] == "(15 more: --rows changes)"
    code, out, _ = run(repo, ws, capsys, "--check", "--rows", "changes")
    assert code == 1 and len(out["changes"]) == 55


def test_rows_names_another_scripts_key_as_every_script_does(tmp_path, capsys):
    # G261: one --rows shape: `no output key 'K'; K is <owner>'s output key: run <owner> --rows K; keys: ...`.
    repo, ws = build(tmp_path)
    assert run(repo, ws, capsys, "--hints")[0] in (0, 1)
    code, out, err = run(repo, ws, capsys, "--rows", "marked_here")
    assert code == 2 and out is None
    assert "run_gaps.py: no output key 'marked_here'; marked_here is unmeasured.py's output key: run unmeasured.py " \
           "--rows marked_here; keys: " in err


def test_a_gap_line_in_another_form_quotes_the_line_and_the_accepted_form(tmp_path):
    # G259: the check names the offending line and the exact accepted form, bold included.
    plan = tmp_path / "area-plan.md"
    plan.write_text("# Plan\n\nThis area's gaps (by hand): 3\n\n**This area's gaps:** 3\n")
    rows = run_gaps.gap_totals(plan, 3, 3)
    [row] = rows
    assert row["form"] == "other"
    assert "`This area's gaps (by hand): 3`" in row["why"], row["why"]
    assert run_gaps.GAP_FORM in row["why"] and "**This area's gaps:** N" in run_gaps.GAP_FORM


# gapfix13 (1.4.42): G260, rule_sentence and the modal vocabulary

_G13_TABLE = ("| Setting | API | Action | |---|---|---| | Text Scaling | `TextScaleFactor` | Layouts must not break "
              "| | Caret Browsing | System setting | Non-interactive text should be navigable |")


def test_a_fragment_beside_a_table_is_judged_against_no_unrelated_row_of_it():
    # accessibility#2: a fragment piece read SHOULD from a whole table's unrelated "should" row.
    found = [("rules", "Meaningful focus order following visual layout"), ("rules", _G13_TABLE)]
    pick = run_gaps.rule_pick("meaningful focus order that follows the visual layout.", found)
    assert pick["rule_sentence"] == found[0][1], pick
    assert run_gaps.modals(pick["rule_sentence"]) == [] and pick["rule_at"] == "rules sentence 1", pick


def test_the_rule_is_the_sentence_holding_the_piece_not_a_longer_one_sharing_its_nouns():
    # code-quality#4: "a nested Directory.Packages.props imports its parent" named the central-versions SHOULD
    # sentence, though "A nested one MUST import its parent" holds it; a code block holding the piece is not
    # judged against an unrelated SHOULD sentence sharing one word.
    found = [("cpm", "- Projects SHOULD turn on central versions with a `Directory.Packages.props` at the root."),
             ("cpm", "- Only the nearest `Directory.Packages.props` applies."),
             ("cpm", "A nested one MUST import its parent explicitly with `GetPathOfFileAbove`.")]
    pick = run_gaps.rule_pick("a nested `Directory.Packages.props` imports its parent.", found)
    assert pick["rule_sentence"] == found[2][1] and pick["rule_at"] == "cpm sentence 3", pick
    code = [("arch", "```csharp // ViewModel with source generators [ObservableObject] public partial class Vm {"),
            ("arch", "- NavigationView + Frame SHOULD be used for page-level navigation")]
    pick = run_gaps.rule_pick("`[ObservableObject]` and `[RelayCommand]` source generators used;", code)
    assert pick["rule_sentence"] == code[0][1] and run_gaps.modal(pick["rule_sentence"]) == (None, None), pick


def test_a_piece_two_checklist_rows_hold_is_judged_at_the_stronger_row_and_names_its_id():
    # skills-and-agents#4: rule-checklist 2#2 named C07 (WARN); R04 (FAIL), in another table, holds it as well.
    general = ("| ID | Criterion | How to check | Severity | |-----|---|---|---| | C01 | Single responsibility | One "
               "concern | WARN | | C07 | Instructions are actionable and specific | Every instruction tells the LLM what "
               "to do concretely, not vague directives like \"handle errors appropriately\" | WARN |")
    specific = ("| ID | Criterion | How to check | Severity | |-----|---|---|---| | R04 | No vague directives | Every "
                "instruction is concrete and actionable; no \"handle appropriately\" or \"write good code\" | FAIL |")
    found = [("general", general), ("rule-specific", specific)]
    pick = run_gaps.rule_pick('every instruction concrete and actionable, never a vague directive like "handle '
                              'errors appropriately";', found)
    assert "R04" in pick["rule_sentence"] and run_gaps.modal(pick["rule_sentence"]) == ("MUST", 3), pick
    assert pick["rule_at"] == "rule-specific sentence 1 row R04", pick


def test_preferred_and_the_other_word_forms_are_modals_and_respect_is_an_imperative():
    # networking#2: "preferred" read as no modal (a MUST) against "SHOULD be preferred"; networking#3: "Respect
    # server rate limits." is a bare imperative.
    assert run_gaps.modal("Cursor pagination is preferred.") == ("PREFERRED", 2)
    assert run_gaps.modal("Preferably cache it.") == ("PREFERABLY", 2)
    assert run_gaps.modal("It is optionally logged.") == ("OPTIONALLY", 1)
    assert run_gaps.imperative("Respect server rate limits.") is True
    pick = run_gaps.rule_pick("respect server rate limits", [("rl", "Respect server rate limits.")])
    assert pick["implied"] is True


def test_a_held_row_names_where_its_rule_sentence_is(tmp_path, capsys):
    # G260: each held_by_wording row says which sentence (and row) its rule_sentence came from.
    repo, ws = build(tmp_path)
    code, out, _ = run(repo, ws, capsys)
    rows = out["held_by_wording"]
    assert rows and all("rule_at" in r for r in rows), rows
    assert all(r["rule_at"] is None or re.fullmatch(r"\S+ sentence \d+( row \S+)?", r["rule_at"]) for r in rows)


def test_a_short_piece_marked_for_another_area_is_named_as_not_owed(tmp_path, capsys):
    # gapfix13b (platform-integration#5, 1.4.42): a short_sentences row that owes no verdict here (`counted` false,
    # marked for another area) is named in `short_not_owed` with where it is counted and why; an owed row is not.
    result = {"area": "implementing/sec", "short_sentences": [
        {"speciality": "building/x", "n": 4, "marked_for": "reviewing/sec", "topic": "authn", "text": "p"},
        {"speciality": "building/x", "n": 5, "marked_for": "implementing/sec", "topic": "authn", "text": "q"}]}
    run_gaps._short_ids(result)
    [row] = run_gaps.short_not_owed(result)
    assert (row["id"], row["counted_at"], row["topic"]) == ("short:building/x:4", ["reviewing/sec"], "authn"), row
    assert "reviewing/sec" in row["why"] and "no verdict" in row["why"], row
    repo, ws = build(tmp_path)
    _, out, _ = run(repo, ws, capsys)
    assert out["short_not_owed"] == [r for r in run_gaps.short_not_owed(out)], out["short_not_owed"]


# gapfix14 (1.4.43): G273, G277, G282, G289, G276 -- --check-homes lists only real problems, and says what to do

def _home(n, topic="t", verdict="lacking"):
    return {"topic": topic, "sentences": [{"speciality": "building/x", "n": n, "verdict": verdict}]}


def _check_homes(ws, repo, capsys, *extra):
    capsys.readouterr()
    code = run_gaps.main(["--check-homes", "--workspace", str(ws), "--repo", str(repo), *extra])
    return code, {(r["speciality"], r["n"], r["kind"]): r for r in json.loads(capsys.readouterr().out)["check_homes"]}


def test_check_homes_never_lists_a_sentence_its_owner_holds_at_its_home(tmp_path, capsys):
    # G277: 25 owner-held rows were listed "counted in no area" (tools/check-homes-post-data.txt).
    repo, ws = build(tmp_path)
    _saved_area(ws, "a/one", {"home_measures": [_home(1)]})
    (ws / "areas" / "a" / "one" / "held.json").write_text(json.dumps(
        {"home:building/x:1@t": {"verdict": "held", "text": None, "why": "the topic says it in other words"}}))
    code, rows = _check_homes(ws, repo, capsys)
    assert (code, rows) == (0, {})


def test_check_homes_lists_a_double_count_with_each_areas_row_ids_and_the_owner(tmp_path, capsys):
    # G273 (b): owner, home topic, the owner's verdict id and verdict, every counting area's ids, what to do.
    repo, ws = build(tmp_path)
    _saved_area(ws, "a/one", {"home_measures": [_home(2)]})
    _saved_area(ws, "a/two", {"lacking_pieces": [
        {"id": "lacking:building/x:2@u", "speciality": "building/x", "n": 2, "topic": "u", "counted": True}]})
    code, rows = _check_homes(ws, repo, capsys)
    row = rows[("building/x", 2, "counted_twice")]
    assert code == 1 and len(rows) == 1
    assert row["owner"] == "a/one" and row["home_topic"] == "t"
    assert row["owner_verdict"] == {"id": "home:building/x:2@t", "verdict": "lacking"}
    assert row["counting"] == {"a/one": ["home:building/x:2@t"], "a/two": ["lacking:building/x:2@u"]}
    assert "--counted-at a/one" in row["why"] and "lacking:building/x:2@u" in row["why"], row["why"]


def test_check_homes_lists_a_home_lack_counted_nowhere_with_its_recorded_owner(tmp_path, capsys):
    repo, ws = build(tmp_path)
    _saved_area(ws, "a/one", {"home_measures": [_home(1)]}, homes={"building/x": {"1": "a/two:u"}})
    _saved_area(ws, "a/two", {})
    code, rows = _check_homes(ws, repo, capsys)
    row = rows[("building/x", 1, "counted_nowhere")]
    assert code == 1 and row["owner"] == "a/two" and row["home_topic"] == "u" and row["counting"] == {}
    assert row["owner_verdict"]["verdict"] == "unjudged" and "--area a/two" in row["why"], row


def test_check_homes_area_filters_to_rows_touching_that_area_and_its_exit_covers_them_only(tmp_path, capsys):
    # G273 (c), G282
    repo, ws = build(tmp_path)
    _saved_area(ws, "a/one", {"home_measures": [_home(2)]})
    _saved_area(ws, "a/two", {"lacking_pieces": [
        {"id": "lacking:building/x:2@u", "speciality": "building/x", "n": 2, "topic": "u", "counted": True}]})
    _saved_area(ws, "a/three", {})
    assert _check_homes(ws, repo, capsys, "--area", "a/two")[0] == 1
    code, rows = _check_homes(ws, repo, capsys, "--area", "a/three")
    assert (code, rows) == (0, {})


def test_the_recorded_home_wins_over_the_word_match_topic(tmp_path, capsys):
    # G277 (platform-web-backend 3 at mcp-server-design): the hold at the recorded home is the verdict; the word-
    # match topic's lacking home measure is no count.
    repo, ws = build(tmp_path)
    _saved_area(ws, "a/one", {"home_measures": [_home(3)], "held_by_wording": [
        {"id": "building/x:3@v", "speciality": "building/x", "n": 3, "topic": "v", "text": "p"}]},
        homes={"building/x": {"3": "a/one:v"}})
    code, rows = _check_homes(ws, repo, capsys)
    assert (code, rows) == (0, {})
    r = {"area": "a/one", "home_measures": [_home(3)], "held_by_wording": [
        {"id": "building/x:3@v", "speciality": "building/x", "n": 3, "topic": "v", "text": "p"}]}
    run_gaps._home_rows(r, {("building/x", 3): "a/one:v"})
    assert r["home_lacking"][0]["counted"] is False and "building/x:3@v" in r["home_lacking"][0]["why_not_counted"]


def test_check_homes_lists_conflicting_home_records_owners_record_first(tmp_path, capsys):
    # late log (hygiene 9): reviewing/code-quality records stale-names, implementing/code-quality (the owner)
    # delete-what-you-supersede.
    repo, ws = build(tmp_path)
    _saved_area(ws, "a/own", {"lacking_pieces": [
        {"id": "lacking:building/x:9@p", "speciality": "building/x", "n": 9, "topic": "p", "counted": True}]},
        homes={"building/x": {"9": "a/own:p"}})
    _saved_area(ws, "a/rev", {}, homes={"building/x": {"9": "a/own:q"}})
    code, rows = _check_homes(ws, repo, capsys)
    row = rows[("building/x", 9, "home_conflict")]
    assert code == 1 and row["records"] == [{"area": "a/own", "home": "a/own:p"}, {"area": "a/rev", "home": "a/own:q"}]
    assert ("building/x", 9, "counted_twice") not in rows and ("building/x", 9, "counted_nowhere") not in rows


def test_held_counted_at_is_structured_and_an_old_why_is_read_too(tmp_path, capsys):
    # G273 (a): `--counted-at AREA` stores counted_at on the verdict; "counted at X" / "the owner is X" are read.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    code, out, err = _g13_mark(repo, ws, capsys, "--held", "lacking:building/security:1@authn", "held", "--why",
                               "the owner counts it", "--counted-at", "reviewing/sec")
    assert code == 0, err
    held = json.loads((ws / "areas" / AREA / "held.json").read_text())
    assert held["lacking:building/security:1@authn"]["counted_at"] == "reviewing/sec"
    code, _, err = _g13_mark(repo, ws, capsys, "--held", "lacking:building/security:1@authn", "not", "--why",
                             "x", "--counted-at", "reviewing/sec")
    assert code == 2 and "--counted-at" in err
    code, _, err = _g13_mark(repo, ws, capsys, "--held", "lacking:building/security:1@authn", "held", "--why",
                             "x", "--counted-at", "no/such")
    assert code == 2 and "no/such" in err
    assert run_gaps.verdict_counted_at({"verdict": "held", "why": "counted at reviewing/sec: its home"}) == \
        "reviewing/sec"
    assert run_gaps.verdict_counted_at({"verdict": "held", "why": "the owner is implementing/x."}) == "implementing/x"
    assert run_gaps.verdict_counted_at({"verdict": "held", "counted_at": "a/b"}) == "a/b"
    assert run_gaps.verdict_counted_at({"verdict": "held", "why": "said in other words"}) is None


def test_a_hand_hold_at_an_unmeasured_home_is_that_sentences_home_verdict(tmp_path, capsys):
    # G276 (platform-database 9): mark.py --hold records it in hand_holds.json; run_gaps lists it, the non-home row
    # pointing at that home names it, and --check-homes reads it as the owner's verdict.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    src = "reference/building--audit.txt"
    code, out, err = _g13_mark(repo, ws, capsys, "--hold", "controls", "--source", f"{src}#1", "--text", AUDIT_1,
                               "--why", "controls says: keep every audit record seven years")
    assert code == 0, err
    assert out["id"] == "hold:building/audit:1@controls" and out["now"] == "held"
    hold = json.loads((ws / "areas" / AREA / "hand_holds.json").read_text())
    assert hold["hold:building/audit:1@controls"]["why"].startswith("controls says")
    code, out, err = _g13_mark(repo, ws, capsys, "--hold", "controls", "--source", f"{src}#1", "--text", AUDIT_1,
                               "--why", "again")
    assert code == 2 and "--refresh" in err
    code, out, _ = run(repo, ws, capsys)
    assert [r["id"] for r in out["hand_holds"]] == ["hold:building/audit:1@controls"]
    r = {"area": "a/one", "building": [{"speciality": "building/x", "sentences": [{"n": 9, "home_guess": "w"}]}],
         "lacking_pieces": [{"id": "lacking:building/x:9@w", "speciality": "building/x", "n": 9, "topic": "w",
                             "counted": True}],
         "hand_holds": [{"id": "hold:building/x:9@u", "speciality": "building/x", "n": 9, "topic": "u"}]}
    [row] = run_gaps.non_home_lacking(r, {("building/x", 9): "a/one:u"})
    assert row["home"] == "u" and row["home_verdict"] == {"id": "hold:building/x:9@u", "verdict": "held"}
    _saved_area(ws, "a/one", {"lacking_pieces": r["lacking_pieces"]}, homes={"building/x": {"9": "a/one:u"}})
    _saved_area(ws, "a/two", {"lacking_pieces": [
        {"id": "lacking:building/x:9@z", "speciality": "building/x", "n": 9, "topic": "z", "counted": True}]})
    code, rows = _check_homes(ws, repo, capsys, "--area", "a/one")
    assert code == 1 and rows[("building/x", 9, "counted_twice")]["owner_verdict"]["verdict"] == "unjudged"
    (ws / "areas" / "a" / "one" / "hand_holds.json").write_text(json.dumps({"hold:building/x:9@u": {
        "topic": "u", "speciality": "building/x", "n": 9, "text": "x", "source": "r#9", "why": "w"}}))
    code, rows = _check_homes(ws, repo, capsys, "--area", "a/one")
    assert (code, rows) == (0, {})


# gapfix14 (1.4.43): G285 --lack pieces, G284 (c) --non-home-held, G288 a `not` needs a why

def test_lack_takes_a_piece_and_refuses_a_second_record_without_refresh(tmp_path, capsys):
    # G285: several pieces of one sentence at one topic are separate rows; a second --lack is refused, not refreshed.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    lack = ["--lack", "controls", "--source", "reference/building--audit.txt#1", "--text", AUDIT_1]
    assert _g13_mark(repo, ws, capsys, *lack, "--why", "retention period")[0] == 0
    code, _, err = _g13_mark(repo, ws, capsys, *lack, "--why", "the review cadence")
    assert code == 2 and "--refresh" in err and "--piece" in err, err
    code, out, err = _g13_mark(repo, ws, capsys, *lack, "--why", "the review cadence", "--piece", "2")
    assert code == 0 and out["id"] == "hand:building/audit:1@controls#2", err
    code, out, _ = _g13_mark(repo, ws, capsys, *lack, "--why", "retention period, seven years", "--refresh")
    assert code == 0 and out["how"] == "refreshed"
    _, after, _ = run(repo, ws, capsys)
    rows = [r for r in after["hand_lacks"] if r["topic"] == "controls"]
    assert len(rows) == 2 and all(r["counted"] for r in rows)
    assert next(t for t in after["topic_totals"] if t["topic"] == "controls")["hand"] == 2
    code, _, err = _g13_mark(repo, ws, capsys, "--lack", "controls", "--source", "reference/building--audit.txt#1",
                             "--text", "Keep every audit record", "--why", "x")
    assert code == 2 and AUDIT_1 in err and "--piece" in err


def test_a_held_row_at_another_topic_never_blocks_a_lack(tmp_path, capsys):
    # G285 (hygiene 9): a lack refused as duplicate_of a held row of the same sentence at another topic.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    for t in ("vp", "authn"):
        _g13_mark(repo, ws, capsys, "--held", f"lacking:building/security:2@{t}", "held", "--why", f"{t} says it")
    run(repo, ws, capsys)
    found = qb.sentences(BUILDING)
    code, out, err = _g13_mark(repo, ws, capsys, "--lack", "controls", "--source",
                               "reference/building--security.txt#2", "--text", found[1], "--why", "no control rule")
    assert code == 0, err
    _, after, _ = run(repo, ws, capsys)
    row = next(r for r in after["hand_lacks"] if r["id"] == "hand:building/security:2@controls")
    assert row["counted"] and "duplicate_of" not in row, row
    code, _, err = _g13_mark(repo, ws, capsys, "--lack", "authn", "--source", "reference/building--security.txt#2",
                             "--text", found[1], "--why", "x")
    assert code == 2 and "lacking:building/security:2@authn" in err      # a row at the same topic still blocks


def test_non_home_held_judges_every_row_whose_home_has_a_verdict_in_one_call(tmp_path, capsys):
    # G284 (c): one call; the count printed; a row whose home has no verdict yet stays counted (G256).
    repo, ws = build(tmp_path)
    _, before, _ = run(repo, ws, capsys)
    rp = ws / "areas" / AREA / "run_gaps.json"
    rep = json.loads(rp.read_text())
    rep["lacking_pieces"].append({"id": "lacking:building/x:1@authn", "speciality": "building/x", "n": 1,
                                  "topic": "authn", "text": "p", "counted": True})
    rep["non_home_lacking"].append({"id": "lacking:building/x:1@authn", "topic": "authn", "home": "ghost"})
    rp.write_text(json.dumps(rep))
    n = len(before["non_home_lacking"])
    code, out, err = _g13_mark(repo, ws, capsys, "--non-home-held")
    assert code == 0, err
    assert (out["non_home_held"], out["skipped_no_home_verdict"], out["verdicts"]) == (n, 1, n), out
    held = json.loads((ws / "areas" / AREA / "held.json").read_text())
    assert held["lacking:building/security:2@authn"]["why"].startswith(
        "judged at home topic implementing/sec:authz (building/security:2@authz: held)")
    assert "lacking:building/x:1@authn" not in held
    _, after, _ = run(repo, ws, capsys)
    assert after["non_home_lacking"] == [] and after["measured_total"] == before["measured_total"] - n


def test_a_not_on_a_held_row_needs_a_why(tmp_path, capsys):
    # G288: a `not` moves the total; an empty why was accepted on a held_by_wording id.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    code, _, err = _g13_mark(repo, ws, capsys, "--held", "building/security:2@authz", "not")
    assert code == 2 and "give --why" in err
    f = tmp_path / "v-gapfix14.json"
    f.write_text(json.dumps({"building/security:2@authz": {"verdict": "not", "why": ""}}))
    code, _, err = _g13_mark(repo, ws, capsys, "--held-file", str(f))
    assert code == 2 and "give --why" in err
    assert _g13_mark(repo, ws, capsys, "--held", "building/security:2@authz", "held")[0] == 0


# gapfix14 (1.4.43, G275): the modal detector reads only a sentence's own rule words

def test_a_lowercase_negated_may_is_must_not_code_hygiene():
    s = ("When you rename or move something, you MUST update or remove every reference; no path, import, or export "
         "may point at the thing that no longer exists.")
    assert run_gaps.modal_weakest(s)[1] == 3 and "MAY" not in [w for w, _ in run_gaps.modals(s)]
    assert run_gaps.modal_weakest("A caller may not open the file twice.") == ("MUST NOT", 3)
    assert run_gaps.modal_weakest("The worker must never block the loop.")[1] == 3


def test_a_modal_in_a_relative_clause_with_have_is_no_modal_data_constraints():
    s = ("`must-not-trust-checks-on-bypassed-data`: no code reading data that may have bypassed constraints "
         "(external file edits, `PRAGMA ignore_check_constraints`) assumes the data satisfies them")
    assert run_gaps.modals(s) == []


def test_a_relative_clause_modal_is_no_modal_bulk_operation_verification():
    s = ("1. **Stale references**: The entire repo MUST be grepped for old names, paths, or identifiers that should "
         "have been updated.")
    assert run_gaps.modal_weakest(s) == ("MUST", 3)


def test_a_quoted_example_modal_is_no_modal_observable_behavior_contract():
    s = ('- You **SHOULD** explicitly document which behaviors are guaranteed and state the rest as '
         '**non-guarantees** (e.g., "iteration order is unspecified and may change").')
    assert run_gaps.modal_weakest(s) == ("SHOULD", 2)


def test_a_parenthesised_modal_is_no_modal_mcp_primitive_design():
    s = ("Reviewer **MUST** reject a tool that only returns static data (should be a resource).")
    assert run_gaps.modal_weakest(s) == ("MUST", 3)


def test_avoid_inside_a_must_sentence_is_its_negation_infra_non_root():
    s = "- The runtime **MUST** run as a non-root user; set an explicit `USER` and avoid UID 0."
    assert run_gaps.modal_weakest(s) == ("MUST", 3)
    r = _rule_row("avoid UID 0.", "The runtime MUST run as a non-root user; set an explicit USER and avoid UID 0.",
                  ["The runtime **MUST** run as a non-root user; set an explicit `USER` and avoid UID 0."])
    assert r["modal_differs"] is False, r
    assert run_gaps.modal_weakest("Avoid global state in handlers.") == ("AVOID", 2)     # an opener still counts


# gapfix14 (1.4.43, G279): rule_sentence names the sentence holding the piece's rule, for every case the logs quote

def test_a_code_block_is_never_the_rule_when_a_prose_sentence_holds_the_piece_concurrency():
    found = [("c", "- `ConfigureAwait(false)` in library code to avoid capturing the synchronization context"),
             ("c", "- Never use `.Result` or `.Wait()` on async methods"),
             ("c", "- All async APIs MUST accept `CancellationToken`"),
             ("c", "```csharp // Library code — ConfigureAwait(false) public async Task<Data> FetchAsync("
                   "CancellationToken ct = default) { var response = await _client.GetAsync(url, ct)"
                   ".ConfigureAwait(false); } ```")]
    pick = run_gaps.rule_pick("ConfigureAwait(false) in library code, no .Result/.Wait(), CancellationToken in all "
                              "async APIs;", found)
    assert not pick["rule_sentence"].startswith("```") and not pick["topic_sentence"].startswith("```"), pick
    assert run_gaps.modal(pick["rule_sentence"])[1] == 3, pick


def test_a_labelled_item_is_its_own_rule_never_a_sibling_items_modal_properties_of_good_tests():
    found = [("intro", "From Kent Beck's Test Desiderata — tests should be:"),
             ("intro", "**Isolated** — tests MUST NOT share mutable state or depend on execution order"),
             ("intro", "**Readable** — a failing test tells you what broke and why"),
             ("intro", "**Structure-insensitive** — refactoring internals SHOULD NOT break tests"),
             ("intro", "**Specific** — a failure points to exactly one cause")]
    pick = run_gaps.rule_pick("a failing test identifies exactly one cause;", found)
    assert pick["rule_sentence"] == found[4][1], pick


def test_a_labelled_imperative_heading_is_the_rule_of_its_items_unit_test_patterns():
    found = [("intro", "**Rules:**"),
             ("intro", "- Each test MUST have one assertion concept (not one `assert` — one logical concept)"),
             ("intro", "- Tests MUST NOT contain logic — no `if`, `for`, `try/catch`, `switch`"),
             ("intro", "**Naming — use descriptive names that read as specifications:**"),
             ("intro", "- `ParseOrder_WithMissingField_ThrowsValidationError`")]
    r = _rule_row("test names read as specifications (e.g., `ParseOrder_WithMissingField_ThrowsValidationError`);",
                  None, [s for _, s in found])
    assert r["rule_sentence"] == found[3][1] and r["modal_topic_implied"] is True, r
    assert (r["modal_topic"], r["modal_differs"]) == ("MUST", False), r


_DMC = [("comments", "- For every changed function, read its comment and docstring against the new body."),
        ("comments", "- Flag comments that narrate history (\"now we\", \"previously\", \"changed to\") instead of "
                     "stating what is true now."),
        ("readmes", "- Every command, flag, path, file name, environment variable and config key mentioned in a "
                    "README, an AGENTS.md or a similar agent instruction file MUST exist and behave as described."),
        ("smells", "- a doc that names a class, function or flag that a search of the repo does not find;"),
        ("smells", "- two docs that give different answers to the same question;"),
        ("smells", "Quote the stale text and the line of code that contradicts it, so the fix is unambiguous."),
        ("why", "A stale claim costs a person an hour and costs an agent a wrong turn it will not question, so a "
                "wrong doc is a defect of the same weight as wrong code.")]


def test_one_wording_gets_one_rule_and_it_is_the_topic_sentence_docs_match_code():
    for piece in ("Name the doc location and the code that contradicts it.",
                  "Name the file and line and the code that contradicts it.",
                  "Each finding quotes or names the stale claim (file and line) and the code location that "
                  "contradicts it;"):
        pick = run_gaps.rule_pick(piece, _DMC)
        assert pick["rule_sentence"] == _DMC[5][1] and pick["implied"] is True, (piece, pick)
    pick = run_gaps.rule_pick("Update the docs and comments for what you changed in the same increment, and "
                              "comment the why, not the what.", _DMC)
    assert pick["rule_sentence"] == pick["topic_sentence"] == _DMC[0][1], pick


def test_a_checklist_row_with_no_modal_is_judged_at_the_must_sentence_holding_the_piece_recipe_quality():
    found = [("verification-checklist", "- [ ] All required sections are present, in the correct order, as "
                                        "level-2 headings."),
             ("requirements", "- The recipe MUST contain all sections defined in the standard template, in the "
                              "prescribed order.")]
    r = _rule_row("all template sections present in order;", None, [s for _, s in found])
    assert r["rule_sentence"] == found[1][1] and r["modal_topic"] == "MUST", r
    assert run_gaps.modals("- [ ] All required sections are present.") == []      # "required sections": no modal
    assert run_gaps.modal("A title is required.") == ("REQUIRED", 3)
    found = [("verification-checklist", "- [ ] Every normative statement uses an ALL-CAPS RFC 2119 keyword."),
             ("requirements", "- RFC 2119 keywords MUST appear in ALL CAPS when used with their normative meaning."),
             ("requirements", "- Every normative statement MUST use one of the RFC 2119 keywords: MUST, MUST NOT, "
                              "REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, or OPTIONAL")]
    pick = run_gaps.rule_pick("Every requirement uses RFC 2119 keywords;", found)
    assert pick["rule_sentence"] == found[2][1], pick
    assert run_gaps.modal_weakest(found[2][1]) == ("MUST", 3)      # a list of the keywords mentions, never uses them


def test_a_pieces_parenthetical_reason_never_picks_the_rule_code_hygiene():
    found = [("remove", "- When you replace an implementation, you MUST delete the one it replaces in the same "
                        "change — do not leave the old and new versions side by side, or behind a flag."),
             ("remove", "- Commented-out code MUST be deleted, not left as a tombstone."),
             ("remove", "Version control is the history."),
             ("scope", "- You MUST NOT delete code you do not understand or cannot confirm is unused.")]
    for piece in ("delete commented-out code (version control is the history);",
                  "and never leave commented-out code behind, since version control is the history "
                  "(design-for-deletion)."):
        pick = run_gaps.rule_pick(piece, found)
        assert pick["rule_sentence"] == found[1][1], (piece, pick)
    assert run_gaps.imperative("Version control is the history.") is False
    assert run_gaps.imperative("Version every schema.") is True


def test_a_held_row_carries_the_severity_cell_of_its_rule_row():
    table = "| Check | Severity | | --- | --- | | Session timeout is set | FAIL | | Logging is on | WARN |"
    r = _rule_row("Logging is on.", "Logging MUST be on.", [table])
    assert r["rule_severity"] == "WARN" and r["modal_topic"] == "SHOULD", r
    r = _rule_row("Logging is on.", "Logging MUST be on.", ["Logging SHOULD be on."])
    assert r["rule_severity"] is None, r


def test_a_held_row_missing_a_modal_field_is_an_error_the_check_reports(tmp_path, capsys):
    # G279: every held_by_wording row carries all its modal fields; a saved row without one is named, exit 2.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    rp = ws / "areas" / AREA / "run_gaps.json"
    rep = json.loads(rp.read_text())
    assert all(set(run_gaps.REQUIRED_ROW_FIELDS) <= set(r) for r in rep["held_by_wording"])
    rid = rep["held_by_wording"][0]["id"]
    del rep["held_by_wording"][0]["modal_topic"]
    rp.write_text(json.dumps(rep))
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert code == 2 and chk["missing_fields"] == [{"id": rid, "missing": ["modal_topic"], "in": "saved"}], chk


def test_a_flat_clause_is_judged_by_its_own_modal_not_a_later_may_clause_feature_management_debug_mode_22():
    # gapfix14 (G280b, implementing-feature-management#5): the piece "The panel's code stays in the debug source
    # set;" is flat; its sentence's and its rule's later MAY clause is another requirement, never its modal.
    sent = ("The panel's code stays in the debug source set; a `BuildConfig.DEBUG` check in `src/main/` MAY gate "
            "only the call into the panel's entry point.")
    rule = ("- **android-guard-needs-buildconfig**: The panel's code stays in the debug source set; a "
            "`BuildConfig.DEBUG` check in `src/main/` MAY gate only the call into the panel's entry point.")
    r = _rule_row("The panel's code stays in the debug source set;", sent, [rule])
    assert (r["modal_sentence"], r["modal_topic"], r["modal_differs"]) == (None, "MUST", False), r
    r = _rule_row("a `BuildConfig.DEBUG` check in `src/main/` MAY gate only the call into the panel's entry point.",
                  sent, [rule])
    assert (r["modal_topic"], r["modal_differs"]) == ("MAY", False), r
    r = _rule_row("The panel's code stays in the debug source set;", sent,           # one clause: G223 still reads it
                  ["The panel's code SHOULD stay in the debug source set."])
    assert r["modal_differs"] is True, r


def test_a_multi_clause_hold_cites_a_topic_sentence_per_clause_never_a_weaker_one(tmp_path, capsys):
    # gapfix14 (G280a/b): each clause of a multi-clause piece is held by some sentence of the same topic at an
    # equal or stronger modal; `--clause/--cites` records which, refusing a weaker one or a sentence of no topic.
    repo, ws = build(tmp_path)
    rules = repo / "cookbook" / "guidelines" / AREA / "authz" / "rules.md"
    rules.write_text(rules.read_text() + "- Callers MAY cache a role grant for a minute.\n")
    run(repo, ws, capsys)
    rid = "building/security:2@authz"
    code, _, err = _g13_mark(repo, ws, capsys, "--held", rid, "held", "--clause", "Deny every request by default",
                             "--cites", "Callers MAY cache a role grant for a minute.")
    assert code == 2 and "weaker" in err and "MAY" in err, err
    code, _, err = _g13_mark(repo, ws, capsys, "--held", rid, "held", "--clause", "Deny every request by default",
                             "--cites", "Deny nothing at all.")
    assert code == 2 and "no sentence of topic authz" in err, err
    code, _, err = _g13_mark(repo, ws, capsys, "--held", rid, "held", "--clause", "Deny every request by default")
    assert code == 2 and "--cites" in err, err
    code, out, _ = _g13_mark(repo, ws, capsys, "--held", rid, "held",
                             "--clause", "Deny every request by default",
                             "--cites", "Deny every request by default unless a role explicitly grants the action.",
                             "--clause", "pinned dependencies",
                             "--cites", "Pin every dependency to an exact version in the lockfile.")
    assert code == 0, out
    saved = json.loads((ws / "areas" / AREA / "held.json").read_text())[rid]
    assert [c["cites"] for c in saved["clauses"]] == [
        "Deny every request by default unless a role explicitly grants the action.",
        "Pin every dependency to an exact version in the lockfile."], saved
    assert saved["clauses"][0]["modal_cites"] == "MUST", saved
    f = tmp_path / "v-gapfix14.json"                    # --held-file takes the same clauses
    f.write_text(json.dumps({rid: {"verdict": "held", "clauses": [
        {"clause": "x", "cites": "Callers MAY cache a role grant for a minute."}]}}))
    code, _, err = _g13_mark(repo, ws, capsys, "--held-file", str(f))
    assert code == 2 and "weaker" in err, err


def test_check_verdicts_lists_one_piece_at_one_topic_judged_differently_in_two_areas(tmp_path, capsys):
    # gapfix14 (G280c, reviewing-infrastructure#4): sibling plans held and not-held the same rows; a structured
    # counted_at hold is left out; a hand hold reads as held; read-only, exit 1 on any row; --area filters.
    repo, ws = build(tmp_path)
    for name, held in (("a/one", {"infra/x:2@t": {"verdict": "held", "why": "says it"},
                                  "lacking:infra/x:3@t": {"verdict": "not", "why": "lack"},
                                  "infra/x:4@t": {"verdict": "held", "why": "w", "counted_at": "a/two"}}),
                       ("a/two", {"infra/x:2@t": {"verdict": "not", "why": "G160 multi-clause"},
                                  "lacking:infra/x:3@t": {"verdict": "held", "why": "in other words"},
                                  "infra/x:4@t": {"verdict": "not", "why": "lack"}}),
                       ("a/three", {"short:infra/y:1": {"verdict": "not", "why": "short"}})):
        d = ws / "areas" / name
        d.mkdir(parents=True)
        (d / "held.json").write_text(json.dumps(held))
    (ws / "areas" / "a" / "two" / "held.json").write_text(json.dumps(
        {**json.loads((ws / "areas" / "a" / "two" / "held.json").read_text()),
         "hold:infra/x:6@t": {"verdict": "not", "why": "x"}}))
    (ws / "areas" / "a" / "three" / "hand_holds.json").write_text(json.dumps(
        {"hold:infra/x:6@t": {"speciality": "infra/x", "n": 6, "topic": "t", "why": "the rule says it"}}))
    before = sorted((p, p.stat().st_mtime_ns) for p in ws.rglob("*"))
    capsys.readouterr()
    code = run_gaps.main(["--check-verdicts", "--workspace", str(ws), "--repo", str(repo)])
    out = json.loads(capsys.readouterr().out)
    assert sorted((p, p.stat().st_mtime_ns) for p in ws.rglob("*")) == before
    rows = {(r["piece"], r["topic"]): r for r in out["check_verdicts"]}
    assert code == 1 and set(rows) == {("infra/x:2", "t"), ("infra/x:3", "t"), ("infra/x:6", "t")}, rows
    assert rows[("infra/x:2", "t")]["verdicts"] == [
        {"area": "a/one", "id": "infra/x:2@t", "verdict": "held", "why": "says it"},
        {"area": "a/two", "id": "infra/x:2@t", "verdict": "not", "why": "G160 multi-clause"}]
    assert {v["area"] for v in rows[("infra/x:3", "t")]["verdicts"]} == {"a/one", "a/two"}
    assert {v["area"] for v in rows[("infra/x:6", "t")]["verdicts"]} == {"a/two", "a/three"}
    capsys.readouterr()
    code = run_gaps.main(["--check-verdicts", "--workspace", str(ws), "--repo", str(repo), "--area", "a/three"])
    out = json.loads(capsys.readouterr().out)
    assert code == 1 and [r["piece"] for r in out["check_verdicts"]] == ["infra/x:6"], out
    (ws / "areas" / "a" / "two" / "held.json").write_text(json.dumps({}))
    (ws / "areas" / "a" / "three" / "hand_holds.json").unlink()
    capsys.readouterr()
    assert run_gaps.main(["--check-verdicts", "--workspace", str(ws), "--repo", str(repo)]) == 0


def test_check_verdicts_leaves_out_a_hold_whose_old_why_says_where_it_is_counted(tmp_path, capsys):
    # gapfix14 (G280c with G273a; cookbook/skills-and-agents building/llm-tooling:2): an older free-text why
    # "counted at <area>" is read as counted_at, so that hold is left out like a structured one.
    repo, ws = build(tmp_path)
    for name, held in (("a/one", {"infra/x:5@t": {"verdict": "held", "why": "counted at a/two, which owns the home"}}),
                       ("a/two", {"infra/x:5@t": {"verdict": "not", "why": "G160"}})):
        d = ws / "areas" / name
        d.mkdir(parents=True)
        (d / "held.json").write_text(json.dumps(held))
    capsys.readouterr()
    code = run_gaps.main(["--check-verdicts", "--workspace", str(ws), "--repo", str(repo)])
    out = json.loads(capsys.readouterr().out)
    assert code == 0 and out["check_verdicts"] == [], out


def test_a_held_row_marked_for_another_area_only_is_not_counted_and_its_not_never_moves_the_total(tmp_path, capsys):
    # gapfix14 (G284b, cookbook/skills-and-agents stayed 139 after three `not` -> `held`): the rows' sentence is
    # marked for another area only, so their `not` counted there, never here; `counted` said true. The flag now
    # predicts the total: a `not` on a counted row adds one, on an uncounted row none.
    repo, ws = build(tmp_path)
    f = ws / "areas" / AREA / "building-security.json"
    data = json.loads(f.read_text())
    data["marks"]["2"] = "reviewing/sec"
    f.write_text(json.dumps(data))
    run(repo, ws, capsys)
    rep = json.loads((ws / "areas" / AREA / "run_gaps.json").read_text())
    rows = {r["id"]: r for r in rep["held_by_wording"]}
    assert rows["building/security:2@authz"]["counted"] is False, rows["building/security:2@authz"]
    assert rows["building/security:1@authn"]["counted"] is True
    total = rep["measured_total"]
    for rid, delta in (("building/security:2@authz", 0), ("building/security:1@authn", 1)):
        assert _g13_mark(repo, ws, capsys, "--held", rid, "not", "--why", "lacking")[0] == 0
        run(repo, ws, capsys)
        now = json.loads((ws / "areas" / AREA / "run_gaps.json").read_text())
        assert now["measured_total"] == total + delta, (rid, now["measured_total"], total)
        total = now["measured_total"]


def test_a_not_on_a_row_whose_home_holds_the_sentence_never_reaches_topic_totals():
    # gapfix14 (G284b, implementing-data#5): `counted` false (L28) and a `not`: topic_totals follows the flag.
    def result(counted):
        return {"area": "a", "topics": [{"topic": "t2", "references": [], "own": {"held": 1, "lacking": 0},
                                         "building_marked_elsewhere": {"held": 0, "lacking": 0},
                                         "held": 1, "lacking": 0}], "home_measures": []}
    for counted, want in ((False, 0), (True, 1)):
        res = result(counted)
        run_gaps._not_held(res, {"speciality": "building/x", "n": 1, "topic": "t2", "counted": counted})
        assert [t["total"] for t in run_gaps.topic_totals(res)] == [want], (counted, res)


def test_an_r9_piece_and_its_topic_row_count_once_at_the_r9_row(tmp_path, capsys):
    # gapfix14 (G281a, implementing-testing#3): lacking:testing/test-adequacy:1@testing and its r9 row were the
    # same piece, both counted; the topic row now shows counted_at "r9" and the R9 row is the one that counts.
    repo, ws = build(tmp_path)
    _, before, _ = run(repo, ws, capsys)
    x = next(r for r in before["lacking_pieces"] if r["counted"] and r["speciality"] == "building/security")
    a = ws / "areas" / AREA
    (a / "gaps" / "new-compliance.json").write_text(json.dumps({
        "folder": "cookbook/guidelines/implementing/sec/compliance", "references": [
            {"file": str(a / "reference" / "building--security.txt"), "sentences": 1, "held": 0, "lacking": 1,
             "lacking_sentences": [x["text"]]}]}))
    _, after, _ = run(repo, ws, capsys)
    twins = [r for r in after["lacking_pieces"] if r["speciality"] == x["speciality"] and r["text"] == x["text"]]
    assert len(twins) > 1                               # the piece lacks at several topics: every row counts at R9
    for row in twins:
        assert (row["counted"], row["counted_at"], row["counted_by"]) == (
            False, "r9", after["r9_lacking"][0]["id"]), row
    assert after["measured_total"] == before["measured_total"] - len(twins) + 1, (
        after["measured_total"], before["measured_total"])
    assert x["id"] not in [r["id"] for r in after["non_home_lacking"]]


def test_missing_subjects_are_counted_beside_measured_total_never_inside_it(tmp_path, capsys):
    # gapfix14 (G286, planning-ui#5): a Missing subject has no source sentence, so no --lack row; its count is shown
    # beside measured_total (run, --check and the digest), never added to it.
    repo, ws = build(tmp_path)
    _, before, _ = run(repo, ws, capsys)
    assert before["missing_subjects"] == 0
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(plan.read_text() + "\n## Missing subjects\n\nWhat is missing.\n\n1. **Key escrow**: none.\n"
                    "   - a sub-bullet is no subject\n2. **Token binding**: none.\n\n## Overlaps\n\n- x\n")
    _, after, _ = run(repo, ws, capsys)
    assert (after["missing_subjects"], after["measured_total"]) == (2, before["measured_total"])
    code, chk, _ = run(repo, ws, capsys, "--check")
    assert chk["missing_subjects"] == 2, chk
    capsys.readouterr()
    run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--digest"])
    assert f"measured_total {before['measured_total']}; missing_subjects 2" in capsys.readouterr().out


def test_the_digest_names_every_row_behind_a_counted_rows_and_measured_total_difference(tmp_path, capsys):
    # gapfix14 (G283, implementing/concurrency 30 rows vs 27): a counted row that moves no figure (a `not` on a row
    # whose sentence is marked for another area only) is named with its why in the check and in the digest line.
    repo, ws = build(tmp_path)
    f = ws / "areas" / AREA / "building-security.json"
    data = json.loads(f.read_text())
    data["marks"]["2"] = "reviewing/sec"
    f.write_text(json.dumps(data))
    run(repo, ws, capsys)
    _g13_mark(repo, ws, capsys, "--held", "building/security:2@authz", "not", "--why", "lacking")
    run(repo, ws, capsys)
    code, chk, _ = run(repo, ws, capsys, "--check")
    differ = chk["counted_rows_differ"]
    assert [r["id"] for r in differ] == ["building/security:2@authz"], differ
    assert "another area" in differ[0]["why"]
    assert len(chk["counted_rows"]) - len(differ) == chk["measured_total"], chk
    capsys.readouterr()
    run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI),
                   "--check", "--digest"])
    line = capsys.readouterr().out.strip().splitlines()[-1]
    assert "counted_rows_differ 1 (building/security:2@authz:" in line, line


def test_the_first_check_prints_the_old_stated_figure_the_new_measured_one_and_the_breakdown(tmp_path, capsys):
    # gapfix14 (G300, implementing-data#10: 603 measured against a stated 337): the check and its digest line give
    # the plan's stated figure, the measured one, their difference and the counters that explain it.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    _g13_mark(repo, ws, capsys, "--held", "short:building/security:6", "not", "--why", "lacking")
    run(repo, ws, capsys)
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(plan.read_text() + "\n## Gaps\n\nThis area's gaps: 1\n")
    code, chk, _ = run(repo, ws, capsys, "--check")
    m = chk["measured_total"]
    fig = chk["figure_change"]
    assert fig == {"stated": 1, "measured": m, "difference": m - 1,
                   "counted_with_prior_verdict": chk["counted_with_prior_verdict"],
                   "counted_never_judged": chk["counted_never_judged"],
                   "verdict_changes": len(chk["verdict_changes"]),
                   "verdict_changes_delta": sum(r["total_delta"] for r in chk["verdict_changes"])}, fig
    capsys.readouterr()
    run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI),
                   "--check", "--digest"])
    line = capsys.readouterr().out.strip().splitlines()[-1]
    assert (f"stated 1 -> measured {m} ({m - 1:+d}: counted_with_prior_verdict {fig['counted_with_prior_verdict']}, "
            f"counted_never_judged {fig['counted_never_judged']}, verdict_changes {fig['verdict_changes']})") in line, line


def test_a_saved_report_view_older_than_a_hand_judgment_names_the_one_refresh_command(tmp_path, capsys):
    # gapfix14 (G291, late log "--digest does not rewrite run_gaps.json"): --digest without --check is a view of the
    # saved report (G122); when a hand lack or hand hold is newer, stderr names it and the exact command to refresh.
    repo, ws = build(tmp_path)
    run(repo, ws, capsys)
    a = ws / "areas" / AREA
    rp = a / "run_gaps.json"
    for name in ("hand_lacks.json", "hand_holds.json"):
        (a / name).write_text("{}")
        os.utime(rp, ((a / name).stat().st_mtime - 10,) * 2)
        capsys.readouterr()
        run_gaps.main(["--area", AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI), "--digest"])
        err = capsys.readouterr().err
        assert name in err and f"run_gaps.py --area {AREA} --workspace {ws} --repo {repo} --hints" in err, err
        (a / name).unlink()


def test_prose_naming_this_areas_gaps_without_a_figure_is_never_a_stated_line(tmp_path, capsys):
    # gapfix14 (G294, planning-networking#1, planning-testing#4): only a line giving the phrase a number states a
    # figure; prose and a wrapped line naming "this area's gaps" with no number after it are not flagged, and a
    # flagged line's why says what made it one.
    repo, ws = build(tmp_path)
    counted = run(repo, ws, capsys)[1]["measured_total"]
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(PLAN + f"\n## Gaps\n\nThis area's gaps: {counted}\n\nWith no speciality, this area's gaps come "
                    "from the subject.\nThey are not\nthis area's gaps, wherever lacking.\n")
    assert run(repo, ws, capsys, "--check")[1]["gap_total"] == []
    plan.write_text(PLAN + f"\n## Gaps\n\nThis area's gaps: {counted}\n\nCounted as this area's gaps: 5\n")
    [g] = run(repo, ws, capsys, "--check")[1]["gap_total"]
    assert g["form"] == "other" and "followed by a number" in g["why"], g


def test_a_lacking_home_measure_sentence_and_its_home_lacking_row_carry_the_text_and_pieces(tmp_path, capsys):
    # gapfix14 (G302, implementing-infrastructure#3, testing#5): a home_lacking row carried `text: null`, so the
    # sentence and its pieces were looked up by hand; a lacking home sentence now carries both.
    repo, ws = build(tmp_path)
    _backups(repo)
    (repo / "cookbook/guidelines/implementing/sec/backups/rules.md").write_text("- Encrypt every backup file.\n")
    _marked_extra(ws, 1, BACKUP)
    code, out, err = run(repo, ws, capsys, "--out", str(tmp_path / "scratch"), "--devteam", str(_devteam(tmp_path)))
    assert code == 0, err
    [s] = [x for m in out["home_measures"] for x in m["sentences"] if x["speciality"] == "building/extra"]
    assert s["verdict"] == "lacking" and s["text"] == BACKUP and s["pieces"], s
    [row] = [r for r in out["home_lacking"] if r["id"].startswith("home:building/extra:1@")]
    assert row["text"] == BACKUP and row["pieces"] == s["pieces"], row


def test_the_area_may_be_given_positionally_as_unmeasured_and_copy_check_take_it(tmp_path, capsys):
    # gapfix14 (G299, implementing-infrastructure#1, reviewing-internationalization#4): run_gaps alone refused a
    # positional area ("unrecognized arguments"); it now reads it as the other scripts do, and two areas refuse.
    repo, ws = build(tmp_path)
    _, want, _ = run(repo, ws, capsys)
    capsys.readouterr()
    assert run_gaps.main([AREA, "--workspace", str(ws), "--repo", str(repo), "--cookr-cli", str(CLI), "--keys"]) == 0
    assert json.loads(capsys.readouterr().out)["measured_total"] == want["measured_total"]
    with pytest.raises(SystemExit):
        run_gaps.main([AREA, "--area", "other/area", "--workspace", str(ws), "--repo", str(repo), "--keys"])
    assert "two areas" in capsys.readouterr().err
    with pytest.raises(SystemExit):
        run_gaps.main(["--help"])
    help_ = " ".join(capsys.readouterr().out.split())
    assert "except with --check-homes or --check-verdicts" in help_ and "keeps the rows touching it" in help_


def test_a_home_verdict_recorded_before_its_row_had_text_keeps_its_verdict(tmp_path):
    # gapfix14 (G302 must move no figure; shipping home:building/platform-windows:3@atomic-commits): a 1.4.42 home
    # row had no text, so its verdict was recorded with `text` null; the row now carries its text (G302). A pin the
    # verdict was recorded without is not checked, so the verdict stands; a recorded text that changed still resets.
    a = tmp_path / "area"
    a.mkdir()
    (a / "held.json").write_text(json.dumps({
        "home:x/y:3@t": {"verdict": "held", "why": "not its home", "text": None},
        "home:x/y:4@t": {"verdict": "held", "why": "not its home"},
        "home:x/y:5@t": {"verdict": "held", "why": "w", "text": "Old wording."}}))
    rows = [{"id": "home:x/y:3@t", "text": "Run lengthy work with async."},
            {"id": "home:x/y:4@t", "text": "Delete dead code."},
            {"id": "home:x/y:5@t", "text": "New wording."}]
    kept = [r["id"] for r in run_gaps._record(a, rows, ("text",), "home sentence")]
    assert kept == ["home:x/y:3@t", "home:x/y:4@t"], rows
    assert rows[2]["verdict_was"] == "held" and "verdict" not in rows[2]


def test_a_reset_why_names_the_rule_sentence_move_or_the_piece_text_gapfix15():
    # G304 (1.4.44): a verdict reset because rule_sentence moved says so, with both sentences; a changed piece
    # text says "piece text changed"; neither names the other's cause.
    row = {"text": "Pin it.", "topic_sentence": "T.", "topic_hash": "h", "rule_sentence": "Deny by default."}
    moved = run_gaps.verdict_reset({"text": "Pin it.", "topic_sentence": "T.", "topic_hash": "h",
                                    "rule_sentence": "Deny always."}, row)
    assert 'rule_sentence moved (was "Deny always.", now "Deny by default.")' in moved, moved
    assert "piece text changed" not in moved, moved
    changed = run_gaps.verdict_reset({"text": "Pin that.", "topic_sentence": "T.", "topic_hash": "h",
                                      "rule_sentence": "Deny by default."}, row)
    assert "piece text changed" in changed and "rule_sentence moved" not in changed, changed
    assert run_gaps.verdict_reset({"text": "Pin it.", "topic_sentence": "T.", "topic_hash": "h",
                                   "rule_sentence": "Deny by default."}, row) is None


def test_check_verdicts_compares_only_rows_of_one_id_kind_gapfix15(tmp_path, capsys):
    # G303 (1.4.44): the plain row and the lacking: row of one piece are different ids; a plain held and a
    # lacking: not never make a row, two areas judging the same id kind differently do.
    repo, ws = build(tmp_path)
    for name, held in (("a/one", {"sec/v:4@t": {"verdict": "held", "why": "w"},
                                  "lacking:sec/v:4@t": {"verdict": "not", "why": "l"},
                                  "home:sec/v:4@t": {"verdict": "held", "why": "h"},
                                  "hand:sec/v:4@t": {"verdict": "held", "why": "h"}}),
                       ("a/two", {"sec/v:4@t": {"verdict": "held", "why": "w"},
                                  "lacking:sec/v:4@t": {"verdict": "not", "why": "l"},
                                  "home:sec/v:4@t": {"verdict": "held", "why": "h"},
                                  "hand:sec/v:4@t": {"verdict": "not", "why": "h"}})):
        d = ws / "areas" / name
        d.mkdir(parents=True)
        (d / "held.json").write_text(json.dumps(held))
    capsys.readouterr()
    code = run_gaps.main(["--check-verdicts", "--workspace", str(ws), "--repo", str(repo)])
    out = json.loads(capsys.readouterr().out)
    assert code == 1 and [(r["piece"], [v["id"] for v in r["verdicts"]]) for r in out["check_verdicts"]] == [
        ("sec/v:4", ["hand:sec/v:4@t", "hand:sec/v:4@t"])], out
    (ws / "areas" / "a" / "two" / "held.json").write_text(json.dumps(
        {"sec/v:4@t": {"verdict": "held", "why": "w"}, "lacking:sec/v:4@t": {"verdict": "held", "why": "l"}}))
    (ws / "areas" / "a" / "one" / "held.json").write_text(json.dumps(
        {"sec/v:4@t": {"verdict": "not", "why": "w"}, "lacking:sec/v:4@t": {"verdict": "not", "why": "l"}}))
    capsys.readouterr()
    run_gaps.main(["--check-verdicts", "--workspace", str(ws), "--repo", str(repo)])
    out = json.loads(capsys.readouterr().out)
    # both kinds now differ across the areas: one row per kind, each naming only its own ids
    assert [(r["kind"], {v["id"] for v in r["verdicts"]}) for r in out["check_verdicts"]] == [
        ("lacking", {"lacking:sec/v:4@t"}), ("plain", {"sec/v:4@t"})], out
