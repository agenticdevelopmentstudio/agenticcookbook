I wrote both research files for `task-breakdown`, and the validate command prints `Research passed.` Every quote was checked against the text of the page it cites. The only differences are spaces that text extraction put before punctuation.

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/task-breakdown/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/task-breakdown/research/research.md`

**Claims per question** (43 in total)
- best-practices: 9 (6 researched, plus the 3 prior claims)
- known-solutions: 18
- platform-guidelines: 9
- experts-view: 7

**Verdicts** (rule: verdict, claim ids)
- break-down-assign-and-prioritize-tasks: supported (SHOULD) — refinement-breaks-down-and-sizes, decompose-to-one-day-or-less, github-sub-issues-break-down-work, nasa-ram-assigns-responsibility, single-accountable-owner, backlog-is-ordered, prince2-work-package-assigns-products
- tasks-specific-and-actionable: supported (SHOULD) — task-specific-enough-to-understand, task-title-states-the-task, next-action-physical-and-visible, smart-task-time-boxed
- link-tasks-to-milestones: supported (SHOULD, where milestones are used) — nasa-tasks-and-milestones-from-wbs, github-milestones-group-issues, linear-issue-in-one-project, sprint-goal-links-the-work
- identify-blocked-tasks-and-blockers: supported (SHOULD) — kanban-unblock-blocked-work, daily-scrum-identifies-impediments, trackers-record-blocked-by-links, jira-flag-with-reason
- task-has-assignee-and-priority: contradicted — task-has-assignee-and-priority-prior, assign-when-work-begins, developers-own-the-sprint-backlog, backlog-is-ordered, linear-priority-levels
- blocked-task-references-blocker: unsupported as MUST; sources support SHOULD — blocked-task-references-blocker-prior, trackers-record-blocked-by-links, jira-flag-with-reason, blocker-note-states-reason-and-dates
- task-milestone-must-exist: unsupported; MAY at most, as a house check — task-milestone-must-exist-prior, github-milestones-group-issues
- task-text-names-action-and-done-test: new (SHOULD; answers *Actionable task wording*) — next-action-physical-and-visible, task-title-states-the-task, task-has-a-done-test, scrum-definition-of-done, kanban-define-started-and-finished, acceptance-criteria-measurable-not-vague
- task-sized-hours-to-a-few-days: new (SHOULD) — small-tasks-hours-to-days, decompose-to-one-day-or-less, linear-break-up-large-estimates, not-small-enough-is-the-pitfall, large-chunky-tasks-hide-design, stories-small-enough-for-an-iteration, wbs-eighty-hour-heuristic
- blocker-links-the-blocking-item: new (SHOULD; answers *Task blocker naming*) — trackers-record-blocked-by-links, waiting-for-names-whom
- blocker-states-reason-and-since: new (SHOULD for the reason, MAY for the dates) — blocker-note-states-reason-and-dates, jira-flag-with-reason
- started-task-has-one-owner: new (SHOULD) — single-accountable-owner, assign-when-work-begins, github-assignees
- backlog-is-kept-ordered: new (SHOULD) — backlog-is-ordered, linear-priority-levels
- split-into-vertical-slices: new (SHOULD) — split-vertically-not-by-layer, wbs-outcomes-not-actions
- breakdown-covers-all-scope: new (SHOULD) — wbs-hundred-percent-rule, nasa-wbs-defines-all-work
- doers-size-their-tasks: new (SHOULD) — doers-estimate-their-tasks, refinement-breaks-down-and-sizes, developers-own-the-sprint-backlog

**Source gaps**
- pmi.org, iso.org and GAO refused the fetches, so the WBS 100% rule and the 80-hour rule come from Wikipedia. The PRINCE2 work package comes from prince2.wiki. Both are secondary sources, and their trust bases say so.
- No study backs any task-size limit. Every size figure is a heuristic from a method owner or practitioner.

**Owner decisions** (six entries in `open_questions`)
- Whether an assignee is required only on started work.
- Priority field or backlog order.
- Whether to keep the milestone-exists check.
- Which size limit to state.
- Whether a blocker must be a tracked item or may be an outside cause.
- Whether every task needs a milestone.
