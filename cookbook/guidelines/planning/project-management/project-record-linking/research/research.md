# Research: project record linking

Researched and accessed 2026-11-24 against base commit `f0dd450e1188364e9e221d912d49657944ae46ad`. Every finding below names its claim id in `research.json`. The quotes in `research.json` are verbatim from the fetched pages.

The topic has no rules of its own, so every verdict is new. The sources agree on a small linking convention:

- Each record gets a unique identifier that is never reused and does not encode status or location.
- A link names its target by that identifier.
- A two-way relationship is recorded once, as a typed link with a reading for each direction, and is shown on both records.
- Records are closed or superseded, never deleted.
- A superseding record and the record it replaces link to each other.
- Blocked work names its blocker.
- Links are checked for dangling targets and orphans.

None of the sources make any of this mandatory for project records. The strongest strength they support is SHOULD.

**Verdicts**

- `record-has-unique-stable-id`: **new**, SHOULD (pg-prince2-unique-identifiers, bp-ids-never-reused, ks-jira-key-names-target)
- `id-never-reused-or-renamed`: **new**, SHOULD (bp-ids-never-reused, bp-identifier-carries-no-status, pg-moved-records-keep-old-names)
- `link-names-target-by-id`: **new**, SHOULD (ks-github-autolink-backlink, ks-jira-key-names-target, ks-backlinks-computed)
- `typed-links-with-both-readings`: **new**, SHOULD (ks-jira-typed-links-two-descriptions, ks-gitlab-bidirectional-links, ks-linear-relations, ks-backlinks-computed)
- `two-way-link-recorded-once-shown-both-ways`: **new**, SHOULD (ks-two-way-link-recorded-once, ks-github-autolink-backlink, ks-github-dependencies-both-directions, ks-gitlab-bidirectional-links, ks-linear-relations, ks-adr-tools-reverse-link, ks-backlinks-computed, bp-bidirectional-traceability). This is the cross-artifact linking rule.
- `close-or-supersede-never-delete`: **new**, SHOULD (pg-deleted-record-breaks-links, ks-linear-relations, bp-supersede-and-link-both)
- `superseding-record-links-both-ways`: **new**, SHOULD (bp-supersede-and-link-both, ks-adr-tools-reverse-link, ev-supersede-not-edit-debated, ev-unrecorded-decisions-contradicted). Microsoft Learn states it as an imperative, and Henderson's dissent is about editing records, not linking them.
- `blocked-record-names-its-blocker`: **new**, SHOULD (pg-github-single-source-and-blockers, ks-github-dependencies-both-directions, ks-linear-relations, ks-gitlab-bidirectional-links)
- `child-record-carries-parent-link`: **new**, MAY (ks-github-sub-issues-and-milestones, ks-github-closing-keywords). Only one vendor documents which end carries the link.
- `realised-risk-links-to-its-issue`: **new**, MAY (bp-risk-realised-links-issue, pg-prince2-integrated-register). Rests on secondary sources only.
- `link-instead-of-copy`: **new**, SHOULD (pg-github-single-source-and-blockers)
- `check-links-for-dangling-targets`: **new**, SHOULD (ks-dangling-link-checks, ks-suspect-links, pg-deleted-record-breaks-links, ev-missing-links-impede)
- `report-unlinked-records`: **new**, MAY (ks-dangling-link-checks, ks-traceability-matrix, ev-missing-links-impede). Doorstop reports this as a warning, not an error.

**Open questions**

- Should a two-way link be written into both records' files, or written once with the reverse computed by the checker? The trackers compute the reverse. File-based records have to choose.
- Should records use one identifier prefix per record type (R-1, D-1, I-1) or one global sequence? The sources require only uniqueness and no reuse.
- Should a link to an unknown identifier fail the check, as Doorstop's error does, or only warn, as Sphinx-Needs does by default?
- Should a link whose target is closed or superseded be reported at all, and if so at what level? Linear keeps it as Related. Doorstop warns when a child links to an inactive parent.
- Must every record link to at least one other record (an orphan check), or only the record types whose host topics require a link?
- Are accepted decision records immutable, as Microsoft Learn and Nygard say? Or may they take dated amendments, which Henderson's teams found worked better?
- When a risk is realised, does its record stay and link forward to the new issue (the "realised, see I-01" convention)? Or does it move to the issue register, as the PRINCE2 summaries describe?

**Limitations**

- PMBOK, ISO 21502 and ISO 31000 are paywalled. PMI's public library pages and ISO's OBP preview returned 403, so no claim rests on them.
- The PRINCE2 manual is paywalled. PRINCE2 is covered only through two accredited trainers' public summaries.
- NASA's Software Engineering Handbook and Gotel and Finkelstein's paper returned 403. Their definition of traceability is cited through Wikipedia.
- The IBM page could be read only through a web-fetch tool, because a direct download returned 403.
- The Kanban Guide, SAFe and LeSS were not researched. The Scrum Guide is silent on links between items.
- Linear's documentation does not say whether a relation is stored once or twice.
- No study measured how often project-record links dangle, so this research makes no metric claim.
- The body of Atlassian's RAID-log article could not be retrieved. The other RAID-log guidance found does not address identifiers or cross-references.

## Best practices

- **bp-ids-never-reused**: Decision records are numbered sequentially, and a number is never reused, so a reference keeps naming the same record (Nygard, MADR).
- **bp-identifier-carries-no-status**: An identifier that must stay valid should not encode things that change, such as status. Links break because people change names (W3C, "Cool URIs don't change").
- **bp-supersede-and-link-both**: A changed decision gets a new record that supersedes the original, and the two are linked rather than the old record being edited (Microsoft Learn, Nygard).
- **bp-bidirectional-traceability**: Traceability means following an item's life both forwards and backwards (Gotel and Finkelstein, via Wikipedia).
- **bp-risk-realised-links-issue**: A risk that materialises becomes an issue, and the register links the risk to the new issue (PRINCE2 wiki, a practitioner course page).

## Known solutions

- **ks-github-autolink-backlink**: GitHub turns a reference by number into a link and writes the reverse link automatically.
- **ks-github-dependencies-both-directions**: GitHub's issue dependencies record blocked-by and blocking relations, mark blocked issues, and expose both directions in the REST API.
- **ks-github-sub-issues-and-milestones**: GitHub links an issue to its parent through sub-issues and to a milestone by association. The parent or milestone shows the children's progress.
- **ks-github-closing-keywords**: On GitHub, the change that resolves an issue carries the link to it, and merging the change closes the issue.
- **ks-jira-typed-links-two-descriptions**: Jira stores one typed link with an outward and an inward description, so a single link reads "is blocked by" from one issue and "blocks" from the other.
- **ks-jira-key-names-target**: Jira names a work item by its key (project prefix, hyphen, number). Putting the key in a commit message links the commit to the item.
- **ks-linear-relations**: Linear shows "Blocked by" on one issue and "Blocks" on the other. A mention becomes a related link, and a resolved blocker stays linked as Related.
- **ks-gitlab-bidirectional-links**: GitLab's linked items are bi-directional and are removed from both items together. Closing a blocked item asks for confirmation.
- **ks-two-way-link-recorded-once**: Across GitLab, Jira and GitHub, a two-way relationship is recorded once and shown from both records, with its own wording on each side.
- **ks-adr-tools-reverse-link**: adr-tools writes both ends of a decision link. Superseding marks the old record and links it to the new one, and a plain link writes a reverse link into the existing record.
- **ks-dangling-link-checks**: Doorstop and Sphinx-Needs check links by default. Both flag links to unknown identifiers. Doorstop also flags links to inactive items, items with no links, and cycles.
- **ks-backlinks-computed**: Sphinx-Needs stores a link once, on the source item, and computes the back link, with separate incoming and outgoing wording.
- **ks-suspect-links**: IBM's lifecycle tools mark a link suspect when either end changes, or when the link is new or unknown.
- **ks-traceability-matrix**: A traceability matrix shows every link at a glance but becomes large and confusing at scale.

## Platform guidelines

Apple, Android and Windows have no bearing on this topic.

- **pg-prince2-unique-identifiers**: PRINCE2's issue and risk registers give every entry a unique reference so it can be tracked and referenced (as summarised by accredited trainers).
- **pg-prince2-integrated-register**: PRINCE2's registers may be kept as one integrated register, with issue reports linked to specific risks.
- **pg-scrum-guide-leaves-attributes**: The Scrum Guide does not prescribe links between backlog items and leaves their attributes to the domain.
- **pg-github-single-source-and-blockers**: GitHub's guidance is to keep a single source of truth, link related items, and state clearly which issues are blocked by or blocking others.
- **pg-moved-records-keep-old-names**: Jira reserves and redirects historical keys, and GitHub redirects a transferred issue's old URL. A moved record keeps its old name working.
- **pg-deleted-record-breaks-links**: A deleted GitHub issue's URL shows page-not-found and nobody is notified, so every link to it dangles.

## The expert's view

- **ev-missing-links-impede**: In an industrial experience report, links assumed to exist turned out to be missing, and the gap blocked the fix when the links were needed (Fucci, Alégroth and Axelsson).
- **ev-unrecorded-decisions-contradicted**: A decision that is not recorded where later work can find it gets re-argued or unknowingly contradicted (Microsoft Learn).
- **ev-supersede-not-edit-debated**: Supersede a decision with a new record rather than altering it. Henderson adds that, in practice, mutability has worked better for his teams.
