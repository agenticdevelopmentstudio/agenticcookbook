
| State | Behavior |
|-------|----------|
| Validating | Deterministic checks (structure, markdownlint, Vale) are running |
| Fixing | A fix-loop iteration is applying auto-fixable and LLM-fixable corrections |
| Approved | No unfixed issues remain; a PR review with Approve is posted |
| Rejected | Unfixable or human-required issues remain after 3 iterations; a Request Changes review is posted |

