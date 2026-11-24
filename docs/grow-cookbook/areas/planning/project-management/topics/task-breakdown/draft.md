---
id: f264cc0b-45d3-4593-a437-7371610c5a8a
title: "Task Breakdown"
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Break work into small, specific tasks with a done test, sized by their doers: one owner once started, an ordered backlog, milestone links and named blockers."
platforms: []
tags:
  - task-breakdown
  - planning
  - project-management
  - work-breakdown-structure
  - blockers
depends-on: []
related:
  - b224ef56-65f5-45fd-8842-767b20df6736
  - 138eed2b-6b13-40ac-8c99-1f7860420b42
references:
  - https://scrumguides.org/scrum-guide.html
  - https://kanbanguides.org/english/
  - https://framework.scaledagile.com/story
  - https://www.nasa.gov/wp-content/uploads/2023/08/nasa-work-breakdown-structure-handbook.pdf
  - https://en.wikipedia.org/wiki/Work_breakdown_structure
  - https://prince2.wiki/management-products/work-package/
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
  - https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/assigning-issues-and-pull-requests-to-other-github-users
  - https://linear.app/docs/issue-property
  - https://linear.app/docs/assigning-issues
  - https://linear.app/docs/projects
  - https://linear.app/method/write-issues-not-user-stories
  - https://support.atlassian.com/jira-software-cloud/docs/flag-an-issue/
  - https://support.atlassian.com/jira-software-cloud/docs/create-or-remove-dependencies-on-your-timeline/
  - https://www.atlassian.com/work-management/project-management/acceptance-criteria
  - https://xp123.com/invest-in-good-stories-and-smart-tasks/
  - https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
  - https://www.joelonsoftware.com/2000/03/29/painless-software-schedules/
  - https://dora.dev/capabilities/working-in-small-batches/
  - https://www.mountaingoatsoftware.com/blog/should-a-team-assign-work-during-sprint-planning
  - https://www.scrum.org/resources/blog/why-pre-assigning-tasks-scrum-bad-idea-and-what-do-instead
  - https://handbook.gitlab.com/handbook/people-group/directly-responsible-individuals/
  - https://www.infoq.com/articles/blockers-defects-process-improvement
  - https://gettingthingsdone.com/2010/10/some-key-gtd-definitions/
  - https://facilethings.com/blog/en/what-is-the-next-action
approved-by: ""
approved-date: ""
triggers: []
---

# Task Breakdown

Break each backlog item into small tasks, sized by the people who will do them, each specific enough to understand, naming a visible action and carrying a pass/fail done test the team agrees on. Give each started task one owner, keep the backlog ordered, link tasks to their milestones where the project uses milestones, and give each blocked task a brief reason, with a "blocked by" link where it waits on a tracked item.

This guideline covers how work is broken into tasks for any delivery team: what makes a task specific and actionable, how large a task may be, who owns it, how tasks are ordered, how a task links to its milestone, and how a blocked task names what it waits on. Writing the spec before code, ordering thin end-to-end slices, milestones themselves and the general record-linking convention are covered elsewhere. A team following this guideline meets the rules below; each rule's keyword says how strictly.

## Rules

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

## Breaking work into tasks

*This section is informative.*

1. Start from the whole scope. List every piece of work it holds, including project management. Where a work breakdown structure is used, check that the activities under each work package add up to all of that package's work.
2. Name the person or team responsible for each piece of work being broken down.
3. Split each story or backlog item into vertical slices: each slice delivers an outcome a user or the project can see, from interface to storage, not one layer of the system.
4. Let the people who will do the work break each slice into tasks and size them. A task estimated at a week or more, or one nobody can estimate because its work has not been thought through, is split again. Stories stay within one iteration, and WBS work packages within about 80 hours and one reporting period.
5. Write each task: a title that says what it is, the outcome it delivers to its story, the visible action it takes, a done test of pass/fail statements the team agrees on, and a rough time expectation. A sub-issue keeps its link to the parent item.
6. Order the backlog, as a ranked list or by the tracker's priority levels, and give each todo an assignee and a priority.
7. Where the project uses milestones, link each task to the milestone it serves; in Scrum, the Sprint Goal plays that part.
8. When work on a task begins, the person who starts it is its one assignee.

## Handling a blocked task

*This section is informative.*

1. Bring blocked tasks up when active work is reviewed (in Scrum, the Daily Scrum), naming what blocks each one.
2. Where the tracker allows it, mark the task as blocked: GitHub and Linear show it from its "blocked by" link, and Jira adds a flag.
3. Where the task waits on a tracked item, add a "blocked by" link from the task to that item.
4. Add a brief note on the task naming the cause; teams that track flow also write the date the block started.
5. Act to remove the block.
6. When it clears, write the resolved date if the team records dates, and keep the note with the other resolved blockers so recurring causes show up.

## Examples

*This section is informative.*

A task too large and too vague to act on:

```text
Internet integration                       (estimate: 3 weeks)
```

The same work broken down. Each task is small, names a visible action and carries a done test:

```text
Title:     Add the "Sign in with GitHub" button to the login page
Action:    Render the button and wire it to the OAuth start endpoint
Done when: - The button appears on /login for signed-out users
           - Clicking it redirects to github.com/login/oauth/authorize
           - The existing email sign-in still passes its tests
Expect:    about half a day
Assignee:  Dana
Priority:  High
Milestone: Beta sign-up
```

A layer split, and a vertical split of the same story:

```text
By layer (avoid):   "Build the export UI"  /  "Add the export table"  /  "Write the export API"
Vertical slices:    "Export one report as CSV"  /  "Export a filtered report"  /  "Schedule a weekly export"
```

A blocked task waiting on a tracked item:

```text
Blocked by:  #412 Rotate the staging OAuth secret
Note:        Waiting on the new client secret from the identity team; sign-in fails without it.
Blocked:     2026-11-20 -> 2026-11-22
```

## What a reviewer looks for

- A backlog item bigger than a task left unbroken, or a piece of broken-down work with no responsible person or team.
- A breakdown that leaves part of the scope out, or, in a work breakdown structure, a work package whose activities do not add up to its work.
- Stories split by architectural layer instead of into vertical slices.
- Sizes set by someone other than the people who will do the work.
- A task of a week or more, or one that cannot be estimated, left unsplit; a story too big for one iteration; a WBS work package over about 80 hours or one reporting period.
- A task that is not specific, states no outcome, does not serve its story, has a title that does not say what it is, or names a vague verb such as "think".
- A task with no done test, or one whose criteria are not measurable pass/fail statements.
- A task with no time expectation.
- A started task with no assignee or with several; a backlog with no order.
- A todo with no assignee or no priority, or assigned to a milestone that does not exist.
- In a project that uses milestones, a task not linked to the milestone it serves.
- A blocked task not identified, not marked as blocked where the tracker allows it, left without action, with no "blocked by" link where it waits on a tracked item, with no specific blocker, or with no note giving the reason; resolved blocker notes discarded.

## A complete review must establish

- Every backlog item bigger than a task is broken into smaller tasks, and each piece of broken-down work has a responsible person or team.
- The breakdown covers the whole scope; where a WBS is used, each work package's activities add up to its work; and each story is split into vertical slices.
- Each task was sized by the people who will do it.
- No task is a week or more, every unestimable task was split, every story fits one iteration, and every WBS work package is within about 80 hours and one reporting period.
- Every task is specific, states its outcome, serves its story, has a title that states it, names a visible action, carries a pass/fail done test the team agrees on, and has a time expectation.
- Every started task has exactly one assignee, and the backlog is ordered.
- Every todo has an assignee and a priority, and no todo is assigned to a nonexistent milestone.
- Where the project uses milestones, every task is linked to the milestone it serves.
- Every blocked task is identified, marked as blocked where the tracker allows it, acted on, linked to the item it waits on where that is a tracked item, references a specific blocker and carries a brief reason; resolved blocker notes are kept.

## A build must establish

- `break-down-assign-and-prioritize-tasks`: every backlog item bigger than a task is broken into smaller tasks.
- `work-has-a-responsible-owner`: every piece of broken-down work has a responsible person or team.
- `breakdown-covers-all-scope`: the breakdown includes all of the work in scope, project management included.
- `work-package-activities-add-up`: where a WBS is used, each work package's activities add up to all of its work.
- `split-into-vertical-slices`: each story or backlog item is split into vertical slices, not by architectural layer.
- `doers-size-their-tasks`: every task's size was set by the people who will do it.
- `task-sized-hours-to-a-few-days`: every task fits in hours to a couple of days, and none is a week or more.
- `split-large-estimates`: no task estimated at a week or more is left unsplit.
- `split-unestimable-tasks`: no task whose duration cannot be estimated is left unsplit.
- `story-fits-one-iteration`: every user story fits within one iteration.
- `work-package-within-eighty-hours`: where a WBS is used, every lowest-level work package is about 80 hours of effort or less.
- `work-package-within-one-reporting-period`: where a WBS is used, every lowest-level work package fits within one reporting period.
- `tasks-specific-and-actionable`: every task is specific enough for everyone on the team to understand.
- `task-states-its-outcome`: every task describes a concrete piece of work with a defined outcome.
- `task-serves-its-story`: every task contributes to the story it belongs to.
- `task-title-states-the-task`: every task's title states directly what the task is.
- `task-names-visible-action`: every task names a physical, visible action.
- `task-has-done-test`: every task carries a done test the team agrees on.
- `done-test-is-pass-fail`: every done test is a set of measurable pass/fail statements.
- `task-has-time-expectation`: every task carries a time expectation.
- `started-task-has-one-owner`: every started task has exactly one assignee.
- `backlog-is-kept-ordered`: the backlog is ordered, by rank or by priority levels.
- `task-has-assignee-and-priority`: every todo has an assignee and a priority.
- `link-tasks-to-milestones`: where the project uses milestones, every task is linked to the milestone it serves.
- `task-milestone-must-exist`: no todo is assigned to a milestone that does not exist.
- `identify-blocked-tasks-and-blockers`: every blocked task, and what blocks it, is identified when active work is reviewed.
- `mark-blocked-tasks`: where the tracker allows it, every blocked task is marked as blocked.
- `remove-identified-blockers`: every identified blocker is acted on.
- `blocker-links-the-blocking-item`: every blocked task that waits on a tracked item has a "blocked by" link to it.
- `blocker-states-reason`: every blocked task carries a brief note naming the cause.
- `blocker-records-dates`: where dates are recorded, a blocker note gives the start date and the resolved date.
- `keep-resolved-blockers`: resolved blocker notes are kept.
- `blocked-task-references-blocker`: every blocked todo references a specific blocker.

## Rationale

*This section is informative.*

The method owners agree on the shape of a breakdown. The Scrum Guide has refinement break items into smaller, more precise ones with a description, order and size, and has the Developers who do the work size it and own their plan. The NASA WBS Handbook defines all of a project's work as a product-oriented structure and ties responsibility for it to organisations through a Responsibility Assignment Matrix. PRINCE2 hands work to a team as a work package. GitHub's sub-issues, Jira's links and Linear's estimates are the trackers' forms of the same practice.

Small tasks rest on heuristics, not studies. DORA and Spolsky independently give hours to a couple of days, with a week as too big; the Scrum Guide says decomposition into items of one day or less is often done; SAFe and INVEST bound stories at an iteration; the WBS 80-hour rule bounds a work package, which is coarser than a task. The sources agree on "small" but not on one number, so the size rules are SHOULDs, and the number the guideline settles on is an open question for the owner.

Wording rules come from Wake's SMART tasks, Linear's method and GTD's next action, and the done test from the Scrum Guide's Definition of Done, the Kanban Guide's definition of when an item is started and finished, and Atlassian's acceptance criteria. One owner per piece of work comes from Linear and GitLab's DRIs; Cohn and Scrum.org advise choosing the owner when the work begins. GitHub allows up to ten assignees, so single ownership is a team practice, not a tool constraint. GTD's Waiting For list, which keeps items waiting on someone or something else apart from the rest, is the personal-method counterpart of marking a task as blocked.

The second check found five claims that support their statement only in part, so no rule citing them carries a MUST: `decompose-to-one-day-or-less` (cited by `break-down-assign-and-prioritize-tasks` and `task-sized-hours-to-a-few-days`), `trackers-record-blocked-by-links` (cited by `mark-blocked-tasks` and `blocker-links-the-blocking-item`), `waiting-for-names-whom` (cited by `mark-blocked-tasks`), `split-vertically-not-by-layer` (cited by `split-into-vertical-slices`) and `wbs-hundred-percent-rule` (cited by `breakdown-covers-all-scope` and `work-package-activities-add-up`). The 100% rule and the 80-hour rule come from Wikipedia's summary of the PMI standard, and PRINCE2 from the PRINCE2 wiki, because the primary texts could not be fetched.

Three rules are kept word for word from the projectteam's checks for the owner to decide: `task-has-assignee-and-priority`, `blocked-task-references-blocker` and `task-milestone-must-exist`. The research contradicts the first as a check on every todo (assignment is advised when work begins, Scrum orders the backlog rather than labelling priority, and Linear allows "No priority"), and finds no source stating the other two; trackers only offer existing milestones to pick. The owner's open questions are whether an assignee is required only on started work, whether priority is a field or backlog order, whether the milestone-exists check stays, which size limit to state, whether a blocker has to be a tracked item or may be an outside cause, and whether every task links to a milestone or only tasks in projects that use milestones.

Ordering thin end-to-end slices belongs to [adc.principle.steel-thread-first](cookbook:b224ef56-65f5-45fd-8842-767b20df6736), and writing the spec before code to [adc.guideline.planning.code-quality.spec-driven-development](cookbook:138eed2b-6b13-40ac-8c99-1f7860420b42).

## References

*This section is informative. Every reference is informative.*

- Schwaber and Sutherland, [The Scrum Guide](https://scrumguides.org/scrum-guide.html)
- Vacanti and Coleman, [The Kanban Guide](https://kanbanguides.org/english/)
- Scaled Agile, [Story](https://framework.scaledagile.com/story)
- NASA, [Work Breakdown Structure Handbook](https://www.nasa.gov/wp-content/uploads/2023/08/nasa-work-breakdown-structure-handbook.pdf)
- Wikipedia, [Work breakdown structure](https://en.wikipedia.org/wiki/Work_breakdown_structure)
- PRINCE2 wiki, [Work package](https://prince2.wiki/management-products/work-package/)
- GitHub, [Adding sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues), [Creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies), [About milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones) and [Assigning issues and pull requests](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/assigning-issues-and-pull-requests-to-other-github-users)
- Linear, [Issue properties](https://linear.app/docs/issue-property), [Assigning issues](https://linear.app/docs/assigning-issues), [Projects](https://linear.app/docs/projects) and [Write issues, not user stories](https://linear.app/method/write-issues-not-user-stories)
- Atlassian, [Flag a work item](https://support.atlassian.com/jira-software-cloud/docs/flag-an-issue/), [Create or remove dependencies on your timeline](https://support.atlassian.com/jira-software-cloud/docs/create-or-remove-dependencies-on-your-timeline/) and [Acceptance criteria](https://www.atlassian.com/work-management/project-management/acceptance-criteria)
- Bill Wake, [INVEST in Good Stories, and SMART Tasks](https://xp123.com/invest-in-good-stories-and-smart-tasks/)
- Humanizing Work, [The Humanizing Work Guide to Splitting User Stories](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/)
- Joel Spolsky, [Painless Software Schedules](https://www.joelonsoftware.com/2000/03/29/painless-software-schedules/)
- DORA, [Working in small batches](https://dora.dev/capabilities/working-in-small-batches/)
- Mike Cohn, [Should a Team Assign Work During Sprint Planning?](https://www.mountaingoatsoftware.com/blog/should-a-team-assign-work-during-sprint-planning)
- Scrum.org, [Why pre-assigning tasks in Scrum is a bad idea](https://www.scrum.org/resources/blog/why-pre-assigning-tasks-scrum-bad-idea-and-what-do-instead)
- GitLab, [Directly Responsible Individuals](https://handbook.gitlab.com/handbook/people-group/directly-responsible-individuals/)
- Leopold and Magennis, [Blockers and defects for process improvement](https://www.infoq.com/articles/blockers-defects-process-improvement)
- David Allen, [Some key GTD definitions](https://gettingthingsdone.com/2010/10/some-key-gtd-definitions/); FacileThings, [What is the next action](https://facilethings.com/blog/en/what-is-the-next-action)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
