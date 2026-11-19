"""Tests for write_brief.py: prompts filled from templates, the write brief, rounds."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import write_brief as wb  # noqa: E402

FIX = HERE / "fixtures"
REPO = "/repo"
PY = "/venv/bin/python"
ARTIFACT = "cookbook/guidelines/implementing/feature-management/feature-flags"
COOKR = f"PYTHONPATH={REPO}/skills/cookr/cli {PY} -P -m cookr -p {REPO}"


def common(**extra):
    return wb.common(REPO, PY, today="2026-11-16", **extra)


def test_every_prompt_carries_date_privacy_and_cookr_line():
    for name in wb.PROMPTS:
        values = common(artifact=ARTIFACT, topic="feature-flags", topic_dir="/t", kind="existing",
                        claims="- a", reviews="r", diff="d", round="2", lint_rule="", open="- R1.1: x",
                        base="abc", copies="", last_run="out", verdicts="v", refuted="r", dropped="d",
                        owner="o", frontmatter="f", max_rounds="3")
        text = wb.fill(name, values)
        assert "{{" not in text, name
        assert "2026-11-16" in text, name
        if name != "second-check":
            assert COOKR in text, name
    for name in ("research", "second-check"):
        assert wb.PRIVACY in wb.fill(name, common(artifact=ARTIFACT, topic_dir="/t", claims="- a"))


def test_unfilled_placeholder_is_an_error():
    with pytest.raises(wb.Unfilled) as e:
        wb.fill("research", common())
    assert "artifact" in str(e.value)


def test_research_prompt_strength_and_validate_line():
    text = wb.fill("research", common(artifact=ARTIFACT, topic_dir="/t"))
    assert "supported at the rule's stated strength" in text
    assert "Do not repeat trust scores" in text
    assert f"{COOKR} validate --research {ARTIFACT}" in text
    assert "takes the artifact folder" in text


def test_review_prompts_carry_the_rulings():
    criteria = (HERE / "prompts" / "criteria.md").read_text(encoding="utf-8")
    full = wb.fill("review-full", common(artifact=ARTIFACT, topic="ff", topic_dir="/t", max_rounds="3"))
    scoped = wb.fill("review-scoped", common(artifact=ARTIFACT, topic="ff", topic_dir="/t", max_rounds="3",
                                             reviews="r", diff="d", round="2", lint_rule="", open="- R1.1: x"))
    for text in (full, scoped):
        assert criteria.strip().replace("{{repo}}", REPO) in text
        assert "## Checked" in text and "verdict: pass" in text
        assert "is never a finding" in " ".join(text.split())
        assert "Only its wording is exempt" in text
        assert "citations are authoritative" in text
        assert "every instance" in text
    assert "## Rulings" in scoped and "fixed|disputed-accepted|routed|open" in scoped
    assert "Never ask to reverse a fix" in scoped


def _topic(tmp_path: Path, name: str = "feature-flags") -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    folder = repo / ARTIFACT
    (folder / "research").mkdir(parents=True)
    shutil.copy(FIX / name / "research.json", folder / "research" / "research.json")
    tdir = tmp_path / "topic"
    tdir.mkdir()
    if (FIX / name / "second-check.md").exists():
        shutil.copy(FIX / name / "second-check.md", tdir / "second-check.md")
    return repo, tdir


def test_write_brief_from_the_trial(tmp_path):
    repo, tdir = _topic(tmp_path)
    path = wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    text = path.read_text(encoding="utf-8")
    assert "{{" not in text
    assert (HERE / "prompts" / "criteria.md").read_text(encoding="utf-8").strip().replace(
        "{{repo}}", str(repo)) in text
    assert "the strength of the weakest claim it\n   cites" in text
    corrections = text.split("Second-check corrections, refuted (")[1].split("Second-check corrections, citation")[0]
    assert corrections.count("\n- ") == 6
    assert text.split("citation dropped (")[1].split("Owner list:")[0].strip().endswith("none")
    for cid in ("openfeature-default-required-no-throw", "vendor-sdks-default-on-error"):
        assert f"- {cid}:" in corrections or cid in corrections
    assert "- gate-all-features: contradicted (claims: gate-all-features-prior" in text
    assert f"{repo}/{ARTIFACT}/research/research.md" in text
    assert str(tdir / "owner-list.md") in text
    assert "`version`, `modified` and Change History are left" in text
    assert "lead-in" in text
    assert "spec-lists-flag-keys" in text.split("Owner list:")[1]


def _round(tdir: Path, review: str, draft: str = "draft\n") -> None:
    (tdir / "review.md").write_text(review, encoding="utf-8")
    (tdir / "draft.md").write_text(draft, encoding="utf-8")


def test_append_saves_rounds_and_findings(tmp_path):
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    _round(tdir, "# Review\n\n## Findings\n\n- one wrong\n- two wrong\n\n## Checked\n\n- fine\n\nverdict: fail\n",
           "draft one\n")
    (tdir / "disputes.md").write_text("- R1.2: claim x says otherwise\n", encoding="utf-8")
    assert wb.append(tdir)["round"] == 1
    assert (tdir / "review-1.md").exists() and (tdir / "draft-1.md").read_text() == "draft one\n"
    brief = (tdir / "write-brief.md").read_text(encoding="utf-8")
    assert "## Round 1 findings" in brief and "- R1.1: one wrong" in brief and "- R1.2: two wrong" in brief
    assert "- R1.2: claim x says otherwise" in brief
    assert "fine" not in brief.split("## Round 1 findings")[1]
    # idempotent: the same review is not a new round
    assert wb.append(tdir)["round"] == 1
    assert brief == (tdir / "write-brief.md").read_text(encoding="utf-8")


def test_append_refuses_a_fourth_round(tmp_path):
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    for n in (1, 2, 3):
        _round(tdir, f"## Findings\n\n- still wrong {n}\n\nverdict: fail\n", f"draft {n}\n")
        assert wb.append(tdir)["round"] == n
    _round(tdir, "## Findings\n\n- again\n\nverdict: fail\n", "draft 4\n")
    with pytest.raises(wb.TooManyRounds):
        wb.append(tdir)


def test_review_prompt_round_one_is_full_and_round_two_scoped(tmp_path):
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    (tdir / "draft.md").write_text("a\nb\n", encoding="utf-8")
    first = wb.review(tdir, str(repo), PY, ARTIFACT, today="2026-11-16")
    assert first["round"] == 1 and "a full review" in first["prompt"].read_text()
    _round(tdir, "## Findings\n\n- b is wrong\n\nverdict: fail\n", "a\nb\n")
    wb.append(tdir)
    (tdir / "draft.md").write_text("a\nc\n", encoding="utf-8")
    second = wb.review(tdir, str(repo), PY, ARTIFACT, today="2026-11-16")
    text = second["prompt"].read_text()
    assert second["round"] == 2 and "scoped re-review" in text
    assert "- R1.1: b is wrong" in text
    assert str(tdir / "review-1.md") in text
    diff = second["diff"].read_text()
    assert "-b" in diff and "+c" in diff


def test_cli_prompt(tmp_path, capsys):
    rc = wb.main(["prompt", "second-check", "--repo", REPO, "--cookr-py", PY, "--today", "2026-11-16",
                  "--set", f"artifact={ARTIFACT}", "--set", "claims=- a-claim"])
    assert rc == 0
    assert "- a-claim" in capsys.readouterr().out
    assert wb.main(["prompt", "second-check", "--repo", REPO, "--cookr-py", PY]) == 2


def test_the_must_bar_has_one_source_criteria(tmp_path):
    # ruling 2: which claims cannot carry MUST is stated once, in criteria.md
    template = (HERE / "prompts" / "write-brief.md").read_text(encoding="utf-8")
    assert "cannot carry MUST" not in template
    criteria = (HERE / "prompts" / "criteria.md").read_text(encoding="utf-8")
    assert "cannot carry MUST" in criteria
    repo, tdir = _topic(tmp_path)
    text = wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16").read_text(encoding="utf-8")
    assert text.count("cannot carry MUST") == 1


def test_a_dropped_citation_is_not_listed_as_refuted(tmp_path):
    repo, tdir = _topic(tmp_path)
    (tdir / "second-check.md").write_text(
        "## kept-claim\n- quote-found: yes\n- supports-claim: yes\n- citation 1: holds\n"
        "- citation 2: lacks\n- result: confirmed\n- correction: citation 2 dropped (lacks the quote)\n\n"
        "## weak-claim\n- quote-found: yes\n- supports-claim: partly\n- result: refuted\n"
        "- correction: refuted (supports-claim partly)\n", encoding="utf-8")
    refuted, dropped = wb._corrections(tdir)
    assert refuted == "- weak-claim: refuted (supports-claim partly)"
    assert dropped == "- kept-claim: citation 2 dropped (lacks the quote)"


def test_the_two_ruled_prompt_sentences_are_pinned():
    # m7: M25 and M26 deleted these with every test passing.
    second = " ".join(wb.fill("second-check", common(artifact=ARTIFACT, claims="- c")).split())
    assert "`partly` is not `yes`: a claim the quote only partly supports is refuted." in second
    scoped = " ".join(wb.fill("review-scoped", common(artifact=ARTIFACT, topic="ff", topic_dir="/t", max_rounds="3",
                                                      reviews="r", diff="d", round="2", lint_rule="", open="- R1.1: x")).split())
    assert ("Raise a new finding only on text the diff shows changed this round, or for a factual error "
            "against a cited claim (name the claim).") in scoped
    # 1.4.11: the stage detail moved from SKILL.md to its reference files
    def ref(name):
        return " ".join((HERE.parent / "references" / name).read_text(encoding="utf-8").split())
    assert "`partly` is not `yes`" in ref("stage-2.md")
    assert "raises a new finding only on text the diff shows changed or for a factual error" in ref("stage-4.md")


def test_review_prompts_end_lint_with_the_fixed_line():
    for name in ("review-full", "review-scoped"):
        text = " ".join(wb.fill(name, common(artifact=ARTIFACT, topic="ff", topic_dir="/t", max_rounds="3",
                                             reviews="r", diff="d", round="2", lint_rule="", open="- x")).split())
        assert "as the section's last line, exactly `lint: clean` (no lint error) or `lint: fail <n>`" in text, name
        assert "[FAIL]" not in text, name


REPORT = {"failures": [{"sentence": "Flags MUST default off.", "to": ["rules"], "reason": "judged fail by j: lost"},
                       {"sentence": None, "to": None, "reason": "copy x is not folded"}],
          "missing": ["Remove a flag within 30 days."]}


def test_a_lossless_failure_is_recorded_as_open_findings_and_opens_one_round_past_the_cap(tmp_path, capsys):
    # Ruling 1: a script records it, the next scoped review rules on it.
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    for n in (1, 2, 3):
        _round(tdir, f"## Findings\n\n- wrong {n}\n\nverdict: {'pass' if n == 3 else 'fail'}\n", f"draft {n}\n")
        wb.append(tdir)
    (tmp_path / "run.json").write_text(json.dumps(REPORT), encoding="utf-8")
    assert wb.main(["lossless", str(tdir), "--report", str(tmp_path / "run.json")]) == 0
    assert json.loads(capsys.readouterr().out)["findings"] == 3
    brief = (tdir / "write-brief.md").read_text(encoding="utf-8")
    section = brief.split("## Lossless failure after round 3")[1]
    assert "- L3.1: Lost sentence, accounted for nowhere: \"Remove a flag within 30 days.\"" in section
    assert "- L3.2: Lossless failure: \"Flags MUST default off.\" (moved to ['rules']): judged fail by j: lost" in section
    assert "- L3.3: Lossless failure: copy x is not folded" in section
    assert wb.record_lossless(tdir, REPORT)["new"] is False  # the same report twice changes nothing
    assert brief == (tdir / "write-brief.md").read_text(encoding="utf-8")
    (tdir / "draft.md").write_text("restored\n", encoding="utf-8")
    fourth = wb.review(tdir, str(repo), PY, ARTIFACT, today="2026-11-16")
    text = fourth["prompt"].read_text()
    assert fourth["round"] == 4 and "round 4 of at most 4" in text and "- L3.1: Lost sentence" in text
    _round(tdir, "## Findings\n\nnone\n\n## Rulings\n\n- L3.1: fixed\n- L3.2: fixed\n- L3.3: fixed\n\nverdict: pass\n",
           "restored\n")
    assert wb.append(tdir)["round"] == 4
    _round(tdir, "## Findings\n\n- more\n\nverdict: fail\n", "draft 5\n")
    with pytest.raises(wb.TooManyRounds):
        wb.append(tdir)


def test_a_lossless_report_with_no_failure_is_refused(tmp_path):
    with pytest.raises(wb.NoFailure):
        wb.record_lossless(tmp_path, {"failures": [], "missing": []})


def _lint_round(tdir, lint: str, verdict: str = "fail") -> dict:
    _round(tdir, f"## Findings\n\n- one wrong\n\n## Lint\n\n{lint}\n\nverdict: {verdict}\n", "draft\n")
    return wb.append(tdir)


def test_a_failed_lint_reaches_the_author_as_findings_to_fix(tmp_path):
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    _lint_round(tdir, "[FAIL] FM-02: summary over 160 characters\n[WARN] W1: style\n\nlint: fail 1")
    section = (tdir / "write-brief.md").read_text(encoding="utf-8").split("## Round 1 findings")[1]
    assert "Lint failed (`lint: fail 1`)" in section and "fix each lint error" in section
    assert "[FAIL] FM-02: summary over 160 characters" in section and "[WARN] W1: style" in section
    assert "verdict: fail" not in section.split("Lint failed")[1]


def test_a_missing_or_malformed_lint_line_is_the_reviewers_fault(tmp_path):
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    _lint_round(tdir, "RESULT: CLEAN", verdict="pass")
    brief = (tdir / "write-brief.md").read_text(encoding="utf-8")
    section = brief.split("## Round 1 findings")[1]
    assert "the reviewer's" in section and "Leave the draft unchanged on lint grounds" in section
    assert "RESULT: CLEAN" in section  # the reason names the line read
    (tdir / "draft.md").write_text("draft\nmore\n", encoding="utf-8")
    raw = wb.review(tdir, str(repo), PY, ARTIFACT, today="2026-11-16")["prompt"].read_text()
    # n7: the rule is its own paragraph, one blank line on each side.
    assert "A lint WARN is not an error.\n\nRound 1's review did not end `## Lint`" in raw
    assert "a missing or malformed one fails the round.\n\nWrite " in raw
    prompt = " ".join(raw.split())
    assert ("Round 1's review did not end `## Lint` with the lint line. End `## Lint` with exactly "
            "`lint: clean` or `lint: fail <n>` as its last line") in prompt
    # a review with no ## Lint section at all
    _round(tdir, "## Findings\n\n- two wrong\n\nverdict: fail\n", "draft\nmore\n")
    wb.append(tdir)
    section = (tdir / "write-brief.md").read_text(encoding="utf-8").split("## Round 2 findings")[1]
    assert "no `## Lint` section" in section and "Leave the draft unchanged on lint grounds" in section


def test_a_clean_lint_adds_nothing_and_restates_nothing(tmp_path):
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    _lint_round(tdir, "lint: clean")
    section = (tdir / "write-brief.md").read_text(encoding="utf-8").split("## Round 1 findings")[1]
    assert "lint" not in section.lower()
    (tdir / "draft.md").write_text("draft\nmore\n", encoding="utf-8")
    prompt = wb.review(tdir, str(repo), PY, ARTIFACT, today="2026-11-16")["prompt"].read_text()
    assert "did not end `## Lint`" not in prompt
    assert "A lint WARN is not an error.\n\nWrite " in prompt  # n7: the slot leaves no stray line


def test_a_lint_report_holding_a_fence_stays_inside_the_briefs_fence(tmp_path):
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    report = ["```", "[FAIL] FM-02: x", "```", "", "lint: fail 1"]
    _lint_round(tdir, "\n".join(report))
    lines = (tdir / "write-brief.md").read_text(encoding="utf-8").split("Lint failed")[1].splitlines()
    opening = next(i for i, l in enumerate(lines) if l.startswith("```"))
    fence = lines[opening]
    assert set(fence) == {"`"} and len(fence) >= 4
    closing = lines.index(fence, opening + 1)
    assert lines[opening + 1:closing] == report

    # a run of four or more backticks inside: the fence is one longer
    assert wb._fence(["`````", "x ```` y"]) == "``````"
    assert wb._fence(["plain"]) == "````"


def _cli(cwd: Path, *args: str, env: dict | None = None) -> str:
    import os
    import subprocess
    r = subprocess.run([sys.executable, str(HERE / "write_brief.py"), *args], cwd=cwd,
                       capture_output=True, text=True, check=True, env={**os.environ, **(env or {})})
    return r.stdout


def test_relative_repo_and_cookr_py_name_the_same_files_as_absolute_ones(tmp_path):
    # The prompts carry --repo and --cookr-py to a subagent that runs elsewhere:
    # a relative path given from another cwd is written out absolute.
    repo, tdir = _topic(tmp_path)
    py = tmp_path / "venv" / "bin" / "python"
    py.parent.mkdir(parents=True)
    py.write_text("", encoding="utf-8")
    other = tmp_path / "elsewhere"
    other.mkdir()
    prompt = ["prompt", "author", "--set", f"artifact={ARTIFACT}", "--set", f"topic_dir={tdir}", "--today", "2026-11-16"]
    absolute = _cli(other, *prompt, "--repo", str(repo), "--cookr-py", str(py))
    relative = _cli(tmp_path, *prompt, "--repo", "repo", "--cookr-py", "venv/bin/python")
    assert relative == absolute and f"-p {repo}" in relative
    assert _cli(tmp_path, *prompt, "--repo", "repo", "--cookr-py", "python3") == absolute.replace(str(py), "python3")
    write = ["write", "topic", "--artifact", ARTIFACT, "--today", "2026-11-16"]
    _cli(other, *write[:1], str(tdir), *write[2:], "--repo", str(repo), "--cookr-py", str(py))
    first = (tdir / "write-brief.md").read_text(encoding="utf-8")
    for f in ("write-brief.md", "owner-list.md", "base.txt"):
        (tdir / f).unlink(missing_ok=True)
    _cli(tmp_path, *write, "--repo", "repo", "--cookr-py", "venv/bin/python")
    assert (tdir / "write-brief.md").read_text(encoding="utf-8") == first
    # review, round 1 (the full prompt) and round 2 (the scoped one)
    review = ["--artifact", ARTIFACT, "--today", "2026-11-16"]
    for n in (1, 2):
        _cli(other, "review", str(tdir), *review, "--repo", str(repo), "--cookr-py", str(py))
        absolute = (tdir / "review-prompt.md").read_text(encoding="utf-8")
        _cli(tmp_path, "review", "topic", *review, "--repo", "repo", "--cookr-py", "venv/bin/python")
        assert (tdir / "review-prompt.md").read_text(encoding="utf-8") == absolute, n
        assert cookr_of(repo, py) in absolute and ("This is round 2 of" in absolute) == (n == 2), n
        _round(tdir, "## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n", "draft\n")
        wb.append(tdir)
        (tdir / "draft.md").write_text("draft\nchanged\n", encoding="utf-8")


def cookr_of(repo, py) -> str:
    return f"PYTHONPATH={repo}/skills/cookr/cli {py} -P -m cookr -p {repo}"


def test_a_tilde_path_is_expanded_before_it_is_made_absolute(tmp_path):
    # A quoted `~/...` (or a COOKR_PY set in quotes) reaches the script unexpanded.
    home = tmp_path / "home"
    repo = home / "repo"
    repo.mkdir(parents=True)
    other = tmp_path / "elsewhere"
    other.mkdir()
    prompt = ["prompt", "author", "--set", f"artifact={ARTIFACT}", "--set", "topic_dir=/t", "--today", "2026-11-16"]
    absolute = _cli(other, *prompt, "--repo", str(repo), "--cookr-py", str(home / "x" / "python"))
    env = {"HOME": str(home)}
    assert _cli(other, *prompt, "--repo", "~/repo", "--cookr-py", "~/x/python", env=env) == absolute
    assert _cli(other, *prompt, "--repo", "~/repo", env={**env, "COOKR_PY": "~/x/python"}) == absolute
    assert cookr_of(repo, home / "x" / "python") in absolute and "~/repo" not in absolute and "~/x" not in absolute
    # a topic dir given as ~/... is the same dir
    tdir = home / "topic"
    tdir.mkdir()
    out = _cli(other, "review", "~/topic", "--artifact", ARTIFACT, "--today", "2026-11-16",
               "--repo", "~/repo", "--cookr-py", "~/x/python", env=env)
    assert (tdir / "review-prompt.md").is_file() and str(tdir) in out


_BARE = __import__("re").compile(r"(?<![\w/.:{}-])(?:tbd|cookbook|guide)/")


def test_no_filled_prompt_names_a_repo_path_without_the_repo():
    # Every path into the cookbook is {{repo}}/...; the only bare ones allowed
    # are arguments to the cookr line, which carries `-p <repo>`, and git
    # tree paths (`<rev>:<path>`).
    import re
    for name in wb.PROMPTS:
        values = common(artifact=ARTIFACT, topic="feature-flags", topic_dir="/t", kind="existing",
                        claims="- a", reviews="r", diff="d", round="2", lint_rule="", open="- R1.1: x",
                        base="abc", copies="", last_run="out", verdicts="v", refuted="r", dropped="d",
                        owner="o", frontmatter="f", max_rounds="3")
        for no, line in enumerate(wb.fill(name, values).splitlines(), 1):
            line = re.sub(re.escape(COOKR) + r"[^`]*", "", line)
            assert not _BARE.search(line), f"{name}:{no}: {line}"


def test_write_refuses_a_rerun_once_a_round_or_lossless_failure_is_recorded(tmp_path, capsys):
    # G1: `write` rebuilds write-brief.md and would drop `## Round <N> findings`
    # and `## Lossless failure after round <N>`; later rounds run nothing.
    repo, tdir = _topic(tmp_path)
    args = ["write", str(tdir), "--repo", str(repo), "--cookr-py", PY, "--artifact", ARTIFACT,
            "--today", "2026-11-16"]
    assert wb.main(args) == 0
    _round(tdir, "## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n")
    wb.append(tdir)
    brief = (tdir / "write-brief.md").read_text(encoding="utf-8")
    capsys.readouterr()
    assert wb.main(args) == 4
    err = capsys.readouterr().err
    assert "review-1.md" in err and "--restart" in err and len(err.strip().splitlines()) == 1
    assert (tdir / "write-brief.md").read_text(encoding="utf-8") == brief
    # a lossless failure alone (before any review round) refuses it too
    repo2, tdir2 = _topic(tmp_path / "two")
    assert wb.main(["write", str(tdir2), *args[2:]]) == 0
    wb.record_lossless(tdir2, REPORT)
    brief2 = (tdir2 / "write-brief.md").read_text(encoding="utf-8")
    capsys.readouterr()
    assert wb.main(["write", str(tdir2), *args[2:]]) == 4
    assert "lossless-0.md" in capsys.readouterr().err
    assert (tdir2 / "write-brief.md").read_text(encoding="utf-8") == brief2


def test_a_lossless_round_author_cites_what_it_adds(tmp_path):
    # G4: a lost sentence carried into a rule adds no word its cited claims do
    # not cover; one no cited claim can cover is disputed instead.
    values = common(artifact=ARTIFACT, topic_dir="/t")
    author = " ".join(wb.fill("author", values).split())
    for text in (author,):
        assert "every word added to the rule must be covered by a claim the rule cites" in text
        assert "add the claim to its citations, at the strength the claims allow" in text
        assert "disputed in disputes.md instead of added uncovered" in text
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    wb.record_lossless(tdir, REPORT)
    section = " ".join((tdir / "write-brief.md").read_text(encoding="utf-8")
                       .split("## Lossless failure after round 0")[1].split())
    assert "every word added to the rule must be covered by a claim the rule cites" in section
    assert "add the claim to its citations, at the strength the claims allow" in section
    assert "disputed in disputes.md instead of added uncovered" in section


def test_the_scoped_review_allows_a_routed_ruling():
    # G2: a finding that belongs to a sibling topic is ruled `routed`.
    scoped = " ".join(wb.fill("review-scoped", common(artifact=ARTIFACT, topic="ff", topic_dir="/t",
                                                      max_rounds="3", reviews="r", diff="d", round="2",
                                                      lint_rule="", open="- R1.1: x")).split())
    assert "fixed|disputed-accepted|routed|open" in scoped
    assert "`routed`: the finding belongs to a named sibling topic and was recorded in that sibling's write-brief.md if it has not passed stage 4, or in its integrate.md if it has" in scoped


def test_write_restart_moves_the_earlier_run_aside_and_starts_again_at_round_one(tmp_path, capsys):
    # Fix round 1: stage 5 sends a research finding back to stage 2; stage 3
    # then runs `write --restart`, which keeps the earlier run in run-<k>/.
    import review_findings as rf
    repo, tdir = _topic(tmp_path)
    args = ["write", str(tdir), "--repo", str(repo), "--cookr-py", PY, "--artifact", ARTIFACT,
            "--today", "2026-11-16"]
    assert wb.main(args) == 0
    for n in (1, 2):
        (tdir / "draft.md").write_text(f"draft {n}\n", encoding="utf-8")
        wb.review(tdir, str(repo), PY, ARTIFACT, today="2026-11-16")
        _round(tdir, f"## Findings\n\n- wrong {n}\n\n## Lint\n\nlint: clean\n\nverdict: fail\n", f"draft {n}\n")
        wb.append(tdir)
    wb.record_lossless(tdir, REPORT)
    moved = sorted(p.name for p in tdir.glob("*-[0-9]*.md"))
    assert moved == ["diff-2.md", "draft-1.md", "draft-2.md", "lossless-2.md", "review-1.md", "review-2.md"]
    assert rf.status(tdir)["rounds"] == 2 and rf.allowed_rounds(tdir) == 4
    assert wb.main([*args, "--restart"]) == 0
    run = tdir / "run-1"
    # 1.4.7, G5: the unnumbered files the stages wrote go too
    whole = sorted([*moved, "draft.md", "owner-list.md", "review-prompt.md", "review.md"])
    assert sorted(p.name for p in run.iterdir()) == whole
    assert not list(tdir.glob("*-[0-9]*.md"))
    brief = (tdir / "write-brief.md").read_text(encoding="utf-8")
    assert "## Round 1 findings" not in brief and "## Lossless failure" not in brief
    # status reads only the top level: the round count starts again
    status = rf.status(tdir)
    assert status["rounds"] == 0 and status["open"] == [] and status["next"] == "review"
    assert rf.allowed_rounds(tdir) == 3
    assert wb.review(tdir, str(repo), PY, ARTIFACT, today="2026-11-16")["round"] == 1
    # a second restart takes the next free number; without the flag it refuses
    _round(tdir, "## Findings\n\n- again\n\n## Lint\n\nlint: clean\n\nverdict: fail\n")
    wb.append(tdir)
    assert wb.main(args) == 4
    assert wb.main([*args, "--restart"]) == 0
    assert sorted(p.name for p in (tdir / "run-2").iterdir()) == ["draft-1.md", "draft.md", "owner-list.md",
                                                                  "review-1.md", "review-prompt.md", "review.md"]
    assert sorted(p.name for p in run.iterdir()) == whole


def test_write_restart_moves_disputes_aside_with_the_old_run(tmp_path):
    # Fix round 2 ruling: disputes.md's ids belong to the old run.
    repo, tdir = _topic(tmp_path)
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    _round(tdir, "## Findings\n\n- one\n- two\n\n## Lint\n\nlint: clean\n\nverdict: fail\n")
    old = "- R1.2: claim x says otherwise"
    (tdir / "disputes.md").write_text(old + "\n", encoding="utf-8")
    wb.append(tdir)
    assert old in (tdir / "write-brief.md").read_text(encoding="utf-8")
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16", restart_run=True)
    assert (tdir / "run-1" / "disputes.md").read_text(encoding="utf-8") == old + "\n"
    assert not (tdir / "disputes.md").exists()
    assert old not in (tdir / "write-brief.md").read_text(encoding="utf-8")
    # the new run's first round lists none of the old dispute lines
    _round(tdir, "## Findings\n\n- new one\n\n## Lint\n\nlint: clean\n\nverdict: fail\n", "new draft\n")
    assert wb.append(tdir)["round"] == 1
    assert old not in (tdir / "write-brief.md").read_text(encoding="utf-8")


def test_write_restart_reads_everything_before_it_moves_anything(tmp_path, capsys):
    # Fix round 3: a restart whose research cannot be read moves nothing.
    repo, tdir = _topic(tmp_path)
    args = ["write", str(tdir), "--repo", str(repo), "--cookr-py", PY, "--artifact", ARTIFACT,
            "--today", "2026-11-16"]
    assert wb.main(args) == 0
    _round(tdir, "## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n")
    (tdir / "disputes.md").write_text("- R1.1: no\n", encoding="utf-8")
    wb.append(tdir)
    before = {p.name: p.read_bytes() for p in tdir.iterdir()}
    research = repo / ARTIFACT / "research" / "research.json"
    research.unlink()
    capsys.readouterr()
    assert wb.main([*args, "--restart"]) not in (0, None)
    err = capsys.readouterr().err
    assert "research.json" in err and len(err.strip().splitlines()) == 1
    assert {p.name: p.read_bytes() for p in tdir.iterdir()} == before
    assert not list(tdir.glob("run-*"))
    research.write_text("{not json", encoding="utf-8")   # malformed: the same
    assert wb.main([*args, "--restart"]) not in (0, None)
    assert {p.name: p.read_bytes() for p in tdir.iterdir()} == before
    # nothing to move: no run-<k>/ is made
    empty = tmp_path / "empty"
    empty.mkdir()
    assert wb.restart(empty) is None and not list(empty.glob("run-*"))


FROM = ("## From debug-mode's review\n\n- R1.2 (debug-mode): rule x here contradicts debug-mode's "
        "rule y; reconcile.\n  - a continuation line\n")
FROM2 = "## From logging's review\n\n- R2.1 (logging): name the log level.\n"


def test_write_keeps_the_from_sections_a_sibling_routed_here(tmp_path):
    # Fix round 3 ruling: `## From <topic>'s review` sections survive `write`,
    # verbatim, at the end of the rebuilt brief.
    repo, tdir = _topic(tmp_path)
    # a first write: the orchestrator appended to a brief before this topic's stage 3
    (tdir / "write-brief.md").write_text(FROM + "\n" + FROM2, encoding="utf-8")
    text = wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16").read_text(encoding="utf-8")
    assert text.startswith("# Write brief: ")
    assert text.endswith("\n" + FROM + "\n" + FROM2)
    # --restart: the old run's round sections go, the From sections stay
    _round(tdir, "## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n")
    wb.append(tdir)
    brief = (tdir / "write-brief.md").read_text(encoding="utf-8")
    assert "## Round 1 findings" in brief and FROM in brief and FROM2 in brief
    text = wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16",
                    restart_run=True).read_text(encoding="utf-8")
    assert "## Round 1 findings" not in text
    assert text.endswith("\n" + FROM + "\n" + FROM2)
    assert text.count("## From debug-mode's review") == 1


FENCED = ("## From ui's review\n\n- R1.3 (ui): the rule's example is wrong:\n\n```md\n## x\n## Round 9 findings\n```\n\n"
          "~~~~\n## y\n```\n## still inside the tilde fence\n~~~~\n- R1.4 (ui): after the fences.\n")


def test_a_fenced_heading_line_neither_ends_nor_starts_a_from_section(tmp_path):
    # Fix round 4: a `## ` line inside a ``` or ~~~ fence is no heading.
    repo, tdir = _topic(tmp_path)
    other = "## Notes\n\n```\n## From fake's review\n```\n"
    (tdir / "write-brief.md").write_text(FENCED + "\n" + other, encoding="utf-8")
    text = wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16").read_text(encoding="utf-8")
    assert text.endswith("\n" + FENCED)
    assert "fake's review" not in text


def _owner_rounds(tdir, third):
    """Three failed rounds whose third finding, `third`, is open at round 3:
    `next: owner`, its id R1.3."""
    from test_review_findings import review as rv
    for name in ("review-1.md", "review-2.md", "review-3.md"):
        (tdir / name).unlink(missing_ok=True)
    (tdir / "review-1.md").write_text(rv(["a is wrong", "b is wrong", third], "fail"), encoding="utf-8")
    (tdir / "review-2.md").write_text(rv([], "fail", ["R1.1: fixed", "R1.2: fixed", "R1.3: open"]),
                                      encoding="utf-8")
    (tdir / "review-3.md").write_text(rv([], "fail", ["R1.3: open"]), encoding="utf-8")


def test_write_restart_keeps_only_routed_findings_in_integrate_md(tmp_path):
    # 1.4.9, fix round 2 (N1): a sibling's routed finding (`## From <sibling>'s
    # review`) stays at the top level; the stopped run's own `## For the owner`
    # and its `integrated:` line go only into run-<k>/integrate.md, since round
    # ids restart per run.
    import review_findings as rf
    tdir = tmp_path / "keys"
    tdir.mkdir()
    (tdir / "base.txt").write_text("abc\n", encoding="utf-8")
    _owner_rounds(tdir, "OLD: the rotation period is unsourced")
    assert rf.status(tdir)["next"] == "owner"
    routed = ("## From storage's review\n\n"
              "- R2.3: the key-rotation rule contradicts storage/keys.\n")
    (tdir / "integrate.md").write_text("# Integrate: keys\n\n" + routed, encoding="utf-8")
    assert rf.to_owner(tdir)["added"] == 1
    with (tdir / "integrate.md").open("a", encoding="utf-8") as f:
        f.write("\nintegrated: 2026-11-15\n")
    stopped = (tdir / "integrate.md").read_text(encoding="utf-8")
    assert "**R1.3**" in stopped and "OLD" in stopped
    run = wb.restart(tdir)
    assert (run / "integrate.md").read_text(encoding="utf-8") == stopped
    kept = (tdir / "integrate.md").read_text(encoding="utf-8")
    assert kept == "# Integrate: keys\n\n" + routed
    import stage_status
    assert not stage_status.integrated(tdir)
    # the new run's round 3 fails with another R1.3: it reaches the owner
    _owner_rounds(tdir, "NEW: the key-wrap rule drops the MUST NOT")
    status = rf.status(tdir)
    assert status["next"] == "owner" and status["open"][0]["text"].startswith("NEW")
    assert rf.to_owner(tdir)["added"] == 1
    text = (tdir / "integrate.md").read_text(encoding="utf-8")
    assert "NEW: the key-wrap rule" in text and "OLD" not in text and routed in text
    # an integrate.md with nothing routed moves whole: nothing stays
    lone = tmp_path / "lone"
    lone.mkdir()
    (lone / "base.txt").write_text("x\n", encoding="utf-8")
    (lone / "integrate.md").write_text("# Integrate: lone\n\n## For the owner\n\n- **R1.1** a\n",
                                       encoding="utf-8")
    run = wb.restart(lone)
    assert (run / "integrate.md").read_text(encoding="utf-8").endswith("- **R1.1** a\n")
    assert not (lone / "integrate.md").exists()
    # an `integrated:` line below the last routed section is the run's, not the sibling's
    last = tmp_path / "last"
    last.mkdir()
    (last / "integrate.md").write_text("# Integrate: last\n\n" + routed + "\nintegrated: 2026-11-15\n",
                                       encoding="utf-8")
    wb.restart(last)
    assert (last / "integrate.md").read_text(encoding="utf-8") == "# Integrate: last\n\n" + routed


def test_write_restart_moves_the_stopped_run_whole_and_keeps_only_the_inputs(tmp_path):
    # 1.4.7, G5: every file the stages wrote at the top level (draft.md,
    # review.md, integrate.md, the filled prompts, lossless-run.json, logs)
    # goes into run-<k>/ with the numbered ones; only the topic's inputs stay.
    repo, tdir = _topic(tmp_path)
    inputs = {"base.txt": "abc\n", "current.md": "old text\n", "research-brief.md": "brief\n",
              "team-run.md": "team\n", "agent-run.md": "agent\n"}
    for name, text in inputs.items():
        (tdir / name).write_text(text, encoding="utf-8")
    (tdir / "research").mkdir()
    (tdir / "research" / "notes.md").write_text("n\n", encoding="utf-8")
    (tdir / "write-brief.md").write_text(FROM, encoding="utf-8")
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16")
    _round(tdir, "## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n")
    wb.append(tdir)
    wb.record_lossless(tdir, REPORT)
    stage_files = {"integrate.md": "## For the owner\n", "review-prompt.md": "p\n", "author-prompt.md": "a\n",
                   "lossless-judge-prompt.md": "j\n", "lossless-run.json": "{}\n", "validate-out.txt": "v\n",
                   "lossless-out-1.json": "{}\n", "disputes.md": "- R1.1: no\n"}
    for name, text in stage_files.items():
        (tdir / name).write_text(text, encoding="utf-8")
    (tdir / "scratch").mkdir()
    (tdir / "scratch" / "x.txt").write_text("x\n", encoding="utf-8")
    before = sorted(p.name for p in tdir.iterdir())
    second_check = (tdir / "second-check.md").read_bytes()
    wb.write(tdir, str(repo), PY, ARTIFACT, kind="existing", today="2026-11-16", restart_run=True)
    run = tdir / "run-1"
    kept = sorted(p.name for p in tdir.iterdir() if p.name != "run-1")
    assert kept == sorted([*inputs, "research", "second-check.md", "write-brief.md", "owner-list.md"])
    assert set(kept) - {"owner-list.md", "write-brief.md"} <= set(wb.RESTART_KEEPS)
    assert sorted(p.name for p in run.iterdir()) == sorted(set(before) - set(kept) | {"owner-list.md"})
    for name, text in inputs.items():
        assert (tdir / name).read_text(encoding="utf-8") == text
    assert (tdir / "second-check.md").read_bytes() == second_check
    assert (tdir / "research" / "notes.md").exists() and (run / "scratch" / "x.txt").exists()
    assert (run / "draft.md").read_text(encoding="utf-8") == "draft\n"
    assert (run / "integrate.md").read_text(encoding="utf-8") == "## For the owner\n"
    # the rebuilt brief keeps the From section; the old run's brief is not moved but rebuilt
    assert (tdir / "write-brief.md").read_text(encoding="utf-8").endswith("\n" + FROM)
    # a topic holding only its inputs has nothing to move
    fresh = tmp_path / "fresh"
    fresh.mkdir()
    for name in ("base.txt", "current.md", "second-check.md", "write-brief.md"):
        (fresh / name).write_text("x\n", encoding="utf-8")
    assert wb.restart(fresh) is None and not list(fresh.glob("run-*"))


def test_the_lossless_judge_names_what_carries_the_missing_content():
    # 1.4.7, G6: a fail's note names every rule or part of this artifact that
    # carries any of the missing content, or says none does, so the
    # orchestrator can retarget the entry once.
    text = " ".join(wb.fill("lossless-judge", common(artifact=ARTIFACT, base="abc", copies="",
                                                       last_run="out")).split())
    assert ("a `fail` note must name every rule or part of this artifact that carries any of the "
            "missing content, or say that none does") in text
    assert "retargeted" in text
    # 1.4.8: after the author's rewrite a retargeted entry's stale fail is
    # re-judged like any other; only a second retarget is refused.
    assert "a fresh fail on an entry already `retargeted` is recorded as the hard failure" in text
    assert "so its fail is final" not in text
