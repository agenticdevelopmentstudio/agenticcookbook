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
