You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/milestone-scheduling/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/milestone-scheduling/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/planning/project-management/milestone-scheduling`.

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
- R1.1: `rules.md`, `define-and-sequence-milestones` against `milestone-has-status-and-target-date`: the same behaviours are required twice, at two strengths. `define-and-sequence-milestones` says Planning SHOULD "give each a target date" and "track each one's status". The owner-listed `milestone-has-status-and-target-date` holds "Every milestone has a status and target date" at MUST. Under behavioral-requirements (must-use-keywords-with-defined-semantics) and cookbook-compliance (must-not-contradict), one behaviour cannot be both absolute and waivable. This is the same class of finding decision-records R1.1 raised. The rule also bundles five behaviours into one sentence: define, sequence, date, record the chains, and track status and progress (behavioral-requirements must-not-bundle-behaviors-into-one-requirement). The overlap shows up again in `a-build-must-establish.md` (the `define-and-sequence-milestones` line), in the first bullet of `what-a-reviewer-looks-for.md` ("not defined, sequenced, dated or tracked") and in the first bullet of `a-complete-review-must-establish.md` ("sequenced, dated and tracked"). Fix: keep the rule's fixed name, but cut it to define the milestones, put them in sequence and record the dependency chains between them (same citations). Drop the target date and the status from it; they belong to the owner-listed rule, and their strength is the owner's open question. Move progress tracking into a new SHOULD rule, e.g. `track-milestone-progress`: "Each milestone's progress SHOULD be tracked, for example as the completion of the work linked to it (claims: github-milestones-due-date-progress, linear-milestones-optional-date)". Give it a build-bar line, then narrow the build-bar, review-focus and review-bar wording to match.
- R1.2: `rules.md`, `justify-missing-logic` and `justify-unavoidable-hard-constraints` (these are the only two instances): both are SHOULD, but each cites a claim that states the requirement as "must", and neither claim was refuted. `missing-logic-justified` (trust 74, second check confirmed) quotes GAO: "any activity that is missing predecessor or successor logic must be clearly justified in the schedule documentation". `avoid-hard-date-constraints` (trust 74) quotes GAO: "If a hard constraint cannot be avoided, it must be used judiciously and must be fully justified by referring to some controlling event outside the schedule". The second check notes that the quote "matches the claim's scope and strength". Under criterion 3, each rule sits at the strength of the weakest claim it cites, so these two are understated. Both rules are conditional on a departure (a missing link, an unavoidable constraint), so MUST does not make the underlying SHOULD rules absolute. I checked every other rule for an unrefuted "must" claim cited at SHOULD and found none. `sequence-with-logic` quotes "must be logically sequenced", but it is refuted and cannot carry MUST. Fix: raise both rules to MUST: "...MUST be justified in the schedule documentation" and "...MUST be justified in the schedule's basis document by the event outside the schedule that controls it". Then update `rationale.md` paragraphs 1 and 2. They currently say "the rules carry its practice at SHOULD" and "The cycle rule is the one MUST"; they should name the two justification MUSTs too.
- R1.3: `examples.md`, the sentence after the Python block: the cycle message it shows, `cycle in milestone chain: start -> launch -> beta -> api-freeze -> start`, is not what the code prints. I added `depends_on["start"] = {"launch"}` and ran the example under Python 3 with several `PYTHONHASHSEED` values. Every run printed `cycle in milestone chain: api-freeze -> docs-ready -> launch -> start -> api-freeze`. graphlib lists the cycle in successor order, each node followed by one that depends on it. The example shows dependency (predecessor) order, which graphlib never prints, and it names `beta` where graphlib names `docs-ready`. The hedge "(the order the error lists varies)" does not cover a reversed direction. This is a factual error against `topological-order-iff-acyclic`, which says graphlib reports the cycle. Fix: replace it with the real output, `cycle in milestone chain: api-freeze -> docs-ready -> launch -> start -> api-freeze`. Then change the parenthetical to say graphlib lists each milestone followed by one that depends on it, starting from whichever node it reaches first.
- R1.4: `artifact.json` `related`, `intro.md` paragraph 2 and `rationale.md` last paragraph: the guideline hands parts of its scope to two indexed siblings, but it names them only by freeform description ("Delivery dependencies on other teams, tasks and their blockers ... are covered by their own guidelines"; "belong to the dependency-tracking guideline, tasks and their blockers to the task-breakdown guideline"). `related` is `[]`. The two siblings are dependency-tracking (`3f978ba7-c8c1-4b53-8fda-12e5a6966b75`) and task-breakdown (`f264cc0b-45d3-4593-a437-7371610c5a8a`). cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) and criterion 6 (`related` matches the new text) both apply, as in decision-records R1.4. Fix: add both UUIDs to `related`. In `rationale.md`, write them as `[adc.guideline.planning.project-management.dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75)` and `[adc.guideline.planning.project-management.task-breakdown](cookbook:f264cc0b-45d3-4593-a437-7371610c5a8a)`, and link the intro's mentions the same way. The project-record-linking mention stays freeform, because that topic has no artifact or UUID yet.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/milestone-scheduling, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/review.md:
- `# Review: milestone-scheduling`
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
