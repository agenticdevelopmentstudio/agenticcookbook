--- draft-2.md
+++ draft.md
@@ -78,7 +78,7 @@
 - **split-large-estimates**: A task estimated at a week or more SHOULD be broken into smaller tasks. (claims: linear-break-up-large-estimates, small-tasks-hours-to-days, not-small-enough-is-the-pitfall)
 - **split-unestimable-tasks**: A task whose duration cannot be estimated, because the work behind it has not been thought through, SHOULD be broken into smaller tasks. (claims: large-chunky-tasks-hide-design, linear-break-up-large-estimates, task-title-states-the-task)
 - **story-fits-one-iteration**: A user story above the tasks SHOULD be small enough to finish within one iteration. (claim: stories-small-enough-for-an-iteration)
-- **work-package-within-eighty-hours**: In a work breakdown structure, a lowest-level work package SHOULD be no more than 80 hours of effort. (claim: wbs-eighty-hour-heuristic)
+- **work-package-within-eighty-hours**: In a work breakdown structure, a lowest-level work package SHOULD be no more than about 80 hours of effort. (claim: wbs-eighty-hour-heuristic)
 - **work-package-within-one-reporting-period**: In a work breakdown structure, a lowest-level work package SHOULD take no longer than one reporting period. (claim: wbs-eighty-hour-heuristic)
 
 ### Task wording
@@ -121,7 +121,7 @@
 1. Start from the whole scope. List every piece of work it holds, including project management. Where a work breakdown structure is used, check that the activities under each work package add up to all of that package's work.
 2. Name the person or team responsible for each piece of work being broken down.
 3. Split each story or backlog item into vertical slices: each slice delivers an outcome a user or the project can see, from interface to storage, not one layer of the system.
-4. Let the people who will do the work break each slice into tasks and size them. A task estimated at a week or more, or one nobody can estimate because its work has not been thought through, is split again. Stories stay within one iteration, and work packages within 80 hours and one reporting period.
+4. Let the people who will do the work break each slice into tasks and size them. A task estimated at a week or more, or one nobody can estimate because its work has not been thought through, is split again. Stories stay within one iteration, and WBS work packages within about 80 hours and one reporting period.
 5. Write each task: a title that says what it is, the outcome it delivers to its story, the visible action it takes, a done test of pass/fail statements the team agrees on, and a rough time expectation. A sub-issue keeps its link to the parent item.
 6. Order the backlog, as a ranked list or by the tracker's priority levels, and give each todo an assignee and a priority.
 7. Where the project uses milestones, link each task to the milestone it serves; in Scrum, the Sprint Goal plays that part.
@@ -180,10 +180,10 @@
 ## What a reviewer looks for
 
 - A backlog item bigger than a task left unbroken, or a piece of broken-down work with no responsible person or team.
-- A breakdown that leaves part of the scope out, or a work package whose activities do not add up to its work.
+- A breakdown that leaves part of the scope out, or, in a work breakdown structure, a work package whose activities do not add up to its work.
 - Stories split by architectural layer instead of into vertical slices.
 - Sizes set by someone other than the people who will do the work.
-- A task of a week or more, or one that cannot be estimated, left unsplit; a story too big for one iteration; a work package over 80 hours or one reporting period.
+- A task of a week or more, or one that cannot be estimated, left unsplit; a story too big for one iteration; a WBS work package over about 80 hours or one reporting period.
 - A task that is not specific, states no outcome, does not serve its story, has a title that does not say what it is, or names a vague verb such as "think".
 - A task with no done test, or one whose criteria are not measurable pass/fail statements.
 - A task with no time expectation.
@@ -195,9 +195,9 @@
 ## A complete review must establish
 
 - Every backlog item bigger than a task is broken into smaller tasks, and each piece of broken-down work has a responsible person or team.
-- The breakdown covers the whole scope, each work package's activities add up to its work, and each story is split into vertical slices.
+- The breakdown covers the whole scope; where a WBS is used, each work package's activities add up to its work; and each story is split into vertical slices.
 - Each task was sized by the people who will do it.
-- No task is a week or more, every unestimable task was split, every story fits one iteration, and every work package is within 80 hours and one reporting period.
+- No task is a week or more, every unestimable task was split, every story fits one iteration, and every WBS work package is within about 80 hours and one reporting period.
 - Every task is specific, states its outcome, serves its story, has a title that states it, names a visible action, carries a pass/fail done test the team agrees on, and has a time expectation.
 - Every started task has exactly one assignee, and the backlog is ordered.
 - Every todo has an assignee and a priority, and no todo is assigned to a nonexistent milestone.
@@ -216,7 +216,7 @@
 - `split-large-estimates`: no task estimated at a week or more is left unsplit.
 - `split-unestimable-tasks`: no task whose duration cannot be estimated is left unsplit.
 - `story-fits-one-iteration`: every user story fits within one iteration.
-- `work-package-within-eighty-hours`: where a WBS is used, every lowest-level work package is 80 hours of effort or less.
+- `work-package-within-eighty-hours`: where a WBS is used, every lowest-level work package is about 80 hours of effort or less.
 - `work-package-within-one-reporting-period`: where a WBS is used, every lowest-level work package fits within one reporting period.
 - `tasks-specific-and-actionable`: every task is specific enough for everyone on the team to understand.
 - `task-states-its-outcome`: every task describes a concrete piece of work with a defined outcome.
