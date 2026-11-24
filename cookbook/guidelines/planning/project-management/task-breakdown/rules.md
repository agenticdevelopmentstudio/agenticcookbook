
### Breaking the work down

- **break-down-assign-and-prioritize-tasks**: Planning SHOULD break each backlog item that is bigger than task-sized-hours-to-a-few-days allows into smaller tasks. (claims: refinement-breaks-down-and-sizes, decompose-to-one-day-or-less, github-sub-issues-break-down-work)
- **work-has-a-responsible-owner**: Each piece of work that is broken into tasks, such as a work package or a parent item, SHOULD have a person or team responsible for it. (claims: nasa-ram-assigns-responsibility, prince2-work-package-assigns-products)
- **breakdown-covers-all-scope**: A breakdown SHOULD include all of the work in the project's scope, project management included. (claims: wbs-hundred-percent-rule, nasa-wbs-defines-all-work)
- **work-package-activities-add-up**: In a work breakdown structure, the activities in each work package SHOULD add up to all of the work needed to complete that work package. (claim: wbs-hundred-percent-rule)
- **split-into-vertical-slices**: A story or backlog item SHOULD be split into vertical slices, each defined by the outcome it delivers, rather than by architectural layer (one item for the UI, another for the database). (claims: split-vertically-not-by-layer, wbs-outcomes-not-actions)
- **doers-size-their-tasks**: Tasks SHOULD be sized by the people who will do them, not sized by management and handed down. (claims: doers-estimate-their-tasks, refinement-breaks-down-and-sizes, developers-own-the-sprint-backlog)

### Task size

- **task-sized-hours-to-a-few-days**: A task SHOULD be small enough to finish in hours to a couple of days; a task of a week or more has not been broken down enough. (claims: small-tasks-hours-to-days, decompose-to-one-day-or-less, not-small-enough-is-the-pitfall)
- **split-large-estimates**: A task estimated at a week or more SHOULD be broken into smaller tasks. (claims: linear-break-up-large-estimates, small-tasks-hours-to-days, not-small-enough-is-the-pitfall)
- **split-unestimable-tasks**: A task whose duration cannot be estimated, because the work behind it has not been thought through, SHOULD be broken into smaller tasks. (claims: large-chunky-tasks-hide-design, linear-break-up-large-estimates, task-title-states-the-task)
- **story-fits-one-iteration**: A user story above the tasks SHOULD be small enough to finish within one iteration. (claim: stories-small-enough-for-an-iteration)
- **work-package-within-eighty-hours**: In a work breakdown structure, a lowest-level work package SHOULD be no more than about 80 hours of effort. (claim: wbs-eighty-hour-heuristic)
- **work-package-within-one-reporting-period**: In a work breakdown structure, a lowest-level work package SHOULD take no longer than one reporting period. (claim: wbs-eighty-hour-heuristic)

### Task wording

- **tasks-specific-and-actionable**: Each task SHOULD be specific enough that everyone on the team can understand what it involves. (claim: task-specific-enough-to-understand)
- **task-states-its-outcome**: Each task SHOULD describe a concrete piece of work with a defined outcome. (claim: task-specific-enough-to-understand)
- **task-serves-its-story**: Each task SHOULD contribute to the story it belongs to. (claim: smart-task-time-boxed)
- **task-title-states-the-task**: Each task's title SHOULD state directly, in plain language, what the task is. (claim: task-title-states-the-task)
- **task-names-visible-action**: Each task's text SHOULD name a physical, visible action, so that anyone can tell it was done, rather than a vague verb such as "think". (claim: next-action-physical-and-visible)
- **task-has-done-test**: Each task SHOULD carry a done test the team agrees on: the conditions the work must meet to count as done. (claims: task-has-a-done-test, scrum-definition-of-done, kanban-define-started-and-finished, next-action-physical-and-visible)
- **done-test-is-pass-fail**: A task's done test SHOULD be a set of measurable pass/fail statements. (claims: acceptance-criteria-measurable-not-vague, task-has-a-done-test)
- **task-has-time-expectation**: Each task SHOULD carry a time expectation, not necessarily a formal estimate, so the person doing it knows when to seek help. (claim: smart-task-time-boxed)

### Ownership and order

- **started-task-has-one-owner**: Once work on a task begins, the task SHOULD have exactly one assignee, the person directly responsible for it, even where the tracker allows several. (claims: single-accountable-owner, assign-when-work-begins, github-assignees)
- **backlog-is-kept-ordered**: The backlog SHOULD be kept ordered, as a ranked list or by a tracker's priority levels. (claims: backlog-is-ordered, linear-priority-levels)
- **task-has-assignee-and-priority**: Each todo MUST pass this check: Every todo has an assignee and priority (claim: task-has-assignee-and-priority-prior)

### Milestones

- **link-tasks-to-milestones**: Where a project uses milestones, each task SHOULD be linked to the milestone it serves (in Scrum, the Sprint Goal). (claims: nasa-tasks-and-milestones-from-wbs, github-milestones-group-issues, linear-issue-in-one-project, sprint-goal-links-the-work)
- **task-milestone-must-exist**: A todo's milestone MUST pass this check: no todo is assigned to a nonexistent milestone (claim: task-milestone-must-exist-prior)

### Blocked tasks

- **identify-blocked-tasks-and-blockers**: The team SHOULD identify each blocked task, and what blocks it, when it reviews its active work, as in a Daily Scrum. (claims: daily-scrum-identifies-impediments, kanban-unblock-blocked-work)
- **mark-blocked-tasks**: Where the tracker allows it, a blocked task SHOULD be marked as blocked, so it shows apart from work that is not waiting. (claims: trackers-record-blocked-by-links, jira-flag-with-reason, waiting-for-names-whom)
- **remove-identified-blockers**: The team SHOULD act to remove each blocker it identifies. (claims: kanban-unblock-blocked-work, daily-scrum-identifies-impediments)
- **blocker-links-the-blocking-item**: Where a blocked task waits on a tracked item, it SHOULD record that item as a "blocked by" link from the blocked task. (claim: trackers-record-blocked-by-links)
- **blocker-states-reason**: A blocked task SHOULD carry, on the item itself, a brief note with enough text to name the cause of the block. (claims: blocker-note-states-reason-and-dates, jira-flag-with-reason)
- **blocker-records-dates**: A blocker note MAY record the date the block started and the date it was resolved. (claim: blocker-note-states-reason-and-dates)
- **keep-resolved-blockers**: Resolved blocker notes SHOULD be kept, not thrown away, so they can be clustered to improve the process. (claim: blocker-note-states-reason-and-dates)
- **blocked-task-references-blocker**: A blocked todo MUST pass this check: blocked todos reference a specific blocker (claim: blocked-task-references-blocker-prior)

