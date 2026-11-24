
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

