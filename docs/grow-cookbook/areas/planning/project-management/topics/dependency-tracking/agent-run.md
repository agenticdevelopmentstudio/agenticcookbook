I wrote both files and the validator prints `Research passed.`

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/dependency-tracking/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/dependency-tracking/research/research.md`

**Claims per question (32 in total)**
- best-practices: 11 (9 from research, plus the 2 `-prior` claims for the unsupported rules)
- known-solutions: 8
- platform-guidelines: 7
- experts-view: 6

**Verdicts**
- `map-internal-and-external-dependencies`: supported (internal-and-external-dependency-classes, raid-log-tracks-dependencies-with-risks, cluster-blockers-internal-external, identify-dependencies-in-planning-with-others)
- `track-dependency-availability-and-status`: supported (raid-entry-owner-due-date-status, review-dependencies-regularly, document-dependency-type-source-timeline, kanban-guide-unblock-and-review, tracker-health-on-track-at-risk-off-track)
- `flag-at-risk-or-blocked-dependencies`: supported (github-issue-dependencies-blocked-icon, linear-blocked-by-flags, jira-flag-impediment, jira-plans-off-track-dependencies, leopold-red-blocker-sticker-days-blocked)
- `dependency-has-type-and-status`: unsupported, because the sources support it only at SHOULD (dependency-has-type-and-status-prior, document-dependency-type-source-timeline, raid-entry-owner-due-date-status)
- `blocked-dependency-linked-to-affected-work`: unsupported, because the sources support it only at SHOULD (blocked-dependency-linked-to-affected-work-prior, github-projects-define-blockers-and-fields, github-issue-dependencies-blocked-icon, jira-plans-off-track-dependencies, at-risk-dependency-entered-as-risk)
- `dependency-owner-agreed-on-both-sides`: new, SHOULD (owner-agreed-and-confirmed-by-other-side, raid-entry-owner-due-date-status, apm-common-difficulties, document-dependency-type-source-timeline)
- `dependency-has-need-by-date`: new, SHOULD (dependency-statement-with-need-by-date, raid-entry-owner-due-date-status, apm-common-difficulties)
- `dependency-status-values`: new, SHOULD; this answers the "Blocked dependency flagging" question (tracker-health-on-track-at-risk-off-track, raid-entry-owner-due-date-status, linear-blocked-by-flags, jira-plans-off-track-dependencies, linear-update-reminders-and-staleness, stale-log-loses-value)
- `escalate-blocked-dependency-before-milestone`: new, SHOULD (safe-art-sync-escalation-point, prince2-manage-by-exception, scrum-guide-impediments, less-just-talk-and-scouts, communicate-dependency-changes)
- `at-risk-dependency-logged-as-risk`: new, SHOULD (at-risk-dependency-entered-as-risk, apm-common-difficulties)
- `reduce-dependencies-before-tracking`: new, SHOULD (rescope-to-remove-dependencies, less-minimise-dependencies-feature-teams, each-dependency-halves-on-time-chance)
- `record-blocker-reason-and-duration`: new, MAY to SHOULD (leopold-red-blocker-sticker-days-blocked, jira-flag-impediment, cluster-blockers-internal-external)
- `identify-dependencies-during-planning`: new, SHOULD (identify-dependencies-in-planning-with-others, safe-pi-planning-identifies-dependencies)

**Notes**
- **Sources I could not read.** pmi.org, iso.org and the GAO guide returned 403 errors, so no claim cites the PMBOK Guide, ISO 21502, ISO 31000 or GAO. I could reach PRINCE2 only through secondary sources (APM and prince2.wiki). These gaps are listed in `limitations`.
- **Low-trust figure.** The claim that each dependency halves the chance of on-time completion is a teaching model from a talk, not a study. It is scored 25.
- **Quotes I replaced.** Before validating, I found that five claims carried quoted sentences that were not in my fetched-quote notes (Jira flag, LeSS coordination, the Essex review and identification claims, PRINCE2). I replaced them with quotes from those notes. The Scrum Guide quote differed from my notes only in its apostrophe, which I changed to match them.
- **Not committed.** I have not committed the two files, because the brief said to write those two files and change nothing else.
