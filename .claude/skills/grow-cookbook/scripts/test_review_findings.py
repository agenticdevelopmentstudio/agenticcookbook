"""review_findings.py: review rounds parsed, counted and routed to the owner.

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import review_findings as rf  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def read(*parts: str) -> str:
    return FIXTURES.joinpath(*parts).read_text(encoding="utf-8")


def test_the_trials_checked_notes_are_not_findings():
    review = rf.parse(read("feature-flags", "review-9.md"), 9)
    assert len(review["findings"]) == 1
    assert review["findings"][0]["id"] == "R9.1"
    assert review["findings"][0]["text"].startswith("`rules.md`, `typescript-localstorage-default`")
    assert len(review["checked"]) == 10
    assert review["verdict"] == "fail"


def test_a_not_reported_paragraph_ends_the_findings():
    review = rf.parse(read("feature-flags", "review-4.md"), 4)
    assert len(review["findings"]) == 5
    assert any("Version, `modified` and Change History" in c for c in review["checked"])


def test_a_finding_keeps_its_indented_sub_list():
    review = rf.parse(read("debug-mode", "review-1.md"))
    assert len(review["findings"]) == 12
    nine = review["findings"][8]["text"]
    assert "four rules have no defect line" in nine and "Fix: add one defect line for each." in nine


def review(findings: list[str], verdict: str, rulings: list[str] = (), checked: list[str] = (),
           lint: str = "lint: clean") -> str:
    out = ["# Review: t", "", "## Findings", ""] + [f"- {f}" for f in findings]
    out += ["", "## Checked", ""] + [f"- {c}" for c in checked]
    if rulings:
        out += ["", "## Rulings", ""] + [f"- {r}" for r in rulings]
    return "\n".join(out + ["", "## Lint", "", lint, "", f"verdict: {verdict}", ""])


def test_rounds_rulings_and_the_owner_route(tmp_path):
    (tmp_path / "review-1.md").write_text(review(["a is wrong", "b is wrong", "c is wrong"], "fail"))
    (tmp_path / "review-2.md").write_text(review(
        ["d is new"], "fail", ["R1.1: fixed", "R1.2: disputed-accepted — the claim says so", "R1.3: open — still MUST"]))
    status = rf.status(tmp_path)
    assert status["rounds"] == 2 and status["next"] == "write"
    assert [f["id"] for f in status["open"]] == ["R1.3", "R2.1"]
    (tmp_path / "review-3.md").write_text(review([], "fail", ["R1.3: open", "R2.1: fixed"]))
    status = rf.status(tmp_path)
    assert status["next"] == "owner"
    assert [f["id"] for f in status["open"]] == ["R1.3"]
    assert status["open"][0]["history"] == ["round 1: raised", "round 2: open — still MUST", "round 3: open"]
    (tmp_path / "integrate.md").write_text("# Integrate: t\n\n## For the owner\n\nnone\n\n## Step 3: cookr bump\nx\n")
    assert rf.to_owner(tmp_path)["added"] == 1
    text = (tmp_path / "integrate.md").read_text()
    owner = text[text.index("## For the owner"):text.index("## Step 3")]
    assert "**R1.3**" in owner and "c is wrong" in owner and "none" not in owner
    assert rf.to_owner(tmp_path)["added"] == 0  # not added twice


def test_a_pass_goes_to_integrate(tmp_path, capsys):
    (tmp_path / "review-1.md").write_text(review([], "pass", checked=["fine"]))
    assert rf.main(["status", str(tmp_path)]) == 0
    assert json.loads(capsys.readouterr().out)["next"] == "integrate"
    assert rf.to_owner(tmp_path)["added"] == 0
    assert not (tmp_path / "integrate.md").exists()


def test_a_bold_ruling_id_and_a_lone_none_bullet(tmp_path):
    # m1: the trial wrote `- **R1.1**: fixed` and `- none` under findings.
    (tmp_path / "review-1.md").write_text(review(["a is wrong"], "fail"))
    (tmp_path / "review-2.md").write_text(review(["none"], "pass", ["**R1.1**: fixed — done"]))
    status = rf.status(tmp_path)
    assert rf.rounds(tmp_path)[1]["findings"] == []
    assert status["open"] == [] and status["next"] == "integrate"
    (tmp_path / "review-2.md").write_text(review(["`none`"], "pass", ["**R1.1: fixed** — done"]))
    assert rf.status(tmp_path)["open"] == []


def test_the_lint_line_fails_closed():
    # Ruling (fix round 2): only the fixed last line of ## Lint counts.
    def errors(lint):
        return rf.parse(review(["x"], "fail", lint=lint))["lint_errors"]
    assert errors("[PASS] SCHEMA-1\n[WARN] W2: style\n\nlint: clean") == []
    assert errors("[FAIL] L4: no approved-by\n[FAIL] L5: x\n\nlint: fail 2") == ["lint: fail 2"]
    assert errors("[FAIL] L4: no approved-by") != []                       # no lint line
    assert errors("RESULT: NOT CLEAN — 2 failing checks.") != []           # prose, no lint line
    for bad in ("lint: CLEAN", "lint: fail", "lint: fail 0", "lint: clean, 1 warning", "`lint: clean`"):
        assert errors(bad) != [], bad                                      # malformed
    assert errors("lint: clean\n[FAIL] L4: after the line") != []          # not the last line
    no_section = "# Review: t\n\n## Findings\n\n- x\n\nverdict: fail\n"
    assert rf.parse(no_section)["lint_errors"] != []


def test_a_lint_error_at_the_cap_stops_the_topic_and_never_reaches_the_owner(tmp_path):
    # Ruling 3: a standing lint error is read from ## Lint; at the cap it stops.
    lint = "[FAIL] L4: missing approved-by\n\nlint: fail 1"
    for n in (1, 2):
        (tmp_path / f"review-{n}.md").write_text(review(["x"], "fail", lint=lint))
    assert rf.status(tmp_path)["next"] == "write"  # below the cap: the author fixes it
    (tmp_path / "review-3.md").write_text(review(["x"], "fail", lint=lint))
    status = rf.status(tmp_path)
    assert (status["next"], status["why"]) == ("stop", "a lint error stands at the round cap")
    (tmp_path / "integrate.md").write_text("# Integrate: t\n\n## For the owner\n\nnone\n")
    assert rf.to_owner(tmp_path)["added"] == 0
    (tmp_path / "review-3.md").write_text(review(["x"], "fail", lint="RESULT: NOT CLEAN"))
    assert rf.status(tmp_path)["next"] == "stop"  # an unreadable lint line is a lint error
    (tmp_path / "review-3.md").write_text(review(["x"], "fail", lint="[WARN] W2: style\n\nlint: clean"))
    assert rf.status(tmp_path)["next"] == "owner"


def test_a_pass_with_no_readable_lint_line_is_no_pass(tmp_path):
    # A missing or malformed lint line is a lint error: the round counts as failed.
    (tmp_path / "review-1.md").write_text(review([], "pass", lint="all clean"))
    status = rf.status(tmp_path)
    assert status["next"] == "write" and status["lint_errors"]


def lossless(tmp_path, n, items=("Lost sentence: \"a\"",)):
    (tmp_path / f"lossless-{n}.md").write_text(
        "# Lossless failure\n\n## Findings\n\n" + "".join(f"- {i}\n" for i in items))


def test_a_lossless_failure_opens_one_round_past_the_cap(tmp_path):
    # Ruling 1: the extra round rules on it; a pass goes back to stage 5.
    for n in (1, 2, 3):
        (tmp_path / f"review-{n}.md").write_text(review([], "pass" if n == 3 else "fail", ["R1.1: fixed"] if n > 1 else []))
    lossless(tmp_path, 3)
    status = rf.status(tmp_path)
    assert (status["next"], status["allowed_rounds"]) == ("write", 4)
    assert [f["id"] for f in status["open"]] == ["L3.1"]
    (tmp_path / "review-4.md").write_text(review([], "pass", ["L3.1: fixed — restored"]))
    status = rf.status(tmp_path)
    assert (status["next"], status["open"]) == ("integrate", [])


def test_a_failed_lossless_round_stops_the_topic_and_never_reaches_the_owner(tmp_path):
    for n in (1, 2, 3):
        (tmp_path / f"review-{n}.md").write_text(review([], "pass" if n == 3 else "fail"))
    lossless(tmp_path, 3)
    (tmp_path / "review-4.md").write_text(review([], "fail", ["L3.1: open — still lost"]))
    status = rf.status(tmp_path)
    assert (status["next"], status["why"]) == ("stop", "the round the lossless failure opened failed")
    (tmp_path / "integrate.md").write_text("# Integrate: t\n\n## For the owner\n\nnone\n")
    assert rf.to_owner(tmp_path)["added"] == 0


def test_a_second_lossless_failure_stops_the_topic(tmp_path):
    (tmp_path / "review-1.md").write_text(review([], "pass"))
    lossless(tmp_path, 1)
    (tmp_path / "review-2.md").write_text(review([], "pass", ["L1.1: fixed"]))
    assert rf.status(tmp_path)["next"] == "integrate"
    lossless(tmp_path, 2)
    status = rf.status(tmp_path)
    assert (status["next"], status["why"]) == ("stop", "a second lossless failure")


def test_a_routed_ruling_closes_a_finding(tmp_path):
    # G2: a finding handed to a sibling topic's integrate.md is ruled `routed`.
    assert "routed" in rf.RULINGS
    assert "`routed`: the finding belongs to a named sibling topic and was recorded in that sibling's write-brief.md if it has not passed stage 4, or in its integrate.md if it has" in " ".join(rf.__doc__.split())
    (tmp_path / "review-1.md").write_text(review(["a belongs to sibling x", "b is wrong"], "fail"))
    (tmp_path / "review-2.md").write_text(review(
        ["none"], "pass", ["R1.1: routed — recorded in x's integrate.md", "**R1.2**: fixed"]))
    parsed = rf.rounds(tmp_path)[1]["rulings"]
    assert parsed["R1.1"] == {"ruling": "routed", "reason": "recorded in x's integrate.md"}
    status = rf.status(tmp_path)
    assert status["open"] == [] and status["next"] == "integrate"


def test_owner_dedupes_only_within_its_own_section(tmp_path):
    # 1.4.10, N4 (rereview 2's input): a sibling's routed finding kept across a
    # restart carries the sibling's bold id **R1.3**; the topic's own new
    # R1.3 still reaches the owner, since `owner` looks for a recorded id only
    # inside `## For the owner`.
    import review_findings as rf
    import write_brief as wb
    t = tmp_path / "keys"
    t.mkdir()
    (t / "base.txt").write_text("x\n", encoding="utf-8")
    routed = ("## From storage's review\n\n"
              "- **R1.3**: the key-rotation rule contradicts storage/keys.\n")
    (t / "integrate.md").write_text("# Integrate: keys\n\n" + routed, encoding="utf-8")
    (t / "draft.md").write_text("d\n", encoding="utf-8")
    wb.restart(t)
    (t / "review-1.md").write_text(review(["a is wrong", "b is wrong", "NEW: the key-wrap rule drops the MUST NOT"],
                                          "fail"), encoding="utf-8")
    (t / "review-2.md").write_text(review([], "fail", ["R1.1: fixed", "R1.2: fixed", "R1.3: open"]),
                                   encoding="utf-8")
    (t / "review-3.md").write_text(review([], "fail", ["R1.3: open"]), encoding="utf-8")
    st = rf.status(t)
    assert st["next"] == "owner" and st["open"][0]["id"] == "R1.3"
    assert rf.to_owner(t)["added"] == 1
    text = (t / "integrate.md").read_text(encoding="utf-8")
    assert routed in text and "## For the owner\n" in text
    assert "NEW: the key-wrap rule" in text.split("## For the owner\n", 1)[1]
    # a second run of `owner` sees its own entry and adds nothing
    assert rf.to_owner(t)["added"] == 0
    assert (t / "integrate.md").read_text(encoding="utf-8") == text


def test_routed_keeps_a_findings_fenced_evidence():
    # 1.4.11, N6 (rereview 3's input): a fenced block nested in a routed
    # finding is its evidence; the owner item keeps it, verbatim.
    t = ("# Integrate: rows\nintegrated: 2026-11-16\n\n## From debug-mode's review\n\n"
         "- R1.5: artifact.json has an empty platforms list:\n"
         "  ```json\n  \"platforms\": []\n  ```\n"
         "  list the platforms its rules cover.\n")
    assert rf.routed(t) == [
        "from debug-mode's review: R1.5: artifact.json has an empty platforms list:\n"
        "  ```json\n  \"platforms\": []\n  ```\n"
        "list the platforms its rules cover."]
    # a fenced block with no finding before it is an item of its own
    assert rf.routed("## From a's review\n\n```\n## not a heading\n```\n- R1.2: x\n") == [
        "from a's review: ```\n## not a heading\n```", "from a's review: R1.2: x"]


def test_routed_continuations_stay_in_their_finding():
    # 1.4.11, N9 (rereview 3's input): a lazy (unindented) continuation and a
    # paragraph after a blank line stay part of their finding; only a new
    # top-level `- ` bullet starts another.
    t = "## From a's review\n\n- R1.1: first line\nlazy continuation\n- R1.2: x\n\n  second paragraph of R1.2\n"
    assert rf.routed(t) == [
        "from a's review: R1.1: first line lazy continuation",
        "from a's review: R1.2: x\n\nsecond paragraph of R1.2"]
    # Only `- ` starts a finding (the prompts write `- `): a `* ` line is
    # text of the finding before it, never lost and never a new item.
    assert rf.routed("## From a's review\n\n- R1.1: one\n* R1.2: two\n") == [
        "from a's review: R1.1: one * R1.2: two"]


def test_the_fence_pattern_is_defined_once():
    # 1.4.11, N8: `_FENCE` was defined twice.
    src = (Path(__file__).resolve().parent / "review_findings.py").read_text(encoding="utf-8")
    assert src.count("_FENCE = ") == 1
