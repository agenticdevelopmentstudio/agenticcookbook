# milestone-scheduling: research

Researched 2026-11-24 for `cookbook/guidelines/planning/project-management/milestone-scheduling`. The full record, with every quote, citation and verdict, is `research.json` beside this file. Apple, Android and Windows have no bearing on this topic.

## Best practices

Best practices: what is current best practice for this topic?

- A milestone is a zero-duration point that marks a key event or stage, and every schedule carries a start and a finish milestone (`milestones-are-zero-duration-key-events`). Where milestones are standardised, each is documented with a description, completion criteria, a work-breakdown reference and a decision authority (`standard-milestones-documented-with-criteria`).
- Sequence the work with logic links, so that critical dates can be met and progress can be measured, and verify that the logic is complete and defensible (`sequence-with-logic`). Every activity should have a predecessor and a successor, and any gap in the logic must be justified (`missing-logic-justified`).
- Keep hard date constraints out of the baseline and the official status updates. An unavoidable constraint is justified by an event outside the schedule (`avoid-hard-date-constraints`).
- Identify the critical path, which is the longest path through the logic and sets the earliest finish (`critical-path-is-longest-path`).
- Assess the network for circular logic, because a loop makes an activity its own predecessor (`assess-network-for-circular-logic`).
- Take status against a status date: past dates are actuals and future dates are forecasts (`status-date-separates-actual-from-remaining`). Update on a regular cadence set by the project's duration, complexity and risk, and track progress more often than it is reported (`update-regularly-track-finer-than-report`). Statusing shows what is complete, in progress or late (`status-reveals-late-work`).
- Hold schedule contingency as explicit buffer, not as padding inside each estimate (`schedule-contingency-is-explicit`, `risk-margin-not-padding`). A schedule risk analysis, fed from the risk register, sizes that buffer for a chosen level of confidence (`schedule-risk-analysis-sizes-contingency`).
- Keep a baseline under change control and monitor the forecast against it for variance and its downstream effect (`baseline-and-variance`).
- Each status update carries a narrative that gives the status of key milestone dates and explains any change to them (`schedule-narrative-explains-changes`).
- The two prior Verify rules are recorded as their own claims because no source holds them at the must-hold strength they state: `milestone-has-status-and-target-date-prior` and `blocked-milestone-has-issue-or-concern-prior`.

## Known solutions

Known solutions: what solutions, patterns, libraries and tools already exist, and how do they compare?

- **GitHub.** A milestone groups issues and pull requests and shows a due date and a completion percentage (`github-milestones-due-date-progress`). The Projects roadmap layout places items on a timeline from date and iteration fields and can mark milestones (`github-projects-roadmap-dates`). Issue dependencies record what blocks what (`github-issue-dependencies`). Project status updates carry a status such as On track or At risk, a start date, a target date and a message (`github-status-updates`).
- **Linear.** Project milestones are stages that show a completion percentage. A date on a milestone is optional (`linear-milestones-optional-date`). Project dependencies are end-to-start links, and a violated one is drawn in red (`linear-project-dependencies`). Cycles are time-boxes that are not tied to releases, so a cycle is not a milestone (`linear-cycles-not-releases`). Project updates carry an On track, At risk or Off track health indicator, text on challenges, and reminders on a set cadence (`linear-project-health-updates`).
- **Jira.** Plans use finish-before-start dependencies and turn a dependency red when it puts the dependent item at risk (`jira-plan-dependencies`). They also warn about off-track dependencies and overdue open work (`jira-off-track-warnings`). A flag marks an item as blocked, with an optional comment (`jira-flag-impediment`). Jira does not stop cyclic links from being created. Atlassian's guidance is to export the links afterwards and scan them for loops (`jira-cyclic-links-detected-after`).
- **Microsoft Project** cannot calculate dates across a circular dependency, and by default it cancels the action that would create one (`ms-project-refuses-circular-dependency`).
- **Cycle check and critical path in code.** A complete topological order exists only if the graph is acyclic. Python's `graphlib` raises `CycleError` and reports one cycle (`topological-order-iff-acyclic`). Once the graph is acyclic, the critical path is its longest path, which NetworkX's `dag_longest_path` computes (`critical-path-is-dag-longest-path`). In short: GitHub and Linear record dependencies, Jira detects loops only after the fact, Microsoft Project refuses them at entry, and a topological sort is the check a team can run itself.
- **Methods compared.** Critical path scheduling centres on activities and their logic, while critical chain centres on resources and protects chains with buffers (`critical-path-vs-critical-chain`). Evidence-based scheduling simulates outcomes from past estimate accuracy and gives a probability for each ship date (`evidence-based-scheduling`). Shape Up fixes the time and lets the scope vary (`fixed-time-variable-scope`).

## Platform guidelines

Platform guidelines: what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?

Apple, Android and Windows have no bearing on milestone scheduling. The platform owners here are the trackers, the method owners and the runtime library.

- **GitHub** advises teams to say clearly which issues block which, to keep one target ship date in a single field, and to use milestones to show how issues add up to a goal (`github-define-blocked-by-and-one-target-date`).
- **Scrum Guide.** Teams plan against a Product Goal and review progress toward it at each Sprint Review (`scrum-product-goal-target`). Sprints are fixed-length (`scrum-sprint-fixed-length`). Burn-downs, burn-ups and cumulative flow help forecasting but do not replace empiricism (`scrum-forecasting-practices`). Impediments are raised daily, and removing them is part of the Scrum Master's accountability (`scrum-impediments`).
- **Kanban Guide.** Delivery is forecast with a service level expectation, which is an elapsed time paired with a probability and based on historical cycle time (`kanban-sle-forecast`). Active management keeps items from ageing and unblocks blocked work (`kanban-unblock-and-age`).
- **PRINCE2 7.** An issue is anything that could affect the project, including a problem or a concern (`prince2-issue-includes-concern`).
- **SAFe.** PI planning produces a board of delivery dates and dependencies, and milestones are used to monitor progress and risk (`safe-planning-board-milestones`). The roadmap commits the next increment and forecasts the two after it (`safe-roadmap-commit-near-forecast-far`).
- **Runtime.** Python's `graphlib` is the standard-library check for cycles (`topological-order-iff-acyclic`).
- The PMBOK Guide and ISO 21502 could not be read (see `limitations` in research.json), so they make no claim here.

## The expert's view

The expert's view: if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

- **Do:** link milestones by logic, check the chains for cycles with a topological sort, find the critical path, hold explicit buffer, take status against a status date, and explain every change to a milestone date (`sequence-with-logic`, `topological-order-iff-acyclic`, `critical-path-is-longest-path`, `schedule-contingency-is-explicit`, `status-date-separates-actual-from-remaining`, `schedule-narrative-explains-changes`).
- **Avoid:** pinning dates with hard constraints. This corrupts the critical path and undermines every date after the constraint (`hard-constraints-defeat-cpm`). Also avoid adding so many milestones that they hide the work driving them (`too-many-milestones-mask-work`).
- **Usually gotten wrong:** using today's date or the last save date as the status date (`status-date-not-view-date`), and committing to dates before decisions have narrowed the uncertainty (`commit-after-cone-narrows`). One practitioner adds that most schedules are not believed because they are not kept as working tools (`schedules-are-halfhearted`). That is an anecdote and is scored low.
- **Forecasting:** give dates as ranges drawn from history, not as single promises (`kanban-sle-forecast`, `evidence-based-scheduling`, `scrum-forecasting-practices`).
- **Blocked and at-risk milestones:** name the issue, the blocking item or the risk with the status. The trackers support this (`github-issue-dependencies`, `jira-flag-impediment`, `linear-project-health-updates`), PRINCE2 counts a concern as an issue (`prince2-issue-includes-concern`), and GAO wants every date change explained (`schedule-narrative-explains-changes`). No source makes it a must-hold check, so the rule holds as a SHOULD.
- **Verdicts on the prior rules.** `define-and-sequence-milestones`, `identify-at-risk-or-blocked-milestones` and `milestone-chains-have-no-cycles` are supported. `milestone-has-status-and-target-date` is unsupported as a rule for every milestone: Linear and GitHub make milestone dates optional, and GAO asks only that key milestones be reported (`milestone-has-status-and-target-date-prior`). It holds as a SHOULD. `blocked-milestone-has-issue-or-concern` is unsupported as a must-hold check and holds as a SHOULD (`blocked-milestone-has-issue-or-concern-prior`).
