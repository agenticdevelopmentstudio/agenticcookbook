
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pr-review-001 | structural-validation | PR adding an artifact with a missing `id` field | Phase 1 reports a frontmatter failure and posts a Request Changes review |
| pr-review-002 | markdownlint | PR with a markdownlint-fixable list-indent violation | The violation is auto-fixed and the re-validation passes |
| pr-review-003 | vale-cookbook-style | Requirement text containing "should probably handle as needed" | Vale flags the hedging and vague-term rules |
| pr-review-004 | fix-loop | An issue that remains after each of 3 iterations | The loop stops at 3 iterations and flags the issue as unfixable |
| pr-review-005 | fix-categorization | One markdownlint error, one inferrable missing value, one design question | Categorized respectively as auto-fixable, LLM-fixable, and human-required |
| pr-review-006 | content-completeness | A MUST requirement with no test vector | The completeness check fails for that requirement |
| pr-review-007 | convention-compliance | A requirement named `REQ_001` | Flagged as not kebab-case |

