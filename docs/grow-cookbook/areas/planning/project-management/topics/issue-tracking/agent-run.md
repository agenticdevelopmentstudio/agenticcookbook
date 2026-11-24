I wrote both research files for issue-tracking, and the exact cookr validate line prints `Research passed.`

Files:
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/issue-tracking/research/research.json
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/issue-tracking/research/research.md

Claims per question (46 in all):
- best-practices: 24 (this includes the two `-prior` claims)
- known-solutions: 12
- platform-guidelines: 4
- experts-view: 6

Verdicts:
- identify-assess-severity-and-triage: supported (triage-identifies-categorizes-prioritizes, severity-describes-impact, triage-sets-severity-on-every-defect, linear-triage-inbox)
- link-issues-to-findings: unsupported (link-issues-to-findings-prior, link-related-records)
- track-resolution-status: supported (status-tracks-to-resolution, scrum-impediments-removed, kanban-active-management)
- escalate-critical-issues: supported (escalate-critical-full-attention, critical-notifies-beyond-assignee)
- issue-has-severity-and-status: contradicted (issue-has-severity-and-status-prior, triage-sets-severity-on-every-defect, github-no-default-severity, jira-priority-conflates-severity, linear-priority-five-levels)
- critical-issue-owned-or-escalated: supported (escalate-critical-full-attention, critical-notifies-beyond-assignee, issue-has-one-owner)
- resolved-issue-references-resolution: supported (record-resolution, resolution-reason-from-fixed-set, link-fix-to-issue, jira-resolution-field-unresolved)
- defect-has-severity-every-issue-has-status: new (triage-sets-severity-on-every-defect, status-tracks-to-resolution)
- severity-kept-apart-from-priority: new (severity-separate-from-priority, mozilla-bugzilla-severity-priority-fields, google-issue-tracker-priority-and-severity, jira-priority-conflates-severity)
- define-issue-severity-levels: new (severity-levels-defined, regression-not-severity)
- severity-change-needs-rationale: new (severity-change-needs-rationale)
- severity-set-by-assessor-not-reporter: new (priority-inflation)
- escalation-path-documented: new (escalation-procedure-documented)
- escalate-unresolved-after-time-limit: new (escalate-unresolved-after-time)
- triage-has-a-named-owner: new (triage-has-named-owner)
- triage-new-issues-promptly: new (triage-within-time-bound, untriaged-is-visible)
- every-issue-has-one-owner: new (issue-has-one-owner)
- record-resolution-reason: new (resolution-reason-from-fixed-set, itil-known-error)
- link-fix-change-to-issue: new (link-fix-to-issue)
- close-duplicates-linking-canonical: new (close-duplicates-link-canonical, duplicates-refiled)
- close-unplanned-work-definitively: new (close-not-planned-definitively)
- verify-resolution-before-close: new (verify-resolution)
- keep-closed-issues-as-history: new (keep-closed-as-history)
- communicate-resolution-to-stakeholders: new (communicate-resolution)
- issue-records-minimum-fields: new (issue-log-minimum-fields, spolsky-three-things)
- keep-priority-scale-small: new (avoid-extra-fields, linear-priority-five-levels)
- one-tracker-everyone-uses: new (bug-database-everyone-uses, pmbok-issue-log)
- issue-covers-more-than-defects: new (prince2-issue-broad, pmbok-issue-log)
- flag-stale-issues: new (stale-issues-flagged, kanban-active-management)

The two verdicts that go against the brief:
- **issue-has-severity-and-status (contradicted):** Mozilla lets tasks and enhancements carry a severity of N/A, and GitHub, Jira and Linear have no severity field. The supported form is the new `defect-has-severity-every-issue-has-status`.
- **link-issues-to-findings (unsupported):** no source mentions "specialist findings". The sources only support linking related records, which belongs to project-record-linking.

Sources I could not use as primaries, recorded in `limitations`:
- **PMBOK:** the PMI library returned 403, so its issue definition comes from a CDC newsletter that quotes it.
- **ISO 21502 and ISO 31000:** paywalled, with no public issue text.
- **ITIL 4:** paywalled, so its "known error" definition comes from Atlassian's own page.
- **SAFe and LeSS:** not researched.
- **The IEEE TSE priority-inflation paper:** only its abstract (read from OpenAlex) is quoted.

I made no commit, since the brief said to write the two files and edit nothing else.
