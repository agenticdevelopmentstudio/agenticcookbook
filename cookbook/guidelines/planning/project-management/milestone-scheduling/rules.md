
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

