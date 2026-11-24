---
id: 23e55c7c-c16e-40d1-88a0-4b51148d2660
title: Project Record Linking
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "How project records link: unique identifiers never reused, typed links by identifier shown on both ends, records superseded not deleted, links checked."
platforms: []
tags:
  - project-management
  - traceability
  - identifiers
  - links
  - project-records
depends-on: []
related:
  - 2b7a1593-48e0-4bbe-8e14-0df7a863628d
  - 3f978ba7-c8c1-4b53-8fda-12e5a6966b75
  - f77eeffe-2699-4028-9195-4bfc23c75e91
  - 023d4c91-d797-4e82-880c-a4ad7906a54a
  - a55182ef-3144-407c-b64a-6377f37f5c63
  - f264cc0b-45d3-4593-a437-7371610c5a8a
references:
  - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://adr.github.io/madr/
  - https://www.w3.org/Provider/Style/URI
  - https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
  - https://github.com/joelparkerhenderson/architecture-decision-record
  - https://github.com/npryce/adr-tools/blob/master/src/adr-new
  - https://en.wikipedia.org/wiki/Requirements_traceability
  - https://prince2.wiki/management-products/issue-register
  - https://prince2.wiki/management-products/risk-register/
  - https://www.prince2.com/uk/blog/the-risk-register-what-to-include-and-what-to-avoid
  - https://ferdinebi.github.io/software-engineering-with-ai/delivery/project-management/risk-issue-management/
  - https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
  - https://docs.github.com/en/rest/issues/issue-dependencies
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues
  - https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/transferring-an-issue-to-another-repository
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/deleting-an-issue
  - https://confluence.atlassian.com/adminjiraserver/configuring-issue-linking-938847862.html
  - https://confluence.atlassian.com/jirasoftware/referencing-issues-in-your-development-work-1688898766.html
  - https://support.atlassian.com/migration/kb/migration-of-jiras-historical-keys-for-issues-and-projects/
  - https://linear.app/docs/issue-property
  - https://docs.gitlab.com/user/work_items/linked_items/
  - https://doorstop.readthedocs.io/en/v3.1/cli/validation.html
  - https://sphinx-needs.readthedocs.io/en/latest/configuration.html
  - https://www.ibm.com/docs/SSYMRC_7.0.3/com.ibm.jazz.vvc.doc/topics/c_linkval.html
  - https://arxiv.org/abs/2206.04462
approved-by: ""
approved-date: ""
triggers: []
---

# Project Record Linking

Give every project record an identifier that is unique, never reused and free of anything that changes, such as status, and make every link name its target by that identifier. Give each link a type that reads correctly from both ends, show a two-way relationship on both records, and close or supersede a record instead of deleting it, linking a superseding record and the one it replaces to each other. Check the links for targets that do not exist.

This guideline covers the linking convention shared by a delivery team's project records: risks, decisions, dependencies, issues, milestones and tasks. It covers how a record is identified, how a link names its target, what type a link carries, which record carries which link, and how the links are checked. The fields that belong to one kind of record stay with that record's own guideline: decision supersession with decision records, issue resolution with issue tracking, blocked milestones with milestone scheduling, task blockers with task breakdown, and the risk and dependency fields with risk tracking and dependency tracking. Requirements traceability for safety-critical work is outside it.

Following this guideline means keeping each SHOULD rule below, or stating why a record departs from it; a MAY rule is an option the team can take or leave. No rule here is a MUST.

## Rules

### Identifying records

- **record-has-unique-stable-id**: Each project record SHOULD have an identifier that is unique among the project's records, so it can be tracked and referenced. (claims: pg-prince2-unique-identifiers, bp-ids-never-reused, ks-jira-key-names-target)
- **id-never-reused-or-renamed**: A record's identifier SHOULD NOT be reused for another record, and SHOULD keep naming the same record when the record moves; where a move gives the record a new identifier, the old one SHOULD still lead to the record. (claims: bp-ids-never-reused, pg-moved-records-keep-old-names)
- **identifier-carries-no-status**: A record's identifier SHOULD NOT encode anything that changes over the record's life, such as its status. (claim: bp-identifier-carries-no-status)

### Writing links

- **link-names-target-by-id**: A link from one record to another SHOULD name its target by the target's identifier. (claims: ks-github-autolink-backlink, ks-jira-key-names-target, ks-backlinks-computed)
- **typed-links-with-both-readings**: A link SHOULD carry a type, such as relates to, blocks or duplicates, with a reading for each direction, such as "blocks" from one record and "is blocked by" from the other. (claims: ks-jira-typed-links-two-descriptions, ks-gitlab-bidirectional-links, ks-linear-relations, ks-backlinks-computed)
- **two-way-link-recorded-once-shown-both-ways**: A two-way relationship between two records SHOULD be one relationship that is shown from both records, each in its own reading, and removing it SHOULD remove it from both. (claims: ks-two-way-link-recorded-once, ks-github-autolink-backlink, ks-github-dependencies-both-directions, ks-gitlab-bidirectional-links, ks-linear-relations, ks-adr-tools-reverse-link, ks-backlinks-computed, bp-bidirectional-traceability)
- **link-instead-of-copy**: A record SHOULD link to the record that holds a piece of information rather than copy that information, so the project keeps a single source of truth. (claim: pg-github-single-source-and-blockers)

### Which record carries which link

- **blocked-record-names-its-blocker**: A record whose work is blocked SHOULD state which record blocks it, by a blocked-by link to that record. (claims: pg-github-single-source-and-blockers, ks-github-dependencies-both-directions, ks-linear-relations, ks-gitlab-bidirectional-links)
- **child-record-carries-parent-link**: A record that is part of a larger one, such as a sub-issue under its parent issue, work under a milestone, or the change that resolves an issue, MAY carry the link to the larger record. (claims: ks-github-sub-issues-and-milestones, ks-github-closing-keywords)
- **superseding-record-links-both-ways**: A record that supersedes another SHOULD link to the record it replaces, and the replaced record SHOULD be marked superseded, with a link to its replacement. (claims: bp-supersede-and-link-both, ks-adr-tools-reverse-link, ev-supersede-not-edit-debated, ev-unrecorded-decisions-contradicted)
- **realised-risk-links-to-its-issue**: When a risk materialises and becomes an issue, the issue and the risk it came from MAY be linked, so the connection between them is kept. (claims: bp-risk-realised-links-issue, pg-prince2-integrated-register)

### Keeping links valid

- **close-or-supersede-never-delete**: A record that is no longer current SHOULD be closed or marked superseded rather than deleted, so the links to it keep leading to it. (claims: pg-deleted-record-breaks-links, ks-linear-relations, bp-supersede-and-link-both)
- **check-links-for-dangling-targets**: The project's links SHOULD be checked for any link whose identifier names no existing record, and each such link SHOULD be reported. (claims: ks-dangling-link-checks, pg-deleted-record-breaks-links, ev-missing-links-impede)
- **mark-changed-links-suspect**: A link check MAY mark a link suspect when the record at either end changes, or when the link is new, so the link is checked again before it is trusted. (claim: ks-suspect-links)
- **report-unlinked-records**: A link check MAY report a record that has no links to or from any other record. (claims: ks-dangling-link-checks, ks-traceability-matrix, ev-missing-links-impede)

## Linking project records

This section is informative: it shows one way to keep the rules, not a required method.

1. Give each record its identifier when it is created, and never hand that identifier to another record. Decision logs number records sequentially and never reuse a number (Nygard, MADR); Jira keys are a project prefix, a hyphen and a number, such as ABC-123. Which scheme the project's records use, one prefix per record type or one sequence for all, is left open here: the sources ask only that identifiers be unique and not reused.
2. Keep status, owner and other changing facts in the record's fields, never in its identifier. W3C's advice for web addresses is the model: documents change status, so an address that names a status breaks.
3. Write each link with its type and the target's identifier: "D-4 supersedes D-2", "T-12 is blocked by DEP-3". A tracker turns a reference by number or key into a link: GitHub converts #26, and Jira links a commit whose message holds the key.
4. Make a two-way relationship visible from both records. GitLab's linked items are bi-directional and are removed from both items together; Jira stores one link with an outward and an inward description; GitHub writes a backlink by default and exposes blocked-by and blocking from both ends; Sphinx-Needs stores the link on the source item and computes the back link; adr-tools writes the reverse link into the existing record. For records kept as files, whether both files hold the link or one file holds it and a checker computes the reverse is left open here.
5. When a record is finished with, close it or mark it superseded; do not delete it. A deleted GitHub issue's address shows page-not-found and nobody is notified, while Linear keeps a resolved blocker linked as Related. Whether an accepted decision record may still take dated amendments is a question for decision records, and is not settled here.
6. Run a link check, by tool or by hand, whenever records are added, moved or closed. Doorstop and Sphinx-Needs check links by default: both flag a link to an unknown identifier, and Doorstop also reports links to inactive items, items with no links, and cycles. IBM's lifecycle tools mark a link suspect when either end changes. Whether a link to an unknown identifier fails the check or only warns, whether a link to a closed or superseded record is reported at all, and which records must have at least one link, are left open here.
7. To see every link at once, a traceability matrix lists records against records; it becomes large and confusing as the project grows, so a check that lists only the problems scales better.

How the tools compare:

- **GitHub** links by number with an automatic backlink, records blocked-by and blocking dependencies with a Blocked icon, nests sub-issues under a parent, and closes an issue when a change that names it with a closing keyword is merged. A transferred issue's old address redirects; a deleted one is gone.
- **Jira** names each item by its key, gives each link type an outward and an inward description (relates to, duplicates, blocks, clones by default), and reserves and redirects a moved item's old keys.
- **Linear** shows Blocked by on one issue and Blocks on the other, turns a mention into a related link, and moves the relation to Related once the blocker is resolved.
- **GitLab** keeps linked items as bi-directional relationships (relates to, blocks, is blocked by) and asks for confirmation before a blocked item is closed.
- **Doorstop and Sphinx-Needs** keep items as files, check their links by default, and, in Sphinx-Needs, compute back links with separate incoming and outgoing wording.

## Examples

This section is informative; the records below are illustrations, not a format the guideline requires. Their identifier prefixes are one possible scheme, not a choice the guideline makes.

A superseded decision and its replacement:

```markdown
# D-2: Store attachments in the database
Status: superseded by D-4

# D-4: Store attachments in object storage
Status: accepted
Supersedes: D-2
```

A blocked task, shown from both ends of the link:

| Record | Link type, as read from this record | Target |
|---|---|---|
| T-12 Offline sign-in | is blocked by | DEP-3 |
| DEP-3 Token-refresh endpoint | blocks | T-12 |

A realised risk and the issue it became:

| Record | Status | Link |
|---|---|---|
| R-7 Vendor API rate limits | realised | see I-01 |
| I-01 Sync fails under vendor rate limits | open | came from R-7 |

A link check's report:

```text
T-15 is blocked by DEP-9: no record DEP-9
I-04: no links to or from any record
```

## What a reviewer looks for

Checks that every project record has an identifier unique in the project, that no identifier has been reused or carries a status, and that a moved record's old identifier still leads to it. Checks that every link names its target by identifier, carries a type that reads correctly from each end, and that a two-way relationship shows on both records and was removed from both when it was removed. Checks that blocked work names its blocker, that a superseding record and the one it replaces link to each other with the old one marked superseded, that no record has been deleted where it could have been closed or superseded, and that information is linked rather than copied between records. Checks that the links have been checked for identifiers that name no record, and that every dangling link found was reported.

## A complete review must establish

- Each SHOULD rule is kept or its departure is stated: `record-has-unique-stable-id`, `id-never-reused-or-renamed`, `identifier-carries-no-status`, `link-names-target-by-id`, `typed-links-with-both-readings`, `two-way-link-recorded-once-shown-both-ways`, `link-instead-of-copy`, `blocked-record-names-its-blocker`, `superseding-record-links-both-ways`, `close-or-supersede-never-delete`, `check-links-for-dangling-targets`.
- Each MAY rule is noted where it was used: `child-record-carries-parent-link`, `realised-risk-links-to-its-issue`, `mark-changed-links-suspect`, `report-unlinked-records`.

## A build must establish

- `record-has-unique-stable-id`: every project record has an identifier unique among the project's records.
- `id-never-reused-or-renamed`: no identifier names more than one record, and each moved record's old identifier still leads to it.
- `identifier-carries-no-status`: no identifier encodes the record's status or another fact that changes.
- `link-names-target-by-id`: every link names its target by the target's identifier.
- `typed-links-with-both-readings`: every link has a type with a reading for each direction.
- `two-way-link-recorded-once-shown-both-ways`: each two-way relationship shows on both records, and removing it removes it from both.
- `link-instead-of-copy`: information held in one record is linked from the others, not copied into them.
- `blocked-record-names-its-blocker`: every blocked record has a blocked-by link to the record that blocks it.
- `child-record-carries-parent-link`: where used, each part record carries the link to the record it is part of.
- `superseding-record-links-both-ways`: each superseding record links to the one it replaces, and the replaced one is marked superseded with a link back.
- `realised-risk-links-to-its-issue`: where used, each issue that came from a realised risk is linked to that risk.
- `close-or-supersede-never-delete`: no record that others link to has been deleted; it was closed or marked superseded.
- `check-links-for-dangling-targets`: the links have been checked, and each link whose identifier names no record has been reported.
- `mark-changed-links-suspect`: where used, links whose ends changed, or that are new, were marked suspect and checked again.
- `report-unlinked-records`: where used, the check reports records with no links.

## Rationale

This section is informative.

A link is only as good as the name it uses for its target. The sources agree on what keeps that name working: a unique reference for each register entry (PRINCE2, as its accredited trainers summarise it), a number that is never reused (Nygard, MADR), an identifier that holds nothing that changes (W3C, "Cool URIs don't change"), and old names that keep resolving when a record moves (Jira's reserved historical keys, GitHub's redirect for a transferred issue). Deletion is the one move no tracker repairs: a deleted GitHub issue shows page-not-found and nobody is told, so every link to it dangles. That is why records are closed or superseded instead. A decision that is not recorded where later work can find it gets argued again or contradicted without anyone knowing (Microsoft Learn), which is why a superseding record and the one it replaces link to each other.

Typed links with a reading for each direction, shown on both records, are what every tracker researched does: Jira's outward and inward descriptions, GitLab's bi-directional linked items, GitHub's backlinks and its blocked-by and blocking API, Linear's Blocked by and Blocks, adr-tools' reverse link and Sphinx-Needs' computed back links. Traceability, as Gotel and Finkelstein define it for requirements, means following an item both forwards and backwards. Checking the links is what the traceability tools do by default (Doorstop, Sphinx-Needs, IBM's lifecycle tools), and one industrial experience report found that links assumed to exist were missing and that the gap blocked the fix when the links were needed.

Every rule is a recommendation or an option because the sources are: none makes any of these practices mandatory for project records, and several are stated for one kind of record, such as decision records, and applied here to the others by analogy. Three claims were weakened by the second check and carry no MUST: that trackers record a two-way relationship once, which is this research's reading of their behaviour rather than anything they say; that traceability runs both ways for any item, which the source defines for requirements only; and that links are often missing, which rests on one case. Three rules are options rather than recommendations: carrying the link on the child record (only GitHub documents which end carries it), linking a realised risk to its issue (secondary sources only), and reporting unlinked records (Doorstop treats this as a warning, not an error). Marking changed links suspect rests on one vendor's documentation.

The Scrum Guide does not prescribe links between backlog items and leaves their attributes to the team. PMBOK, ISO 21502, ISO 31000 and the PRINCE2 manual are paywalled and could not be read, so no rule rests on them; the Kanban Guide, SAFe and LeSS were not researched; and no study measured how often project-record links dangle. Several questions are the owner's and are left open: whether a two-way link is written in both records' files or once with its reverse computed; whether identifiers use one prefix per record type or one sequence; whether a link to an unknown identifier fails the check or only warns; whether a link to a closed or superseded record is reported, and at what level; whether every record must have a link or only the kinds whose own guidelines require one; whether accepted decision records are immutable or may take dated amendments; and whether a realised risk keeps its record and links forward to the issue or moves to the issue register.

## References

This section is informative; every reference below is informative, and none is normative.

- Michael Nygard, *Documenting Architecture Decisions* (Cognitect): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- *MADR: Markdown Architectural Decision Records*: https://adr.github.io/madr/
- Tim Berners-Lee, *Cool URIs don't change* (W3C): https://www.w3.org/Provider/Style/URI
- Microsoft Learn, *Maintain an architecture decision record (ADR)*: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- Joel Parker Henderson, *Architecture decision record*: https://github.com/joelparkerhenderson/architecture-decision-record
- Nat Pryce, *adr-tools* (`src/adr-new`): https://github.com/npryce/adr-tools/blob/master/src/adr-new
- Wikipedia, *Requirements traceability*: https://en.wikipedia.org/wiki/Requirements_traceability
- PRINCE2 Wiki, *Issue register* and *Risk register*: https://prince2.wiki/management-products/issue-register, https://prince2.wiki/management-products/risk-register/
- ILX Group, *The risk register: what to include (and what to avoid)*: https://www.prince2.com/uk/blog/the-risk-register-what-to-include-and-what-to-avoid
- *Risk & Issue Management* (course page): https://ferdinebi.github.io/software-engineering-with-ai/delivery/project-management/risk-issue-management/
- GitHub Docs, *Autolinked references and URLs*: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls
- GitHub Docs, *Creating issue dependencies* and *REST API endpoints for issue dependencies*: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies, https://docs.github.com/en/rest/issues/issue-dependencies
- GitHub Docs, *Adding sub-issues* and *About milestones*: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues, https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
- GitHub Docs, *Linking a pull request to an issue*: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
- GitHub Docs, *Best practices for Projects*: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- GitHub Docs, *Transferring an issue to another repository* and *Deleting an issue*: https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/transferring-an-issue-to-another-repository, https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/deleting-an-issue
- Atlassian Documentation, *Configuring issue linking* and *Referencing issues in your development work*: https://confluence.atlassian.com/adminjiraserver/configuring-issue-linking-938847862.html, https://confluence.atlassian.com/jirasoftware/referencing-issues-in-your-development-work-1688898766.html
- Atlassian Support, *Handling of historical key conflicts in Jira Cloud migrations*: https://support.atlassian.com/migration/kb/migration-of-jiras-historical-keys-for-issues-and-projects/
- Linear Docs, *Issue properties*: https://linear.app/docs/issue-property
- GitLab Docs, *Linked items*: https://docs.gitlab.com/user/work_items/linked_items/
- Doorstop, *Integrity checks*: https://doorstop.readthedocs.io/en/v3.1/cli/validation.html
- Sphinx-Needs, *Configuration*: https://sphinx-needs.readthedocs.io/en/latest/configuration.html
- IBM Documentation, *Link validity in projects that are enabled for configurations*: https://www.ibm.com/docs/SSYMRC_7.0.3/com.ibm.jazz.vvc.doc/topics/c_linkval.html
- Fucci, Alégroth and Axelsson, *When Traceability Goes Awry: an Industrial Experience Report*: https://arxiv.org/abs/2206.04462

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
