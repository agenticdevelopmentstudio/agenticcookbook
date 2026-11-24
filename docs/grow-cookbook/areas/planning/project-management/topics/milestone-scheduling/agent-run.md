I wrote both research files and the validate command prints `Research passed.`

- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/milestone-scheduling/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/milestone-scheduling/research/research.md`

**Claims per question (50 in all):**
- best-practices: 17, including the two `-prior` claims
- known-solutions: 18
- platform-guidelines: 10
- experts-view: 5

**Verdicts:**
- define-and-sequence-milestones, supported: sequence-with-logic, milestones-are-zero-duration-key-events, github-milestones-due-date-progress, github-projects-roadmap-dates, github-define-blocked-by-and-one-target-date, linear-milestones-optional-date, linear-project-dependencies, jira-plan-dependencies, safe-planning-board-milestones
- identify-at-risk-or-blocked-milestones, supported: status-reveals-late-work, jira-off-track-warnings, jira-flag-impediment, linear-project-health-updates, github-status-updates, github-issue-dependencies, kanban-unblock-and-age, scrum-impediments
- milestone-has-status-and-target-date, unsupported: milestone-has-status-and-target-date-prior, schedule-narrative-explains-changes, baseline-and-variance, github-status-updates, linear-milestones-optional-date, github-milestones-due-date-progress
  - It holds only as a SHOULD: Linear and GitHub make milestone dates optional, and GAO asks only that key milestones be reported.
- milestone-chains-have-no-cycles, supported: assess-network-for-circular-logic, ms-project-refuses-circular-dependency, topological-order-iff-acyclic, jira-cyclic-links-detected-after
- blocked-milestone-has-issue-or-concern, unsupported: blocked-milestone-has-issue-or-concern-prior, github-issue-dependencies, jira-flag-impediment, prince2-issue-includes-concern, schedule-narrative-explains-changes, linear-project-health-updates
  - It holds only as a SHOULD; no source makes it a must-hold check.
- milestone-marks-a-key-event, new (SHOULD): milestones-are-zero-duration-key-events, standard-milestones-documented-with-criteria, too-many-milestones-mask-work
- link-milestones-by-logic-not-fixed-dates, new (SHOULD): sequence-with-logic, missing-logic-justified, avoid-hard-date-constraints, hard-constraints-defeat-cpm
- check-chains-by-topological-sort, new (SHOULD; answers the cycle-detection question): topological-order-iff-acyclic, assess-network-for-circular-logic, ms-project-refuses-circular-dependency, jira-cyclic-links-detected-after
- identify-the-critical-path, new (SHOULD): critical-path-is-longest-path, critical-path-is-dag-longest-path, critical-path-vs-critical-chain
- status-against-a-status-date, new (SHOULD): status-date-separates-actual-from-remaining, update-regularly-track-finer-than-report, status-date-not-view-date, linear-project-health-updates
- hold-explicit-schedule-contingency, new (SHOULD): schedule-contingency-is-explicit, risk-margin-not-padding, schedule-risk-analysis-sizes-contingency, critical-path-vs-critical-chain
- keep-a-baseline-and-report-variance, new (SHOULD): baseline-and-variance
- explain-every-milestone-date-change, new (SHOULD): schedule-narrative-explains-changes, avoid-hard-date-constraints
- at-risk-milestone-names-its-risk, new (SHOULD; the at-risk half of the blocked-milestone question): linear-project-health-updates, github-status-updates, prince2-issue-includes-concern, schedule-risk-analysis-sizes-contingency, schedule-narrative-explains-changes
- forecast-dates-from-history-as-ranges, new (SHOULD): kanban-sle-forecast, scrum-forecasting-practices, evidence-based-scheduling, commit-after-cone-narrows, schedules-are-halfhearted
- fix-the-date-flex-the-scope, new (MAY): fixed-time-variable-scope, scrum-sprint-fixed-length, scrum-product-goal-target, linear-cycles-not-releases
- commit-near-term-forecast-later, new (MAY): safe-roadmap-commit-near-forecast-far, commit-after-cone-narrows

The new rules' strengths are written in the summary field. The verdict format has no strength field, so they are not on the verdicts themselves.

The PMBOK Guide, ISO 21502's text and the PRINCE2 7 manual all refused the fetch or are paywalled, so none of them is quoted. They are listed under `limitations`.

Before validating, I checked every GAO quote against the text extracted from the PDF, and all were found. I also removed two details I could not trace to a fetched page: the Kanban Guide's named authors (now credited to "kanbanguides.org", dated 2025-05) and a "manual co-author" description of the PRINCE2 article's writer.

`research.json` also has one key the example shape doesn't list, `research_questions`, holding the brief's six research questions. The validator accepted it.

Nothing was committed, since the task asked only for the two files. I also deleted a temporary text file I had made in the scratchpad.
