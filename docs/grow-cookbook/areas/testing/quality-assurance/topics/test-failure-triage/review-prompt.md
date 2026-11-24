You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-failure-triage/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-failure-triage/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/testing/quality-assurance/test-failure-triage`.

This is round 2 of at most 3: a scoped re-review, not a
fresh one.

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

The findings still open, to rule on:
- R1.1: `rules.md`, two MUST rules cite claims that carry only SHOULD (criterion 3, the strength rule). Every instance: (1) **evidence-states-what-was-observed** (MUST) cites `bp-separate-information-from-judgment`, whose trust basis says ICD 203 "carries 'should', a recommendation" and which research.md calls "a 'should' standard from outside software". It also cites `ev-get-data-first`, a secondary review (trust 48) that research.md puts at SHOULD ("The sources support only a SHOULD ... (bp-explain-uncertainty-and-gaps, ev-get-data-first)"). (2) **bug-names-observed-misbehavior** (MUST) cites `bp-failure-message-desired-actual`, whose quote is "it should clearly express the desired outcome, the actual outcome" and which comes from a secondary practitioner book. No other MUST rule cites a should-strength claim. The other three supported MUST rules cite tool definitions, tool data and a study's classification, and the five owner-list rules carry the accepted "This MUST hold:" lead-in. Fix: keep both rules at MUST and cite only the imperative claims that hold the MUST: `(claims: bp-bug-report-observed-vs-expected, bp-failure-record-copies-log)` for evidence-states-what-was-observed and `(claim: bp-bug-report-observed-vs-expected)` for bug-names-observed-misbehavior. Mozilla's "Clearly separate facts (observations) from speculations" still carries the "an argument from what is likely is not evidence" clause. The ICD 203, Agans and SWE-at-Google support can stay in `rationale.md`. If the author keeps those citations, the rule has to drop to SHOULD instead, and its line in `a-complete-review-must-establish.md` moves from the MUST list to the SHOULD list.
- R1.2: `examples.md`, the example verdicts do not keep the MUST rule **high-confidence-needs-reproduction-and-mechanism** ("`confidence` is 1-10"), and one of them leans toward the owner's open question. Every instance: (1) the flake verdict states "Confidence: likely.", a likelihood term instead of a 1-10 value. That is the ICD 203 alternative the owner list leaves open ("or replaced by a stated likelihood term ... as ICD 203 has it"), so the illustration shows the unsettled option as if it were the practice. (2) The uncertain verdict states no confidence at all, although the 1-10 rule and **verdict-states-confidence-and-its-basis** apply to every verdict. Fix: give the flake example a value on the stated scale below 9, since it has no reproduction on demand and no confirmed mechanism, for example "Confidence: 6 (1-10). Rests on the same-revision pass and the history; not yet reproduced on demand, so a product-side race in the cart update is not ruled out." Add a confidence line with its basis and gaps to the uncertain example, for example "Confidence: 3 (1-10). One timeout and one passing rerun; no trace and no runner-wide signal."
- R1.3: `examples.md`, flake verdict, the line "(log lines copied below)" points to log lines that the example never shows. The example therefore does not show what **evidence-states-what-was-observed** and **gather-failure-artifacts-before-classifying** ask for, or what `what-a-reviewer-looks-for.md` checks ("with the log lines copied in"). Fix: add two or three illustrative copied log lines under the `Observed:` entry, for example the assertion line and its file:line, or reword it to "(the assertion line and stack trace are copied into the record)".

1. Rule on every open finding above, in `## Rulings`, one line each:
   `- <id>: fixed|disputed-accepted|routed|open — <reason>`.
   - `fixed`: the change resolves it.
   - `disputed-accepted`: the author disputed it in disputes.md and is
     right. A dispute you reject is `open`, with why.
   - `routed`: the finding belongs to a named sibling topic and was recorded
     in that sibling's write-brief.md if it has not passed stage 4, or in its
     integrate.md if it has. Name the sibling in the reason.
   - `open`: it still stands.
2. Raise a new finding only on text the diff shows changed this round, or for
   a factual error against a cited claim (name the claim). Nothing else is
   reviewed again.
3. Never ask to reverse a fix an earlier round asked for unless you cite the
   claim that makes that fix wrong.
A new finding names every instance of its class in the changed text.

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-failure-triage, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/review.md:
- `# Review: test-failure-triage`
- `## Findings`: new findings only, one top-level `- ` bullet each: the file,
  the rule or line, what is wrong (every instance), and the fix. Write `none`
  if there are none.
- `## Checked`: what you checked and found right, one bullet each.
- `## Rulings`: one line per open finding, as above.
- `## Lint`: the /lint-artifact result, then, as the section's last line,
  exactly `lint: clean` (no lint error) or `lint: fail <n>` (n lint errors).
  A script reads only that line; without it the round counts as a lint
  failure.
- last, a line of its own, exactly `verdict: pass` or `verdict: fail`.
  `fail` when a new finding, a ruling of `open`, or a lint error stands.
Reply with the verdict line only.
