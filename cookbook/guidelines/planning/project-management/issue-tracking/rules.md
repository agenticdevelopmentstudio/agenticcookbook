
### Recording issues

- **one-tracker-everyone-uses**: Every project, whatever its size, SHOULD keep its issues in one tracker or issue log that everyone on the team uses, with filing kept light enough that people do not go around it. (claims: bug-database-everyone-uses, pmbok-issue-log)
- **issue-covers-more-than-defects**: The tracker MAY hold as an issue anything that could affect the project, not only a defect: a problem, a concern, an opportunity, a request for change, something off-specification or a matter not yet settled, raised by any stakeholder. (claims: prince2-issue-broad, pmbok-issue-log)
- **issue-records-minimum-fields**: An issue record SHOULD carry at least a unique identifier, a description, a summary of its impact, its owner, its current status and its next steps or target date, and a defect's description SHOULD give the steps to reproduce it, what was expected and what was seen instead. (claims: issue-log-minimum-fields, spolsky-three-things)
- **defect-has-severity-every-issue-has-status**: Every issue SHOULD carry a status, and every defect SHOULD carry a severity. (claims: triage-sets-severity-on-every-defect, status-tracks-to-resolution)
- **issue-has-severity-and-status**: This MUST hold: Every issue has severity and status (claim: issue-has-severity-and-status-prior)
- **keep-priority-scale-small**: A tracker's fields and priority levels SHOULD be kept few, as Linear's five fixed priority values are, because extra fields and finer levels make issues harder to file and to rank for little return. (claims: avoid-extra-fields, linear-priority-five-levels)
- **link-issues-to-findings**: A team SHOULD do this: link issues to specialist findings when applicable (claim: link-issues-to-findings-prior)

### Triage

- **identify-assess-severity-and-triage**: Each new issue SHOULD be triaged: identified, categorized by kind and owning area, assessed for severity by its impact, prioritized, and decided on whether, when and by whom it is worked. (claims: triage-identifies-categorizes-prioritizes, severity-describes-impact, triage-sets-severity-on-every-defect, linear-triage-inbox)
- **triage-has-a-named-owner**: Someone SHOULD be explicitly responsible for triaging new issues, a named person or a rotation, so that every new issue is seen and prioritized. (claim: triage-has-named-owner)
- **triage-new-issues-promptly**: A new issue SHOULD be triaged within a stated time, Mozilla's being one week, and until then be visibly marked or held apart as awaiting triage. (claims: triage-within-time-bound, untriaged-is-visible)
- **every-issue-has-one-owner**: Each issue SHOULD be assigned to exactly one owner once it is triaged, and stay owned by one person until it is closed. (claim: issue-has-one-owner)

### Severity

- **severity-kept-apart-from-priority**: An issue's severity (its impact) and its priority (the order in which it is fixed) SHOULD be kept in separate fields, because one field for both conflates impact with scheduling. (claims: severity-separate-from-priority, mozilla-bugzilla-severity-priority-fields, google-issue-tracker-priority-and-severity, jira-priority-conflates-severity)
- **define-issue-severity-levels**: A project SHOULD define a small severity scale whose levels are described by user impact, data loss and whether a workaround exists, judged by impact alone, so that being a regression neither raises nor lowers an issue's level. (claims: severity-levels-defined, regression-not-severity)
- **severity-set-by-assessor-not-reporter**: An issue's severity SHOULD be set by those who assess the issue, not by the person who filed it, because people filing issues inflate the priority of their own. (claim: priority-inflation)
- **severity-change-needs-rationale**: A project MAY require each change to an issue's severity to carry a comment giving the reason for it. (claim: severity-change-needs-rationale)

### Tracking and escalation

- **track-resolution-status**: An issue's status SHOULD move through a defined workflow from open to a closed state, and the issue SHOULD be actively managed on the way, its blockers removed. (claims: status-tracks-to-resolution, scrum-impediments-removed, kanban-active-management)
- **flag-stale-issues**: An issue that goes a set time without activity MAY be flagged as stale, as Kubernetes does after 90 days, so that it does not age unnoticed. (claims: stale-issues-flagged, kanban-active-management)
- **escalate-critical-issues**: An issue at the most severe level SHOULD get the immediate attention of anyone who can reasonably help, and a notice beyond the triage queue, as Mozilla notifies Release Management of its S1 and S2 bugs. (claims: escalate-critical-full-attention, critical-notifies-beyond-assignee)
- **critical-issue-owned-or-escalated**: A critical issue SHOULD be assigned to one owner within a short, stated time (Mozilla assigns S1 bugs within two business days) or else be escalated, so that it is never left without an owner. (claims: escalate-critical-full-attention, critical-notifies-beyond-assignee, issue-has-one-owner)
- **escalation-path-documented**: A project SHOULD agree on its escalation process and write it down as part of planning how it will manage issues. (claim: escalation-procedure-documented)
- **escalate-unresolved-after-time-limit**: An issue that stays unresolved past an agreed time, which trackers tie to its priority, SHOULD be escalated by the agreed escalation procedure. (claim: escalate-unresolved-after-time)

### Resolving issues

- **resolved-issue-references-resolution**: When an issue is resolved, how it was resolved SHOULD be recorded on the issue itself, so that no closed issue reads as unresolved. (claims: record-resolution, jira-resolution-field-unresolved)
- **record-resolution-reason**: A closed issue SHOULD record why it closed as one reason from a fixed set, such as fixed, won't fix, duplicate, cannot reproduce, by design or, for an ITIL problem with a documented root cause and workaround, known error. (claims: resolution-reason-from-fixed-set, itil-known-error)
- **link-fix-change-to-issue**: The change that fixes an issue SHOULD be linked to the issue, as a GitHub pull request or commit with a closing keyword, a Jira commit message carrying the issue key, or a Jira Service Management problem linked to its fixing change does. (claim: link-fix-to-issue)
- **verify-resolution-before-close**: A fix SHOULD be confirmed, by the reporter, a named verifier or a test, before the issue is closed. (claim: verify-resolution)
- **communicate-resolution-to-stakeholders**: Once an issue is resolved, its stakeholders MAY be told how it was resolved. (claim: communicate-resolution)

### Closing without a fix

- **close-duplicates-linking-canonical**: A duplicate issue SHOULD be closed with a link to the original issue and its reporter told, since important issues are often filed again. (claims: close-duplicates-link-canonical, duplicates-refiled)
- **close-unplanned-work-definitively**: Work the team will not do SHOULD be closed as not planned, with an honest explanation, rather than left open. (claim: close-not-planned-definitively)
- **keep-closed-issues-as-history**: Closed issues SHOULD remain in the tracker as a historical record for lessons learned. (claim: keep-closed-as-history)

