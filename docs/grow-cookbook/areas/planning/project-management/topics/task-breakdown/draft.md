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
summary: "Break work into small, specific tasks with a done test, sized by their doers, one owner once started, an ordered backlog, milestone links and named blockers."
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

Break the work down into small tasks, sized by the people who will do them, each specific enough to understand, naming a visible action and a done test the team agrees on. Give each task one owner once work on it starts, keep the backlog ordered, link each task to the milestone it serves, and record each blocked task's blocker as a link with a brief reason.

This guideline covers how work is broken into tasks for any delivery team: what makes a task specific and actionable, how large a task may be, who owns it, how tasks are ordered, how a task links to its milestone, and how a blocked task names what it waits on. Writing the spec before code, ordering thin end-to-end slices, milestones themselves and the general record-linking convention are covered elsewhere. A team following this guideline meets the rules below; each rule's keyword says how strictly.

## Rules

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

## Breaking work into tasks

*This section is informative.*

1. Start from the whole scope. List every piece of work it holds, including project management, and leave out anything outside it.
2. Split each story or backlog item into vertical slices: each slice delivers an outcome a user or the project can see, from interface to storage, not one layer of the system.
3. Let the people who will do the work break each slice into tasks and size them. A task that comes out at a week or more, or that nobody can estimate because its design has not been thought through, is split again. Stories stay within one iteration.
4. Write each task: a short title that says what it is, the visible action it takes, a done test of pass/fail statements the team agrees on, and a rough time expectation. A sub-issue keeps its link to the parent item.
5. Order the backlog, as a ranked list or by the tracker's priority levels, and link each task to the milestone or Sprint Goal it serves.
6. Leave tasks unassigned until work on them begins. Whoever starts a task becomes its one assignee.

## Handling a blocked task

*This section is informative.*

1. Mark the task as blocked in the tracker: a "blocked by" link in GitHub, Jira or Linear, and a flag in Jira.
2. Link the blocked task to the item it waits on.
3. Add a brief note on the task naming the cause; teams that track flow also write the date the block started.
4. Raise the block when active work is reviewed (in Scrum, the Daily Scrum), and act to remove it.
5. When it clears, write the resolved date if the team records dates, and keep the note with the other resolved blockers so recurring causes show up.

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
Milestone: Beta sign-up
```

A layer split, and a vertical split of the same story:

```text
By layer (avoid):   "Build the export UI"  /  "Add the export table"  /  "Write the export API"
Vertical slices:    "Export one report as CSV"  /  "Export a filtered report"  /  "Schedule a weekly export"
```

A blocked task:

```text
Blocked by:  #412 Rotate the staging OAuth secret
Note:        Waiting on the new client secret from the identity team; sign-in fails without it.
Blocked:     2026-11-20 -> 2026-11-22
```

## What a reviewer looks for

- Large work left as one task, with no breakdown into smaller tasks, and no person or team responsible for it.
- A breakdown that leaves part of the scope out, or holds work outside it.
- Stories split by architectural layer instead of into vertical slices.
- Sizes set by someone other than the people who will do the work.
- A task of a week or more, a large or unknown estimate left unsplit, or a story too big for one iteration; a WBS work package over about 80 hours or one reporting period.
- A task whose title or text does not say what it is, names a vague verb such as "think", or has no clear outcome.
- A task with no done test, or one whose criteria are vague or are not pass/fail statements.
- A task with no time expectation.
- A started task with no assignee or with several.
- A backlog with no order.
- A todo with no assignee or no priority, or assigned to a milestone that does not exist.
- A task not linked to the milestone it serves.
- A blocked task not marked as blocked, with no "blocked by" link, no specific blocker, or no note giving the reason.
- Resolved blocker notes discarded.

## A complete review must establish

- Every piece of larger work is broken into smaller tasks, the work has a responsible person or team, and the tasks are ordered.
- The breakdown covers the whole scope and nothing outside it, and each story is split into vertical slices.
- Each task was sized by the people who will do it.
- No task is a week or more, every large or unknown estimate was split, every story fits one iteration, and every WBS work package is within about 80 hours and one reporting period.
- Every task is specific, has a title that states it, names a visible action, carries a pass/fail done test the team agrees on, and has a time expectation.
- Every started task has exactly one assignee, and the backlog is ordered.
- Every todo has an assignee and a priority, and no todo is assigned to a nonexistent milestone.
- Every task is linked to the milestone it serves.
- Every blocked task is identified, marked as blocked, linked to its specific blocker and given a brief reason; resolved blocker notes are kept.

## A build must establish

- `break-down-assign-and-prioritize-tasks`: larger work is broken into smaller tasks, the work has a responsible person or team, and the tasks are ordered.
- `breakdown-covers-all-scope`: the tasks add up to all of the work in scope and hold nothing outside it.
- `split-into-vertical-slices`: each story or backlog item is split into vertical slices, not by architectural layer.
- `doers-size-their-tasks`: every task's size was set by the people who will do it.
- `task-sized-hours-to-a-few-days`: every task fits in hours to a couple of days, and none is a week or more.
- `split-large-estimates`: no task with a large or unknown estimate is left unsplit.
- `story-fits-one-iteration`: every user story fits within one iteration.
- `work-package-within-eighty-hours`: where a WBS is used, every lowest-level work package is within about 80 hours and one reporting period.
- `tasks-specific-and-actionable`: every task has a clear outcome and a short title that states what it is.
- `task-text-names-action-and-done-test`: every task names a visible action and a done test the team agrees on.
- `done-test-is-pass-fail`: every done test is a set of measurable pass/fail statements.
- `task-has-time-expectation`: every task carries a time expectation.
- `started-task-has-one-owner`: every started task has exactly one assignee.
- `backlog-is-kept-ordered`: the backlog is ordered, by rank or by priority levels.
- `task-has-assignee-and-priority`: every todo has an assignee and a priority.
- `link-tasks-to-milestones`: every task is linked to the milestone it serves.
- `task-milestone-must-exist`: no todo is assigned to a milestone that does not exist.
- `identify-blocked-tasks-and-blockers`: every blocked task is identified, marked as blocked where the tracker allows, and acted on when active work is reviewed.
- `blocker-links-the-blocking-item`: every blocked task has a "blocked by" link to what it waits on.
- `blocker-states-reason`: every blocked task carries a brief note naming the cause.
- `blocker-records-dates`: where dates are recorded, a blocker note gives the start date and the resolved date.
- `keep-resolved-blockers`: resolved blocker notes are kept.
- `blocked-task-references-blocker`: every blocked todo references a specific blocker.

## Rationale

*This section is informative.*

The method owners agree on the shape of a breakdown. The Scrum Guide has refinement break items into smaller, more precise ones with a description, order and size, and has the Developers who do the work size it and own their plan. The NASA WBS Handbook defines all of a project's work as a product-oriented structure and ties responsibility to it through a Responsibility Assignment Matrix. PRINCE2 hands work to a team as a work package. GitHub's sub-issues, Jira's links and Linear's estimates are the trackers' forms of the same practice.

Small tasks rest on heuristics, not studies. DORA and Spolsky independently give hours to a couple of days, with a week as too big; the Scrum Guide says decomposition into items of one day or less is often done; SAFe and INVEST bound stories at an iteration; the WBS 80-hour rule bounds a work package, which is coarser than a task. The sources agree on "small" but not on one number, so the size rules are SHOULDs, and the number the guideline settles on is an open question for the owner.

Wording rules come from Wake's SMART tasks, Linear's method and GTD's next action, and the done test from the Scrum Guide's Definition of Done, the Kanban Guide's definition of when an item is started and finished, and Atlassian's acceptance criteria. One owner per piece of work comes from Linear and GitLab's DRIs; Cohn and Scrum.org advise choosing the owner when the work begins. GitHub allows up to ten assignees, so single ownership is a team practice, not a tool constraint.

The vertical-slice, 100%-rule and GTD claims were each found by the second check to support their claim only in part, so the rules citing them hold at SHOULD. The 100% rule and the 80-hour rule come from Wikipedia's summary of the PMI standard, and PRINCE2 from the PRINCE2 wiki, because the primary texts could not be fetched.

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
