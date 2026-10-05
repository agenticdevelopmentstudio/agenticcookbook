
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Job worker | `agenticdevelopercookbook://ingredients/infrastructure/job-worker` | Owns the poll-claim loop, lease heartbeat, handler dispatch table, result reporting, and the idempotency contract | Yes | Supported job types, batch size, poll interval (default 5 seconds), per-handler timeout, concurrency limit |
| LLM backend | `agenticdevelopercookbook://ingredients/infrastructure/llm-backend` | Executes each handler's inference step with schema-constrained output through a configured provider | Yes | Backend kind (OpenAI-compatible HTTP endpoint or CLI subprocess) and endpoint, selected by environment variable or config file |
| Categorize and tag handler | `agenticdevelopercookbook://ingredients/infrastructure/categorize-and-tag-handler` | The concrete handler registered for the `categorize_and_tag` job type | Yes | Registered in the job worker's dispatch table at startup; receives the LLM backend by injection |

