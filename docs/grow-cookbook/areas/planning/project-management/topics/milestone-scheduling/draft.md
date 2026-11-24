---
id: 023d4c91-d797-4e82-880c-a4ad7906a54a
title: "Milestone Scheduling"
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Define milestones as key events linked by logic, keep their chains acyclic, find the critical path, take status on a date, explain date changes, name blockers."
platforms: []
tags:
  - milestones
  - scheduling
  - critical-path
  - project-management
  - planning
depends-on: []
related: []
references:
  - https://www.gao.gov/assets/d1689G.pdf
  - https://apm.org.uk/resources/what-is-project-management/what-is-scheduling-in-project-management/
  - https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-roadmap-layout
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/sharing-project-updates
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
  - https://linear.app/docs/project-milestones
  - https://linear.app/docs/project-dependencies
  - https://linear.app/docs/use-cycles
  - https://linear.app/docs/initiative-and-project-updates
  - https://support.atlassian.com/jira-software-cloud/docs/what-are-dependencies-in-advanced-roadmaps
  - https://support.atlassian.com/jira-software-cloud/docs/troubleshoot-warnings-on-your-timeline-in-advanced-roadmaps
  - https://support.atlassian.com/jira-software-cloud/docs/flag-an-issue/
  - https://support.atlassian.com/jira/kb/how-to-identify-cyclic-issue-links-or-loops-in-jira/
  - https://support.microsoft.com/en-us/article/49988375-7b43-4e55-abeb-d21e6ed9bff8
  - https://docs.python.org/3/library/graphlib.html
  - https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.dag_longest_path.html
  - https://www.scrumguides.org/scrum-guide.html
  - https://kanbanguides.org/english/
  - https://www.peoplecert.org/news-and-announcements/prince2-7-issues
  - https://framework.scaledagile.com/PI-planning
  - https://framework.scaledagile.com/roadmap
  - https://basecamp.com/shapeup/1.2-chapter-03
  - https://www.joelonsoftware.com/2007/10/26/evidence-based-scheduling/
  - https://www.construx.com/wp-content/uploads/2019/02/CxWhitePaper_ConeOfUncertainty.pdf
approved-by: ""
approved-date: ""
triggers: []
---

# Milestone Scheduling

Define each milestone as a zero-duration key event, link milestones and the work between them by logic rather than fixed dates, keep the dependency chains free of cycles and find the critical path. Take status against a status date, keep a baseline, explain every change to a milestone date, and name the issue or risk behind every blocked or at-risk milestone.

This guideline covers how a delivery team defines milestones, sequences the work between them, sets their target dates, keeps the schedule current, checks the dependency chains for cycles, finds the critical path, holds contingency, forecasts and commits to dates, and accounts for milestones that are at risk or blocked. Delivery dependencies on other teams, tasks and their blockers, and the general convention for linking project records are covered by their own guidelines. A team following this guideline meets the rules below; each rule's keyword says how strictly.

## Rules

### Defining milestones

- **define-and-sequence-milestones**: Planning SHOULD define the project's milestones, put them in sequence, give each a target date, record the dependency chains between them and track each one's status and progress. (claims: sequence-with-logic, milestones-are-zero-duration-key-events, github-milestones-due-date-progress, github-projects-roadmap-dates, linear-milestones-optional-date, linear-project-dependencies, jira-plan-dependencies, safe-planning-board-milestones)
- **milestone-marks-a-key-event**: A milestone SHOULD mark a key event or stage of the project as a point in time with no duration. (claim: milestones-are-zero-duration-key-events)
- **schedule-has-start-and-finish-milestones**: The schedule SHOULD include a milestone for the project's start and one for its finish. (claim: milestones-are-zero-duration-key-events)
- **work-is-not-a-milestone**: Work SHOULD be scheduled as activities leading to a milestone, not represented as milestones. (claim: too-many-milestones-mask-work)
- **keep-milestones-few**: A schedule SHOULD NOT carry so many milestones that the activity sequences most likely to delay them become hard to identify. (claim: too-many-milestones-mask-work)
- **document-standard-milestones**: Where a team uses a standard set of milestones, it MAY document each with a description, completion criteria, a reference to its place in the work breakdown and the authority that decides it is reached. (claim: standard-milestones-documented-with-criteria)
- **one-place-for-the-target-date**: A target ship date SHOULD be tracked in a single place, not spread across several fields. (claim: github-define-blocked-by-and-one-target-date)

### Sequencing by logic

- **link-milestones-by-logic-not-fixed-dates**: Milestones and the activities between them SHOULD be sequenced by logic links, each activity having at least one predecessor and one successor, rather than placed by fixed dates. (claims: sequence-with-logic, missing-logic-justified, hard-constraints-defeat-cpm, github-define-blocked-by-and-one-target-date, linear-project-dependencies, jira-plan-dependencies)
- **justify-missing-logic**: An activity other than the start and finish milestones that has no predecessor or no successor SHOULD be justified in the schedule documentation. (claim: missing-logic-justified)
- **no-hard-constraints-in-the-baseline**: The baseline schedule and the official status updates SHOULD NOT carry hard date constraints. (claims: avoid-hard-date-constraints, hard-constraints-defeat-cpm)
- **justify-unavoidable-hard-constraints**: A hard date constraint that cannot be avoided SHOULD be justified in the schedule's basis document by the event outside the schedule that controls it. (claim: avoid-hard-date-constraints)

### Cycles and the critical path

- **milestone-chains-have-no-cycles**: The dependency chains between milestones MUST have no cycles. (claims: assess-network-for-circular-logic, topological-order-iff-acyclic)
- **check-chains-by-topological-sort**: A milestone plan's dependency chains SHOULD be checked for cycles by a topological sort of the dependency links exported from the tracker, a sort that completes only when the links hold no cycle. (claims: topological-order-iff-acyclic, assess-network-for-circular-logic, jira-cyclic-links-detected-after, ms-project-refuses-circular-dependency)
- **report-the-cycle-found**: A cycle check that fails SHOULD report the cycle it found, by the milestones or links in it. (claims: topological-order-iff-acyclic, jira-cyclic-links-detected-after)
- **identify-the-critical-path**: Once its chains are acyclic, the schedule SHOULD identify its critical path: the longest-duration path through the logic-linked activities, which sets the earliest finish date. (claims: critical-path-is-longest-path, critical-path-is-dag-longest-path)
- **critical-chain-is-an-option**: A team MAY schedule by critical chain, which centres on keeping resources at a constant utilisation, instead of by critical path, which centres on the activities. (claim: critical-path-vs-critical-chain)

### Contingency

- **hold-explicit-schedule-contingency**: The schedule SHOULD hold explicit contingency, a reserve of time for known risks and uncertainty, as separate contingency activities that can be monitored. (claims: schedule-contingency-is-explicit, risk-margin-not-padding)
- **estimate-without-padding**: Activity durations SHOULD be estimated for most likely conditions, with no padding or margin for risk inside them. (claim: risk-margin-not-padding)
- **size-contingency-by-risk-analysis**: A team MAY size its contingency with a schedule risk analysis: a statistical simulation of the schedule's risks that gives the reserve of time needed for a chosen level of confidence and identifies the high-priority risks. (claim: schedule-risk-analysis-sizes-contingency)

### Taking status

- **status-against-a-status-date**: Each schedule update SHOULD be taken against a stated status date, with every date before it an actual and every date after it a forecast. (claim: status-date-separates-actual-from-remaining)
- **status-date-is-not-view-or-save-date**: The date on which the schedule is viewed and its latest save date SHOULD NOT be used as its status date. (claim: status-date-not-view-date)
- **update-on-a-regular-cadence**: The schedule SHOULD be updated regularly, at a cadence set by the project's duration, complexity and risk. (claims: update-regularly-track-finer-than-report, linear-project-health-updates, schedules-are-halfhearted)
- **track-more-often-than-reported**: Progress SHOULD be tracked in the schedule more often than it is reported. (claim: update-regularly-track-finer-than-report)

### Milestone status and date changes

- **milestone-has-status-and-target-date**: Each milestone MUST pass this check: Every milestone has a status and target date (claim: milestone-has-status-and-target-date-prior)
- **keep-a-baseline-and-report-variance**: The team SHOULD keep a baseline schedule under change control and monitor each forecast against it, to reveal where a forecast milestone date differs from its baseline date and whether that variance affects downstream work. (claim: baseline-and-variance)
- **explain-every-milestone-date-change**: Each status update SHOULD give the status of the key milestone dates, the finish date included, and explain any change to them. (claim: schedule-narrative-explains-changes)
- **document-schedule-changes**: Every change made to the schedule during statusing SHOULD be documented, and each salient change justified along with its likely effect on later activities. (claim: schedule-narrative-explains-changes)

### At-risk and blocked milestones

- **identify-at-risk-or-blocked-milestones**: Each status update SHOULD identify the milestones that are at risk or blocked, from the late and overdue work, off-track dependencies, blocking links and flags that statusing and the tracker show. (claims: status-reveals-late-work, jira-off-track-warnings, jira-flag-impediment, github-issue-dependencies, linear-project-health-updates, github-status-updates)
- **act-on-blocked-milestones**: The team SHOULD raise what blocks a milestone when it reviews its active work, and act to remove it. (claims: kanban-unblock-and-age, scrum-impediments)
- **at-risk-milestone-names-its-risk**: A status update that reports a milestone at risk SHOULD name the risk or concern that puts it at risk. (claims: linear-project-health-updates, github-status-updates, prince2-issue-includes-concern, schedule-narrative-explains-changes)
- **blocked-milestone-has-issue-or-concern**: A blocked milestone MUST pass this check: no milestone is blocked without a corresponding issue or concern (claim: blocked-milestone-has-issue-or-concern-prior)

### Forecasting and committing to dates

- **forecast-dates-from-history-as-ranges**: A forecast milestone date SHOULD be drawn from the team's history, its cycle times or its past estimate accuracy, and given as an elapsed time or a date paired with a probability. (claims: kanban-sle-forecast, evidence-based-scheduling)
- **forecast-charts-do-not-replace-empiricism**: A team MAY forecast progress with burn-down, burn-up or cumulative flow charts, used alongside inspection of the work actually done and not in place of it. (claim: scrum-forecasting-practices)
- **commit-after-uncertainty-narrows**: A team SHOULD NOT commit to a milestone date until the decisions that narrow the uncertainty in its estimate have been made. (claim: commit-after-cone-narrows)
- **commit-near-term-forecast-later**: A roadmap MAY commit the next increment and present the increments after it only as forecasts. (claim: safe-roadmap-commit-near-forecast-far)
- **fix-the-date-flex-the-scope**: A team MAY fix the time a piece of work gets, as an appetite or a fixed-length Sprint or cycle, and vary its scope to fit, planning against a goal rather than deriving the date from a fixed scope. (claims: fixed-time-variable-scope, scrum-sprint-fixed-length, scrum-product-goal-target, linear-cycles-not-releases)

## Building a milestone schedule

*This section is informative.*

1. List the key events the project has to reach: its start, its finish, and the events between them, such as a decision, a release or a hand-over. Each one is a point in time, not a stretch of work. Where the team keeps a standard set, each entry carries its description, completion criteria, place in the work breakdown and deciding authority.
2. Put the work in as activities that lead to the milestones, each with a most-likely duration and no padding.
3. Link the activities and milestones by logic: GitHub's "blocked by" dependencies, Linear's end-to-start project dependencies, or Jira plan dependencies. Every activity has a predecessor and a successor; any that lacks one is explained in the schedule's notes.
4. Leave the dates to the logic. Working copies take a hard constraint when the team is testing float or resources; the baseline and the official updates carry none, except one tied to an outside event that is named in the basis document.
5. Export the links and run the cycle check below. Fix every cycle it reports, then run it again.
6. Compute the critical path, add the contingency as its own activities, and record the target ship date in one field.
7. Save the result as the baseline. From then on a date moves only through the team's change control.

## Checking the chains and finding the critical path

*This section is informative.*

A topological sort orders the milestones so that every one comes after the milestones it depends on. A complete order exists only when the graph has no cycle, so the sort is the cycle check: Python's `graphlib.TopologicalSorter` raises `CycleError`, and its second argument is one cycle, listed with the same node first and last. Trackers differ here: Jira does not stop a cyclic link being made, and Atlassian's advice is to export the links and scan them; Microsoft Project cannot calculate dates across a loop and offers to cancel the action that would make one.

With the graph acyclic, the critical path is its longest path by duration. NetworkX's `dag_longest_path` computes it from durations on the links.

## Taking a status update

*This section is informative.*

1. Pick the status date: the date the update is as of, never simply today or the last save.
2. Record actual starts and finishes up to that date, and forecast everything after it.
3. Read what the update shows: work complete, in progress or late, overdue open items, off-track dependencies and flagged items, and the current critical path.
4. Mark each milestone's status, using the tracker's own vocabulary (Linear's On track, At risk or Off track; a GitHub Projects status update; a Jira flag).
5. For each blocked milestone, name the issue or concern that blocks it; for each at-risk one, name the risk. Raise the blocked ones at the next review of active work.
6. Compare each forecast milestone date with its baseline date and say whether a slip reaches later work.
7. Write the update's narrative: the status of the key dates and the finish date, each change to them and why, and its likely effect.

## Examples

*This section is informative.*

A cycle check over the exported milestone links, followed by the critical path:

```python
from graphlib import TopologicalSorter, CycleError
import networkx as nx

# milestone -> the milestones it depends on
depends_on = {
    "api-freeze": {"start"},
    "docs-ready": {"api-freeze"},
    "beta": {"api-freeze"},
    "launch": {"beta", "docs-ready"},
}

try:
    order = list(TopologicalSorter(depends_on).static_order())
except CycleError as err:
    raise SystemExit(f"cycle in milestone chain: {' -> '.join(err.args[1])}")

# durations, in working days, of the work on each link
days = {("start", "api-freeze"): 15, ("api-freeze", "docs-ready"): 5,
        ("api-freeze", "beta"): 10, ("beta", "launch"): 5, ("docs-ready", "launch"): 3}
g = nx.DiGraph()
for (a, b), d in days.items():
    g.add_edge(a, b, days=d)
print(nx.dag_longest_path(g, weight="days"))   # ['start', 'api-freeze', 'beta', 'launch']
```

Had `start` also depended on `launch`, the sort would have stopped with `cycle in milestone chain: start -> launch -> beta -> api-freeze -> start` (the order the error lists varies).

A status update for one milestone:

```text
Status date:  2026-11-20
Milestone:    Beta
Status:       At risk
Baseline:     2026-12-01    Forecast: 2026-12-05 (+4 days)
Risk:         R-14 Load tests may fail on the new storage tier; mitigation in progress
Change:       Forecast moved 4 days after the API freeze slipped; launch still holds inside its contingency
```

A milestone given as work, and the same plan done as events with the work between them:

```text
As work (avoid):   "Build the export service"  (milestone, 3 weeks)
As events:         start -> [build export service, 15 days] -> Export service live (milestone)
```

## What a reviewer looks for

- Milestones that are not defined, sequenced, dated or tracked, or that span a stretch of work instead of marking an event.
- A schedule with no start or finish milestone, work represented as milestones, or so many milestones that the work driving them is hard to see.
- A target ship date held in more than one field.
- Milestones or activities placed by fixed dates rather than linked by logic, or an activity with no predecessor or successor and no stated reason.
- Hard date constraints in the baseline or an official status update, or an unavoidable one with no outside event named in the basis document.
- A cycle in the dependency chains; no topological-sort check over the exported links; a failed check that does not name its cycle.
- No critical path identified, or one that is not the longest path through the logic.
- No explicit contingency, risk margin padded into durations, or contingency that is not its own activity.
- An update with no status date, or one that uses the viewing date or the save date as its status date.
- A schedule left without regular updates, or progress tracked no more often than it is reported.
- A milestone with no status or no target date.
- No baseline under change control, or forecasts not compared with it.
- A changed milestone date, or a salient schedule change, with no explanation or effect stated.
- An at-risk or blocked milestone not identified; a blocked milestone with no corresponding issue or concern, or not raised and acted on; an at-risk milestone whose risk is not named.
- A forecast given as one firm date with no basis in the team's history or no probability, or a commitment made before the decisions that narrow the estimate.

## A complete review must establish

- Every milestone is defined as a key event with no duration, sequenced, dated and tracked; the schedule has start and finish milestones; work is not represented as milestones; the milestones are few enough that the work driving them is visible.
- Each target ship date is tracked in one place.
- Every activity and milestone is linked by logic, with each missing link justified, and the baseline and official updates carry no unjustified hard date constraint.
- The dependency chains hold no cycle, as shown by a topological sort of the exported links, and any cycle found was reported.
- The critical path is identified as the longest path through the acyclic logic.
- Contingency is explicit, held as separate activities, and durations carry no padding.
- Every update is taken against a valid status date, on a regular cadence, and progress is tracked more often than it is reported.
- Every milestone has a status and a target date.
- A baseline is kept under change control, each forecast is compared with it, and every change to a key milestone date, and every salient schedule change, is explained.
- Every at-risk or blocked milestone is identified; every blocked one has a corresponding issue or concern and is raised and acted on; every at-risk one names its risk.
- Forecast dates are drawn from history and carry a probability, and no date is committed before the uncertainty in its estimate has narrowed.

## A build must establish

- `define-and-sequence-milestones`: the milestones are defined, sequenced, given target dates, linked by dependency chains and tracked for status and progress.
- `milestone-marks-a-key-event`: each milestone marks a key event or stage and has no duration.
- `schedule-has-start-and-finish-milestones`: the schedule has a start milestone and a finish milestone.
- `work-is-not-a-milestone`: no work is represented as a milestone.
- `keep-milestones-few`: the milestones are few enough that the activity sequences driving them stay easy to identify.
- `document-standard-milestones`: where a standard set of milestones is used and documented, each entry has a description, completion criteria, a work-breakdown reference and a deciding authority.
- `one-place-for-the-target-date`: each target ship date is tracked in one place.
- `link-milestones-by-logic-not-fixed-dates`: every activity and milestone is joined by logic links, each activity with a predecessor and a successor.
- `justify-missing-logic`: every activity missing a predecessor or successor, other than the start and finish milestones, is justified in the schedule documentation.
- `no-hard-constraints-in-the-baseline`: the baseline and the official status updates carry no hard date constraint.
- `justify-unavoidable-hard-constraints`: every unavoidable hard date constraint names its controlling outside event in the basis document.
- `milestone-chains-have-no-cycles`: the dependency chains between milestones hold no cycle.
- `check-chains-by-topological-sort`: the exported dependency links pass a topological sort.
- `report-the-cycle-found`: a failed cycle check names the cycle it found.
- `identify-the-critical-path`: the critical path is identified as the longest-duration path through the acyclic logic.
- `critical-chain-is-an-option`: where the team schedules by critical chain instead of critical path, the schedule is built around keeping resources at a constant utilisation.
- `hold-explicit-schedule-contingency`: contingency is held as separate, monitored contingency activities.
- `estimate-without-padding`: activity durations are most-likely estimates with no risk margin inside them.
- `size-contingency-by-risk-analysis`: where a schedule risk analysis is run, it gives the contingency for a stated level of confidence and lists the high-priority risks.
- `status-against-a-status-date`: each update states its status date, with actuals before it and forecasts after it.
- `status-date-is-not-view-or-save-date`: no update uses the viewing date or the latest save date as its status date.
- `update-on-a-regular-cadence`: the schedule is updated on a regular cadence suited to the project's duration, complexity and risk.
- `track-more-often-than-reported`: progress is tracked more often than it is reported.
- `milestone-has-status-and-target-date`: every milestone has a status and a target date.
- `keep-a-baseline-and-report-variance`: a baseline is kept under change control and each forecast milestone date is compared with its baseline date and its downstream effect.
- `explain-every-milestone-date-change`: each status update gives the status of the key milestone dates, the finish date included, and explains each change to them.
- `document-schedule-changes`: every change made during statusing is documented, and each salient one is justified with its likely effect.
- `identify-at-risk-or-blocked-milestones`: each status update identifies the at-risk and blocked milestones.
- `act-on-blocked-milestones`: each blocked milestone is raised when active work is reviewed and acted on.
- `at-risk-milestone-names-its-risk`: every milestone reported at risk names the risk or concern behind it.
- `blocked-milestone-has-issue-or-concern`: no milestone is blocked without a corresponding issue or concern.
- `forecast-dates-from-history-as-ranges`: each forecast milestone date is drawn from the team's history and paired with a probability.
- `forecast-charts-do-not-replace-empiricism`: where burn-down, burn-up or cumulative flow charts forecast progress, the work actually done is inspected as well.
- `commit-after-uncertainty-narrows`: no milestone date is committed before the decisions that narrow its estimate are made.
- `commit-near-term-forecast-later`: where a roadmap commits only the next increment, the later increments are marked as forecasts.
- `fix-the-date-flex-the-scope`: where the time is fixed, the scope is what varies to fit it.

## Rationale

*This section is informative.*

Most of the practice comes from the US Government Accountability Office's Schedule Assessment Guide (GAO-16-89G), a primary government standard for schedule quality: milestones as zero-duration events, logic links over fixed dates, the critical path, the status date, explicit contingency, the baseline and the narrative that explains each date change. The UK's Association for Project Management states the same logic and critical-path practice independently. GAO is written for large government programmes; the rules carry its practice at SHOULD, and its schedule risk analysis is a MAY, since few software teams run one.

The cycle rule is the one MUST. A loop makes an activity its own predecessor, so no date can be computed across it: GAO says so, Microsoft Project cannot calculate dates across one, and a complete topological order exists if and only if the graph has no cycle. The trackers differ on how a cycle is caught. Jira does not stop one being made and Atlassian's advice is to detect it afterwards, while Microsoft Project offers to cancel the action, so a topological sort the team runs itself is the dependable check.

The trackers supply the moving parts. GitHub milestones carry a due date and a completion percentage, GitHub issue dependencies record what blocks what, and GitHub Projects status updates carry a status, dates and a message. Linear milestones show completion and make a date optional, its project dependencies are end-to-start, and its project updates carry a health indicator and text on challenges. Jira plans mark dependencies at risk, warn of overdue work, and flag blocked items. The Kanban Guide and the Scrum Guide add the forecasting and the handling of impediments: Kanban's service level expectation pairs an elapsed time with a probability drawn from cycle-time history, and the Scrum Guide counts burn charts as useful but no substitute for empiricism. McConnell's cone of uncertainty warns against committing early; SAFe commits one increment and forecasts the next two.

The second check found twelve claims supported only in part, and their trust was lowered: logic sequencing (no source says it lets progress be measured), hard constraints and the status date (GAO does not call either a "common error"), Microsoft Project's cancel option (not stated as the default), the critical-chain buffers, the risk-analysis inputs, GitHub's status values, Spolsky's evidence-based scheduling and his remark on halfhearted schedules, the Product Goal as a contrast to dated milestones, Linear cycles as "not a milestone", and the FAA example of standard milestones. No rule citing them carries MUST, and the rules are worded to what the quotes hold.

Two rules are kept word for word from projectteam's checks for the owner to decide: `milestone-has-status-and-target-date` and `blocked-milestone-has-issue-or-concern`. No source makes either a must-hold check. Linear and GitHub make a milestone's date optional and GAO asks for the status of key milestones; the trackers let a blocked item carry a reason but do not require one. The owner's open questions are whether these two stay as must-hold checks or become SHOULDs, whether a target date is a committed date or a forecast from the logic (GAO keeps hard constraints out of the baseline), whether the at-risk case joins the blocked case in one rule, which status vocabulary the cookbook names, whether it names an update cadence, and whether fixing the date and flexing the scope stays as an option beside critical-path scheduling.

Delivery dependencies on other teams belong to the dependency-tracking guideline, tasks and their blockers to the task-breakdown guideline, and the links between project records to the project-record-linking guideline, all in `planning/project-management`.

## References

*This section is informative. Every reference is informative.*

- US Government Accountability Office, [Schedule Assessment Guide: Best Practices for Project Schedules (GAO-16-89G)](https://www.gao.gov/assets/d1689G.pdf)
- Association for Project Management, [What is scheduling in project management?](https://apm.org.uk/resources/what-is-project-management/what-is-scheduling-in-project-management/)
- GitHub, [About milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones), [Customizing the roadmap layout](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-roadmap-layout), [Creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies), [Sharing project updates](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/sharing-project-updates) and [Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- Linear, [Project milestones](https://linear.app/docs/project-milestones), [Project dependencies](https://linear.app/docs/project-dependencies), [Cycles](https://linear.app/docs/use-cycles) and [Initiative and project updates](https://linear.app/docs/initiative-and-project-updates)
- Atlassian, [What are dependencies in plans](https://support.atlassian.com/jira-software-cloud/docs/what-are-dependencies-in-advanced-roadmaps), [Troubleshoot warnings on your timeline](https://support.atlassian.com/jira-software-cloud/docs/troubleshoot-warnings-on-your-timeline-in-advanced-roadmaps), [Flag a work item](https://support.atlassian.com/jira-software-cloud/docs/flag-an-issue/) and [How to identify cyclic issue links or loops in Jira](https://support.atlassian.com/jira/kb/how-to-identify-cyclic-issue-links-or-loops-in-jira/)
- Microsoft, [Circular dependencies in Project](https://support.microsoft.com/en-us/article/49988375-7b43-4e55-abeb-d21e6ed9bff8)
- Python, [graphlib: Functionality to operate with graph-like structures](https://docs.python.org/3/library/graphlib.html)
- NetworkX, [dag_longest_path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.dag_longest_path.html)
- Schwaber and Sutherland, [The Scrum Guide](https://www.scrumguides.org/scrum-guide.html)
- kanbanguides.org, [The Kanban Guide](https://kanbanguides.org/english/)
- PeopleCert, [PRINCE2 7 issues](https://www.peoplecert.org/news-and-announcements/prince2-7-issues)
- Scaled Agile, [PI Planning](https://framework.scaledagile.com/PI-planning) and [Roadmap](https://framework.scaledagile.com/roadmap)
- Ryan Singer, [Shape Up: Set Boundaries](https://basecamp.com/shapeup/1.2-chapter-03)
- Joel Spolsky, [Evidence Based Scheduling](https://www.joelonsoftware.com/2007/10/26/evidence-based-scheduling/)
- Steve McConnell, [The Cone of Uncertainty](https://www.construx.com/wp-content/uploads/2019/02/CxWhitePaper_ConeOfUncertainty.pdf)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
