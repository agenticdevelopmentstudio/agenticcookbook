# Owner list: dependency-tracking

For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **dependency-has-type-and-status** — verdict `unsupported` (claims: dependency-has-type-and-status-prior, document-dependency-type-source-timeline, raid-entry-owner-due-date-status). Prior text, kept word for word: "Every dependency has a type and status" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "A dependency record MUST keep this true:" (the one change the reviewer accepts)
  - against: Each identified dependency is documented with its type (inward or outward), its source, its specification and its timeline, agreed in a signed-off dependency agreement, and then monitored for its whole life.
  - against: In a RAID log each dependency entry has a designated owner, a due date and a status, and Blocked is one of the statuses a dependency entry takes.
- **blocked-dependency-linked-to-affected-work** — verdict `unsupported` (claims: blocked-dependency-linked-to-affected-work-prior, github-projects-define-blockers-and-fields, github-issue-dependencies-blocked-icon, jira-plans-off-track-dependencies, at-risk-dependency-entered-as-risk). Prior text, kept word for word: "blocked or at-risk dependencies are linked to affected milestones or todos" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "A dependency record MUST keep this true:" (the one change the reviewer accepts)
  - against: GitHub's guidance for Projects is to define which issues are blocked by or blocking others, track status in a single-select field with preset values and target dates in a date field, and automate updates so the project stays current.
  - against: GitHub Issues records dependencies as 'blocked by' and 'blocking' links between issues, and marks a blocked issue with a Blocked icon on project boards and the Issues page.
  - against: Jira Plans treats work-item links as dependencies (Blocks by default), and its dependencies view and program board show a dependency in red when it is off-track, with filters to list only off-track dependencies.
  - against: A dependency assessed as a risk to the project, or a threat to it such as lateness, is also entered in the risk log or register and reviewed for its effect on milestones.

## Open questions

- Whether the two Verify clauses (every dependency has a type and status; blocked or at-risk dependencies are linked to affected milestones or todos) stay as must-hold checks as a house convention, or are restated at SHOULD, the strength the sources support.
- Which status vocabulary the cookbook adopts for a dependency: the trackers' project-health set (On track, At risk, Off track) plus Blocked and Done, or another set; the sources offer several and none is a standard.
- What 'type' means for a dependency in the cookbook: internal versus external (PRINCE2), internal / intra / external (MSP, Essex), inward versus outward (APM), the PMBOK's mandatory / discretionary, or what the dependency is on (team, vendor, task, decision); the sources use all of these.
- When a blocked or at-risk dependency is escalated: at a fixed review cadence, as soon as its need-by date is forecast to be missed (PRINCE2's manage-by-exception), or at a named forum such as SAFe's ART Sync; the sources give no single trigger.
- Whether a dependency at risk is also entered as a risk (Essex, APM), which would couple this topic to risk-tracking, or stays only in the dependency record.
