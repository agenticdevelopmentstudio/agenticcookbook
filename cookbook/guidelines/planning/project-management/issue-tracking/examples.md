
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

