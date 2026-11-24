# Integrate: issue-tracking

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'issue-has-severity-and-status' cites 'issue-has-severity-and-status-prior', which the research rules contradicted
- rule 'link-issues-to-findings' cites 'link-issues-to-findings-prior', which the research rules unsupported

Open questions from the owner list:

- Which severity scale the cookbook adopts: Mozilla's four levels (S1 Catastrophic to S4 Small/Trivial) or Atlassian's three (Critical, Major, Minor), or another.
- Whether tasks and enhancements carry a severity, or only defects (Mozilla allows N/A for tasks and enhancements).
- The escalation time limit for an unresolved critical issue, and who it escalates to (Mozilla assigns S1 within 2 business days and notifies Release Management; Linear's example is a 24 hour SLA for Urgent).
- Whether the reporter (or a named verifier) must confirm a fix before the issue is closed, or the fixer may close it.
- Whether the rule to link issues to specialist findings stays, since no source covers specialist findings; the general linking convention is project-record-linking's.
- Whether priority stays optional beside severity (Mozilla makes it optional) or is required.

- from the phase 3 code review (claude-code-review/f2): `issue-has-severity-and-status` (MUST) requires a severity on every issue, while `defect-has-severity-every-issue-has-status`, `issue-covers-more-than-defects` and the review bar put severity on defects only, so an enhancement, a concern or an issue awaiting its assessor fails the MUST. The review suggests restating the MUST as status on every issue and severity on defects, or dropping it in favour of the SHOULD.

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped 1.0.0 → 1.0.1; /add-artifact approved it (no lint failures; it notes `issue-has-severity-and-status` overlaps `defect-has-severity-every-issue-has-status`, and both owner-listed rules keep their prior wording until the owner decides).

integrated: 2026-11-24
