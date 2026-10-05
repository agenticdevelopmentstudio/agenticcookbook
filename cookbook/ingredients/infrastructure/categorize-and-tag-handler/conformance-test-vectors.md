
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| categorize-handler-001 | handler-job-type, input-payload, output-result | Job of type `categorize_and_tag` with `{ "title": "How to prune roses", "body": "..." }` | Handler returns `{ category, tags }` with an optional `confidence` |
| categorize-handler-002 | schema-constrained-output | Inspect the LLM request the handler builds | The request carries the result JSON Schema; no free-text parsing step exists |
| categorize-handler-003 | confidence-advisory | LLM returns `confidence: 1.4` | Output fails validation; handler reports a retryable failure |
| categorize-handler-004 | idempotent-categorization | Same job is processed twice | The second run produces no additional category or tag writes |
| categorize-handler-005 | category-single-best-fit, tags-keywords | LLM returns a category and an empty tag list | Result is accepted; `tags` is an empty array |

