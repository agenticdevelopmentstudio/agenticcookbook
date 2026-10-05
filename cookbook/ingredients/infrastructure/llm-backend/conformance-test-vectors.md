
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| llm-backend-001 | llm-backend-selectable | Switch the configured backend kind from an HTTP endpoint to a CLI tool and restart | Handlers run against the new backend with no code change |
| llm-backend-002 | structured-output | A handler requests inference with a result schema | The request carries the schema or equivalent structured-output constraint; the result is validated against it |
| llm-backend-003 | invalid-output-fails-retryable | Stub backend returns output missing a required field | Handler fails the job with `retryable: true`; no malformed result is reported |
| llm-backend-004 | backend-injected | Run a handler with a stub backend | Handler produces its result without any network or subprocess call |

