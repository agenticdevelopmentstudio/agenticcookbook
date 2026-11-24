# task-breakdown: research

How work is broken into tasks: what makes a task specific and actionable, how large it may be, who owns it, how it is ordered, how it links to a milestone, and how a blocked task names what it waits on. Spec-driven-development, steel-thread-first, milestone-scheduling and project-record-linking own their own ground and are not restated here. The claims, citations and scores are in `research.json`.

Apple, Android and Windows have no bearing on this topic and were not researched.

## Best practices

**Break the work down until each task is small.** A task should take hours to a couple of days. A task of a week or more has not been broken down enough. DORA and Spolsky, two independent publishers, give the same range (`small-tasks-hours-to-days`), and the Scrum Guide's "one day or less" agrees (`decompose-to-one-day-or-less`). These are heuristics. No study backs any one number, so the sources support a **SHOULD** for small tasks and no particular limit.

**A task is specific and actionable.**
- A task is specific enough that everyone can understand what it involves, and it has a clear, defined outcome (`task-specific-enough-to-understand`).
- Its title states directly what the task is, and work that is not yet a task gets broken down before it goes in the tracker (`task-title-states-the-task`).
- Each task names a physical, visible next step that anyone can check was done. Avoid vague verbs such as "think" (`next-action-physical-and-visible`).

Rule **tasks-specific-and-actionable** is supported at **SHOULD**.

**Every task carries a done test the team agrees on** (`task-has-a-done-test`): clear, testable conditions for when it is complete. This matches the Scrum Guide's Definition of Done (`scrum-definition-of-done`) and the Kanban Guide's definition of when an item is started and finished (`kanban-define-started-and-finished`). Together with the wording claims above, this gives the new rule **task-text-names-action-and-done-test** at **SHOULD**. It answers the research question *Actionable task wording*.

**One owner per piece of work.** Linear assigns an issue to a single person, and GitLab's handbook says DRIs are usually assigned per task. Both say this is to remove ambiguity about ownership (`single-accountable-owner`). Experts add that the owner should be chosen when the work begins, not when it is planned (`assign-when-work-begins`, in The expert's view). Together these give the new rule **started-task-has-one-owner** at **SHOULD**.

**Prior rule `task-has-assignee-and-priority` ("Every todo has an assignee and priority"): contradicted as a check on every todo.** The research claim against it is `task-has-assignee-and-priority-prior`.
- Against an assignee on every todo: Cohn and Scrum.org advise against assigning all tasks at planning (`assign-when-work-begins`), and in Scrum the Developers own the plan (`developers-own-the-sprint-backlog`).
- Against a priority on every todo: Scrum orders the backlog instead of labelling each item (`backlog-is-ordered`), and Linear's priority field includes "No priority" (`linear-priority-levels`).

The sources support **SHOULD** for one owner on each started task and for an ordered backlog. They support no MUST that every todo carry both fields.

## Known solutions

**Breakdown structures.**
- **WBS.** NASA's handbook defines the WBS as a product-oriented breakdown of all the work, subdivided only as far as management needs (`nasa-wbs-defines-all-work`). The PMI 100% rule says the children of each element cover exactly the parent's work, down to the activities (`wbs-hundred-percent-rule`). Elements are defined by outcomes, not actions (`wbs-outcomes-not-actions`). A heuristic caps a work package at about 80 hours (`wbs-eighty-hour-heuristic`). The PMI material comes from a secondary source, because pmi.org could not be fetched.
- **New rule `breakdown-covers-all-scope`** (from the WBS claims above): **SHOULD**.
- **PRINCE2 work package.** A formal set of instructions that assigns responsibility for products to a team (`prince2-work-package-assigns-products`). Secondary source.
- **INVEST and SMART.** INVEST stories are small, a few person-weeks at most, while SAFe says a few days or less (`stories-small-enough-for-an-iteration`). SMART tasks are relevant to their story and time-boxed (`smart-task-time-boxed`).

**Trackers** (GitHub Issues, Jira, Linear).
- Sub-issues break larger work into tasks (`github-sub-issues-break-down-work`).
- Linear says a large estimate signals uncertainty and recommends splitting the issue (`linear-break-up-large-estimates`). With `decompose-to-one-day-or-less`, `not-small-enough-is-the-pitfall`, `large-chunky-tasks-hide-design` and `wbs-eighty-hour-heuristic`, this gives the new rule **task-sized-hours-to-a-few-days** at **SHOULD**. The owner picks the number (see open questions).
- **Assignment.** Linear allows one assignee. GitHub allows up to 10 (`github-assignees`), so single ownership is a practice the team chooses, not something every tool enforces.
- **Priority.** Linear has five priority levels, and "No priority" is one of them (`linear-priority-levels`).
- **Milestones.** GitHub milestones group issues (`github-milestones-group-issues`). Linear puts each issue in at most one project, and the project carries milestones (`linear-issue-in-one-project`). In WBS practice, tasks and milestones both come from the lowest-level WBS elements (`nasa-tasks-and-milestones-from-wbs`).
- **Blockers.** All three trackers record a blocker as a "blocked by" / "blocks" link to the blocking item and mark blocked items visibly (`trackers-record-blocked-by-links`, three independent publishers). Jira also lets you flag an item as an impediment and add a comment giving the reason (`jira-flag-with-reason`). GTD's Waiting For list shows a blocker can be a person or outside thing, not only a tracked item (`waiting-for-names-whom`).

**Rule link-tasks-to-milestones: supported at SHOULD** in projects that use milestones (`nasa-tasks-and-milestones-from-wbs`, `github-milestones-group-issues`, `linear-issue-in-one-project`, `sprint-goal-links-the-work`). The sources treat milestones as optional grouping. They support no MUST that every task carry one.

**Prior rule task-milestone-must-exist ("no todo is assigned to a nonexistent milestone"): unsupported** (`task-milestone-must-exist-prior`). No source states this rule. Trackers only let you pick from existing milestones (`github-milestones-group-issues`), which prevents the problem by design but is not a stated rule. It holds at most as a **MAY**, a house integrity check the owner can choose to keep.

**New rule blocker-links-the-blocking-item: SHOULD** (`trackers-record-blocked-by-links`, `waiting-for-names-whom`). It answers the research question *Task blocker naming*.

## Platform guidelines

The method owners' own guides govern here. Web trackers are covered under Known solutions.

**Scrum Guide.**
- The Developers decompose items into work items of one day or less, at their own discretion (`decompose-to-one-day-or-less`).
- They own the Sprint Backlog (`developers-own-the-sprint-backlog`).
- Refinement breaks items down and gives each a description, order and size (`refinement-breaks-down-and-sizes`).
- Work must meet the Definition of Done (`scrum-definition-of-done`).
- The backlog is ordered (`backlog-is-ordered`). With `linear-priority-levels`, this gives the new rule **backlog-is-kept-ordered** at **SHOULD**.
- The Sprint Goal ties the Sprint's work to one objective (`sprint-goal-links-the-work`).
- The Daily Scrum identifies impediments, and the Scrum Master causes their removal (`daily-scrum-identifies-impediments`).

**Kanban Guide.**
- Items must be actively managed, and unblocking blocked work is one way to do that (`kanban-unblock-blocked-work`).
- The team defines its work items and when each is started and finished (`kanban-define-started-and-finished`).

**Rule break-down-assign-and-prioritize-tasks: supported at SHOULD.** Its claims are `refinement-breaks-down-and-sizes`, `decompose-to-one-day-or-less`, `github-sub-issues-break-down-work`, `nasa-ram-assigns-responsibility`, `single-accountable-owner`, `backlog-is-ordered` and `prince2-work-package-assigns-products`.

**Rule identify-blocked-tasks-and-blockers: supported at SHOULD.** Its claims are `kanban-unblock-blocked-work`, `daily-scrum-identifies-impediments`, `trackers-record-blocked-by-links` and `jira-flag-with-reason`. The Kanban Guide's "must" covers active management as a whole. Unblocking is one form of it, not a separate MUST.

## The expert's view

**What to do.**
- **Let the people doing the work size it.** A schedule handed down from management fails (`doers-estimate-their-tasks`, Spolsky and the Scrum Guide). With `refinement-breaks-down-and-sizes` and `developers-own-the-sprint-backlog`, this gives the new rule **doers-size-their-tasks** at **SHOULD**.
- **Assign tasks when work starts.** Each person signs up for their first task at planning and picks the next as work progresses (`assign-when-work-begins`, Cohn and Scrum.org). Cohn names exceptions, so this is a SHOULD, not a ban.
- **Record each blocker on the blocked item.** Give it a brief reason that names the cause, plus the date it started and the date it was resolved. Keep resolved blockers so they can be grouped to find patterns (`blocker-note-states-reason-and-dates`, Leopold and Magennis). Jira's flag comment covers the same reason (`jira-flag-with-reason`). Together these give the new rule **blocker-states-reason-and-since**: **SHOULD** for the reason and **MAY** for the dates, which only "some teams" record.

**What to avoid.**
- **Splitting by architectural layer.** One item for the UI and one for the database gives small items that are neither independent nor valuable. Split into vertical slices instead (`split-vertically-not-by-layer`). WBS's "outcomes, not actions" points the same way (`wbs-outcomes-not-actions`). Together these give the new rule **split-into-vertical-slices** at **SHOULD**.
- **Large, hand-wavy tasks.** They hide the design work nobody has done yet (`large-chunky-tasks-hide-design`).

**What people usually get wrong.**
- Not breaking work into small enough pieces, or regrouping small pieces before release (`not-small-enough-is-the-pitfall`).
- Assigning every task at the start of a Sprint (`assign-when-work-begins`).
- Writing acceptance criteria that are either too vague or too detailed, instead of measurable pass/fail statements (`acceptance-criteria-measurable-not-vague`).

**Prior rule blocked-task-references-blocker ("blocked todos reference a specific blocker"): unsupported as a MUST** (`blocked-task-references-blocker-prior`). Every tracker makes the link possible (`trackers-record-blocked-by-links`), and practitioners record the reason (`jira-flag-with-reason`, `blocker-note-states-reason-and-dates`). No source requires it. The sources support **SHOULD**.
