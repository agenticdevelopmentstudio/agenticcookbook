You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/task-breakdown/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/task-breakdown/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/planning/project-management/task-breakdown`.

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
- R1.1: `rules.md` **link-tasks-to-milestones**, plus its echoes in other parts (source fidelity, and owner-list open question 6). The research supports this rule only "at SHOULD in projects that use milestones" (research.md, Known solutions: "The sources treat milestones as optional grouping"). The cited `github-milestones-group-issues` says "You *can* use milestones". The rule drops that scope and applies to every task, which outruns its claims and answers the owner's open question ("whether every task must link to a milestone, or only tasks in a project that uses milestones"). Every instance: `rules.md` link-tasks-to-milestones ("Each task SHOULD be linked…"); `a-build-must-establish.md` ("every task is linked to the milestone it serves"); `a-complete-review-must-establish.md` ("Every task is linked to the milestone it serves."); `what-a-reviewer-looks-for.md` ("A task not linked to the milestone it serves."); `intro.md` ("link each task to the milestone it serves"); `breaking-work-into-tasks.md` step 5 ("link each task to the milestone or Sprint Goal it serves"). Fix: scope the rule the way the research does ("Where a project uses milestones, each task SHOULD be linked to the milestone it serves…"), and give the same scope to the bar, review-bar, review-focus, intro and how-to lines.
- R1.2: `rules.md` **blocker-links-the-blocking-item**, plus its echoes (source fidelity, and owner-list open question 5). The rule, and the parts that repeat it, require every blocked task to link to a blocking *item*. One of its two cited claims, `waiting-for-names-whom`, is the research's evidence that a blocker "can be a person or outside thing, not only a tracked item" (research.md, Known solutions). So the rule does not follow from that claim, and it answers the owner's open question ("whether a blocker must name a tracked item … or may name an outside cause in text"). Every instance: `rules.md` blocker-links-the-blocking-item; `a-build-must-establish.md` ("every blocked task has a \"blocked by\" link to what it waits on"); `a-complete-review-must-establish.md` ("linked to its specific blocker"); `what-a-reviewer-looks-for.md` ("with no \"blocked by\" link"); `handling-a-blocked-task.md` step 2 ("Link the blocked task to the item it waits on"); `intro.md` ("record each blocked task's blocker as a link"). Fix: scope the rule to blockers that are tracked items ("Where a blocked task waits on a tracked item, it SHOULD record it as a \"blocked by\" link…"), say nothing about outside causes, and give the same scope to the bar, review-bar, review-focus, how-to and intro lines.
- R1.3: `breaking-work-into-tasks.md` step 6 and `examples.md` contradict the owner-listed MUST **task-has-assignee-and-priority** ("Each todo MUST pass this check: Every todo has an assignee and priority"), and they answer owner-list open question 1. Every instance: step 6, "Leave tasks unassigned until work on them begins", tells the reader to break the MUST and settles the question in Cohn's favour. The worked task in `examples.md` (Title / Action / Done when / Expect / Milestone) has no assignee and no priority, so the guideline's own good example fails its MUST. No how-to step sets a priority or an assignee on a todo. Fix: reword step 6 so it no longer tells the reader to leave tasks unassigned (for example, "Whoever starts a task becomes its one assignee"). Add `Assignee:` and `Priority:` lines to the worked example. Add a how-to step that sets each todo's assignee and priority, so the informative parts satisfy the rule they sit beside and leave the open question to the owner.
- R1.4: The review and build parts state more than their rules (behavioral-requirements must-be-independently-testable: the bars must test what the rule says). Every instance: **breakdown-covers-all-scope** says only that the breakdown includes all the scope's work, with children adding up to their parent. It rightly leaves out "nothing outside scope", because the second check found that `wbs-hundred-percent-rule`'s quote does not state it. Yet `a-build-must-establish.md` ("and hold nothing outside it"), `a-complete-review-must-establish.md` ("and nothing outside it"), `what-a-reviewer-looks-for.md` ("or holds work outside it") and `breaking-work-into-tasks.md` step 1 ("and leave out anything outside it") all add it. **identify-blocked-tasks-and-blockers** marks a task as blocked only "where the tracker allows". `a-complete-review-must-establish.md` ("marked as blocked") and `what-a-reviewer-looks-for.md` ("A blocked task not marked as blocked") drop that condition. Fix: remove the out-of-scope clause from the four lines, and add "where the tracker allows" to the two blocked-marking lines.
- R1.5: `rules.md`: compound rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement and must-be-independently-testable). Several rules not on the owner list each bundle behaviours that can pass or fail separately, so the build bar cannot pass or fail a part. Every instance: **break-down-assign-and-prioritize-tasks** (break larger work into tasks; assign responsibility to a person or team; order the tasks, and the ordering also duplicates backlog-is-kept-ordered); **tasks-specific-and-actionable** (specific enough for everyone to understand; relevant to its story; a clear, defined outcome; a short title that states the task); **task-text-names-action-and-done-test** (names a physical, visible action; carries a done test the team agrees on); **identify-blocked-tasks-and-blockers** (identify each blocked task and its blocker; mark it blocked where the tracker allows; act to unblock it in a regular review of active work); **work-package-within-eighty-hours** (at most about 80 hours of effort; no longer than one reporting period). Fix: keep each prior name (break-down-assign-and-prioritize-tasks, tasks-specific-and-actionable, identify-blocked-tasks-and-blockers) on one behaviour, and split each other behaviour into its own named rule with its own citation and its own build-bar line. Where a part is already covered by another rule (ordering by backlog-is-kept-ordered), drop it instead of splitting it. Split the new rules task-text-names-action-and-done-test and work-package-within-eighty-hours the same way.
- R1.6: `rules.md`: unanchored relative terms (behavioral-requirements should-not-use-unanchored-relative-terms). Every instance: **split-large-estimates**, "a large estimate", has no threshold, although task-sized-hours-to-a-few-days supplies one (a week or more). **done-test-is-pass-fail**, "neither too vague nor too detailed": "too detailed" has no threshold, and the pass/fail clause already rules out "too vague". **tasks-specific-and-actionable**, "a short title", has no length or test. Fix: anchor "large" to the task-size rule (for example, "an estimate of a week or more, or none"), drop "nor too detailed" or give it a test, and replace "short" with a test (the title "states directly what the task is" already carries the requirement, so "short" can go).
- R1.7: `rationale.md`, paragraph 4 ("The vertical-slice, 100%-rule and GTD claims were each found by the second check to support their claim only in part…"). The second check refuted five claims, not three. The paragraph leaves out `decompose-to-one-day-or-less` (cited by break-down-assign-and-prioritize-tasks and task-sized-hours-to-a-few-days) and `trackers-record-blocked-by-links` (cited by identify-blocked-tasks-and-blockers and blocker-links-the-blocking-item). That makes it look as if those rules rest on fully confirmed claims. Fix: name all five refuted claims, and the rules that cite them, in that paragraph.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/task-breakdown, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/review.md:
- `# Review: task-breakdown`
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
