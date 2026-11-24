# Integrate: dependency-tracking

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'dependency-has-type-and-status' cites 'dependency-has-type-and-status-prior', which the research rules unsupported
- rule 'blocked-dependency-linked-to-affected-work' cites 'blocked-dependency-linked-to-affected-work-prior', which the research rules unsupported

Open questions from the owner list:

- Whether the two Verify clauses (every dependency has a type and status; blocked or at-risk dependencies are linked to affected milestones or todos) stay as must-hold checks as a house convention, or are restated at SHOULD, the strength the sources support.
- Which status vocabulary the cookbook adopts for a dependency: the trackers' project-health set (On track, At risk, Off track) plus Blocked and Done, or another set; the sources offer several and none is a standard.
- What 'type' means for a dependency in the cookbook: internal versus external (PRINCE2), internal / intra / external (MSP, Essex), inward versus outward (APM), the PMBOK's mandatory / discretionary, or what the dependency is on (team, vendor, task, decision); the sources use all of these.
- When a blocked or at-risk dependency is escalated: at a fixed review cadence, as soon as its need-by date is forecast to be missed (PRINCE2's manage-by-exception), or at a named forum such as SAFe's ART Sync; the sources give no single trigger.
- Whether a dependency at risk is also entered as a risk (Essex, APM), which would couple this topic to risk-tracking, or stays only in the dependency record.

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped 1.0.0 → 1.0.1; /add-artifact approved it (no lint failures; warnings: the Blocked and at-risk subsection holds 8 rules, and the names `record-blocker-reason-and-duration` and `escalate-blocked-dependency-before-milestone` say more than their rules). The phase 3 code review fixes renamed those two new rules to `record-blocker-reason` and `escalate-unresolved-blocked-dependency`; only prior rule names are fixed.

integrated: 2026-11-24
