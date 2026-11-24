
### Breaking the work down

- **break-down-assign-and-prioritize-tasks**: Planning SHOULD break larger work down into smaller tasks, assign responsibility for the work to a person or team, and order the tasks. (claims: refinement-breaks-down-and-sizes, decompose-to-one-day-or-less, github-sub-issues-break-down-work, nasa-ram-assigns-responsibility, single-accountable-owner, backlog-is-ordered, prince2-work-package-assigns-products)
- **breakdown-covers-all-scope**: A breakdown SHOULD include all of the work in the project's scope, with the tasks under each piece of work adding up to all of that piece's work. (claims: wbs-hundred-percent-rule, nasa-wbs-defines-all-work)
- **split-into-vertical-slices**: A story or backlog item SHOULD be split into vertical slices, each defined by the outcome it delivers, rather than by architectural layer (one item for the UI, another for the database). (claims: split-vertically-not-by-layer, wbs-outcomes-not-actions)
- **doers-size-their-tasks**: Tasks SHOULD be sized by the people who will do them, not sized by management and handed down. (claims: doers-estimate-their-tasks, refinement-breaks-down-and-sizes, developers-own-the-sprint-backlog)

### Task size

- **task-sized-hours-to-a-few-days**: A task SHOULD be small enough to finish in hours to a couple of days; a task of a week or more has not been broken down enough. (claims: small-tasks-hours-to-days, decompose-to-one-day-or-less, not-small-enough-is-the-pitfall)
- **split-large-estimates**: A task with a large estimate, or one too hand-wavy for its duration to be known, SHOULD be broken into smaller tasks. (claims: linear-break-up-large-estimates, large-chunky-tasks-hide-design, not-small-enough-is-the-pitfall)
- **story-fits-one-iteration**: A user story above the tasks SHOULD be small enough to finish within one iteration. (claim: stories-small-enough-for-an-iteration)
- **work-package-within-eighty-hours**: In a work breakdown structure, a lowest-level work package SHOULD be no more than about 80 hours of effort and no longer than one reporting period. (claim: wbs-eighty-hour-heuristic)

### Task wording

- **tasks-specific-and-actionable**: Each task SHOULD be specific enough that everyone can understand what it involves: a concrete piece of work, relevant to the story it belongs to, with a clear, defined outcome and a short title that states directly what the task is. (claims: task-specific-enough-to-understand, task-title-states-the-task, smart-task-time-boxed)
- **task-text-names-action-and-done-test**: Each task's text SHOULD say what is to be done, as a physical, visible action rather than a vague verb such as "think", and when it is done, as a done test the team agrees on. (claims: next-action-physical-and-visible, task-title-states-the-task, task-has-a-done-test, scrum-definition-of-done, kanban-define-started-and-finished)
- **done-test-is-pass-fail**: A task's done test SHOULD be a set of clear, measurable pass/fail statements, neither too vague nor too detailed. (claims: acceptance-criteria-measurable-not-vague, task-has-a-done-test)
- **task-has-time-expectation**: Each task SHOULD carry a time expectation, not necessarily a formal estimate, so the person doing it knows when to seek help. (claim: smart-task-time-boxed)

### Ownership and order

- **started-task-has-one-owner**: Once work on a task begins, the task SHOULD have exactly one assignee, the person directly responsible for it, even where the tracker allows several. (claims: single-accountable-owner, assign-when-work-begins, github-assignees)
- **backlog-is-kept-ordered**: The backlog SHOULD be kept ordered, as a ranked list or by a tracker's priority levels. (claims: backlog-is-ordered, linear-priority-levels)
- **task-has-assignee-and-priority**: Each todo MUST pass this check: Every todo has an assignee and priority (claim: task-has-assignee-and-priority-prior)

### Milestones

- **link-tasks-to-milestones**: Each task SHOULD be linked to the milestone it serves (in Scrum, the Sprint Goal), so it traces to the schedule event its work delivers. (claims: nasa-tasks-and-milestones-from-wbs, github-milestones-group-issues, linear-issue-in-one-project, sprint-goal-links-the-work)
- **task-milestone-must-exist**: A todo's milestone MUST pass this check: no todo is assigned to a nonexistent milestone (claim: task-milestone-must-exist-prior)

### Blocked tasks

- **identify-blocked-tasks-and-blockers**: The team SHOULD identify each blocked task and what blocks it, mark the task as blocked where the tracker allows, and act to unblock it as part of reviewing active work regularly, as in a Daily Scrum. (claims: kanban-unblock-blocked-work, daily-scrum-identifies-impediments, trackers-record-blocked-by-links, jira-flag-with-reason)
- **blocker-links-the-blocking-item**: A blocked task SHOULD record what it waits on as a "blocked by" link from it to the blocking item. (claims: trackers-record-blocked-by-links, waiting-for-names-whom)
- **blocker-states-reason**: A blocked task SHOULD carry, on the item itself, a brief note giving the reason it is blocked, with enough text to name the cause. (claims: blocker-note-states-reason-and-dates, jira-flag-with-reason)
- **blocker-records-dates**: A blocker note MAY record the date the block started and the date it was resolved. (claim: blocker-note-states-reason-and-dates)
- **keep-resolved-blockers**: Resolved blocker notes SHOULD be kept, not thrown away, so they can be clustered to improve the process. (claim: blocker-note-states-reason-and-dates)
- **blocked-task-references-blocker**: A blocked todo MUST pass this check: blocked todos reference a specific blocker (claim: blocked-task-references-blocker-prior)

