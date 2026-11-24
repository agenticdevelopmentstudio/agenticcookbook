You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-impact-analysis/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-impact-analysis/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/testing/quality-assurance/test-impact-analysis`.

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
- R1.1: `rules.md` `run-the-full-suite-periodically`, `selecting-tests-for-a-change.md` step 9, `rationale.md` paragraph 4: the full-run rule outruns two of the claims it cites, and the text calls things full runs that the research says are not. Every instance: (1) `tap-milestones-batch-commits` says TAP runs, per milestone, the targets affected since the previous milestone (the second check confirms: "milestones run tests selected by reverse dependencies on files changed since the previous milestone"), which is a batched affected-set run, not the full suite; step 9 lists "Google TAP's milestones" as a full run. (2) `android-test-mapping-directory-rules` says TEST_MAPPING has separate postsubmit groups, which are still directory-mapped tests, not the full suite; step 9 lists "Android's postsubmit groups" as a full run. (3) Rationale paragraph 4 opens "A full run stays behind the subset in every source that selects", but most of the selecting sources read (Nx, Bazel, Pants, Turborepo, Target Determinator, bazel-diff, GitHub Actions, GitLab, Gradle) say nothing of a full run; only Microsoft, Launchable, Develocity and Mill do. Fix: reword step 9 so TAP milestones are a batched run of everything affected since the last milestone and Android postsubmit groups are a later, wider mapped group, not full runs; either widen the rule so these two claims support it (for example "the full suite, or every test affected by the changes since the last such run, at some later point ...") or cite them from a rule they do support (both claims come from a `new` verdict, so they must stay cited somewhere); and change "in every source that selects" to name the sources that say it.
- R1.2: `rationale.md` (with `rules.md`): the rationale for allowing deviation (behavioral-requirements `must-explain-rationale-for-should-requirements`) and the conditions for a MAY (`should-document-conditions-for-may-requirements`) are missing for these rules; the rationale never mentions them and the rule text gives no reason: `diff-against-a-known-good-base` (SHOULD; why a known-good base and when another base is acceptable), `log-each-fallback` (SHOULD; why the fallback is logged, from `bazel-diff-fallback-costs-speed`), and `decide-change-by-content` (MAY; when content hashing is worth using rather than names or commit metadata). Every other SHOULD has its reason in the rationale or inline (`path-skipped-required-checks-resolve` carries its "so a skipped workflow does not block the merge"). Fix: add one sentence each to the rationale from the claims already cited (Nx's latest-successful-commit recommendation and Turborepo's shallow-checkout behaviour; bazel-diff logging which path each run took; bazel-diff hashing content rather than names or metadata).
- R1.3: `rules.md` `always-select-new-changed-and-failing-tests` ("recently new, recently changed, recently failed or recently flaky") and `retrain-a-learned-selector` ("retrain it regularly"): unanchored relative terms (behavioral-requirements `should-not-use-unanchored-relative-terms`); a reviewer cannot tell PASS from FAIL on "recently" or "regularly". The research gives no threshold (Develocity and Meta use the same words), so a number would be invented. Fix: anchor each to a window the team states and records (for example "recently, within a window the team states" and "on a cadence the team states"), or say in the rationale that the sources give no threshold and the team sets one; the same applies to the matching lines in `a-build-must-establish.md`.
- R1.4: `rationale.md` paragraph 5 ("The four Verify checks"), `a-build-must-establish.md` and `what-a-reviewer-looks-for.md` (the owner rules' "site", "residue path", "the prose", "commit range"): terms the guideline never defines. "Verify checks" is the author's own wording and names nothing in this guideline. "Site" and "residue path" come from the owner rules, whose wording is exempt, but the surrounding text repeats them (build lines for `each-selection-justified-by-diff`, `every-changed-path-accounted-for`, `fail-closed-is-stated`) without ever saying what a site or a residue path is, while every other part speaks of tests, targets and changed files; a reader cannot apply those MUST rules (behavioral-requirements `must-be-independently-testable`). Fix: in the rationale say "the four rules kept as the owner's text" instead of "Verify checks"; outside the exempt rule text (intro or how-to), say what a site and a residue path are in this guideline's terms (a selected test or test target; a changed path handed to the analysis to attribute), without changing the four rules' wording.
- R1.5: `examples.md`: the record shows a fallback for `package-lock.json` ("every test that uses an npm dependency is selected") but never names the tests that fallback selected, so the illustration of `record-why-each-test-was-selected` and `every-changed-path-accounted-for` leaves the one unattributable path without its sites; it is also unclear whether `pricing:test`, `checkout:test` and `cart:test` are the npm users or graph-only selections. Fix: list the tests the lockfile fallback selected (for example "Selected by fallback (package-lock.json): pricing:test, checkout:test, cart:test, search:test") so every changed path in the record is attributed to named tests.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-impact-analysis, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/review.md:
- `# Review: test-impact-analysis`
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
