
| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Rule inventory and baseline metrics | Rule audit | Rule optimizer, report | one-way | Held in conversation context for the run |
| Audit findings | Rule audit | Rule optimizer | one-way | Duplication, ungated, and mandatory-read findings listed with file locations |
| Approved proposals | User via the rule optimizer | Rule optimizer write step | one-way | Explicit confirmation of each proposal, or a decline of all |
| Original constraint list | Rule files before edits | Validation | one-way | The enumerated MUST, MUST NOT, and SHOULD constraints captured before writes |
| After metrics and reduction percentage | Validation | Report | one-way | Re-measurement by the same method as the audit |
| Report file | Report phase | The user | one-way | Written to `.claude/rule-optimization-report.md` |

Pipeline state lives in conversation context, not on disk (see Design Decisions): an interrupted run restarts from Phase 1.

