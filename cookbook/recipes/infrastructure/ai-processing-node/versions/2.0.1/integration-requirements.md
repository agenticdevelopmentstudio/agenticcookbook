
- **register-handler-at-startup**: The `categorize_and_tag` handler MUST be registered in the job worker's dispatch table at startup, and the job worker's supported-types set MUST include `categorize_and_tag` if and only if that handler is registered.
- **inject-llm-backend**: The node MUST construct the LLM backend from configuration at startup and inject it into every handler that performs inference. A handler MUST NOT select or construct its own backend, so the same handler runs unmodified on the Swift development node and the TypeScript production node.
- **backend-failure-is-job-failure**: When the LLM backend fails or returns output that does not validate against the handler's schema, the handler MUST fail and the job worker MUST report the job as failed with `retryable: true`. A malformed result MUST NOT be passed to the complete call.
- **handler-result-reported-by-worker**: The job worker, not the handler, MUST report the handler's validated result to the backend, and MUST do so only after the handler's schema validation has passed.
- **idempotent-end-to-end**: A job re-claimed after a lease expiry MUST produce the same backend result as the first completion, with no duplicate category or tag entries. The job worker's duplicate-terminal-state tolerance and the handler's idempotent-categorization requirement together satisfy this.
- **stub-backend-testable**: The composition MUST be runnable with a stub LLM backend and a stub job source, so the integration vectors can run without network access to a model or to the `adh` backend.

