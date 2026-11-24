
### Finding and recording dependencies

- **identify-dependencies-during-planning**: A team SHOULD identify its dependencies during planning, together with the other teams, stakeholders and partners who know of hidden ones, and including the inbound dependencies other projects raise. (claims: identify-dependencies-in-planning-with-others, safe-pi-planning-identifies-dependencies)
- **map-internal-and-external-dependencies**: A team SHOULD map each dependency it waits on, such as another team completing a component, an approval, a vendor or a decision from above, and mark whether it is internal, under the team's control, or external, beyond it. (claims: internal-and-external-dependency-classes, raid-log-tracks-dependencies-with-risks)
- **dependency-has-type-and-status**: A dependency record MUST keep this true: Every dependency has a type and status (claim: dependency-has-type-and-status-prior)
- **dependency-owner-agreed-on-both-sides**: Each dependency SHOULD have agreed ownership of its management actions. (claims: owner-agreed-and-confirmed-by-other-side, raid-entry-owner-due-date-status, apm-common-difficulties)
- **dependency-confirmed-by-other-side**: Each dependency SHOULD be communicated to the owner of the other project or team, so that the other side confirms it and tracks it in its own dependency log. (claim: owner-agreed-and-confirmed-by-other-side)
- **dependency-has-need-by-date**: Each dependency SHOULD carry the date by which it is needed. (claims: dependency-statement-with-need-by-date, raid-entry-owner-due-date-status, apm-common-difficulties)
- **need-by-date-agreed-with-source**: A dependency's need-by date SHOULD be agreed with the dependency's source, to confirm that the date is achievable, resources included. (claim: dependency-statement-with-need-by-date)

### Keeping status current

- **dependency-status-values**: A dependency's status SHOULD be taken from a short preset list of values, one of which marks the dependency as blocked. (claims: tracker-health-on-track-at-risk-off-track, raid-entry-owner-due-date-status, linear-blocked-by-flags, github-projects-define-blockers-and-fields)
- **track-dependency-availability-and-status**: A team SHOULD keep tracking each dependency's status for the whole life of the dependency. (claims: raid-entry-owner-due-date-status, document-dependency-type-source-timeline, tracker-health-on-track-at-risk-off-track)
- **review-dependencies-at-regular-points**: A team SHOULD review its dependencies at regular points, such as status meetings, steering reviews and sprint planning. (claims: review-dependencies-regularly, kanban-guide-unblock-and-review)
- **stale-status-is-a-signal**: A dependency whose status update is overdue SHOULD be treated as a sign that its record is stale, and its status reconciled before the record is relied on again. (claims: linear-update-reminders-and-staleness, stale-log-loses-value)
- **include-dependencies-in-status-reports**: Dependencies SHOULD be included in the team's standard status reports. (claim: communicate-dependency-changes)
- **report-dependency-changes**: A change to a dependency SHOULD be pushed to the people it affects. (claim: communicate-dependency-changes)

### Blocked and at-risk dependencies

- **flag-at-risk-or-blocked-dependencies**: A blocked or off-track dependency SHOULD be flagged where everyone working on the affected work can see it, such as by a blocked-by link with a Blocked icon or flag on the board, a Jira Impediment flag, or a red mark on the blocked item. (claims: github-issue-dependencies-blocked-icon, linear-blocked-by-flags, jira-flag-impediment, jira-plans-off-track-dependencies, leopold-red-blocker-sticker-days-blocked)
- **blocked-dependency-linked-to-affected-work**: A dependency record MUST keep this true: blocked or at-risk dependencies are linked to affected milestones or todos (claim: blocked-dependency-linked-to-affected-work-prior)
- **record-blocker-reason**: A blocked dependency's record SHOULD give a brief reason why it is blocked. (claims: leopold-red-blocker-sticker-days-blocked, jira-flag-impediment)
- **count-days-dependency-blocked**: A blocked dependency's record MAY count the days it has stayed blocked. (claim: leopold-red-blocker-sticker-days-blocked)
- **keep-resolved-dependency-blockers**: The records of a dependency's resolved blockers SHOULD be kept, not thrown away. (claim: leopold-red-blocker-sticker-days-blocked)
- **analyse-resolved-blockers**: A team MAY cluster its resolved dependency blockers by internal and external causes, then by what they have in common, to find which kinds of blocker recur. (claim: cluster-blockers-internal-external)
- **at-risk-dependency-logged-as-risk**: A dependency assessed as a risk to the project, or threatened such as by lateness, SHOULD be acknowledged as a source of risk with a management plan, such as mitigation or contingency. (claims: at-risk-dependency-entered-as-risk, apm-common-difficulties)
- **at-risk-dependency-reviewed-against-milestones**: A dependency assessed as a risk to the project SHOULD be reviewed for its effect on the project's milestones. (claim: at-risk-dependency-entered-as-risk)

### Escalating and reducing dependencies

- **escalate-unresolved-blocked-dependency**: A blocked dependency the team cannot resolve locally SHOULD be escalated through a named forum or by exception, such as SAFe's ART Sync, the PRINCE2 project board once tolerance is exceeded, or the Scrum Master for an impediment. (claims: safe-art-sync-escalation-point, prince2-manage-by-exception, scrum-guide-impediments)
- **coordinate-directly-with-the-other-team**: A team MAY coordinate a dependency directly with the team it depends on, by talking to that team or by sending a scout to monitor the interface and report back. (claim: less-just-talk-and-scouts)
- **reduce-dependencies-before-tracking**: Teams SHOULD be organised to minimise the dependencies between them, so that each can complete its work without waiting on another. (claims: rescope-to-remove-dependencies, less-minimise-dependencies-feature-teams, each-dependency-halves-on-time-chance)
- **rescope-to-remove-difficult-dependency**: In extreme circumstances, a project MAY be re-scoped to remove a difficult dependency, for example by bringing its delivery within the project's control. (claim: rescope-to-remove-dependencies)

