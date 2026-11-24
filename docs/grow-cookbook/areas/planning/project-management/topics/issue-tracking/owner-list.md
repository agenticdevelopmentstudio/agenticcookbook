# Owner list: issue-tracking

For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **link-issues-to-findings** — verdict `unsupported` (claims: link-issues-to-findings-prior, link-related-records). Prior text, kept word for word: "link issues to specialist findings when applicable" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "A team SHOULD do this:" (the one change the reviewer accepts)
  - against: Trackers let an issue reference related issues, pull requests, incidents and changes; none of the sources links issues to review findings as such.
- **issue-has-severity-and-status** — verdict `contradicted` (claims: issue-has-severity-and-status-prior, triage-sets-severity-on-every-defect, github-no-default-severity, jira-priority-conflates-severity, linear-priority-five-levels). Prior text, kept word for word: "Every issue has severity and status" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "This MUST hold:" (the one change the reviewer accepts)
  - against: Mozilla counts a defect as triaged only once it has a severity, so that no critical issue is missed; tasks and enhancements may carry a severity of N/A.
  - against: GitHub ships default labels (bug, duplicate, wontfix and others) but no severity or priority; teams add them as labels or a project single-select field.
  - against: Jira ships priority but no severity field; its default priority descriptions read as severity.
  - against: Linear offers a fixed five-value priority (No priority to Urgent), no severity field, and deliberately no custom priorities.

## Open questions

- Which severity scale the cookbook adopts: Mozilla's four levels (S1 Catastrophic to S4 Small/Trivial) or Atlassian's three (Critical, Major, Minor), or another.
- Whether tasks and enhancements carry a severity, or only defects (Mozilla allows N/A for tasks and enhancements).
- The escalation time limit for an unresolved critical issue, and who it escalates to (Mozilla assigns S1 within 2 business days and notifies Release Management; Linear's example is a 24 hour SLA for Urgent).
- Whether the reporter (or a named verifier) must confirm a fix before the issue is closed, or the fixer may close it.
- Whether the rule to link issues to specialist findings stays, since no source covers specialist findings; the general linking convention is project-record-linking's.
- Whether priority stays optional beside severity (Mozilla makes it optional) or is required.
