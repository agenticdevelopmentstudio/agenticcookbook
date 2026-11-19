"""apply_second_check.py: stage 2's second check applied to research.json by script.

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import apply_second_check as asc  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "feature-flags"
TRIAL_SCORES = {  # what the trial's runner lowered by hand, from second-check.md's corrections
    "openfeature-default-required-no-throw": 72, "vendor-sdks-default-on-error": 68,
    "setup-may-fail-evaluation-may-not": 60, "openfeature-vendor-agnostic": 65,
    "sdks-cache-in-local-storage": 55, "store-no-downloaded-code": 70,
}


def trial_before(tmp: Path) -> tuple[Path, Path]:
    """The trial's feature-flags research and second check as they were before the hand edits."""
    art = tmp / "feature-flags"
    (art / "research").mkdir(parents=True)
    data = json.loads((FIXTURE / "research.json").read_text(encoding="utf-8"))
    for claim in data["claims"]:
        basis = claim["trust"]["basis"]
        if "Second check" in basis:
            claim["trust"]["basis"] = basis[: basis.index(" Second check")]
            claim["trust"]["score"] += 20
    (art / "research" / "research.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    check = tmp / "second-check.md"
    text = (FIXTURE / "second-check.md").read_text(encoding="utf-8")
    check.write_text(re.sub(r"(?m)^- correction:.*\n", "", text), encoding="utf-8")
    return art, check


def claims(art: Path) -> dict:
    data = json.loads((art / "research" / "research.json").read_text(encoding="utf-8"))
    return {c["id"]: c for c in data["claims"]}


def test_the_trials_partly_claims_are_lowered_to_the_scores_the_runner_set_by_hand(tmp_path):
    art, check = trial_before(tmp_path)
    report = asc.apply(art, check, "2026-11-16")
    after = claims(art)
    assert {c: after[c]["trust"]["score"] for c in TRIAL_SCORES} == TRIAL_SCORES
    assert sorted(report["refuted"]) == sorted(TRIAL_SCORES)
    # the agent wrote "result: confirmed" on all six; the rule makes them refuted
    assert sorted(report["result_disagrees"]) == sorted(TRIAL_SCORES)
    assert "Second check 2026-11-16: refuted" in after["vendor-sdks-default-on-error"]["trust"]["basis"]
    assert "lowered 88->68" in after["vendor-sdks-default-on-error"]["trust"]["basis"]
    assert {c["claim"] for c in report["corrections"]} == set(TRIAL_SCORES)
    assert check.read_text(encoding="utf-8").count("- correction:") == 6


def test_a_second_run_changes_nothing(tmp_path):
    art, check = trial_before(tmp_path)
    asc.apply(art, check, "2026-11-16")
    first = (art / "research" / "research.json").read_text(encoding="utf-8")
    report = asc.apply(art, check, "2026-11-16")
    assert (art / "research" / "research.json").read_text(encoding="utf-8") == first
    assert report["refuted"] == []
    assert len(report["corrections"]) == 6  # still listed for the write brief


def synthetic(tmp: Path, block: str, citations: list[dict], independence="multi-independent"):
    art = tmp / "t"
    (art / "research").mkdir(parents=True)
    claim = {"id": "c1", "question": "best-practice", "claim": "x", "quote": "q",
             "citations": citations, "source_type": "doc", "generated_by": "a", "query": "q",
             "trust": {"score": 80, "basis": "b."}, "independence": independence}
    (art / "research" / "research.json").write_text(json.dumps({"claims": [claim]}), encoding="utf-8")
    check = tmp / "second-check.md"
    check.write_text(f"# Second check: t\n\n## c1\n{block}", encoding="utf-8")
    return art, check


def cite(publisher: str) -> dict:
    return {"title": publisher, "publisher": publisher, "url": f"https://{publisher}.example"}


def test_a_citation_lacking_the_quote_is_dropped_and_independence_recomputed(tmp_path):
    block = ("- quote-found: yes\n- supports-claim: yes\n- citation 1: holds-quote\n"
             "- citation 2: lacks-quote\n- result: confirmed\n- note: n\n")
    art, check = synthetic(tmp_path, block, [cite("a"), cite("b")])
    report = asc.apply(art, check, "2026-11-16")
    claim = claims(art)["c1"]
    assert [c["publisher"] for c in claim["citations"]] == ["a"]
    assert claim["independence"] == "single"
    assert claim["trust"]["score"] == 80  # confirmed: no penalty
    assert report["dropped"] == [{"claim": "c1", "citation": "https://b.example"}]


def test_independence_is_never_raised(tmp_path):
    block = ("- quote-found: yes\n- supports-claim: yes\n- citation 1: holds-quote\n"
             "- citation 2: holds-quote\n- citation 3: lacks-quote\n- result: confirmed\n")
    art, check = synthetic(tmp_path, block, [cite("a"), cite("b"), cite("c")], "single")
    asc.apply(art, check, "2026-11-16")
    assert claims(art)["c1"]["independence"] == "single"


def test_no_citation_is_dropped_when_none_holds_the_quote(tmp_path):
    block = "- quote-found: no\n- supports-claim: no\n- citation 1: lacks-quote\n- result: refuted\n- note: gone\n"
    art, check = synthetic(tmp_path, block, [cite("a")])
    report = asc.apply(art, check, "2026-11-16")
    claim = claims(art)["c1"]
    assert len(claim["citations"]) == 1
    assert claim["trust"]["score"] == 40  # not found: -40
    assert report["result_disagrees"] == []


def test_an_unknown_claim_id_is_reported(tmp_path, capsys):
    art, check = synthetic(tmp_path, "- quote-found: yes\n- supports-claim: yes\n- result: confirmed\n", [cite("a")])
    check.write_text(check.read_text(encoding="utf-8").replace("## c1", "## nope"), encoding="utf-8")
    assert asc.main([str(art), str(check), "--date", "2026-11-16"]) == 2
    assert json.loads(capsys.readouterr().out)["unknown"] == ["nope"]


def test_cli_prints_json(tmp_path, capsys):
    art, check = trial_before(tmp_path)
    assert asc.main([str(art), str(check), "--date", "2026-11-16"]) == 0
    assert len(json.loads(capsys.readouterr().out)["refuted"]) == 6
    shutil.rmtree(art)


def test_claims_to_check_are_the_trials_38(tmp_path, capsys):
    """Every claim a contradicted or new verdict names, prior claims aside: the
    trial's runner listed 38 for feature-flags, and its second check has a block
    for each."""
    art = tmp_path / "feature-flags"
    (art / "research").mkdir(parents=True)
    shutil.copy(FIXTURE / "research.json", art / "research" / "research.json")
    ids = asc.to_check(art)
    assert len(ids) == 38 and len(set(ids)) == 38
    assert not [i for i in ids if i.endswith("-prior")]
    blocks = {b["id"] for b in asc.parse((FIXTURE / "second-check.md").read_text(encoding="utf-8"))}
    assert blocks == set(ids)
    assert asc.main([str(art), "--list"]) == 0
    assert capsys.readouterr().out.split() == ids
