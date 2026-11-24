
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
- **child-record-carries-parent-link**: Where a record is part of a larger one, such as a sub-issue under its parent issue, work under a milestone, or the change that resolves an issue, the link between them MAY be carried on the smaller record. (claims: ks-github-sub-issues-and-milestones, ks-github-closing-keywords)
- **superseding-record-links-both-ways**: A record that supersedes another SHOULD link to the record it replaces, and the replaced record SHOULD be marked superseded, with a link to its replacement. (claims: bp-supersede-and-link-both, ks-adr-tools-reverse-link, ev-supersede-not-edit-debated, ev-unrecorded-decisions-contradicted)
- **realised-risk-links-to-its-issue**: When a risk materialises and becomes an issue, the issue and the risk it came from MAY be linked, so the connection between them is kept. (claims: bp-risk-realised-links-issue, pg-prince2-integrated-register)

### Keeping links valid

- **close-or-supersede-never-delete**: A record that is no longer current SHOULD be closed or marked superseded rather than deleted, so the links to it keep leading to it. (claims: pg-deleted-record-breaks-links, ks-linear-relations, bp-supersede-and-link-both)
- **check-links-for-dangling-targets**: The project's links SHOULD be checked for any link whose identifier names no existing record, and each such link SHOULD be reported. (claims: ks-dangling-link-checks, pg-deleted-record-breaks-links, ev-missing-links-impede)
- **mark-changed-links-suspect**: A link check MAY mark a link suspect when the record at either end changes, or when the link is new, so the link is checked again before it is trusted. (claim: ks-suspect-links)
- **report-unlinked-records**: A link check MAY report a record that has no links to or from any other record. (claims: ks-dangling-link-checks, ks-traceability-matrix, ev-missing-links-impede)

