
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pr-scope-001 | placement-analysis | A recipe placed in `guidelines/` with a recipe-type domain | Flagged as incorrect placement |
| pr-scope-002 | granularity-check | A recipe with 18 MUST requirements | Flagged as potentially too broad |
| pr-scope-003 | granularity-check | A recipe with 2 requirements | Flagged as potentially too narrow |
| pr-scope-004 | overlap-detection | A recipe whose requirement names duplicate an existing recipe's | Overlap flagged with the matching file named |
| pr-scope-005 | ecosystem-fit | A new recipe that no existing related recipe links to | Backlink candidates are listed |
| pr-scope-006 | refactoring-proposal, granular-assessment | A recipe with 10 parts of which 2 are novel | The proposal extracts exactly those 2 parts, per requirement |

