
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Job worker | [adc.ingredient.infrastructure.job-worker](cookbook:22fbf585-c5a3-425a-94f1-ba9b570ebfde) | Owns the poll-claim loop, lease heartbeat, handler dispatch table, result reporting, and the idempotency contract | Yes | Supported job types, batch size, poll interval (default 5 seconds), per-handler timeout, concurrency limit |
| LLM backend | [adc.ingredient.infrastructure.llm-backend](cookbook:597e9cd0-453a-42b8-a464-8ba8d31a6efc) | Executes each handler's inference step with schema-constrained output through a configured provider | Yes | Backend kind (OpenAI-compatible HTTP endpoint or CLI subprocess) and endpoint, selected by environment variable or config file |
| Categorize and tag handler | [adc.ingredient.infrastructure.categorize-and-tag-handler](cookbook:7c0b4381-0a41-4d8c-8b90-1614038b1a94) | The concrete handler registered for the `categorize_and_tag` job type | Yes | Registered in the job worker's dispatch table at startup; receives the LLM backend by injection |

