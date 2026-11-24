# dependency-tracking: research

Researched 2026-11-24 against base commit `f0dd450e1188364e9e221d912d49657944ae46ad`. The scope is the delivery dependencies a team waits on: other teams, vendors, tasks and decisions, both internal and external. Software dependencies are out of scope. Claim records are in `research.json`.

Apple, Android and Windows have no bearing on this topic. The platforms that matter are the method and standards owners and the trackers.

## Best practices

- **Classify each dependency as internal or external.** An internal dependency is under the team's control. An external one is not, such as a product from another project or a decision from above. Some guidance adds a middle class for dependencies between projects inside one programme. (`internal-and-external-dependency-classes`)
- **Write each dependency as a statement.** The form is "We are dependent on X to deliver Y on date Z in order for us to deliver AA". Agree the need-by date with the providing side. (`dependency-statement-with-need-by-date`)
- **Document each dependency's type, source, specification and timeline.** Get a signed-off agreement with the provider, then monitor the dependency for its whole life. The source gives these fields as examples, not a required set. (`document-dependency-type-source-timeline`)
- **Agree an owner, and have the other side confirm the dependency.** The providing project should record it in its own dependency log. (`owner-agreed-and-confirmed-by-other-side`)
- **Give each RAID-log entry an owner, a due date and a status.** "Blocked" appears as one of a dependency's statuses. (`raid-entry-owner-due-date-status`)
- **Review dependencies at regular points.** Status meetings, steering reviews and sprint planning are suitable. No source names a cadence. (`review-dependencies-regularly`)
- **Enter a dependency that threatens the project in the risk register too.** Review it for its effect on programme milestones. (`at-risk-dependency-entered-as-risk`)
- **Identify dependencies during planning, together with the other teams, stakeholders and partners.** They know about hidden dependencies. Capture inbound dependencies that other projects raise. (`identify-dependencies-in-planning-with-others`)
- **Report dependencies through the normal channels.** Include them in the standard status reports, and push a notice to affected people when one changes. (`communicate-dependency-changes`)

**Strength.** The guidance is consistently SHOULD-level ("should", "needs", "consider"). None of these sources makes any field mandatory for every dependency.

## Known solutions

- **GitHub Issues** links issues as "blocked by" and "blocking", and shows a Blocked icon on boards and the Issues page. (`github-issue-dependencies-blocked-icon`)
- **GitHub Projects** guidance says to:
  - define the blocker links;
  - track status in a single-select field with preset values;
  - track target dates in a date field;
  - automate updates so the project stays current. (`github-projects-define-blockers-and-fields`)
- **Linear** links issues as blocked-by and blocking. It flags blockers orange and blocked work red, and moves the link to "Related" once the blocker is resolved. (`linear-blocked-by-flags`)
- **Linear also handles stale status.** It reminds a project's owner when an update is due, and greys the health icon when updates are overdue. (`linear-update-reminders-and-staleness`)
- **Health status.** Linear and GitHub both give a project a health value from a short preset list: On track, At risk, Off track. Both apply it to projects, not to individual dependencies. Using the same vocabulary for a dependency record is an inference from these sources. (`tracker-health-on-track-at-risk-off-track`)
- **Jira** has a single "Flagged" field with the one value "Impediment". Everyone in the space can see it, and a comment can explain the flag. (`jira-flag-impediment`)
- **Jira Plans** treats work-item links as "Blocks" dependencies. Its dependencies view and program board draw an off-track dependency in red, and can show only off-track ones. (`jira-plans-off-track-dependencies`)
- **A RAID log** keeps risks, assumptions, issues and dependencies in one list. Its dependency entries cover waiting on another team, an approval or a vendor. (`raid-log-tracks-dependencies-with-risks`)

**How they compare:**
- **Linking and flagging.** The trackers link one work item to another and flag blocked items automatically. Only Jira Plans calculates off-track dependencies from the schedule.
- **Status.** None of the trackers gives a dependency its own owner, need-by date or status. Those come from the project or item fields.
- **RAID log.** It records owner, due date and status for each dependency by hand, but links nothing.
- **SAFe board.** SAFe's ART planning board records dependencies against feature delivery dates; see Platform guidelines.

## Platform guidelines

- **SAFe** sets dependency work in three places:
  - PI Planning identifies cross-team dependencies.
  - Its outputs include an ART planning board showing feature delivery dates and dependencies.
  - PI objectives expose the dependencies that need coordination. (`safe-pi-planning-identifies-dependencies`)
- **SAFe escalation** goes to the ART Sync, the primary point for cross-team impediments that teams cannot resolve locally. There, business owners check that dependencies are being actively managed. (`safe-art-sync-escalation-point`)
- **LeSS** coordinates directly. Teams "just talk" to the other team, send scouts to an interface they depend on, or have a leading team track the others. (`less-just-talk-and-scouts`)
- **LeSS also prefers removing dependencies to managing them.** Feature teams minimise dependencies between teams, and a felt need for Scrum of Scrums signals unnecessary dependency. (`less-minimise-dependencies-feature-teams`)
- **The Scrum Guide** has no dependency record. A blocker is an impediment: the Daily Scrum identifies it, and the Scrum Master causes its removal. (`scrum-guide-impediments`)
- **The Kanban Guide** requires active management of items in the workflow, and lists unblocking blocked work as one form of it. Regular review of active items is described as common practice. (`kanban-guide-unblock-and-review`)
- **PRINCE2** escalates by exception: the project manager escalates to the board when a situation exceeds tolerance. This source is a secondary summary. Applying the rule to dependency dates is an inference. (`prince2-manage-by-exception`)
- **PRINCE2 and MSP** classify dependencies as internal, external, and in MSP's case beyond the programme environment. These definitions are reached through APM's guidance. (`internal-and-external-dependency-classes`)
- **Not reachable:**
  - PMBOK Guide (PMI), ISO 21502 and ISO 31000 could not be read. No finding rests on them; see limitations.
  - GitHub, Linear and Jira are covered under Known solutions, from their own documentation.

## The expert's view

- **Blockers.** Mark a blocked item with a red note that gives the reason. Count the days it stays blocked at each stand-up. Keep the notes after the blocker is resolved. (`leopold-red-blocker-sticker-days-blocked`)
- **Find patterns in blockers.** Cluster recorded blockers by internal and external cause, then by what they have in common, to find which kinds recur. (`cluster-blockers-internal-external`)
- **What usually goes wrong:**
  - the dependency is never identified;
  - no owner is agreed;
  - what is needed, and by when, cannot be pinned down early.

  The remedy is to keep such a dependency under constant review as a risk, with a mitigation or contingency plan. (`apm-common-difficulties`)
- **Prefer removing dependencies to tracking them.** Re-scope or trade solutions so the dependency comes inside the team's control, and organise teams so they do not wait on each other. APM, Team Topologies and DORA say this independently, and LeSS agrees. (`rescope-to-remove-dependencies`)
- **A log nobody updates goes stale,** and outdated statuses must be reconciled before it is useful again. (`stale-log-loses-value`)
- **Each dependency roughly halves the chance of on-time completion.** This figure is a teaching model from a talk, reported second-hand. It names no study, sample or measure, so it fails the statistical bar. Use it only for the direction of the effect, never as a number. (`each-dependency-halves-on-time-chance`)

### Verdicts on the brief's rules

| Rule | Verdict | Claims |
|---|---|---|
| `map-internal-and-external-dependencies` | Supported, as worker focus at SHOULD strength | `internal-and-external-dependency-classes`, `raid-log-tracks-dependencies-with-risks`, `cluster-blockers-internal-external`, `identify-dependencies-in-planning-with-others` |
| `track-dependency-availability-and-status` | Supported | `raid-entry-owner-due-date-status`, `review-dependencies-regularly`, `document-dependency-type-source-timeline`, `kanban-guide-unblock-and-review`, `tracker-health-on-track-at-risk-off-track` |
| `flag-at-risk-or-blocked-dependencies` | Supported | `github-issue-dependencies-blocked-icon`, `linear-blocked-by-flags`, `jira-flag-impediment`, `jira-plans-off-track-dependencies`, `leopold-red-blocker-sticker-days-blocked` |
| `dependency-has-type-and-status` | Unsupported | `dependency-has-type-and-status-prior`, `document-dependency-type-source-timeline`, `raid-entry-owner-due-date-status` |
| `blocked-dependency-linked-to-affected-work` | Unsupported | `blocked-dependency-linked-to-affected-work-prior`, `github-projects-define-blockers-and-fields`, `github-issue-dependencies-blocked-icon`, `jira-plans-off-track-dependencies`, `at-risk-dependency-entered-as-risk` |

**Why the two Verify rules are unsupported.**
- `dependency-has-type-and-status` is a must-hold check. The sources support it only at SHOULD: APM documents type "e.g." among other fields, and Atlassian's RAID guidance gives a status to each entry.
- `blocked-dependency-linked-to-affected-work` is also a must-hold check. The sources support it only at SHOULD: GitHub recommends defining blocked-by links, Jira draws them, and APM and Essex review dependencies against milestones. None requires the link for every blocked dependency.

### New practices the rules do not cover

Each new practice below is supported at SHOULD unless marked otherwise.

- **`dependency-owner-agreed-on-both-sides`**: an owner is agreed, and the providing side confirms the dependency. (`owner-agreed-and-confirmed-by-other-side`, `raid-entry-owner-due-date-status`, `apm-common-difficulties`, `document-dependency-type-source-timeline`)
- **`dependency-has-need-by-date`**: each dependency carries a need-by date agreed with the provider. (`dependency-statement-with-need-by-date`, `raid-entry-owner-due-date-status`, `apm-common-difficulties`)
- **`dependency-status-values`** answers the brief's "Blocked dependency flagging" question. A dependency carries a status from a short preset list: On track, At risk and Off track (Linear, GitHub), plus Blocked (RAID example, GitHub, Linear). Jira's off-track state is calculated from the schedule, and a stale status is itself a signal. No standard fixes the set. (`tracker-health-on-track-at-risk-off-track`, `raid-entry-owner-due-date-status`, `linear-blocked-by-flags`, `jira-plans-off-track-dependencies`, `linear-update-reminders-and-staleness`, `stale-log-loses-value`)
- **`escalate-blocked-dependency-before-milestone`**: a blocked dependency the team cannot resolve is escalated through a named forum or by exception. The sources name the SAFe ART Sync, the PRINCE2 board, and the Scrum Master for impediments; LeSS goes directly to the other team. No source gives a single trigger time. (`safe-art-sync-escalation-point`, `prince2-manage-by-exception`, `scrum-guide-impediments`, `less-just-talk-and-scouts`, `communicate-dependency-changes`)
- **`at-risk-dependency-logged-as-risk`**: a dependency that threatens the project is entered in the risk register. (`at-risk-dependency-entered-as-risk`, `apm-common-difficulties`)
- **`reduce-dependencies-before-tracking`**: re-scope, or change team structure, to remove a dependency where possible. (`rescope-to-remove-dependencies`, `less-minimise-dependencies-feature-teams`, `each-dependency-halves-on-time-chance`)
- **`record-blocker-reason-and-duration`** (MAY to SHOULD; practitioner and tool sources only): a blocked item records why it is blocked and how long it has been blocked. (`leopold-red-blocker-sticker-days-blocked`, `jira-flag-impediment`, `cluster-blockers-internal-external`)
- **`identify-dependencies-during-planning`**: dependencies are found in planning, with the other teams. (`identify-dependencies-in-planning-with-others`, `safe-pi-planning-identifies-dependencies`)
