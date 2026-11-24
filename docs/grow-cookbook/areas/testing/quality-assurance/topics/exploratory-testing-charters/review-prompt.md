You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters`.

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
- R1.1: `examples.md`, `running-a-chartered-session.md` step 8, `intro.md` paragraph 1: the text drops or makes conditional the expectation that the MUST rule `anomaly-carries-all-four-parts` requires on every anomaly ("where (URL or path), what was seen, what was expected instead, and how repeatable it appeared. An anomaly missing the expectation is a fail"). There are three instances. (1) The example finding has no `Expected:` line, only `Oracle:`, and its `Where: checkout, order confirmation page` is neither a URL nor a path, so the guideline's own illustration fails one of its MUST rules. (2) How-to step 8 says "what was expected (where that is not obvious) or why the behaviour is a problem". That makes the expectation optional, so following the how-to breaks the MUST, and it settles the owner's open question on whether the expectation stays a mandatory fourth part. (3) The intro's summary of a finding lists "where it was seen, the steps to reproduce it, the environment, why it is a problem, and how repeatable it was" and leaves out what was expected. Fix: give the example finding a path (for example `Where: /checkout/confirmation`) and an `Expected:` line (for example "the confirmation page shows the current cart total, 2 items, 30.00"), and keep the `Oracle:` line if wanted. In step 8, list what was expected unconditionally and give why the behaviour is a problem as an addition, not an alternative. Add "what was expected" to the intro's list.
- R1.2: `examples.md`, the session report with no problems found: the line `Time: 50 minutes on charter, 10 on opportunity (an unexpected currency switch in settings)` records an unexpected behaviour inside a report whose result is "no problems found". The charter puts "account settings" out of scope, and the report neither reports the behaviour as out-of-charter (MUST `findings-stay-inside-charter`) nor leaves it out of the clean result (MUST `clean-pass-reports-coverage`: "Padding a clean pass with severity-free observations is a fail"). The illustration takes a side on two owner open questions: whether an out-of-charter anomaly is raised or only listed as out-of-charter, and whether observations beside a clean result are a fail. Fix: make the opportunity time an off-charter area that held no anomaly and is not excluded by the charter (for example "10 on opportunity (the order-history page linked from the confirmation)"), and change the `New charter noted:` line to match.
- R1.3: `what-a-reviewer-looks-for.md`: the review focus weakens or leaves out MUST rules. There are three instances. (1) "kept within any step cap" treats the MUST `session-has-hard-step-cap` (25 browser steps per pass) as optional, which leans on the owner's open question on whether a step cap is kept at all. (2) "on the system's own origin" restates `stay-on-charter-origin` ("the site's own origin") in the open question's alternative wording. (3) Nothing checks the `clean-pass-reports-coverage` fail conditions (padding a clean pass with severity-free observations, a silent empty result) or the "URL or path" form of where in `anomaly-carries-all-four-parts`. Fix: write "kept within 25 browser steps per pass and on the site's own origin", and add checks that a clean pass is neither padded with severity-free observations nor returned empty, and that each anomaly gives where as a URL or path.
- R1.4: `running-a-chartered-session.md`: the how-to says it "shows one way to keep the rules", but none of its ten steps mentions four of the five MUST rules: `session-has-hard-step-cap` (step 5 sets only a time box), `stay-on-charter-origin` (step 6), `findings-stay-inside-charter` (step 6 covers only opportunity time and new charters, not reporting an anomaly in an excluded area as out-of-charter) and `clean-pass-reports-coverage` (step 10 does not say a clean pass is reported without padding and never as an empty result). Following the how-to as written therefore does not keep the rules it claims to show (completeness). Fix: add the 25-step cap per pass to step 5, the own-origin limit and the out-of-charter handling to step 6, and the no-padding, no-empty-result requirement to step 10, worded so that no open question is settled.
- R1.5: `rules.md`, two rules bundle independently testable behaviours under separate RFC keywords (recipe-quality behavioral-requirements, must-not-bundle-behaviors-into-one-requirement). (1) `look-for-what-specs-cannot-anticipate` asks a session to aim at what specifications and scripted tests do not cover, and also to treat documentation as unconfirmed until the product has been tried. A session can pass one and fail the other. (2) `charter-neither-too-narrow-nor-too-broad` asks a charter not to list individual tests, and also to be focused enough that the tester can tell when its target has been explored. Its build-bar line already checks the two separately. `finding-is-observed-not-inferred` is not an instance: its SHOULD and SHOULD NOT state one behaviour, positively and negatively. Fix: keep the prior name `look-for-what-specs-cannot-anticipate` for the first clause and move the documentation clause into a new SHOULD rule (for example `treat-documentation-as-unconfirmed`, citing `bolton-documentation-is-rumour`). Split `charter-neither-too-narrow-nor-too-broad` (a new rule, so it may be renamed) into two SHOULD rules, for example `charter-does-not-list-tests` and `charter-target-is-finishable`, each citing its claims. Add a build-bar line and a review-bar entry for each new rule.
- R1.6: `rationale.md`, last paragraph: "Most rules are recommendations because each rests on a single publisher's method, syllabus or guidance" is false for many of the SHOULD rules, which cite several independent publishers. Examples: `finding-gives-steps-to-reproduce` (ISTQB, Mozilla, Apple, Android, Rapid Software Testing, Microsoft), `report-anomaly-where-what-expected-repeatable` (ISTQB, ISO, Mozilla, Apple, Bolton, Rapid Software Testing), `session-is-time-boxed` (ISTQB, session-based test management, Lyndsay), `look-for-what-specs-cannot-anticipate` (ISO, ISTQB, Bolton, HTSM), `session-is-debriefed` (ISTQB, session-based test management), `finding-is-observed-not-inferred` (Rapid Software Testing, Mozilla, Bolton), `repeatability-states-retry` (Rapid Software Testing, Mozilla), `one-problem-per-finding` (Apple, Rapid Software Testing) and `finding-records-environment` (ISTQB, Rapid Software Testing). This is a source-fidelity error in the stated justification. Fix: give the reason the research actually gives: the research holds these rules at SHOULD against a practitioner-consensus bar, and the sources state them as reporting or method guidance a team can justifiably depart from. Drop the single-publisher claim, or limit it to the rules it is true of (for example `off-charter-work-logged-as-opportunity`, `dispatch-sessions-as-todo-charters`, `charter-set-kept-open`).

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/review.md:
- `# Review: exploratory-testing-charters`
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
