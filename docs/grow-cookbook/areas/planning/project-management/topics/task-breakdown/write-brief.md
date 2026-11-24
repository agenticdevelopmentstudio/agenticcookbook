# Write brief: task-breakdown

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/task-breakdown (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/task-breakdown/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/task-breakdown/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>

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

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- break-down-assign-and-prioritize-tasks: supported (claims: refinement-breaks-down-and-sizes, decompose-to-one-day-or-less, github-sub-issues-break-down-work, nasa-ram-assigns-responsibility, single-accountable-owner, backlog-is-ordered, prince2-work-package-assigns-products)
- tasks-specific-and-actionable: supported (claims: task-specific-enough-to-understand, task-title-states-the-task, next-action-physical-and-visible, smart-task-time-boxed)
- link-tasks-to-milestones: supported (claims: nasa-tasks-and-milestones-from-wbs, github-milestones-group-issues, linear-issue-in-one-project, sprint-goal-links-the-work)
- identify-blocked-tasks-and-blockers: supported (claims: kanban-unblock-blocked-work, daily-scrum-identifies-impediments, trackers-record-blocked-by-links, jira-flag-with-reason)
- task-has-assignee-and-priority: contradicted (claims: task-has-assignee-and-priority-prior, assign-when-work-begins, developers-own-the-sprint-backlog, backlog-is-ordered, linear-priority-levels)
- blocked-task-references-blocker: unsupported (claims: blocked-task-references-blocker-prior, trackers-record-blocked-by-links, jira-flag-with-reason, blocker-note-states-reason-and-dates)
- task-milestone-must-exist: unsupported (claims: task-milestone-must-exist-prior, github-milestones-group-issues)
- task-text-names-action-and-done-test: new (claims: next-action-physical-and-visible, task-title-states-the-task, task-has-a-done-test, scrum-definition-of-done, kanban-define-started-and-finished, acceptance-criteria-measurable-not-vague)
- task-sized-hours-to-a-few-days: new (claims: small-tasks-hours-to-days, decompose-to-one-day-or-less, linear-break-up-large-estimates, not-small-enough-is-the-pitfall, large-chunky-tasks-hide-design, stories-small-enough-for-an-iteration, wbs-eighty-hour-heuristic)
- blocker-links-the-blocking-item: new (claims: trackers-record-blocked-by-links, waiting-for-names-whom)
- blocker-states-reason-and-since: new (claims: blocker-note-states-reason-and-dates, jira-flag-with-reason)
- started-task-has-one-owner: new (claims: single-accountable-owner, assign-when-work-begins, github-assignees)
- backlog-is-kept-ordered: new (claims: backlog-is-ordered, linear-priority-levels)
- split-into-vertical-slices: new (claims: split-vertically-not-by-layer, wbs-outcomes-not-actions)
- breakdown-covers-all-scope: new (claims: wbs-hundred-percent-rule, nasa-wbs-defines-all-work)
- doers-size-their-tasks: new (claims: doers-estimate-their-tasks, refinement-breaks-down-and-sizes, developers-own-the-sprint-backlog)

Second-check corrections, refuted (criteria 3 applies to these claims):
- decompose-to-one-day-or-less: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- trackers-record-blocked-by-links: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- waiting-for-names-whom: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST
- split-vertically-not-by-layer: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST
- wbs-hundred-percent-rule: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **task-has-assignee-and-priority** — verdict `contradicted` (claims: task-has-assignee-and-priority-prior, assign-when-work-begins, developers-own-the-sprint-backlog, backlog-is-ordered, linear-priority-levels). Prior text, kept word for word: "Every todo has an assignee and priority" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Experts advise against assigning every task up front at planning: each person claims their first task and then chooses the next as work progresses, so assignment happens close to when work begins.
  - against: In Scrum the Sprint Backlog, including its breakdown into work, is a plan by and for the Developers, who are accountable for creating it.
  - against: The Scrum Guide orders the Product Backlog, with the Product Owner accountable for that order, rather than assigning each item a priority label.
  - against: Linear offers a fixed five-value priority, including 'No priority', so a tracker's priority field may be left unset.
- **blocked-task-references-blocker** — verdict `unsupported` (claims: blocked-task-references-blocker-prior, trackers-record-blocked-by-links, jira-flag-with-reason, blocker-note-states-reason-and-dates). Prior text, kept word for word: "blocked todos reference a specific blocker" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: GitHub, Jira and Linear each record a blocker as a 'blocked by' / 'blocks' link from the blocked item to the item it waits on, and mark blocked items visibly.
  - against: Jira marks a blocked item with a flag (stored as 'Impediment') and lets the user add a comment giving the reason when flagging or unflagging it.
  - against: Practitioners record each blocker on the blocked item with a brief reason that names its cause, and its start and resolved dates or days blocked, then keep resolved blockers to cluster them for improvement.
- **task-milestone-must-exist** — verdict `unsupported` (claims: task-milestone-must-exist-prior, github-milestones-group-issues). Prior text, kept word for word: "no todo is assigned to a nonexistent milestone" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: GitHub milestones group issues to track their progress; an issue is associated with a milestone chosen from the repository's existing milestones.

## Open questions

- Whether 'every todo has an assignee' should become 'every started todo has exactly one assignee', leaving unstarted todos unassigned as Cohn and Scrum.org advise, or stay a check on every todo as a projectteam convention; the owner decides.
- Whether 'priority' is kept as a per-task field (as Linear and Jira offer) or replaced by backlog order (as the Scrum Guide has it), and whether 'no priority' is an allowed value.
- Whether 'no todo is assigned to a nonexistent milestone' is kept as a house referential-integrity check; no external source states it, though trackers only offer existing milestones to pick.
- Which task-size limit the guideline states: one day or less (Scrum Guide), hours to a couple of days with a week as too big (DORA), 2 to 16 hours (Spolsky), or 80 hours (WBS heuristic); the sources agree on 'small' but not on one number.
- Whether a blocker must name a tracked item (a blocked-by link) or may name an outside cause in text (a vendor, a missing decision), and whether its start date is required.
- Whether every task must link to a milestone, or only tasks in a project that uses milestones; the sources describe milestones as optional grouping.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `rules.md` **link-tasks-to-milestones**, plus its echoes in other parts (source fidelity, and owner-list open question 6). The research supports this rule only "at SHOULD in projects that use milestones" (research.md, Known solutions: "The sources treat milestones as optional grouping"). The cited `github-milestones-group-issues` says "You *can* use milestones". The rule drops that scope and applies to every task, which outruns its claims and answers the owner's open question ("whether every task must link to a milestone, or only tasks in a project that uses milestones"). Every instance: `rules.md` link-tasks-to-milestones ("Each task SHOULD be linked…"); `a-build-must-establish.md` ("every task is linked to the milestone it serves"); `a-complete-review-must-establish.md` ("Every task is linked to the milestone it serves."); `what-a-reviewer-looks-for.md` ("A task not linked to the milestone it serves."); `intro.md` ("link each task to the milestone it serves"); `breaking-work-into-tasks.md` step 5 ("link each task to the milestone or Sprint Goal it serves"). Fix: scope the rule the way the research does ("Where a project uses milestones, each task SHOULD be linked to the milestone it serves…"), and give the same scope to the bar, review-bar, review-focus, intro and how-to lines.
- R1.2: `rules.md` **blocker-links-the-blocking-item**, plus its echoes (source fidelity, and owner-list open question 5). The rule, and the parts that repeat it, require every blocked task to link to a blocking *item*. One of its two cited claims, `waiting-for-names-whom`, is the research's evidence that a blocker "can be a person or outside thing, not only a tracked item" (research.md, Known solutions). So the rule does not follow from that claim, and it answers the owner's open question ("whether a blocker must name a tracked item … or may name an outside cause in text"). Every instance: `rules.md` blocker-links-the-blocking-item; `a-build-must-establish.md` ("every blocked task has a \"blocked by\" link to what it waits on"); `a-complete-review-must-establish.md` ("linked to its specific blocker"); `what-a-reviewer-looks-for.md` ("with no \"blocked by\" link"); `handling-a-blocked-task.md` step 2 ("Link the blocked task to the item it waits on"); `intro.md` ("record each blocked task's blocker as a link"). Fix: scope the rule to blockers that are tracked items ("Where a blocked task waits on a tracked item, it SHOULD record it as a \"blocked by\" link…"), say nothing about outside causes, and give the same scope to the bar, review-bar, review-focus, how-to and intro lines.
- R1.3: `breaking-work-into-tasks.md` step 6 and `examples.md` contradict the owner-listed MUST **task-has-assignee-and-priority** ("Each todo MUST pass this check: Every todo has an assignee and priority"), and they answer owner-list open question 1. Every instance: step 6, "Leave tasks unassigned until work on them begins", tells the reader to break the MUST and settles the question in Cohn's favour. The worked task in `examples.md` (Title / Action / Done when / Expect / Milestone) has no assignee and no priority, so the guideline's own good example fails its MUST. No how-to step sets a priority or an assignee on a todo. Fix: reword step 6 so it no longer tells the reader to leave tasks unassigned (for example, "Whoever starts a task becomes its one assignee"). Add `Assignee:` and `Priority:` lines to the worked example. Add a how-to step that sets each todo's assignee and priority, so the informative parts satisfy the rule they sit beside and leave the open question to the owner.
- R1.4: The review and build parts state more than their rules (behavioral-requirements must-be-independently-testable: the bars must test what the rule says). Every instance: **breakdown-covers-all-scope** says only that the breakdown includes all the scope's work, with children adding up to their parent. It rightly leaves out "nothing outside scope", because the second check found that `wbs-hundred-percent-rule`'s quote does not state it. Yet `a-build-must-establish.md` ("and hold nothing outside it"), `a-complete-review-must-establish.md` ("and nothing outside it"), `what-a-reviewer-looks-for.md` ("or holds work outside it") and `breaking-work-into-tasks.md` step 1 ("and leave out anything outside it") all add it. **identify-blocked-tasks-and-blockers** marks a task as blocked only "where the tracker allows". `a-complete-review-must-establish.md` ("marked as blocked") and `what-a-reviewer-looks-for.md` ("A blocked task not marked as blocked") drop that condition. Fix: remove the out-of-scope clause from the four lines, and add "where the tracker allows" to the two blocked-marking lines.
- R1.5: `rules.md`: compound rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement and must-be-independently-testable). Several rules not on the owner list each bundle behaviours that can pass or fail separately, so the build bar cannot pass or fail a part. Every instance: **break-down-assign-and-prioritize-tasks** (break larger work into tasks; assign responsibility to a person or team; order the tasks, and the ordering also duplicates backlog-is-kept-ordered); **tasks-specific-and-actionable** (specific enough for everyone to understand; relevant to its story; a clear, defined outcome; a short title that states the task); **task-text-names-action-and-done-test** (names a physical, visible action; carries a done test the team agrees on); **identify-blocked-tasks-and-blockers** (identify each blocked task and its blocker; mark it blocked where the tracker allows; act to unblock it in a regular review of active work); **work-package-within-eighty-hours** (at most about 80 hours of effort; no longer than one reporting period). Fix: keep each prior name (break-down-assign-and-prioritize-tasks, tasks-specific-and-actionable, identify-blocked-tasks-and-blockers) on one behaviour, and split each other behaviour into its own named rule with its own citation and its own build-bar line. Where a part is already covered by another rule (ordering by backlog-is-kept-ordered), drop it instead of splitting it. Split the new rules task-text-names-action-and-done-test and work-package-within-eighty-hours the same way.
- R1.6: `rules.md`: unanchored relative terms (behavioral-requirements should-not-use-unanchored-relative-terms). Every instance: **split-large-estimates**, "a large estimate", has no threshold, although task-sized-hours-to-a-few-days supplies one (a week or more). **done-test-is-pass-fail**, "neither too vague nor too detailed": "too detailed" has no threshold, and the pass/fail clause already rules out "too vague". **tasks-specific-and-actionable**, "a short title", has no length or test. Fix: anchor "large" to the task-size rule (for example, "an estimate of a week or more, or none"), drop "nor too detailed" or give it a test, and replace "short" with a test (the title "states directly what the task is" already carries the requirement, so "short" can go).
- R1.7: `rationale.md`, paragraph 4 ("The vertical-slice, 100%-rule and GTD claims were each found by the second check to support their claim only in part…"). The second check refuted five claims, not three. The paragraph leaves out `decompose-to-one-day-or-less` (cited by break-down-assign-and-prioritize-tasks and task-sized-hours-to-a-few-days) and `trackers-record-blocked-by-links` (cited by identify-blocked-tasks-and-blockers and blocker-links-the-blocking-item). That makes it look as if those rules rest on fully confirmed claims. Fix: name all five refuted claims, and the rules that cite them, in that paragraph.

## Round 2 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R2.1: `rules.md` **work-package-within-eighty-hours** and **work-package-within-one-reporting-period**, plus their echoes, in text that changed this round (source fidelity against `wbs-eighty-hour-heuristic`, and behavioral-requirements must-be-independently-testable: the bars must test what the rule says). The claim says WBS heuristics cap a work package "at about 80 hours". It is a rule of thumb with no study behind it (its trust basis). The split in this round dropped "about", so the rule and its echoes now state a hard 80-hour line that the claim does not give. The echoes in the review bar, review focus and how-to also dropped the rule's WBS scope ("In a work breakdown structure", "where a WBS is used"; the previous draft said "WBS work package"). As a result they apply the 80-hour and reporting-period limits, and the add-up check, to every work package. Every instance: `rules.md` work-package-within-eighty-hours ("no more than 80 hours of effort"); `a-build-must-establish.md` work-package-within-eighty-hours ("80 hours of effort or less"); `a-complete-review-must-establish.md` line 2 ("each work package's activities add up to its work", no WBS scope) and line 4 ("every work package is within 80 hours and one reporting period"); `what-a-reviewer-looks-for.md` line 2 ("a work package whose activities do not add up to its work", no WBS scope) and line 5 ("a work package over 80 hours or one reporting period"); `breaking-work-into-tasks.md` step 4 ("work packages within 80 hours and one reporting period"). Fix: restore "about 80 hours" in the rule and in every 80-hour echo. Restore the WBS scope ("in a work breakdown structure" or "WBS work package") on the review-bar, review-focus and how-to lines that name work packages.

## Round 3 findings

Verdict: pass. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

none
