--- draft-1.md
+++ draft.md
@@ -19,7 +19,9 @@
   - project-management
   - planning
 depends-on: []
-related: []
+related:
+  - 3f978ba7-c8c1-4b53-8fda-12e5a6966b75
+  - f264cc0b-45d3-4593-a437-7371610c5a8a
 references:
   - https://www.gao.gov/assets/d1689G.pdf
   - https://apm.org.uk/resources/what-is-project-management/what-is-scheduling-in-project-management/
@@ -56,13 +58,14 @@
 
 Define each milestone as a zero-duration key event, link milestones and the work between them by logic rather than fixed dates, keep the dependency chains free of cycles and find the critical path. Take status against a status date, keep a baseline, explain every change to a milestone date, and name the issue or risk behind every blocked or at-risk milestone.
 
-This guideline covers how a delivery team defines milestones, sequences the work between them, sets their target dates, keeps the schedule current, checks the dependency chains for cycles, finds the critical path, holds contingency, forecasts and commits to dates, and accounts for milestones that are at risk or blocked. Delivery dependencies on other teams, tasks and their blockers, and the general convention for linking project records are covered by their own guidelines. A team following this guideline meets the rules below; each rule's keyword says how strictly.
+This guideline covers how a delivery team defines milestones, sequences the work between them, sets their target dates, keeps the schedule current, checks the dependency chains for cycles, finds the critical path, holds contingency, forecasts and commits to dates, and accounts for milestones that are at risk or blocked. Delivery dependencies on other teams are covered by [adc.guideline.planning.project-management.dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75), tasks and their blockers by [adc.guideline.planning.project-management.task-breakdown](cookbook:f264cc0b-45d3-4593-a437-7371610c5a8a), and the general convention for linking project records by its own guideline. A team following this guideline meets the rules below; each rule's keyword says how strictly.
 
 ## Rules
 
 ### Defining milestones
 
-- **define-and-sequence-milestones**: Planning SHOULD define the project's milestones, put them in sequence, give each a target date, record the dependency chains between them and track each one's status and progress. (claims: sequence-with-logic, milestones-are-zero-duration-key-events, github-milestones-due-date-progress, github-projects-roadmap-dates, linear-milestones-optional-date, linear-project-dependencies, jira-plan-dependencies, safe-planning-board-milestones)
+- **define-and-sequence-milestones**: Planning SHOULD define the project's milestones, put them in sequence and record the dependency chains between them. (claims: sequence-with-logic, milestones-are-zero-duration-key-events, github-milestones-due-date-progress, github-projects-roadmap-dates, linear-milestones-optional-date, linear-project-dependencies, jira-plan-dependencies, safe-planning-board-milestones)
+- **track-milestone-progress**: Each milestone's progress SHOULD be tracked, for example as the completion of the work linked to it. (claims: github-milestones-due-date-progress, linear-milestones-optional-date)
 - **milestone-marks-a-key-event**: A milestone SHOULD mark a key event or stage of the project as a point in time with no duration. (claim: milestones-are-zero-duration-key-events)
 - **schedule-has-start-and-finish-milestones**: The schedule SHOULD include a milestone for the project's start and one for its finish. (claim: milestones-are-zero-duration-key-events)
 - **work-is-not-a-milestone**: Work SHOULD be scheduled as activities leading to a milestone, not represented as milestones. (claim: too-many-milestones-mask-work)
@@ -73,9 +76,9 @@
 ### Sequencing by logic
 
 - **link-milestones-by-logic-not-fixed-dates**: Milestones and the activities between them SHOULD be sequenced by logic links, each activity having at least one predecessor and one successor, rather than placed by fixed dates. (claims: sequence-with-logic, missing-logic-justified, hard-constraints-defeat-cpm, github-define-blocked-by-and-one-target-date, linear-project-dependencies, jira-plan-dependencies)
-- **justify-missing-logic**: An activity other than the start and finish milestones that has no predecessor or no successor SHOULD be justified in the schedule documentation. (claim: missing-logic-justified)
+- **justify-missing-logic**: An activity other than the start and finish milestones that has no predecessor or no successor MUST be justified in the schedule documentation. (claim: missing-logic-justified)
 - **no-hard-constraints-in-the-baseline**: The baseline schedule and the official status updates SHOULD NOT carry hard date constraints. (claims: avoid-hard-date-constraints, hard-constraints-defeat-cpm)
-- **justify-unavoidable-hard-constraints**: A hard date constraint that cannot be avoided SHOULD be justified in the schedule's basis document by the event outside the schedule that controls it. (claim: avoid-hard-date-constraints)
+- **justify-unavoidable-hard-constraints**: A hard date constraint that cannot be avoided MUST be justified in the schedule's basis document by the event outside the schedule that controls it. (claim: avoid-hard-date-constraints)
 
 ### Cycles and the critical path
 
@@ -184,7 +187,7 @@
 print(nx.dag_longest_path(g, weight="days"))   # ['start', 'api-freeze', 'beta', 'launch']
 ```
 
-Had `start` also depended on `launch`, the sort would have stopped with `cycle in milestone chain: start -> launch -> beta -> api-freeze -> start` (the order the error lists varies).
+Had `start` also depended on `launch`, the sort would have stopped with `cycle in milestone chain: api-freeze -> docs-ready -> launch -> start -> api-freeze` (graphlib lists each milestone followed by one that depends on it, starting from whichever node it reaches first).
 
 A status update for one milestone:
 
@@ -206,7 +209,8 @@
 
 ## What a reviewer looks for
 
-- Milestones that are not defined, sequenced, dated or tracked, or that span a stretch of work instead of marking an event.
+- Milestones that are not defined or sequenced, with no recorded dependency chains between them, or that span a stretch of work instead of marking an event.
+- A milestone whose progress is not tracked.
 - A schedule with no start or finish milestone, work represented as milestones, or so many milestones that the work driving them is hard to see.
 - A target ship date held in more than one field.
 - Milestones or activities placed by fixed dates rather than linked by logic, or an activity with no predecessor or successor and no stated reason.
@@ -224,7 +228,7 @@
 
 ## A complete review must establish
 
-- Every milestone is defined as a key event with no duration, sequenced, dated and tracked; the schedule has start and finish milestones; work is not represented as milestones; the milestones are few enough that the work driving them is visible.
+- Every milestone is defined as a key event with no duration and sequenced, and the dependency chains between milestones are recorded; each milestone's progress is tracked; the schedule has start and finish milestones; work is not represented as milestones; the milestones are few enough that the work driving them is visible.
 - Each target ship date is tracked in one place.
 - Every activity and milestone is linked by logic, with each missing link justified, and the baseline and official updates carry no unjustified hard date constraint.
 - The dependency chains hold no cycle, as shown by a topological sort of the exported links, and any cycle found was reported.
@@ -238,7 +242,8 @@
 
 ## A build must establish
 
-- `define-and-sequence-milestones`: the milestones are defined, sequenced, given target dates, linked by dependency chains and tracked for status and progress.
+- `define-and-sequence-milestones`: the milestones are defined, sequenced and linked by recorded dependency chains.
+- `track-milestone-progress`: each milestone's progress is tracked.
 - `milestone-marks-a-key-event`: each milestone marks a key event or stage and has no duration.
 - `schedule-has-start-and-finish-milestones`: the schedule has a start milestone and a finish milestone.
 - `work-is-not-a-milestone`: no work is represented as a milestone.
@@ -279,9 +284,9 @@
 
 *This section is informative.*
 
-Most of the practice comes from the US Government Accountability Office's Schedule Assessment Guide (GAO-16-89G), a primary government standard for schedule quality: milestones as zero-duration events, logic links over fixed dates, the critical path, the status date, explicit contingency, the baseline and the narrative that explains each date change. The UK's Association for Project Management states the same logic and critical-path practice independently. GAO is written for large government programmes; the rules carry its practice at SHOULD, and its schedule risk analysis is a MAY, since few software teams run one.
-
-The cycle rule is the one MUST. A loop makes an activity its own predecessor, so no date can be computed across it: GAO says so, Microsoft Project cannot calculate dates across one, and a complete topological order exists if and only if the graph has no cycle. The trackers differ on how a cycle is caught. Jira does not stop one being made and Atlassian's advice is to detect it afterwards, while Microsoft Project offers to cancel the action, so a topological sort the team runs itself is the dependable check.
+Most of the practice comes from the US Government Accountability Office's Schedule Assessment Guide (GAO-16-89G), a primary government standard for schedule quality: milestones as zero-duration events, logic links over fixed dates, the critical path, the status date, explicit contingency, the baseline and the narrative that explains each date change. The UK's Association for Project Management states the same logic and critical-path practice independently. GAO is written for large government programmes; the rules carry most of its practice at SHOULD, and its schedule risk analysis is a MAY, since few software teams run one. Where GAO itself says "must", the rules do too: an activity missing logic and an unavoidable hard constraint must each be justified. Both apply only on a departure from the SHOULD rules, so they do not make those rules absolute.
+
+The cycle rule and the two justification rules, `justify-missing-logic` and `justify-unavoidable-hard-constraints`, are the MUSTs. A loop makes an activity its own predecessor, so no date can be computed across it: GAO says so, Microsoft Project cannot calculate dates across one, and a complete topological order exists if and only if the graph has no cycle. The trackers differ on how a cycle is caught. Jira does not stop one being made and Atlassian's advice is to detect it afterwards, while Microsoft Project offers to cancel the action, so a topological sort the team runs itself is the dependable check.
 
 The trackers supply the moving parts. GitHub milestones carry a due date and a completion percentage, GitHub issue dependencies record what blocks what, and GitHub Projects status updates carry a status, dates and a message. Linear milestones show completion and make a date optional, its project dependencies are end-to-start, and its project updates carry a health indicator and text on challenges. Jira plans mark dependencies at risk, warn of overdue work, and flag blocked items. The Kanban Guide and the Scrum Guide add the forecasting and the handling of impediments: Kanban's service level expectation pairs an elapsed time with a probability drawn from cycle-time history, and the Scrum Guide counts burn charts as useful but no substitute for empiricism. McConnell's cone of uncertainty warns against committing early; SAFe commits one increment and forecasts the next two.
 
@@ -289,7 +294,7 @@
 
 Two rules are kept word for word from projectteam's checks for the owner to decide: `milestone-has-status-and-target-date` and `blocked-milestone-has-issue-or-concern`. No source makes either a must-hold check. Linear and GitHub make a milestone's date optional and GAO asks for the status of key milestones; the trackers let a blocked item carry a reason but do not require one. The owner's open questions are whether these two stay as must-hold checks or become SHOULDs, whether a target date is a committed date or a forecast from the logic (GAO keeps hard constraints out of the baseline), whether the at-risk case joins the blocked case in one rule, which status vocabulary the cookbook names, whether it names an update cadence, and whether fixing the date and flexing the scope stays as an option beside critical-path scheduling.
 
-Delivery dependencies on other teams belong to the dependency-tracking guideline, tasks and their blockers to the task-breakdown guideline, and the links between project records to the project-record-linking guideline, all in `planning/project-management`.
+Delivery dependencies on other teams belong to [adc.guideline.planning.project-management.dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75), tasks and their blockers to [adc.guideline.planning.project-management.task-breakdown](cookbook:f264cc0b-45d3-4593-a437-7371610c5a8a), and the links between project records to the project-record-linking guideline, all in `planning/project-management`.
 
 ## References
 
