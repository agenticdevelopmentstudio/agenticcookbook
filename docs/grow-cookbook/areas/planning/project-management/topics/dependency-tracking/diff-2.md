--- draft-1.md
+++ draft.md
@@ -13,13 +13,16 @@
 summary: "Tracking the delivery dependencies a team waits on: found in planning, owned, dated, kept current, flagged when blocked and escalated."
 platforms: []
 tags:
+  - dependency-tracking
   - dependencies
   - project-management
   - blockers
   - escalation
-  - raid-log
 depends-on: []
-related: []
+related:
+  - a55182ef-3144-407c-b64a-6377f37f5c63
+  - f264cc0b-45d3-4593-a437-7371610c5a8a
+  - 023d4c91-d797-4e82-880c-a4ad7906a54a
 references:
   - https://www.apm.org.uk/media/yppd2ddw/interdependencies-fusion-point-guidance.pdf
   - https://www.essex.ac.uk/staff/strategic-project-delivery/dependency-management
@@ -55,7 +58,7 @@
 
 Find the delivery dependencies a team waits on during planning, with the teams that know of them, and record each one with an agreed owner, a need-by date, a type and a status from a short preset list. Review them at regular points, flag a blocked or at-risk one where everyone can see it, link it to the work it holds up, and escalate one the team cannot resolve through a named forum or by exception; where possible, organise teams so the dependency is not there to track.
 
-This guideline covers how any delivery team identifies, records, reviews, flags and escalates its delivery dependencies: what it waits on from other teams, vendors, approvals, tasks and decisions, inside or outside its control. It does not cover software dependencies such as libraries and operating-system frameworks, the ordering of milestones and the critical path, which belong to milestone scheduling, or the general convention for linking project records, which belongs to project record linking. Following it means keeping every MUST rule below, and keeping each SHOULD rule or stating why a dependency record departs from it.
+This guideline covers how any delivery team identifies, records, reviews, flags and escalates its delivery dependencies: what it waits on from other teams, vendors, approvals, tasks and decisions, inside or outside its control. It does not cover software dependencies such as libraries and operating-system frameworks, the ordering of milestones and the critical path, which belong to milestone scheduling, the blocked tasks inside a team's own work, which belong to task breakdown, or the general convention for linking project records, which belongs to project record linking. Following it means keeping every MUST rule below, and keeping each SHOULD rule or stating why a dependency record departs from it.
 
 ## Rules
 
@@ -64,29 +67,36 @@
 - **identify-dependencies-during-planning**: A team SHOULD identify its dependencies during planning, together with the other teams, stakeholders and partners who know of hidden ones, and including the inbound dependencies other projects raise. (claims: identify-dependencies-in-planning-with-others, safe-pi-planning-identifies-dependencies)
 - **map-internal-and-external-dependencies**: A team SHOULD map each dependency it waits on, such as another team completing a component, an approval, a vendor or a decision from above, and mark whether it is internal, under the team's control, or external, beyond it. (claims: internal-and-external-dependency-classes, raid-log-tracks-dependencies-with-risks)
 - **dependency-has-type-and-status**: A dependency record MUST keep this true: Every dependency has a type and status (claim: dependency-has-type-and-status-prior)
-- **dependency-owner-agreed-on-both-sides**: Each dependency SHOULD have agreed ownership of its management actions, and be communicated to the owner of the other project or team so that it confirms the dependency and tracks it in its own dependency log. (claims: owner-agreed-and-confirmed-by-other-side, raid-entry-owner-due-date-status, apm-common-difficulties)
-- **dependency-has-need-by-date**: Each dependency SHOULD carry the date by which it is needed, agreed with the dependency's source to confirm that the date is achievable. (claims: dependency-statement-with-need-by-date, raid-entry-owner-due-date-status, apm-common-difficulties)
+- **dependency-owner-agreed-on-both-sides**: Each dependency SHOULD have agreed ownership of its management actions. (claims: owner-agreed-and-confirmed-by-other-side, raid-entry-owner-due-date-status, apm-common-difficulties)
+- **dependency-confirmed-by-other-side**: Each dependency SHOULD be communicated to the owner of the other project or team, so that the other side confirms it and tracks it in its own dependency log. (claim: owner-agreed-and-confirmed-by-other-side)
+- **dependency-has-need-by-date**: Each dependency SHOULD carry the date by which it is needed. (claims: dependency-statement-with-need-by-date, raid-entry-owner-due-date-status, apm-common-difficulties)
+- **need-by-date-agreed-with-source**: A dependency's need-by date SHOULD be agreed with the dependency's source, to confirm that the date is achievable, resources included. (claim: dependency-statement-with-need-by-date)
 
 ### Keeping status current
 
 - **dependency-status-values**: A dependency's status SHOULD be taken from a short preset list of values, one of which marks the dependency as blocked. (claims: tracker-health-on-track-at-risk-off-track, raid-entry-owner-due-date-status, linear-blocked-by-flags, github-projects-define-blockers-and-fields)
-- **track-dependency-availability-and-status**: A team SHOULD keep tracking each dependency's status for the whole life of the dependency and review its dependencies at regular points, such as status meetings, steering reviews and sprint planning. (claims: raid-entry-owner-due-date-status, review-dependencies-regularly, document-dependency-type-source-timeline, kanban-guide-unblock-and-review)
+- **track-dependency-availability-and-status**: A team SHOULD keep tracking each dependency's status for the whole life of the dependency. (claims: raid-entry-owner-due-date-status, document-dependency-type-source-timeline, tracker-health-on-track-at-risk-off-track)
+- **review-dependencies-at-regular-points**: A team SHOULD review its dependencies at regular points, such as status meetings, steering reviews and sprint planning. (claims: review-dependencies-regularly, kanban-guide-unblock-and-review)
 - **stale-status-is-a-signal**: A dependency whose status update is overdue SHOULD be treated as a sign that its record is stale, and its status reconciled before the record is relied on again. (claims: linear-update-reminders-and-staleness, stale-log-loses-value)
-- **report-dependency-changes**: Dependencies SHOULD be included in the team's standard status reports, and a change to a dependency SHOULD be pushed to the people it affects. (claim: communicate-dependency-changes)
+- **include-dependencies-in-status-reports**: Dependencies SHOULD be included in the team's standard status reports. (claim: communicate-dependency-changes)
+- **report-dependency-changes**: A change to a dependency SHOULD be pushed to the people it affects. (claim: communicate-dependency-changes)
 
 ### Blocked and at-risk dependencies
 
 - **flag-at-risk-or-blocked-dependencies**: A blocked or off-track dependency SHOULD be flagged where everyone working on the affected work can see it, such as by a blocked-by link with a Blocked icon or flag on the board, a Jira Impediment flag, or a red mark on the blocked item. (claims: github-issue-dependencies-blocked-icon, linear-blocked-by-flags, jira-flag-impediment, jira-plans-off-track-dependencies, leopold-red-blocker-sticker-days-blocked)
 - **blocked-dependency-linked-to-affected-work**: A dependency record MUST keep this true: blocked or at-risk dependencies are linked to affected milestones or todos (claim: blocked-dependency-linked-to-affected-work-prior)
-- **record-blocker-reason-and-duration**: A blocked work item SHOULD record a brief reason why it is blocked and how many days it has stayed blocked. (claims: leopold-red-blocker-sticker-days-blocked, jira-flag-impediment)
-- **analyse-resolved-blockers**: A team MAY keep the records of resolved blockers and cluster them by internal and external causes, then by what they have in common, to find which kinds of blocker recur. (claims: leopold-red-blocker-sticker-days-blocked, cluster-blockers-internal-external)
-- **at-risk-dependency-logged-as-risk**: A dependency assessed as a risk to the project, or threatened such as by lateness, SHOULD be acknowledged as a source of risk with a management plan, such as mitigation or contingency, and reviewed for its effect on milestones. (claims: at-risk-dependency-entered-as-risk, apm-common-difficulties)
+- **record-blocker-reason-and-duration**: A blocked dependency's record SHOULD give a brief reason why it is blocked. (claims: leopold-red-blocker-sticker-days-blocked, jira-flag-impediment)
+- **count-days-dependency-blocked**: A blocked dependency's record MAY count the days it has stayed blocked. (claim: leopold-red-blocker-sticker-days-blocked)
+- **keep-resolved-dependency-blockers**: The records of a dependency's resolved blockers SHOULD be kept, not thrown away. (claim: leopold-red-blocker-sticker-days-blocked)
+- **analyse-resolved-blockers**: A team MAY cluster its resolved dependency blockers by internal and external causes, then by what they have in common, to find which kinds of blocker recur. (claim: cluster-blockers-internal-external)
+- **at-risk-dependency-logged-as-risk**: A dependency assessed as a risk to the project, or threatened such as by lateness, SHOULD be acknowledged as a source of risk with a management plan, such as mitigation or contingency. (claims: at-risk-dependency-entered-as-risk, apm-common-difficulties)
+- **at-risk-dependency-reviewed-against-milestones**: A dependency assessed as a risk to the project SHOULD be reviewed for its effect on the project's milestones. (claim: at-risk-dependency-entered-as-risk)
 
 ### Escalating and reducing dependencies
 
 - **escalate-blocked-dependency-before-milestone**: A blocked dependency the team cannot resolve locally SHOULD be escalated through a named forum or by exception, such as SAFe's ART Sync, the PRINCE2 project board once tolerance is exceeded, or the Scrum Master for an impediment. (claims: safe-art-sync-escalation-point, prince2-manage-by-exception, scrum-guide-impediments)
 - **coordinate-directly-with-the-other-team**: A team MAY coordinate a dependency directly with the team it depends on, by talking to that team or by sending a scout to monitor the interface and report back. (claim: less-just-talk-and-scouts)
-- **reduce-dependencies-before-tracking**: Teams SHOULD be organised to minimise the dependencies between them, so that each can complete its work without waiting on another. (claims: rescope-to-remove-dependencies, less-minimise-dependencies-feature-teams)
+- **reduce-dependencies-before-tracking**: Teams SHOULD be organised to minimise the dependencies between them, so that each can complete its work without waiting on another. (claims: rescope-to-remove-dependencies, less-minimise-dependencies-feature-teams, each-dependency-halves-on-time-chance)
 - **rescope-to-remove-difficult-dependency**: In extreme circumstances, a project MAY be re-scoped to remove a difficult dependency, for example by bringing its delivery within the project's control. (claim: rescope-to-remove-dependencies)
 
 ## Recording and tracking a dependency
@@ -99,7 +109,7 @@
 4. Give it an owner, and send it to the owner of the other project or team so it is confirmed there and appears in their dependency log too.
 5. Set its status from the team's preset list. A tracker's single-select field holds such a list, and a date field holds the need-by date. GitHub recommends automating updates so the project stays current.
 6. Review the dependencies at the meetings the team already holds: status meetings, steering reviews, sprint planning, the Daily Scrum. The sources name no cadence.
-7. When one is blocked, flag it where the team will see it, note why, and count the days it stays blocked. When it cannot be cleared locally, take it to the forum the method names, or straight to the other team.
+7. When one is blocked, flag it where the team will see it, note why, and count the days it stays blocked. When it cannot be cleared locally, take it to the forum the method names, or straight to the other team. Keep the note once the block is cleared.
 
 How the tools compare:
 
@@ -121,36 +131,43 @@
 
 | Category | Description | Internal or external | Owner | Confirmed by | Need-by | Status |
 |---|---|---|---|---|---|---|
-| Dependency | Identity team delivers the token-refresh endpoint | Internal | Priya (mobile) | Sam (identity), in the identity team's log | 2026-12-15 | Blocked: waiting on security review, 4 days |
+| Dependency | Identity team delivers the token-refresh endpoint | External | Priya (mobile) | Sam (identity), in the identity team's log | 2026-12-15 | Blocked: waiting on security review, 4 days |
 
 The blocked item it holds up, in a tracker: the offline sign-in issue is "blocked by" the token-refresh issue, carries the board's Blocked icon, and is linked to the release milestone it affects.
 
 ## What a reviewer looks for
 
-Checks that the plan's dependencies were found in planning with the teams that hold them, including those other projects raised, and that each is marked internal or external. Checks that every dependency has a type and a status, an agreed owner confirmed by the other side, and a need-by date agreed with its source. Checks that statuses come from a short preset list that can mark a dependency blocked, that the dependencies are reviewed at regular points and reported in the normal status reports, and that no status is stale. Above all, checks that every blocked or at-risk dependency is flagged where the team can see it and linked to the milestones or todos it affects, that blocked items record why and for how long, that a dependency threatening the project is handled as a risk with a plan, and that a blocked dependency the team cannot clear has been escalated through a named forum or by exception.
+Checks that the plan's dependencies were found in planning with the teams that hold them, including those other projects raised, and that each is marked internal or external. Checks that every dependency has a type and a status, an agreed owner, a confirmation from the other side, and a need-by date agreed with its source. Checks that statuses come from a short preset list that can mark a dependency blocked, that each status is tracked for the dependency's whole life and reviewed at regular points, that dependencies appear in the normal status reports and their changes reach the people affected, and that no status is stale. Above all, checks that every blocked or at-risk dependency is flagged where the team can see it and linked to the milestones or todos it affects, that a blocked dependency's record says why it is blocked, that resolved blockers are kept, that a dependency threatening the project is handled as a risk with a plan and reviewed against milestones, and that a blocked dependency the team cannot clear has been escalated through a named forum or by exception.
 
 ## A complete review must establish
 
 - Each MUST rule is kept, with no exception: `dependency-has-type-and-status`: every dependency has a type and a status; `blocked-dependency-linked-to-affected-work`: every blocked or at-risk dependency is linked to the milestones or todos it affects.
-- Each SHOULD rule is kept or its departure is stated: `identify-dependencies-during-planning`, `map-internal-and-external-dependencies`, `dependency-owner-agreed-on-both-sides`, `dependency-has-need-by-date`, `dependency-status-values`, `track-dependency-availability-and-status`, `stale-status-is-a-signal`, `report-dependency-changes`, `flag-at-risk-or-blocked-dependencies`, `record-blocker-reason-and-duration`, `at-risk-dependency-logged-as-risk`, `escalate-blocked-dependency-before-milestone`, `reduce-dependencies-before-tracking`.
-- Each MAY rule is noted where it was used: `analyse-resolved-blockers`, `coordinate-directly-with-the-other-team`, `rescope-to-remove-difficult-dependency`.
+- Each SHOULD rule is kept or its departure is stated: `identify-dependencies-during-planning`, `map-internal-and-external-dependencies`, `dependency-owner-agreed-on-both-sides`, `dependency-confirmed-by-other-side`, `dependency-has-need-by-date`, `need-by-date-agreed-with-source`, `dependency-status-values`, `track-dependency-availability-and-status`, `review-dependencies-at-regular-points`, `stale-status-is-a-signal`, `include-dependencies-in-status-reports`, `report-dependency-changes`, `flag-at-risk-or-blocked-dependencies`, `record-blocker-reason-and-duration`, `keep-resolved-dependency-blockers`, `at-risk-dependency-logged-as-risk`, `at-risk-dependency-reviewed-against-milestones`, `escalate-blocked-dependency-before-milestone`, `reduce-dependencies-before-tracking`.
+- Each MAY rule is noted where it was used: `count-days-dependency-blocked`, `analyse-resolved-blockers`, `coordinate-directly-with-the-other-team`, `rescope-to-remove-difficult-dependency`.
 
 ## A build must establish
 
 - `identify-dependencies-during-planning`: the dependencies were identified in planning with the other teams, stakeholders and partners, inbound ones included.
 - `map-internal-and-external-dependencies`: each dependency is recorded and marked internal or external.
 - `dependency-has-type-and-status`: every dependency has a type and a status.
-- `dependency-owner-agreed-on-both-sides`: each dependency has an agreed owner and is confirmed in the other side's dependency log.
-- `dependency-has-need-by-date`: each dependency carries a need-by date agreed with its source.
+- `dependency-owner-agreed-on-both-sides`: each dependency has an agreed owner of its management actions.
+- `dependency-confirmed-by-other-side`: each dependency was communicated to the other side's owner, who confirmed it and tracks it in its own log.
+- `dependency-has-need-by-date`: each dependency carries a need-by date.
+- `need-by-date-agreed-with-source`: each need-by date was agreed with the dependency's source.
 - `dependency-status-values`: each status comes from a short preset list that includes a blocked value.
-- `track-dependency-availability-and-status`: each dependency's status is tracked for its whole life and reviewed at regular points.
+- `track-dependency-availability-and-status`: each dependency's status is tracked for its whole life.
+- `review-dependencies-at-regular-points`: the dependencies are reviewed at regular points.
 - `stale-status-is-a-signal`: no dependency is relied on while its status update is overdue.
-- `report-dependency-changes`: dependencies appear in the standard status reports, and changes reach the people they affect.
+- `include-dependencies-in-status-reports`: dependencies appear in the standard status reports.
+- `report-dependency-changes`: each change to a dependency reached the people it affects.
 - `flag-at-risk-or-blocked-dependencies`: each blocked or off-track dependency is visibly flagged.
 - `blocked-dependency-linked-to-affected-work`: each blocked or at-risk dependency is linked to the milestones or todos it affects.
-- `record-blocker-reason-and-duration`: each blocked item records why it is blocked and for how many days.
-- `analyse-resolved-blockers`: where used, resolved blockers are kept and clustered by cause.
-- `at-risk-dependency-logged-as-risk`: each dependency threatening the project is handled as a risk with a management plan and reviewed against milestones.
+- `record-blocker-reason-and-duration`: each blocked dependency's record says why it is blocked.
+- `count-days-dependency-blocked`: where used, each blocked dependency's record counts its days blocked.
+- `keep-resolved-dependency-blockers`: the records of resolved dependency blockers are kept.
+- `analyse-resolved-blockers`: where used, resolved blockers are clustered by cause.
+- `at-risk-dependency-logged-as-risk`: each dependency threatening the project is handled as a risk with a management plan.
+- `at-risk-dependency-reviewed-against-milestones`: each dependency threatening the project is reviewed for its effect on milestones.
 - `escalate-blocked-dependency-before-milestone`: each blocked dependency the team could not resolve was escalated through a named forum or by exception.
 - `coordinate-directly-with-the-other-team`: where used, the team coordinated directly with the team it depends on.
 - `reduce-dependencies-before-tracking`: the team structure was considered for dependencies it could remove.
@@ -160,15 +177,15 @@
 
 This section is informative.
 
-The usual failures with dependencies are that a dependency is never identified, that nobody agrees who owns it, and that what is needed, and by when, cannot be pinned down early. The rules answer each in turn: find dependencies in planning with the people who know of them, agree an owner on both sides, and state a need-by date agreed with the source. A record nobody updates goes stale, which is why the rules ask for regular review, a preset status list and a stale status treated as a warning. The trackers all link a blocked item to its blocker and flag it visibly, which is the basis of the flagging rule.
+The usual failures with dependencies are that a dependency is never identified, that nobody agrees who owns it, and that what is needed, and by when, cannot be pinned down early. The rules answer each in turn: find dependencies in planning with the people who know of them, agree an owner and have the other side confirm the dependency, and state a need-by date agreed with the source. A blocked dependency's reason rests on the practitioners and on Jira's flag comment, so it is a recommendation; the count of days blocked rests on the practitioners alone, so it is an option, as recording a blocked task's dates is in task breakdown. A record nobody updates goes stale, which is why the rules ask for regular review, a preset status list and a stale status treated as a warning. The trackers all link a blocked item to its blocker and flag it visibly, which is the basis of the flagging rule.
 
 Most rules are recommendations because the sources are: APM, the University of Essex and Atlassian write "should", "needs" and "consider", and none makes any field mandatory for every dependency. The two MUST rules are the prior text kept for the owner: the research supports a type and status on each dependency, and a link from a blocked dependency to the work it affects, only at SHOULD, and whether they stay must-hold checks is the owner's decision.
 
 Several other questions are the owner's and are left open here: which status vocabulary a dependency uses (the trackers' On track, At risk and Off track for projects, plus Blocked, or another set); what a dependency's type means (internal or external, inward or outward, mandatory or discretionary, or what it is on); when a blocked or at-risk dependency is escalated (at a review cadence, once its need-by date is forecast to be missed, or at a named forum); and whether a dependency at risk is also entered in the risk register or stays only in the dependency record.
 
-The advice to remove dependencies rather than manage them comes from LeSS, Team Topologies and DORA, which organise teams so they do not wait on each other; LeSS reads a felt need for a Scrum of Scrums as a sign of unnecessary dependency. APM limits re-scoping a project to remove a dependency to extreme circumstances. A practitioner teaching model holds that each team dependency roughly halves the chance of on-time completion; it names no study, and gives only the direction of the effect, never a figure.
-
-The PMBOK Guide, ISO 21502 and ISO 31000 could not be read, and PRINCE2 was reached only through secondary sources, so no rule rests on them. The Scrum Guide has no dependency record; it treats a blocker as an impediment. The Kanban Guide requires items in the workflow to be actively managed, unblocking blocked work included.
+The advice to remove dependencies rather than manage them comes from LeSS, Team Topologies and DORA, which organise teams so they do not wait on each other; LeSS reads a felt need for a Scrum of Scrums as a sign of unnecessary dependency. APM limits re-scoping a project to remove a dependency to extreme circumstances. A practitioner teaching model, reported second-hand and naming no study, holds that each added team dependency lowers the chance of on-time completion; the research uses it for that direction only.
+
+The PMBOK Guide, ISO 21502 and ISO 31000 could not be read, so no rule rests on them. PRINCE2 was reached only through secondary sources, APM's quotation of it and prince2.wiki, which the internal-and-external and escalation rules use. The Scrum Guide has no dependency record; it treats a blocker as an impediment. The Kanban Guide requires items in the workflow to be actively managed, unblocking blocked work included.
 
 ## References
 
