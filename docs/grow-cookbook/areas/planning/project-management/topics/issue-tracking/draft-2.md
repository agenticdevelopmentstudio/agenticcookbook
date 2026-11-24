---
id: f77eeffe-2699-4028-9195-4bfc23c75e91
title: "Issue Tracking"
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Track project issues to close: triage each, assess severity apart from priority, give each one owner, escalate critical ones, record how it was resolved."
platforms: []
tags:
  - issue-tracking
  - triage
  - severity
  - project-management
depends-on: []
related:
  - 2041fbd9-d210-485e-9a3a-b2d8295ed924
  - 86671e07-24b3-476c-88be-91ed8f83eb30
references:
  - https://www.atlassian.com/agile/software-development/bug-triage
  - https://raw.githubusercontent.com/kubernetes/community/master/contributors/guide/issue-triage.md
  - https://www.chromium.org/for-testers/bug-reporting-guidelines/triage-best-practices/
  - https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html
  - https://firefox-source-docs.mozilla.org/bug-mgmt/guides/severity.html
  - https://wiki.mozilla.org/BMO/UserGuide/BugFields
  - https://groups.google.com/g/mozilla.tools.bmo/c/uAZpsT_vd64
  - https://www.atlassian.com/blog/development/realigning-priority-categorization-public-bug-repository
  - https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/
  - https://confluence.atlassian.com/servicedeskcloud/configuring-statuses-resolutions-and-priorities-1097176115.html
  - https://support.atlassian.com/jira-software-cloud/docs/reference-issues-in-your-development-work/
  - https://www.atlassian.com/itsm/problem-management/process
  - https://linear.app/docs/triage
  - https://linear.app/docs/triage-manage-unplanned-work
  - https://linear.app/docs/issue-property
  - https://developers.google.com/issue-tracker/concepts/issues
  - https://developers.google.com/issue-tracker/references/glossary-of-fields
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/closing-an-issue
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues
  - https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
  - https://docs.github.com/en/rest/issues/issues
  - https://stacks.cdc.gov/view/cdc/78626/cdc_78626_DS1.pdf
  - https://www.peoplecert.org/news-and-announcements/prince2-7-issues
  - https://scrumguides.org/scrum-guide.html
  - https://kanbanguides.org/english/
  - https://www.joelonsoftware.com/2000/11/08/painless-bug-tracking/
  - https://api.openalex.org/works/doi:10.1109/tse.2019.2944608
approved-by: ""
approved-date: ""
triggers: []
---

# Issue Tracking

Keep every project issue in one tracker and triage each new one promptly: a named triager gives it one owner and assesses its severity by impact, apart from its priority. Track its status to a closed state, escalate critical issues and issues left unresolved too long by a documented path, and close each issue with a recorded resolution reason, a link to the fixing change and a confirmed fix.

This guideline covers project issues and defects from report to close, for any delivery team and any tracker. A team conforms to it when its tracker, its triage and its closes meet the rules below. Production incidents are covered by [adc.guideline.shipping.incident-response](cookbook:2041fbd9-d210-485e-9a3a-b2d8295ed924), security vulnerability triage by [adc.guideline.reviewing.security.vulnerability-prioritization](cookbook:86671e07-24b3-476c-88be-91ed8f83eb30), risks that have not happened by the `risk-tracking` topic, and the general convention for linking project records by the `project-record-linking` topic.

## Rules

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

## Triaging a new issue

1. Take the issue from the untriaged queue (a `needs-triage` label, an issue with no priority yet, or a triage inbox such as Linear's).
2. Decide what kind of issue it is and which area owns it. A production incident goes to the incident process, and a security vulnerability to vulnerability triage.
3. If it repeats an existing issue, close it as a duplicate with a link to the original and tell its reporter.
4. Assess its severity from its impact on the project's defined scale, whoever filed it and whether or not it is a regression. Set its priority in its own field.
5. Assign it to one owner. A critical issue gets an owner within the project's stated time, or is escalated by the documented path.
6. If the team will not do the work, close it as not planned and explain why.

## Closing an issue

1. Confirm the fix, by the reporter, a named verifier or a test, as the project has chosen.
2. Link the fixing change to the issue: a closing keyword in the pull request or commit, or the issue key in the commit message.
3. Set the resolution reason from the tracker's fixed set, and record how the issue was resolved.
4. Close the issue and leave it in the tracker. Tell its stakeholders how it was resolved, where the project does so.

## Examples

This part is informative. A severity scale, here Mozilla's, which levels by impact, breadth, data loss and workaround (Atlassian uses three levels, Critical, Major and Minor; the scale a project adopts is its own choice):

| Level | Meaning |
|-------|---------|
| S1 (Catastrophic) | Blocks development or testing, may affect more than 25% of users, causes data loss, and has no workaround |
| S2 (Serious) | Major functionality severely impaired, or high impact with no satisfactory workaround |
| S3 (Normal) | Blocks non-critical functionality, or a workaround exists |
| S4 (Small/Trivial) | Minor or cosmetic, with low or no impact on users |

A defect's record, with severity and priority in separate fields:

```text
ID:          PROJ-412
Title:       Export drops the last row of every report
Kind:        defect
Severity:    S2 (no satisfactory workaround)
Priority:    set by triage
Status:      In Progress
Owner:       one named person
Next step:   fix in review; target date 2026-12-05
Description: Steps to reproduce, what was expected, what was seen instead
```

A pull request description that links the fix and closes the issue on merge, on GitHub:

```text
Fixes #412
```

## What a reviewer looks for

- Issues kept outside the team's one tracker, or a tracker so heavy to file in that people go around it.
- An issue record missing its identifier, description, impact, owner, status or next step, or a defect report without steps to reproduce, the expected result and the actual one.
- A defect with no severity, or an issue with no status.
- One field standing for both severity and priority, or a severity scale with undefined levels, or levels judged by something other than impact, such as being a regression.
- Severity set by the reporter, or changed with no reason given where the project requires one.
- New issues that no named person or rotation triages, untriaged issues that look the same as triaged ones, or issues left untriaged past the stated time.
- An issue with no owner or more than one, or a critical issue left without an owner past the stated time and not escalated.
- No written escalation process, or an issue unresolved past the agreed time and not escalated.
- A closed issue with no resolution reason, no record of how it was resolved, no link to the fixing change, or no confirmation of the fix.
- A duplicate closed without a link to the original, not-planned work left open, or closed issues deleted.

## A complete review must establish

- The project keeps its issues in one tracker everyone uses, and every issue reviewed carries the minimum fields, a status and, for a defect, a severity.
- Severity and priority are separate fields, severity follows a defined scale judged by impact, and it was set by an assessor rather than the reporter.
- Every new issue reviewed was triaged within the stated time by a named triager or rotation, was marked as awaiting triage until then, and has exactly one owner.
- Every critical issue reviewed got immediate attention and a notice beyond the triage queue, and was owned within the stated time or escalated.
- The escalation process is written down, and every issue unresolved past the agreed time was escalated by it.
- Every closed issue reviewed records a resolution reason from the fixed set and how it was resolved, links its fixing change where there is one, and had its fix confirmed before it closed.
- Every duplicate reviewed links its original, not-planned work is closed with an explanation, and closed issues remain in the tracker.

## A build must establish

- `one-tracker-everyone-uses`: the project's issues are kept in one tracker that everyone uses, and filing in it is light.
- `issue-covers-more-than-defects`: where the tracker holds issues other than defects, they are matters that could affect the project, raised by any stakeholder.
- `issue-records-minimum-fields`: every issue record carries its identifier, description, impact, owner, status and next steps or target date, and every defect gives steps to reproduce, expected and actual results.
- `defect-has-severity-every-issue-has-status`: every issue carries a status, and every defect a severity.
- `issue-has-severity-and-status`: every issue has a severity and a status.
- `keep-priority-scale-small`: the tracker has few fields and few priority levels.
- `link-issues-to-findings`: an issue raised by a specialist finding links to that finding.
- `identify-assess-severity-and-triage`: every new issue is categorized, assessed for severity by impact, prioritized and decided on.
- `triage-has-a-named-owner`: a named person or rotation is responsible for triaging new issues.
- `triage-new-issues-promptly`: new issues are triaged within the stated time and marked as awaiting triage until then.
- `every-issue-has-one-owner`: every triaged issue has exactly one owner until it closes.
- `severity-kept-apart-from-priority`: severity and priority are separate fields.
- `define-issue-severity-levels`: the project's severity scale is defined, small, and leveled by impact alone.
- `severity-set-by-assessor-not-reporter`: severity is set by whoever assesses the issue, not its reporter.
- `severity-change-needs-rationale`: where the project requires it, every severity change carries a comment giving the reason.
- `track-resolution-status`: every issue's status moves through a defined workflow to a closed state, and its blockers are worked on.
- `flag-stale-issues`: where the project flags stale issues, an issue with no activity for the set time is flagged.
- `escalate-critical-issues`: every critical issue gets immediate attention and a notice beyond the triage queue.
- `critical-issue-owned-or-escalated`: every critical issue is owned within the stated time or escalated.
- `escalation-path-documented`: the escalation process is written down.
- `escalate-unresolved-after-time-limit`: every issue unresolved past the agreed time is escalated by the agreed procedure.
- `resolved-issue-references-resolution`: every resolved issue records how it was resolved.
- `record-resolution-reason`: every closed issue records a resolution reason from a fixed set.
- `link-fix-change-to-issue`: every fixing change is linked to its issue.
- `verify-resolution-before-close`: every fix is confirmed by the reporter, a named verifier or a test before its issue closes.
- `communicate-resolution-to-stakeholders`: where the project tells stakeholders, each resolution is communicated to them.
- `close-duplicates-linking-canonical`: every duplicate is closed with a link to the original issue and its reporter told.
- `close-unplanned-work-definitively`: work the team will not do is closed as not planned, with an explanation.
- `keep-closed-issues-as-history`: closed issues remain in the tracker.

## Rationale

This part is informative. Triage is the regular step that identifies, categorizes and prioritizes new issues and decides who works them; Atlassian, Kubernetes and Chromium describe it the same way, and Mozilla, Linear and Chromium all give it an explicit owner, often a rotation. Mozilla counts a defect as triaged only once it has a severity, so that no critical issue is missed, and lets tasks and enhancements carry a severity of N/A. Every tracker the research covered builds a status workflow into every issue, and the Scrum and Kanban guides make removing blockers part of the method.

Severity records impact and is an input to priority. Mozilla and Atlassian each split a single priority field in two because one field conflated impact with scheduling. The trackers differ: Bugzilla and Google Issue Tracker carry both fields, Jira ships only priority with descriptions that read as severity, GitHub ships neither by default (teams add them as labels or a project field), and Linear has a fixed five-level priority and no severity. Mozilla's four levels and Atlassian's three share the same criteria (data loss, breadth of impact and whether a workaround exists), which is why the rules ask for a defined scale but leave the scale to the project. A peer-reviewed study finds that people filing issues inflate their priority, and Mozilla says severity should not be set by people filing bugs.

Mozilla, Kubernetes, Chromium and Google all give the most severe issues immediate attention, and Mozilla and Linear raise a notice beyond the triage queue: Mozilla notifies Release Management and the component's triage owner of S1 and S2 bugs, and Linear sends the assignee an urgent notice. The CDC's issue-management guidance, which quotes the PMBOK Guide, asks for a documented escalation process and escalation of issues left unresolved too long; Linear ties deadlines to priority. The time limits differ by source (Mozilla's two business days for an S1 owner, Linear's example 24 hour SLA for Urgent), so the rules leave them to the project.

Jira, GitHub, Google Issue Tracker and FogBugz all record why an issue closed from a fixed set of reasons, and in Jira an issue with no resolution reads as Unresolved. GitHub and Jira link the fixing change to the issue. Spolsky's rule is that only the person who opened a bug closes it; Jira and Google use a verifier and Atlassian a test, so the rules name all three and leave the choice to the project. Kubernetes, Linear, GitHub and Google all close a duplicate against its original.

The evidence is practice consensus, not measurement: no source gives an effect size for any triage practice. Several rules rest on one source: the severity-change comment (Mozilla), the escalation process, keeping closed issues and communicating resolutions (the CDC newsletter, from 2012), and the defect report's three parts (Spolsky). PMBOK, ITIL 4 and ISO 21502 are paywalled, so PMBOK is known here through the CDC newsletter and ITIL's known error through Atlassian.

Two rules are kept in their earlier wording for the owner to decide. No source covers linking issues to specialist findings: trackers link an issue to related issues, pull requests, incidents and changes, which is the general linking convention of the `project-record-linking` topic. "Every issue has severity and status" is contradicted as worded: status holds for every issue, but severity holds for defects, and GitHub, Jira and Linear ship no severity field. Which severity scale to adopt, whether tasks and enhancements carry a severity, the escalation time limit and its target, who confirms a fix, and whether priority is required are open for the owner.

## References

This part is informative. Every reference below is informative.

- Atlassian, [Bug triage: A guide to efficient bug management](https://www.atlassian.com/agile/software-development/bug-triage), [Realigning priority categorization in our public bug repository](https://www.atlassian.com/blog/development/realigning-priority-categorization-public-bug-repository) and [Problem management process](https://www.atlassian.com/itsm/problem-management/process)
- Atlassian, [What are work item statuses, priorities, and resolutions?](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/), [Configuring statuses, resolutions, and priorities](https://confluence.atlassian.com/servicedeskcloud/configuring-statuses-resolutions-and-priorities-1097176115.html) and [Reference work items in your development spaces](https://support.atlassian.com/jira-software-cloud/docs/reference-issues-in-your-development-work/)
- Kubernetes, [Issue Triage Guidelines](https://raw.githubusercontent.com/kubernetes/community/master/contributors/guide/issue-triage.md)
- The Chromium Projects, [Triage Best Practices](https://www.chromium.org/for-testers/bug-reporting-guidelines/triage-best-practices/)
- Mozilla, [Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html), [Defect Severity](https://firefox-source-docs.mozilla.org/bug-mgmt/guides/severity.html), [BMO/UserGuide/BugFields](https://wiki.mozilla.org/BMO/UserGuide/BugFields) and Emma Humphries, [Changes to the Firefox Bug Triage Process](https://groups.google.com/g/mozilla.tools.bmo/c/uAZpsT_vd64)
- Linear, [Triage](https://linear.app/docs/triage), [How to manage unplanned work](https://linear.app/docs/triage-manage-unplanned-work) and [Issue properties](https://linear.app/docs/issue-property)
- Google, [Issues](https://developers.google.com/issue-tracker/concepts/issues) and [Glossary of Fields](https://developers.google.com/issue-tracker/references/glossary-of-fields)
- GitHub, [Closing an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/closing-an-issue), [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue), [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues), [Managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels), [Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects) and [REST API endpoints for issues](https://docs.github.com/en/rest/issues/issues)
- Daniel Vitek, U.S. CDC, [Issues Management (CDC Unified Process Project Management Newsletter)](https://stacks.cdc.gov/view/cdc/78626/cdc_78626_DS1.pdf)
- Brad Bigelow, PeopleCert, [PRINCE2 7 Issues: not every issue equals a change](https://www.peoplecert.org/news-and-announcements/prince2-7-issues)
- Ken Schwaber and Jeff Sutherland, [The Scrum Guide](https://scrumguides.org/scrum-guide.html)
- Kanban Guides, [The Kanban Guide](https://kanbanguides.org/english/)
- Joel Spolsky, [Painless Bug Tracking](https://www.joelonsoftware.com/2000/11/08/painless-bug-tracking/)
- Gavidia-Calderon, Sarro, Harman and Barr, [The Assessor's Dilemma: Improving Bug Repair via Empirical Game Theory](https://api.openalex.org/works/doi:10.1109/tse.2019.2944608) (abstract)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
