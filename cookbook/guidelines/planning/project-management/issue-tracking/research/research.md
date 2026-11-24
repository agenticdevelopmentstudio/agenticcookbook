# issue-tracking research

Research for `cookbook/guidelines/planning/project-management/issue-tracking`, made on 2026-11-24 against base commit f0dd450e. The claims, their quotes and citations are in `research.json`. Every rule in the brief is marked "no RFC keyword", so each finding below says what strength (MUST, SHOULD or MAY) the sources support.

Out of scope: production incidents belong to `cookbook/guidelines/shipping/incident-response`, and security vulnerability triage belongs to `cookbook/guidelines/reviewing/security/vulnerability-prioritization`. Both topics exist, so cite them rather than restate them. Risks belong to risk-tracking, and the convention for linking records belongs to project-record-linking.

## Best practices

- **identify-assess-severity-and-triage: supported at SHOULD.**
  - Triage is the regular step that identifies, categorizes and prioritizes each new issue, and decides whether, when and by whom it is worked (`triage-identifies-categorizes-prioritizes`).
  - Severity records impact and feeds priority (`severity-describes-impact`).
  - Mozilla counts a defect as triaged only once it has a severity (`triage-sets-severity-on-every-defect`).
  - Mozilla words this as "must" for its own process. No second publisher does, so the sources support SHOULD for the cookbook.
- **issue-has-severity-and-status: contradicted as worded.**
  - Mozilla lets tasks and enhancements carry a severity of N/A (`triage-sets-severity-on-every-defect`).
  - GitHub, Jira and Linear ship no severity field at all (`github-no-default-severity`, `jira-priority-conflates-severity`, `linear-priority-five-levels`).
  - Status does hold for every issue (`status-tracks-to-resolution`). The supported form is the new rule `defect-has-severity-every-issue-has-status`: every issue has a status (MUST, since every tracker builds it in), and every defect has a severity (SHOULD).
- **track-resolution-status: supported at SHOULD.**
  - Every tracker carries a status through a defined workflow to a closed state (`status-tracks-to-resolution`).
  - Scrum and Kanban both make actively removing blockers part of the method (`scrum-impediments-removed`, `kanban-active-management`).
- **escalate-critical-issues: supported at SHOULD.**
  - The most severe issues get immediate attention and an owner within days. Mozilla assigns S1 bugs within 2 business days, Kubernetes team leaders "drop what you're doing", and Chromium and Google treat P0 as immediate (`escalate-critical-full-attention`).
  - Critical issues are announced beyond the queue (`critical-notifies-beyond-assignee`).
- **critical-issue-owned-or-escalated: supported at SHOULD.** The evidence is the same as for escalate-critical-issues, plus one owner for every issue (`issue-has-one-owner`).
- **resolved-issue-references-resolution: supported at SHOULD.**
  - The resolution is recorded on the issue (`record-resolution`).
  - Trackers hold a resolution reason (`resolution-reason-from-fixed-set`, `jira-resolution-field-unresolved`) and a link to the fixing change (`link-fix-to-issue`).
- **link-issues-to-findings: unsupported.** No source has "specialist findings". Sources support only linking related issues, pull requests, incidents and changes, at MAY (`link-related-records`). That general convention belongs to project-record-linking.

New practices, which no listed rule covers:

- **Issue severity levels** (brief question):
  - `severity-kept-apart-from-priority`, SHOULD: one field for both "conflates severity with scheduling" (`severity-separate-from-priority`).
  - `define-issue-severity-levels`, SHOULD: a small scale defined by data loss, breadth of impact and whether a workaround exists. Examples are Mozilla's S1 to S4 and Atlassian's Critical, Major and Minor (`severity-levels-defined`).
  - `severity-change-needs-rationale`, MAY (`severity-change-needs-rationale`).
- **Issue escalation path** (brief question):
  - `escalation-path-documented`, SHOULD (`escalation-procedure-documented`).
  - `escalate-unresolved-after-time-limit`, SHOULD: the time limit differs by source, so the owner sets it (`escalate-unresolved-after-time`).
- **Issue resolution traceability** (brief question):
  - `record-resolution-reason`, SHOULD (`resolution-reason-from-fixed-set`).
  - `link-fix-change-to-issue`, SHOULD (`link-fix-to-issue`).
  - `verify-resolution-before-close`, SHOULD (`verify-resolution`).
  - `keep-closed-issues-as-history`, SHOULD (`keep-closed-as-history`).
  - `communicate-resolution-to-stakeholders`, MAY (`communicate-resolution`).
- **Triage:**
  - `triage-has-a-named-owner`, SHOULD, often as a rotation (`triage-has-named-owner`).
  - `triage-new-issues-promptly`, SHOULD, with untriaged issues visibly marked. Mozilla's bound is one week (`triage-within-time-bound`, `untriaged-is-visible`).
  - `every-issue-has-one-owner`, SHOULD (`issue-has-one-owner`).
- **Records:**
  - `issue-records-minimum-fields`, SHOULD (`issue-log-minimum-fields`).
  - `close-unplanned-work-definitively`, SHOULD (`close-not-planned-definitively`).
  - `flag-stale-issues`, MAY (`stale-issues-flagged`).

## Known solutions

- **Severity and priority fields** differ across trackers:
  - Bugzilla carries severity and priority as two fields (`mozilla-bugzilla-severity-priority-fields`).
  - Google Issue Tracker carries both, requires priority, and defines P0 to P4 (`google-issue-tracker-priority-and-severity`).
  - Jira ships only priority, and its default descriptions read as severity (`jira-priority-conflates-severity`).
  - GitHub ships no severity or priority. Teams add them as labels or as a project single-select field (`github-no-default-severity`).
  - Linear has a fixed five-value priority and deliberately no custom levels (`linear-priority-five-levels`).
- **Triage queues:**
  - Linear's Triage inbox can require priority before an issue leaves it (`linear-triage-inbox`).
  - Kubernetes uses a `needs-triage` label (`untriaged-is-visible`).
- **Resolution:**
  - Jira's resolution field, GitHub's `state_reason`, Google's Won't fix sub-statuses and FogBugz's resolve reasons all record why an issue closed (`resolution-reason-from-fixed-set`).
  - In Jira, a missing resolution reads as Unresolved (`jira-resolution-field-unresolved`).
  - ITIL's "known error" is a resolution in Jira Service Management (`itil-known-error`).
- **Linking the fix:**
  - GitHub closes an issue through closing keywords in a pull request or commit.
  - Jira links commits and pull requests that carry the issue key.
  - Jira Service Management links problems to the changes that fix them (`link-fix-to-issue`).
- **Duplicates:** Kubernetes, Linear, GitHub's `duplicate_issue_id` and Google's canonical-issue link all close the duplicate against the original (`close-duplicates-link-canonical`), SHOULD as the new rule `close-duplicates-linking-canonical`.
- **Related records:** GitHub and Jira Service Management link related issues, pull requests and incidents (`link-related-records`).

## Platform guidelines

Apple, Android and Windows have no bearing on this topic. The platforms here are the project-management bodies and the trackers.

- **PMBOK**, through a CDC newsletter that quotes it because PMBOK is paywalled: an issue is an unsettled or disputed matter, and every project keeps an issue log (`pmbok-issue-log`).
- **PRINCE2 7**: an issue is "anything that could affect the project", and any stakeholder may raise one. That makes issues broader than defects, the new rule `issue-covers-more-than-defects`, MAY (`prince2-issue-broad`).
- **Scrum Guide**: has no issue log. It gives the Scrum Master the job of removing impediments and the Daily Scrum the job of surfacing them (`scrum-impediments-removed`).
- **Kanban Guide**: work items "must be managed actively", which includes unblocking blocked work and keeping items from ageing (`kanban-active-management`).
- **ISO 21502 and ISO 31000** are paywalled, and their public pages hold no issue text. **ITIL 4** is known here only through Atlassian (`itil-known-error`). **SAFe and LeSS** were not researched.
- **GitHub, Jira, Linear, Bugzilla and Google Issue Tracker**: their own documentation is covered under Known solutions.

## The expert's view

- **Use one tracker that everyone uses, and keep filing cheap.** If filing an issue is too much work, people go around the tracker (`bug-database-everyone-uses`). This is the new rule `one-tracker-everyone-uses`, SHOULD.
- **Keep fields and priority levels few.** Extra fields and finer levels make issues harder to file and to rank (`avoid-extra-fields`, `spolsky-three-things`). This is the new rule `keep-priority-scale-small`, SHOULD.
- **A common mistake is priority inflation.** Reporters inflate the priority of their own issues, and a separate triage team does not cure it. The issue's assessor sets severity, not its reporter (`priority-inflation`). This is the new rule `severity-set-by-assessor-not-reporter`, SHOULD.
- **Another common mistake is treating "regression" as a severity.** Severity is judged by impact alone (`regression-not-severity`).
- **Expect important issues to be filed again**, and merge each duplicate into the canonical issue (`duplicates-refiled`).
- **One owner at a time, and the reporter or a verifier closes.** Each issue belongs to exactly one person until it closes (`issue-has-one-owner`). Spolsky's "golden rule" is that only the person who opened a bug closes it (`verify-resolution`). Whether to require this is an open question for the owner.
