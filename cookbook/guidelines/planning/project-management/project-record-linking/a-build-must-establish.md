
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

