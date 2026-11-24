# Owner list: milestone-scheduling

For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **milestone-has-status-and-target-date** — verdict `unsupported` (claims: milestone-has-status-and-target-date-prior, schedule-narrative-explains-changes, baseline-and-variance, github-status-updates, linear-milestones-optional-date, github-milestones-due-date-progress). Prior text, kept word for word: "Every milestone has a status and target date" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "Each milestone MUST pass this check:" (the one change the reviewer accepts)
  - against: Each status update should carry a narrative giving the status of key milestone dates and explaining any change in them.
  - against: A baseline schedule is kept under change control and the current forecast is monitored against it to reveal milestone variance and its downstream effect.
  - against: GitHub Projects status updates record a status such as On track or At risk, start and target dates, and a message.
  - against: Linear project milestones divide a project into stages with completion percentages; a target date on a milestone is optional.
  - against: GitHub milestones group a repository's issues and pull requests and show a due date and a completion percentage.
- **blocked-milestone-has-issue-or-concern** — verdict `unsupported` (claims: blocked-milestone-has-issue-or-concern-prior, github-issue-dependencies, jira-flag-impediment, prince2-issue-includes-concern, schedule-narrative-explains-changes, linear-project-health-updates). Prior text, kept word for word: "no milestone is blocked without a corresponding issue or concern" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "A blocked milestone MUST pass this check:" (the one change the reviewer accepts)
  - against: GitHub issue dependencies record which issue blocks which, and a blocked issue is marked as blocked by naming the issue it depends on.
  - against: Jira lets a work item be flagged as blocked (Flagged = Impediment) and optionally takes a comment when the flag is added or removed.
  - against: PRINCE2 7 defines an issue as anything that could affect the project, covering problems and concerns as well as opportunities.
  - against: Each status update should carry a narrative giving the status of key milestone dates and explaining any change in them.
  - against: Linear project updates carry a health indicator (On track, At risk, Off track) and a description of status, challenges and next steps, with reminders on a chosen cadence.

## Open questions

- Whether the two unsupported Verify rules (milestone-has-status-and-target-date, blocked-milestone-has-issue-or-concern) are kept as must-hold checks by house policy or restated at the SHOULD strength the sources support; the owner decides.
- Whether 'target date' in milestone-has-status-and-target-date means a fixed committed date or a forecast computed from logic: GAO says baseline and status schedules should not carry hard date constraints, so a policy that every milestone carries a fixed date conflicts with logic-driven scheduling unless the date is a baseline target.
- Whether the at-risk case joins the blocked case in one rule (every blocked or at-risk milestone names its issue or risk) or stays a separate rule; the brief's research question asks for both, the listed rule names only blocked.
- Which status vocabulary the cookbook names: Linear uses On track / At risk / Off track, GitHub Projects uses On track / At risk among others, Jira uses a Flagged = Impediment field; the owner decides whether to fix a vocabulary or leave it to the tracker.
- Whether the cookbook names a schedule update cadence; GAO ties cadence to duration, complexity and risk and gives only an example (track weekly when reporting monthly), so any fixed cadence is a policy choice.
- Whether 'fix the date, flex the scope' (Shape Up, Scrum's fixed-length Sprint) is stated as an option beside critical-path scheduling or left out; the sources present it as a method choice, not a universal practice.
