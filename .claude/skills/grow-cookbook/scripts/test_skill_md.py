"""SKILL.md names every helper script and prompt, and carries the rulings'
fixed phrases, so the procedure and its scripts cannot drift apart. Since
1.4.11 a stage's detail lives in its reference file under `references/`:
each pinned phrase is checked in the file it lives in."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import stage_status  # noqa: E402
import write_brief  # noqa: E402

SKILL_DIR = HERE.parent
SKILL = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
FLAT = " ".join(SKILL.split())
REFERENCES = sorted((SKILL_DIR / "references").glob("*.md"))


def text(name: str) -> str:
    """`name`'s text, whitespace collapsed: `SKILL.md` or `references/<file>`."""
    return " ".join((SKILL_DIR / name).read_text(encoding="utf-8").split())


def every_file() -> str:
    """SKILL.md and every reference, whitespace collapsed, for phrases that
    must be absent everywhere."""
    return " ".join([FLAT] + [" ".join(p.read_text(encoding="utf-8").split()) for p in REFERENCES])


def test_every_script_is_named():
    for script in HERE.glob("*.py"):
        if not script.name.startswith("test_"):
            assert f"scripts/{script.name}" in SKILL or f"`{script.name}`" in SKILL, script.name


def test_every_prompt_is_named_with_its_fill_line():
    for name in write_brief.PROMPTS:
        assert f"`{name}`" in SKILL, name
    for name in ("research", "second-check", "author", "lossless-judge"):
        assert f"write_brief.py prompt {name} " in SKILL, name
    for sub in ("write", "append", "review", "lossless"):
        assert f"write_brief.py {sub} A/topics/<topic>" in SKILL, sub


def test_versions_agree():
    m = re.search(r'^version: "([\d.]+)"', SKILL, re.M)
    assert m and m.group(1) == "1.4.47"
    assert SKILL.count("v1.4.47") >= 3
    assert f"at least {stage_status.MINIMUM}" in SKILL and f"cookr, {stage_status.MINIMUM} or later" in SKILL


def test_rulings_are_in_the_procedure():
    for phrase in (
        ("SKILL.md", "at most 3 review rounds"),                       # A5
        ("references/stage-4.md", "never a finding"),                               # A2
        ("references/stage-4.md", "`## Checked`"),                                  # A3
        ("references/stage-4.md", "never asks to reverse an earlier fix"),          # A4
        ("SKILL.md", "keeps `base.txt`, `current.md` and the brief"),  # A6
        ("references/stage-3.md", "exempts only the rule's wording"),               # B1
        ("references/stage-2.md", "supported at the rule's stated strength"),       # B3
        ("SKILL.md", "A rule's citations are authoritative"),          # C
        ("SKILL.md", "prior rule names never change"),                 # C
        ("references/stage-3.md", "one lead-in in front of it"),                    # D
        ("SKILL.md", "writes the accounting"),                         # E
        ("references/stage-5.md", "--pin-for"),                                     # E
        ("SKILL.md", "one topic at a time, in the order of the plan's"), # F
        ("SKILL.md", "may be researched in parallel"),                 # F
        ("SKILL.md", "sibling's `write-brief.md`"),                    # F
        ("SKILL.md", "apply_second_check.py <repo>/<artifact> --list"),  # G
        ("references/stage-1.md", "Every merged copy is folded into its survivor and checked lossless at stage 5 (`--copy`), whatever its worklist `fold_check`"),  # 1.4.13, G16 (was E4)
        ("references/stage-5.md", "every merged copy, the worklist copies whatever their `fold_check`"),  # G16
        ("references/stage-1.md", "writing `A/building-<name>-quoted.json`"),  # G11
        ("SKILL.md", "into `A/building-<name>-quoted.json`"),  # G11
        ("references/stage-1.md", "Only the partly held and not held sentences count as gaps in the plan"),  # G12
        ("references/stage-1.md", "a 100% held from it says nothing was lost on fold, and nothing about whether the topic is correct"),  # G10
        ("references/stage-1.md", "writes `A/gaps/new-<name>.json`"),  # G18
        ("references/stage-1.md", "it is measured in the survivor's area plan, against the survivor, never in the copy's plan"),  # G14
        ("references/stage-1.md", "It is never silently skipped"),  # G19/G15
        ("references/stage-1.md", "each `marked_here` sentence"),  # G8
        ("references/stage-1.md", "each `mark_conflicts` sentence"),  # G8
        ("SKILL.md", "Quote all it lists: `building`, `marked_here`, `mark_conflicts` (step 1.2"),  # G8/G15/G19
        ("references/stage-1.md", "read every existing plan's `merged` rows that point at this area's folders"),  # G9
        ("SKILL.md", "`incoming` merge and carrying its research questions"),  # G9
        ("references/stage-1.md", "the assignment as the first word after `--`, no `env`"),  # G17
        ("references/stage-1.md", "that topic's folder (`<topic-folder>`, relative to `<repo>`), except a row `unmeasured.py` (step 1.2) lists in `survivor_elsewhere`, and of every speciality"),  # 1.4.14, M1; 1.4.15, N1'
        ("references/stage-1.md", "`unmeasured.py` runs before step 1.3, whose gaps commands need its"),  # M1; 1.4.15, N2'
        ("SKILL.md", "name each `unread_marks` file to the owner"),  # 1.4.15, N3'
        ("references/stage-1.md", "reports it in both the merging and the target area, even when the target plan names the copy"),  # 1.4.15, M1'
        ("SKILL.md", "less `survivor_elsewhere` rows"),  # M1
        ("references/stage-1.md", "records a move, not a merge, and `incoming`, `fold` and `conflicts` all leave it out"),  # M4
        ("references/stage-1.md", "(Action `kept`; a `dropped`, `split` or `new` row still folds)"),  # N2
        ("references/stage-5.md", "only a copy a plan keeps (Action `kept`) and no plan merges"),  # N2
        ("references/stage-1.md", "each `unread_marks` file"),  # N3
        ("SKILL.md", "team_probe.py researchteam"),                    # E6
        ("SKILL.md", "--area <area> --worklist"),                      # E2
        ("references/stage-2.md", "Quote each one **verbatim**"),                   # E28
        ("references/stage-2.md", "takes the artifact folder"),                     # E48
        ("SKILL.md", "PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -P -m cookr -p <repo>"),  # E9/E59
        ("SKILL.md", "A lossless failure never goes to the owner"),    # fix round 1, ruling 1
        ("SKILL.md", "This is the one place `append` runs"),           # m9
        ("SKILL.md", "`next: stop`"),                                  # ruling 3
        ("SKILL.md", "A lossless failure gets exactly one round"),     # fix round 2, n3
        ("references/stage-4.md", "Lint fails closed"),                             # fix round 2, I3
        ("SKILL.md", "the verdict is `pass` and no lint error stands"),  # fix round 3, n6
        ("references/stage-4.md", "leave the draft unchanged on lint grounds"),     # fix round 3, lint to the author
        ("SKILL.md", "relative `<workspace>` is relative to the current directory"),  # fix round 4
        ("SKILL.md", "`git -C ${CLAUDE_SKILL_DIR} rev-parse --show-toplevel`"),  # fix round 5, n8
        ("SKILL.md", "**When it exits 2, stop** and show its message: `<repo>` holds no cookbook"),  # fix round 5, n8
        ("SKILL.md", "`write` refuses a re-run"),                      # 1.4.6, G1
        ("references/stage-4.md", "`routed`: the finding belongs to a named sibling topic and was recorded in that sibling's write-brief.md if it has not passed stage 4, or in its integrate.md if it has"),  # G2, fix round 1
        ("references/stage-5.md", "every word added to the rule must be covered by a claim the rule cites"),  # G4
        ("references/stage-5.md", "then stage 3 again with `write_brief.py write ... --restart`"),  # fix round 1
        ("references/stage-3.md", "`write` keeps every `## From <topic>'s review` section"),  # fix round 3
        ("references/stage-3.md", "moves the stopped run whole into a new `run-<k>/`"),  # 1.4.7, G5
        ("references/stage-3.md", "only the topic's inputs stay"),                  # G5
        ("references/stage-5.md", "retarget the entry once"),                       # G6
        ("references/stage-5.md", "a second judged fail on the same entry is recorded as the hard failure"),  # G6
        ("references/stage-5.md", "content spans more than 3 rules or parts still takes a lossless round"),  # G6
        ("references/stage-1.md", "a merged topic is researched, written and reviewed only under the plan whose area holds its Artifact folder"),  # G7
        ("SKILL.md", "`merged into <folder>`"),                        # G7
        ("SKILL.md", "cookr roles lossless --retarget <artifact> --entry <n> --to <name>"),  # 1.4.8, fix round 1: G6(c)
        ("references/stage-5.md", "a second retarget is refused"),                  # G6(c)
        ("references/stage-5.md", "a stale fail on a retargeted entry is re-judged"),  # ruling: a lossless round re-arms judging
        ("references/stage-5.md", "the retarget allowance stays spent"),            # ruling
        ("references/stage-5.md", "or a stale verdict"),                            # step 3 dispatches a judge for a stale entry
        ("references/stage-3.md", "only what sibling topics routed to `integrate.md` stays"),  # 1.4.9, N1
        ("SKILL.md", "copy it to the sibling's `integrate.md` under `## From <this topic>'s review`"),  # N1
        ("references/stage-5.md", "`--retarget` refuses targets that fail the 80% bar or a tripwire"),  # N2
        ("SKILL.md", "if the sibling is integrated, `stage_status.py` lists each finding in a `## From` section of an integrated topic's `integrate.md` in that topic's `owner`"),  # 1.4.10, N5
        ("SKILL.md", "give the owner every `owner` item of an integrated sibling"),  # N5: the hand-off
        ("SKILL.md", "looks for an id it has already recorded only inside `## For the owner`"),  # N4
        ("SKILL.md", "then step 1 again"),                             # nit 8
        ("SKILL.md", "none of this topic's own findings goes to the owner"),  # 1.4.11, N7
        ("SKILL.md", "however it ends (`next: stop` included), give the owner every `owner` item of an integrated sibling"),  # N7
        ("SKILL.md", "give the owner every topic's `owner` items, verbatim, whatever any topic's outcome"),  # N7: the area's end hand-off
        ("SKILL.md", "see *What reaches the owner*"),                  # N7: the stop bullet points to the one statement
        ("references/stage-1.md", "as `<plan>/<topic>` or as the full `cookbook/guidelines/<plan>/<topic>`, a whole path"),  # 1.4.16, G20
        ("references/stage-1.md", "A name in the prose or in the **Topics** table does not count"),  # G21
        ("SKILL.md", "--keep A/building-<name>.json"),  # G22
        ("references/stage-1.md", "prints it unchanged, says \"marks kept (sentences unchanged)\" on stderr and exits 0"),  # G22, 1.4.18 G38
        ("references/stage-1.md", "regenerates every step-1 output"),  # G23
        ("references/stage-1.md", "A `via` mapping"),  # G25
        ("references/stage-1.md", "is not a measure: the row stays unmeasured"),  # G25
        ("references/stage-1.md", "An artifact two plans both keep (Action `kept`) is a conflict too"),  # G26
        ("SKILL.md", "Re-run `unmeasured.py` and `stage_status.py` (stage-1.md step 4)"),  # G27
        ("references/stage-1.md", "The plan records every change since step 1.2 or step 3"),  # G27
        ("references/stage-1.md", "one that restates a copy merged into the topic"),  # G28
        ("references/stage-1.md", "Note it \"not held: review procedure\""),  # G29
        ("references/stage-1.md", "is quoted once, naming every plan that marks it"),  # G30
        ("references/stage-1.md", "its output never decides held or not held"),  # G31
        ("references/stage-1.md", "`fold_check: false` is superseded by this rule"),  # fold_check
        ("references/stage-1.md", "`fold` names the copy that the survivor's area folds, not this one"),  # merged-row fold
        ("references/stage-1.md", "the worklist's `guidelines/<plan>/<topic>` names it too"),  # 1.4.17, M1
        ("references/stage-1.md", "a topic whose `survivor` or `new_home` is in the area"),  # M5
        ("SKILL.md", "an exit 2 from the template keeps the marked file"),  # M6
        ("references/stage-1.md", "A `--keep` file it cannot read is an exit 2 too"),  # N2
        ("references/stage-1.md", "A gaps folder that does not exist is an exit 2"),  # M4
        ("references/stage-1.md", "with `kind: double-keep` and every keeping plan in `plans`"),  # N4
        ("references/stage-1.md", "Clear `A/gaps/` before step 1.3"),  # 1.4.18, G32
        ("references/stage-1.md", "is judged once, at its home topic"),  # G33
        ("references/stage-1.md", "lacking at the other topics it was measured against is not counted"),  # G33
        ("references/stage-1.md", "A sentence marked for another area is never this area's gap"),  # G33
        ("references/stage-1.md", "its `lacking_numbers`"),  # G34
        ("references/stage-1.md", "they count as gaps of the new topic"),  # G35
        ("references/stage-1.md", "records \"measured in <plan>\" for it and does not count it"),  # G36
        ("references/stage-1.md", "never build them by hand"),  # G37
        ("SKILL.md", "scripts/run_gaps.py --area <area>"),  # G37
        ("SKILL.md", "marks kept (sentences unchanged)"),  # G38
        ("references/stage-1.md", "is listed once, naming both plans: it is no owner item"),  # G39
        ("references/stage-1.md", "re-read each owner question against the plan body it cites"),  # G40
        ("references/stage-1.md", "This applies to writing-side topics only"),  # G41
        ("references/stage-1.md", "the survivors' area"),  # G42
        ("references/stage-1.md", "end its line with `; echo exit=$?`"),  # G43
        ("SKILL.md", "`home_guess` and `gap_candidates` are an advisory guess; the plan names each home"),  # 1.4.19, I1
        ("references/tools.md", "an advisory guess (the plan names each home)"),  # I1
        ("references/stage-1.md", "judge it against that topic's text, or run `cookr roles gaps <home-folder> --against <building file> --json`"),  # I1
        ("SKILL.md", "each of `unmeasured_sentences` by hand"),  # I2
        ("references/stage-1.md", "judge each one by hand at its home topic; it counts as a gap unless held"),  # I2
        ("references/stage-1.md", "each R9 `new-<name>.json` is re-run by hand after it"),  # M4
        ("references/stage-1.md", "Only R9's `new-<name>.json` measures stay hand-built"),  # M4
        ("references/stage-1.md", "each building entry then carries `partial`"),  # M2
        ("references/stage-1.md", "with no guess, over every measured topic"),  # 1.4.20, Minor 1
        ("SKILL.md", "`--hints` adds `paraphrase_hints.py`'s advisory ranking, over every measured topic where no home is guessed"),  # Minor 1
        ("references/stage-1.md", "none is owed for a new topic with no candidate survivor"),  # Minor 2
        ("references/tools.md", "`r9_missing` (owed R9 measures only)"),  # Minor 2
        ("references/stage-1.md", "a sentence is measured only when cookr measured every piece of it"),  # Minor 3
        ("references/tools.md", "`unmeasured_sentences` (a piece not measured: judged by hand)"),  # Minor 3
        ("references/stage-1.md", "keeps its measured pieces' verdicts under `measured_pieces` (and `home_guess`)"),  # 1.4.21 Minor 1, reworded 1.4.23
        ("references/stage-1.md", "a topic whose run failed is never ranked"),  # Nit 1
        ("references/stage-1.md", "or when the worklist has no entry for it"),  # Nit 2
        ("references/stage-1.md", "`unplaced_pieces`: a piece cookr did not measure that no sentence holds"),  # Nit 3
        ("references/tools.md", "`unplaced_pieces` (judged by hand)"),  # Nit 3
        ("references/stage-1.md", "`measured_pieces` is not a verdict on the sentence"),  # 1.4.22, Minor 1
        ("references/stage-1.md", "The sentence's own `held_at` and `lacking_at` stay empty"),  # 1.4.22, Minor 1
        ("references/stage-1.md", "or one with a piece not measured, whatever its measured pieces say"),  # 1.4.22, Minor 1 (--hints)
        ("references/stage-1.md", "each an object: `text`, `measured`, `verdict`, `topic`, `sentences`"),  # 1.4.22, Nit 1
        ("references/stage-1.md", "A measured piece no one sentence holds is never dropped"),  # 1.4.22, Minor 2
        ("references/tools.md", "`measured_pieces` (never a verdict on the sentence)"),  # 1.4.22, Minor 1
        ("references/tools.md", "Run every script with absolute paths, from any directory"),  # 1.4.24, G44
        ("references/stage-1.md", "never removes an R9 `new-<name>.json`"),  # G45
        ("references/stage-1.md", "no one types `rm` or `find`"),  # G45
        ("SKILL.md", "(`--check` on `unmeasured.py` and `run_gaps.py`)"),  # G45
        ("references/stage-1.md", "whatever its speciality (`specialities` [] when none of this area names"),  # G46
        ("references/stage-1.md", "A `pending_target` entry is never clean"),  # G47
        ("references/stage-1.md", 'whatever its mark, as `{"n", "marked_for"}`'),  # G48, G64
        ("references/stage-1.md", "every marking plan in its `marked_by`"),  # G49
        ("references/stage-1.md", "an authored one no speciality names included"),  # G50
        ("references/stage-1.md", "judge it once and record that judgment under each speciality"),  # G51
        ("references/stage-1.md", "`building_marked_elsewhere`"),  # G52
        ("references/stage-1.md", "never an existing topic of this area"),  # G53
        ("references/stage-1.md", "A re-quote carries each mark by its sentence's text, never by its number"),  # G54
        ("SKILL.md", "set a mark with `mark.py`"),  # G55
        ("references/tools.md", "## The marks file"),  # G55
        ("references/stage-1.md", '"area has no speciality"'),  # G57
        ("SKILL.md", "(with the area's `copy_check.py` output)"),  # G58
        ("references/stage-1.md", "The fold must carry everything it names"),  # G58
        ("references/tools.md", "## Output shapes"),  # G59
        ("references/stage-1.md", "An area of copies only"),  # G60
        ("references/stage-1.md", "run the survivor's area plan first"),  # G61
        ("references/stage-1.md", "the plan hands it to the owner and does not decide it"),  # G62
        ("references/stage-1.md", "intent *Evaluate*"),  # G62
        ("references/stage-1.md", "the step-4 `--check` re-run settles"),  # G63
        ("references/stage-1.md", "`<name>` is the speciality's basename"),  # G63
        ("references/stage-1.md", "a planned new area"),  # 1.4.25, G65
        ("references/stage-1.md", "`advisory_failed`"),  # G66, G82
        ("references/stage-1.md", "needs no `--out` scratch run"),  # G67
        ("references/stage-1.md", "`saved_file`"),  # G67
        ("references/stage-1.md", "`home_measures`"),  # G68
        ("references/stage-1.md", "`home--<topic>.json`"),  # G68, renamed 1.4.26 (M1)
        ("references/tools.md", "--mark <n>=<area>[,<area>]"),  # G70
        ("references/tools.md", "never held in a shell variable"),  # G70
        ("references/stage-1.md", "`differs_for`"),  # G71
        ("references/stage-1.md", "not a blocker"),  # G71
        ("references/stage-1.md", "`short_sentences`"),  # G72
        ("references/stage-1.md", "**Sentences and pieces.**"),  # G73
        ("references/stage-1.md", "copy_check wins"),  # G74
        ("references/stage-1.md", "`direction`"),  # G74
        ("references/stage-1.md", "`incoming_unplanned`"),  # G75
        ("references/stage-1.md", "`speciality_points_at_copy`"),  # G75
        ("references/stage-1.md", "`next_why`"),  # G75
        ("references/stage-1.md", "who repoints the speciality is the owner's"),  # G75
        ("references/stage-1.md", "## The short path: two special cases"),  # G80
        ("references/tools.md", "`repo_path.py`"),  # G76
        ("references/stage-1.md", "`--marks` prints `topics`"),  # G77
        ("references/stage-1.md", "**Owner questions:**"),  # G79
        ("references/stage-1.md", "**Step-4 re-check:**"),  # G79
        ("SKILL.md", "**Research questions**, **Owner questions** and **Step-4 re-check**"),  # G79
        ("references/stage-1.md", "steps 1.1–1.3 produce empty output"),  # G80
        ("references/stage-1.md", "writing craft is *How-to / troubleshooting*"),  # G81
        ("references/stage-1.md", "the method owners, the published style guides and the standards bodies"),  # G81
        ("references/stage-1.md", "plans do not escalate on \"acted on\" alone until the owner rules"),  # G81
        ("references/stage-1.md", "**An advisory failure.**"),  # G82
        ("references/stage-1.md", "A kept twin is researched on its own and never borrows its twin's research"),  # G83
        ("references/stage-1.md", "records the survivor's plan as carrying them"),  # G84
        ("references/stage-1.md", "the survivor's research bar governs"),  # gapfix9 fix round 1, review 6
        ("references/stage-1.md", "**A speciality two plans measure.**"),  # G85
        ("references/stage-1.md", "names the contradiction"),  # G86
        ("references/stage-1.md", "chosen from the whole cookbook"),  # G87
        ("references/stage-1.md", "never from another plan's quote"),  # G88
        ("references/stage-1.md", "re-run step 4 in both once both plans exist"),  # G89
        ("references/stage-1.md", "`A/run_gaps.json`"),  # G90
        ("references/tools.md", "`A/run_gaps.json`"),  # G90
        ("references/stage-1.md", "not this plan's to judge, and only need a count"),  # G91
        ("references/stage-1.md", "`cookbook/guidelines/cookbook/<area>/"),  # G92
        ("references/tools.md", "each cut at its own `_Cookbook guidance`"),  # G93
        ("references/tools.md", "*Standing focus* and *Tidy focus*"),  # 1.4.26, I1
        ("references/tools.md", "`left_out`"),  # I1
        ("references/stage-1.md", "`numbering_differs`"),  # I2
        ("references/tools.md", "`numbering_differs`"),  # I2
        ("references/stage-1.md", "`unmeasured_references`"),  # M2
        ("references/stage-1.md", "`advisory_failed` (1.4.26)"),  # M3
        ("references/stage-1.md", "as `DIR/run_gaps.json` with any other `--out DIR`"),  # M4, N2
        ("references/stage-1.md", "never on a refused input"),  # N2
        ("references/stage-1.md", "writes a missing reference into `DIR/reference`, never `A/reference`"),  # M4 writes
        ("references/tools.md", "a missing reference into `DIR/reference` with any other `--out DIR`"),  # M4 writes
        ("references/stage-1.md", "so it is always this plan's to resolve"),  # M5
        ("references/stage-1.md", "a `merged` copy of any area's plan"),  # M6
        ("references/stage-1.md", "or whose plan has no row for it"),  # M7
        ("references/tools.md", "a `--repo` with no `cookbook/guidelines/` exits 2"),  # M8
        ("SKILL.md", "name each `unread_marks` file to the owner under **Owner questions**"),  # N4
        ("references/stage-1.md", "does not decide it, listing it under **Owner questions**"),  # N4
        ("references/stage-1.md", "`stale_reference` (1.4.27)"),  # R-I-1
        ("references/stage-1.md", "rewrite `A/reference` (step 1.1, then steps 1.2 and 1.3) and re-measure"),  # R-I-1, R2-M-3
        ("references/tools.md", "step 1.1, then steps 1.2 and 1.3"),  # R2-M-3
        ("SKILL.md", "rewrite A/reference (step 1.1, then steps 1.2 and 1.3)"),  # R2-M-3
        ("references/stage-1.md", "approved or not"),  # R2-I-1
        ("references/stage-1.md", "the approval stays on record as history"),  # R2-I-1
        ("references/tools.md", "approved or not"),  # R2-I-1
        ("references/stage-1.md", "inside the area other than `A/gaps`"),  # R2-M-1
        ("references/tools.md", "inside the area other than `A/gaps`"),  # R2-M-1
        ("references/stage-1.md", "a `marked_here` reference `A/run_gaps.json` lists stale"),  # R2-M-2
        ("references/stage-1.md", "saves its report and exits 1"),  # R2-M-4
        ("references/tools.md", "saves its report and exits 1"),  # R2-M-4
        ("references/tools.md", "`stale_reference`"),  # R-I-1
        ("references/tools.md", "`reference_format.py`"),  # R-I-1
        ("SKILL.md", "`stale_reference` row stops approval"),  # R-I-1
        ("references/stage-1.md", "`reference-format <N>`"),  # N3-M-1 (1.4.29)
        ("references/stage-1.md", "on the line that names the plan's hash"),  # N3-M-1
        ("references/stage-1.md", "The earlier approval stays in `A/approval.md` as history"),  # N3-M-1
        ("references/stage-1.md", "`approval_why`"),  # N3-M-1
        ("references/tools.md", "`approval_why`"),  # N3-M-1
        ("SKILL.md", "approved under an older reference format"),  # N3-M-1
        ("references/stage-1.md", "saved under an older reference format, or none"),  # N3-I-1
        ("references/tools.md", "`reference_format`"),  # N3-I-1
        ("references/stage-1.md", '`reason` (`"old_format"`, `"no_writer"`, `"old_report"`)'),  # N3-M-2
        ("references/stage-1.md", "`- plan: area-plan.md, git hash-object <hash>, reference-hash <reference_hash>`"),  # N4-I-2 (1.4.30)
        ("references/stage-1.md", "prints no `reference_hash` while `stale_reference` lists any row"),  # N4-I-2
        ("references/stage-1.md", "`git hash-object A/reference.json`"),  # N4-I-2
        ("references/stage-1.md", '`"reference_hash"`'),  # N4-I-2
        ("references/stage-1.md", "approves nothing since 1.4.30"),  # N4-I-2
        ("references/stage-1.md", "saved while it listed a stale row"),  # N4-I-1
        ("references/tools.md", "`reference_hash` str or null"),  # N4-I-2
        ("references/tools.md", '`"reference_hash"`'),  # N4-I-2
        ("references/tools.md", "saved while it listed a stale row"),  # N4-I-1
        ("SKILL.md", "`reference-hash`"),  # N4-I-2
        ("SKILL.md", "`- plan: area-plan.md, git hash-object <hash>, reference-hash <reference_hash>`"),  # N5-M-2 (1.4.31)
        ("SKILL.md", "copy `reference_hash` from `stage_status.py`, never compute it by hand"),  # N5-M-3
        ("SKILL.md", "it is withheld while any reference is stale"),  # N5-M-2
        ("references/stage-1.md", "copy `reference_hash` from `stage_status.py`, never compute it by hand"),  # N5-M-3
        ("references/stage-1.md", "it is withheld while any reference is stale"),  # N5-M-2
        ("references/stage-1.md", '`"unreadable_reference"`'),  # N5-I-1
        ("references/tools.md", '`"unreadable_reference"`'),  # N5-I-1
        ("references/tools.md", "`reason`"),  # N3-M-2
        ("references/stage-1.md", "judge it by hand or re-mark it"),  # R-I-2
        ("references/stage-1.md", "listed and measured once"),  # R-N-1
        ("references/stage-1.md", "an `--out` that is the area folder, or holds it, exits 2"),  # R-M-1
        ("references/stage-1.md", "`not_compared`"),  # R-M-2
        ("references/tools.md", "`not_compared`"),  # R-M-2
        ("references/stage-1.md", "rewritten on every run, never reused"),  # R-M-3
        ("references/stage-1.md", "`--check --out DIR` compares `DIR/run_gaps.json`"),  # R-M-4
        ("references/tools.md", "`--check --out DIR` compares `DIR/run_gaps.json`"),  # R-M-4
        ("references/stage-1.md", "r9_stamp.py A/gaps/new-<name>.json --repo <repo>"),  # fix round 2, Minor 3
        ("SKILL.md", "`scripts/r9_stamp.py <file> --repo <repo>`"),  # fix round 2, Minor 3
        ("references/tools.md", "with `--repo <repo>` so a repo-relative survivor `folder` is found"),  # Minor 3
        ("references/stage-1.md", "the mark goes in the same list item as the phrase"),  # fix round 2, Minor 1
        # gapfix13 (1.4.42)
        ("references/stage-1.md", "stage_status.py --first-check --area <area>"),  # G267
        ("references/stage-1.md", "`A/first-check-before-<version>.txt`"),  # G262
        ("references/stage-1.md", "`A/area-plan-before-<version>.md`"),  # G262
        ("references/stage-1.md", "run_gaps.py --check-homes --workspace <workspace>"),  # G254
        ("references/stage-1.md", "The unit `run_gaps.py` counts is the topic"),  # G256
        ("references/stage-1.md", "mark.py --lack <topic> --source"),  # G253
        ("references/stage-1.md", "is not allowed (1.4.42, G253)"),  # G253
        ("references/stage-1.md", "never edited by hand, 1.4.42, G255"),  # G255
        ("references/stage-1.md", "The accepted form, exactly (1.4.42, G259; step 3)"),  # G259
        ("references/stage-1.md", "| `modal_differs: true` | `not`"),  # G260
        ("references/stage-1.md", "The order, and which wins"),  # G264
        ("references/stage-1.md", "write this run's `### On <version>` subsection first"),  # G265
        ("references/stage-1.md", "report that final value"),  # G266
        ("references/stage-1.md", "`topic_files`, the topic's part files the sentences are read from"),  # gapfix13b
        ("references/stage-1.md", "`short_not_owed` (`run_gaps.py`, advisory in `stage_status.py`) names each one"),
        ("references/stage-1.md", "so Swift-import names swift"),  # gapfix13b (language#5)
        ("references/stage-1.md", "No command here keeps a flag"),  # G263
        ("references/tools.md", "## Cites"),  # G258
        ("SKILL.md", "one python, `$COOKR_PY`, runs every script"),  # G269
    ):
        name, phrase = phrase
        assert phrase.lower() in text(name).lower(), (name, phrase)
    everywhere = every_file()
    assert "myteams researchteam research --help" not in everywhere
    assert "then this step again. Then" not in everywhere     # nit 8: step 5 sends the round to step 1
    assert "which goes to the owner with its" not in everywhere   # N5: no unconditional delivery claim
    assert "without changing `to`" not in everywhere          # N2: --retarget checks the targets first
    assert "the topic stops; nothing goes to the owner" not in everywhere  # N7: no unconditional stop claim
    assert "a copy with `fold_check` false is not folded" not in everywhere  # G16
    assert "platform/platform-windows" not in everywhere      # gapfix13 (G261): the map names building/
    assert "area-plan-before-<old" not in everywhere          # gapfix13 (G262): one backup name


def test_append_runs_in_one_step():
    # m9: named in stage 4's count step only, in SKILL.md, the one place commands live.
    assert every_file().count("write_brief.py append A/topics/<topic>") == 1
    assert SKILL.count("write_brief.py append A/topics/<topic>") == 1


def test_every_reference_is_linked_from_skill_md():
    # 1.4.11: progressive disclosure; a reference no one links is never read.
    assert REFERENCES
    for ref in REFERENCES:
        assert f"](references/{ref.name})" in SKILL, ref.name
    # each stage says plainly to read its reference before it runs
    for n in range(1, 6):
        assert f"Before running stage {n}, read [references/stage-{n}.md](references/stage-{n}.md)" in FLAT, n


def test_skill_md_is_under_500_lines():
    # 1.4.11: the skill-authoring checklist warns past 500 lines.
    assert len(SKILL.splitlines()) < 500


def test_stage_1_runs_unmeasured_before_the_gaps_commands():
    # 1.4.15, N4': the gaps step skips unmeasured.py's survivor_elsewhere rows,
    # so unmeasured.py must come first, in SKILL.md and in stage-1.md.
    # G169 (1.4.37): the command is written in its --area form.
    assert SKILL.index("scripts/unmeasured.py --area <area>") < SKILL.index("roles gaps <topic-folder>")
    stage1 = (SKILL_DIR / "references" / "stage-1.md").read_text(encoding="utf-8")
    assert stage1.index("### Step 1.2: the specialities with no topic") < stage1.index("### Step 1.3: each existing topic")
    assert stage1.index("Place each speciality that has no topic yet") < stage1.index(
        "For each existing topic of the area, measure it")


def test_every_cookr_line_the_skill_gives_runs_isolated():
    # fix round 1, M1 (G44): a cookr line copied from the skill never puts the
    # working directory on sys.path.
    root = Path(__file__).resolve().parent.parent
    for f in [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]:
        text = f.read_text(encoding="utf-8")
        assert "$COOKR_PY -m cookr" not in text, f.name


# --- gapfix11 (1.4.39) ---------------------------------------------------------------------------

AREA_SCRIPTS = ("stage_status", "unmeasured", "run_gaps", "copy_check", "plan_skeleton", "mark", "quote_building")
_LINE = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/scripts/(" + "|".join(AREA_SCRIPTS) + r")\.py([^`\n]*)")


def _command_lines() -> list[tuple[str, str, str]]:
    found = []
    for p in [SKILL_DIR / "SKILL.md", *REFERENCES]:
        for m in _LINE.finditer(p.read_text(encoding="utf-8")):
            found.append((p.name, m.group(1), m.group(2).strip()))
    return found


def test_every_area_script_command_line_is_written_in_full_and_parses():
    # G197 (L12): each command line names --area, --workspace and --repo (a
    # quote_building line --area, --speciality and --file, and --repo with
    # --marks), and each parses through the script's own argparse.
    import argparse
    import importlib
    import shlex

    class Parsed(Exception):
        pass
    lines = _command_lines()
    assert any(s == "quote_building" and "--marks" in args for _, s, args in lines), \
        "the --marks run of quote_building.py is written in full nowhere"
    original = argparse.ArgumentParser.parse_args

    def parse(self, args=None, namespace=None):
        original(self, args, namespace)
        raise Parsed()
    argparse.ArgumentParser.parse_args = parse
    try:
        for name, script, args in lines:
            words = [w.split("|")[0] for w in shlex.split(re.sub(r"<n>|\bN\b(?==)", "1", args).replace("<", "x").replace(">", "x"))]
            need = (("--area", "--speciality", "--file") + (("--repo",) if "--marks" in words else ())
                    if script == "quote_building" else ("--workspace", "--repo") if "--check-homes" in words
                    else ("--area", "--workspace", "--repo"))      # gapfix13 (G254): workspace-wide
            missing = [f for f in need if f not in words]
            assert not missing, f"{name}: {script}.py {args} lacks {missing}"
            try:
                importlib.import_module(script).main(words)
            except Parsed:
                continue
            except SystemExit as e:
                raise AssertionError(f"{name}: {script}.py {args} does not parse (exit {e.code})")
            raise AssertionError(f"{name}: {script}.py {args} never reached its parser")
    finally:
        argparse.ArgumentParser.parse_args = original


def test_every_area_reference_command_passes_the_workspace():
    """gapfix13c (G272): `speciality_reference.py --area` reads the area's home
    records only with `--workspace`; every command template that runs it says so."""
    import re
    texts = [SKILL] + [p.read_text(encoding="utf-8") for p in sorted((SKILL_DIR / "references").glob("*.md"))]
    cmds = [ln for t in texts for ln in t.splitlines() if "speciality_reference.py" in ln and "--area" in ln]
    assert cmds, "no `speciality_reference.py --area` command template found"
    for ln in cmds:
        assert re.search(r"--workspace <workspace>", ln), ln


def test_gapfix14_doc_rules_are_stated():
    # gapfix14 (1.4.43): each doc rule the 42-area re-run found missing is stated where a re-run reads it.
    for name, phrase in (
        ("SKILL.md", "`--check-verdicts --area <area>` run too"),  # G280
        ("references/stage-1.md", "run_gaps.py --check-verdicts --area <area> --workspace <workspace>"),  # G280
        ("references/stage-1.md", "Every hand judgment at a home is recorded, held or lacking"),  # G276
        ("references/stage-1.md", "A Missing subject is never a `--lack` row"),  # G286
        ("references/stage-1.md", "`counted_never_judged` above 0 is the cue"),  # G300
        ("references/stage-1.md", "flags repeated over many calls go in a zsh array"),  # G293
        ("references/stage-1.md", "a brief's own scratch-name rule"),  # G292
        ("references/stage-1.md", "The `### No host` fix, whole"),  # G297
        ("references/stage-1.md", "| A tool or library list"),  # G280
        ("references/stage-1.md", "| A summary paragraph"),  # G280
        ("references/stage-1.md", "Only a line giving this area's gaps a number is read"),  # G294
        ("references/stage-1.md", "is vacuous too"),  # G301
        ("references/stage-1.md", "--keep /dev/null` prints each sentence with its number"),  # G287
        ("references/tools.md", "`--check-homes` and `--check-verdicts`"),  # G273, G280
    ):
        assert " ".join(phrase.lower().split()) in " ".join(text(name).lower().split()), (name, phrase)
