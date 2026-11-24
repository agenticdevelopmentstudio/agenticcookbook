---
id: 2b7a1593-48e0-4bbe-8e14-0df7a863628d
title: Decision Records
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Recording significant decisions: context, rationale, options, decider, date, status and consequences, kept findable, superseded, never silently contradicted."
platforms: []
tags:
  - decision-records
  - adr
  - project-management
  - supersession
depends-on: []
related:
  - 6a653107-929d-418e-865d-636373a27b02
references:
  - https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
  - https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
  - https://docs.cloud.google.com/architecture/architecture-decision-records
  - https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework
  - https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html
  - https://raw.githubusercontent.com/adr/madr/main/template/adr-template.md
  - https://raw.githubusercontent.com/adr/madr/main/template/adr-template-minimal.md
  - https://adr.github.io/madr/
  - https://github.com/npryce/adr-tools
  - https://github.com/thomvaill/log4brains
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  - https://ozimmer.ch/practices/2023/04/03/ADRCreation.html
  - https://github.com/socadk/design-practice-repository/blob/master/artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md
  - https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record
  - https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
  - https://raw.githubusercontent.com/joelparkerhenderson/architecture-decision-record/main/README.md
  - https://peps.python.org/pep-0001/
  - https://www.rfc-editor.org/rfc/rfc7322.txt
  - https://github.com/rust-lang/rfcs/blob/master/0000-template.md
  - https://www.atlassian.com/software/confluence/templates/decision
  - https://confluence.atlassian.com/doc/decisions-blueprint-339739406.html
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
approved-by: ""
approved-date: ""
triggers: []
---

# Decision Records

Record each significant decision once, in a short record that states its context, the decision, why it was made, the options that lost, who decided, when, its status and all its consequences, and keep the record where everyone it affects can find it. A later decision that changes an earlier one never silently contradicts it: it is a new record rather than an edit, it marks the old one superseded, and the old record's status should link to its replacement.

This guideline covers how any delivery team writes, stores, links and supersedes a project or architecture decision record. It does not cover which technical option to choose: a guideline that requires one decision to be recorded, such as [adc.guideline.planning.data.datastore-selection](cookbook:6a653107-929d-418e-865d-636373a27b02), says what to record, and this one says how. Linking between project records in general belongs to project record linking; only the links between a decision and the decisions it supersedes are this guideline's. Following it means keeping every MUST rule below and keeping each SHOULD rule or stating why a record departs from it.

## Rules

- **record-decisions-with-full-context**: A decision record SHOULD state the context that forced the decision, the forces at play, alongside the decision itself and its consequences; these three are the minimum a record holds. (claim: record-context-of-decision)
- **capture-rationale-alternatives-and-decider**: A decision record SHOULD give the reason for the decision, not only the decision, since a record without its justification loses its value when circumstances change. (claim: record-rationale-justification)
- **decision-has-rationale-and-decider**: A decision record SHOULD name who made the decision, as MADR's decision-makers field, the PEP-Delegate header and DACI's Approver do, so the decision-makers are accountable for enforcing it. (claims: record-who-decided, zimmermann-identify-decision-makers)
- **alternatives-are-recorded**: A decision record SHOULD list the options that were considered and ruled out, with why each was not chosen. (claims: record-alternatives-considered, proposal-processes-record-alternatives)
- **no-dummy-alternatives**: A decision record SHOULD NOT list a made-up option that does not work in the given context, presented to make the preferred option shine and to give the impression that several alternatives were evaluated. (claim: zimmermann-dummy-alternative-and-sprint)
- **record-consequences-good-and-bad**: A decision record SHOULD list all the decision's consequences, the costs as well as the benefits, and SHOULD NOT hide them or justify the decision with pros only. (claims: record-consequences-good-and-bad, zimmermann-anti-patterns)
- **record-decision-date**: A decision record SHOULD carry the date the decision was made or last updated. (claim: record-decision-date)
- **record-status-lifecycle**: A decision record SHOULD carry a status, such as proposed while under discussion, accepted once the team accepts it, or superseded once it is replaced; MADR adds rejected and deprecated. (claim: status-lifecycle)
- **one-decision-per-short-record**: A decision record SHOULD hold one decision and be kept short, a couple of pages at most, rather than growing into multi-page architecture documentation. (claims: one-decision-short-record, zimmermann-mega-adr)
- **record-significant-decisions-only**: A team SHOULD write a record for each decision of significant impact, a choice that affects the system's structure or key quality attributes or is difficult to reverse, and not for every choice; each team agrees what counts as significant. (claim: record-significant-decisions)
- **record-rejected-proposals**: A proposal that is rejected SHOULD still be recorded, with the reason for the rejection, so the same question is not reopened. (claim: record-rejected-decisions)
- **record-confidence-level**: A decision record MAY state the confidence level of the decision and the changes in context that would trigger the team to re-evaluate it. (claim: record-confidence-level)
- **decisions-findable-and-linked**: A decision log SHOULD be stored openly, where everyone the decisions affect can find it, and in a store that keeps a history of what was changed, who by and when. (claims: store-openly-findable, store-with-the-code)
- **decision-links-to-its-work**: A decision record SHOULD be linked to the work it affects: the issues that carry it out and the code review that checks changes against it. (claims: link-decisions-to-work, github-issue-pr-linking)
- **acknowledge-contradicted-decisions**: A decision that changes or reverses an earlier recorded decision MUST acknowledge the change: it is written as a new record that names the earlier decision, and the earlier record is marked superseded, so no decision contradicts an earlier one unknowingly. (claims: supersede-and-link, records-prevent-relitigation, cloud-providers-agree-on-supersession)
- **supersede-never-edit-accepted-records**: An accepted decision record SHOULD NOT be edited to change its decision; a changed decision is proposed as a new record that, once accepted, supersedes the old one, whose status alone is updated to point to it. (claims: accepted-records-immutable, adr-tools-supersede-command, clarifications-may-amend)
- **supersession-links-both-ways**: When one record supersedes another, the superseded record's status SHOULD link to the record that replaces it. (claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must)
- **backfill-undocumented-decisions**: When a decision log is started for an existing system, decisions already made but never written down MAY be recorded retroactively, where the data on them is available. (claim: backfill-undocumented)

## Writing a decision record

This section is informative: it shows one way to keep the rules, not a required method.

1. Decide whether the choice is significant: it shapes the system's structure or key quality attributes, or it would be hard to reverse. Spotify's teams reach such decisions through RFCs or engineering meetings and write the record of the outcome.
2. Pick one template and keep to it. Nygard's has Title, Status, Context, Decision and Consequences. MADR adds Decision Drivers, Considered Options with pros and cons, and optional decision-makers, consulted and informed metadata. A Y-statement puts the context, the requirement, the chosen option, the rejected options and the accepted downside in one sentence.
3. Fill in the context, the decision, the rationale, the options that lost and why, the decision-makers, the date, the status and every consequence, good and bad. Add a confidence level and what would trigger a revisit where it helps.
4. Keep the record to one decision and a page or two.
5. Store it with the log, openly, and link it to the issues that carry it out. On GitHub a pull request links to its issues by a keyword in its description or a commit message, across repositories. Jira's link types are configurable and none of its defaults expresses supersession; Linear relates issues as related, blocking or blocked.
6. Share the record once it is reviewed, so the people it affects hear of it.
7. When a decision changes, write a new record. Mark the old one superseded, with a "Status: superseded" line directly under its heading and a link to the new record, and name the old record in the new one. adr-tools does both with `adr new -s <number>`; PEPs carry the same pair as the `Superseded-By` and `Replaces` headers.

Tools that keep a log: adr-tools creates numbered records in the repository; log4brains publishes repository records as a searchable static site with a timeline, uses MADR by default and needs no sequential file numbers; Confluence's Decisions blueprint indexes a space's decisions as a decision log.

## Examples

This section is informative; its records are illustrations, not templates the guideline requires.

A superseded record, marked under its heading:

```markdown
# 7. Keep session data in the database

Status: superseded by [12. Keep session data in a shared cache](0012-session-cache.md)
Date: 2026-03-02
```

The record that replaces it:

```markdown
# 12. Keep session data in a shared cache

Status: accepted
Date: 2026-11-10
Decision-makers: platform team lead
Supersedes: [7. Keep session data in the database](0007-session-database.md)

## Context
Session reads now dominate database load at peak traffic.

## Considered options
- Shared cache: chosen; adds an operated component.
- Database with read replicas: rejected; replication lag breaks read-after-write for sessions.

## Decision
Session data moves to a shared cache.

## Consequences
- Good: database load at peak falls.
- Bad: the team now runs and monitors a cache cluster.
```

A Y-statement of the same decision: "In the context of the web shop service, facing the need to keep user session data consistent and current across instances, we decided for a shared cache and against database replicas, to achieve read-after-write consistency, accepting that the team operates one more component."

## What a reviewer looks for

Checks that every significant decision has a record, and that each record states its context, the decision, its rationale and all its consequences, the costs included. Checks that a record names its decider, carries a date and a status, lists the options that lost with why, and lists no made-up option. Checks that each record holds one decision and stays short, that rejected proposals are recorded with their reason, and that the log is stored openly with history and linked to the work. Above all, checks that no decision contradicts an earlier one without a new record that names it, that no accepted record was edited to change its decision, and that each superseded record's status links to its replacement.

## A complete review must establish

- The MUST rule is kept, with no exception: `acknowledge-contradicted-decisions`: every decision that changes or reverses an earlier one is a new record that names it, and the earlier record is marked superseded.
- Each SHOULD rule is kept or its departure is stated: `record-decisions-with-full-context`, `capture-rationale-alternatives-and-decider`, `decision-has-rationale-and-decider`, `alternatives-are-recorded`, `no-dummy-alternatives`, `record-consequences-good-and-bad`, `record-decision-date`, `record-status-lifecycle`, `one-decision-per-short-record`, `record-significant-decisions-only`, `record-rejected-proposals`, `decisions-findable-and-linked`, `decision-links-to-its-work`, `supersede-never-edit-accepted-records`, `supersession-links-both-ways`.
- Each MAY rule is noted where it was used: `record-confidence-level`, `backfill-undocumented-decisions`.

## A build must establish

- `record-decisions-with-full-context`: each record states the context, the decision and its consequences.
- `capture-rationale-alternatives-and-decider`: each record gives the reason for its decision.
- `decision-has-rationale-and-decider`: each record names who made the decision.
- `alternatives-are-recorded`: each record lists the options ruled out, with why each lost.
- `no-dummy-alternatives`: no record lists a made-up option that does not work in its context.
- `record-consequences-good-and-bad`: each record lists its costs as well as its benefits.
- `record-decision-date`: each record carries the date it was made or last updated.
- `record-status-lifecycle`: each record carries a status.
- `one-decision-per-short-record`: each record holds one decision and is a couple of pages at most.
- `record-significant-decisions-only`: a record exists for each significant decision, and the team's meaning of significant is agreed.
- `record-rejected-proposals`: each rejected proposal is recorded with its reason.
- `record-confidence-level`: where used, the record states its confidence and what would trigger a revisit.
- `decisions-findable-and-linked`: the log is stored openly, in a store that keeps its history.
- `decision-links-to-its-work`: each record links to the issues and code review that carry it out.
- `acknowledge-contradicted-decisions`: no decision changes an earlier one without a new record naming it and the earlier record marked superseded.
- `supersede-never-edit-accepted-records`: no accepted record was edited to change its decision.
- `supersession-links-both-ways`: each superseded record's status links to its replacement.
- `backfill-undocumented-decisions`: where used, past decisions recorded retroactively are ones whose data was available.

## Rationale

This section is informative.

Without a recorded motivation, a later team either accepts a decision blindly or reverses it blindly, and a decision that is never recorded is likely to be forgotten, debated again or contradicted without anyone knowing. Writing the record also clarifies a group's thinking, and brevity matters most. That is why the minimum is context, decision and consequences, why the rationale and the losing options go in, and why the one firm rule is that a changed decision acknowledges the one it changes. The acknowledgement is the strongest consensus in the research: AWS, Microsoft, Google Cloud, Nygard, Fowler, the GDS Way and PEP 1 all keep the earlier decision visible.

Most rules are recommendations because the sources disagree on the template. Nygard's original record and the GOV.UK template have no alternatives section, and MADR marks its decision-makers field optional, so the research supports naming the decider and recording alternatives as recommendations. Immutability is a recommendation too: the GDS Way allows a clarification to update a record during implementation, and Henderson's teams find amending records works better for them, while Microsoft, AWS and Fowler keep accepted records unchanged.

Several questions are the owner's and are left open here: whether naming the decider is required; whether alternatives belong on every record or only where two or more options were real; whether a clarification may edit an accepted record in place; whether records live in the code repository, a wiki readable by non-developers, or both; which template to standardise on; whether deprecated is a status distinct from superseded, and whether a superseded record may ever be deleted; and whether records are numbered sequentially.

The research found no study that measures whether recording alternatives or deciders improves outcomes; the support is consensus guidance. One mining study of GitHub repositories found adoption of decision records low but growing, which is context, not support. The Scrum and Kanban Guides define no decision record, and the primary texts of PMBOK, ISO 21502, PRINCE2, SAFe and LeSS were not reachable. An imperfect log that is accurate and current is still better than none.

## References

This section is informative; every reference below is informative, and none is normative.

- Michael Nygard, *Documenting Architecture Decisions* (Cognitect, 2011): https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- AWS Prescriptive Guidance, *ADR process*: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
- Microsoft Azure Well-Architected, *Architecture decision record*: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- Google Cloud, *Architecture decision records overview*: https://docs.cloud.google.com/architecture/architecture-decision-records
- GOV.UK, *Architectural Decision Record Framework*: https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework
- The GDS Way, *Architecture decisions*: https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html
- MADR template and minimal template: https://raw.githubusercontent.com/adr/madr/main/template/adr-template.md, https://raw.githubusercontent.com/adr/madr/main/template/adr-template-minimal.md, https://adr.github.io/madr/
- adr-tools: https://github.com/npryce/adr-tools
- log4brains: https://github.com/thomvaill/log4brains
- Martin Fowler, *Architecture Decision Record*: https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
- Olaf Zimmermann, *ADR creation*: https://ozimmer.ch/practices/2023/04/03/ADRCreation.html
- Design Practice Repository, *Y-statement ADR template*: https://github.com/socadk/design-practice-repository/blob/master/artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md
- Spotify Engineering, *When should I write an Architecture Decision Record*: https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record
- Thoughtworks Technology Radar, *Lightweight Architecture Decision Records*: https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
- Joel Parker Henderson, *Architecture decision record*: https://raw.githubusercontent.com/joelparkerhenderson/architecture-decision-record/main/README.md
- PEP 1, *PEP Purpose and Guidelines*: https://peps.python.org/pep-0001/
- RFC 7322, *RFC Style Guide*: https://www.rfc-editor.org/rfc/rfc7322.txt
- Rust RFC template: https://github.com/rust-lang/rfcs/blob/master/0000-template.md
- Atlassian, DACI decision template and Decisions blueprint: https://www.atlassian.com/software/confluence/templates/decision, https://confluence.atlassian.com/doc/decisions-blueprint-339739406.html
- GitHub Docs, *Linking a pull request to an issue*: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
