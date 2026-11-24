
- **LLM backend returns invalid schema**: the handler MUST fail the job with `retryable: true` rather than passing a malformed result to complete (backend-failure-is-job-failure).
- **Startup with empty handler registry**: the node MUST log a warning and start normally; it will claim no jobs (no supported types), poll an empty result, and idle.
- **Large batch with mixed types**: the node SHOULD process jobs in the batch concurrently up to a configurable concurrency limit, with each job's heartbeat running independently.
- **Backend slower than the lease**: a long LLM call that outlasts one heartbeat interval relies on the job worker's heartbeat running independently of the handler, so the lease stays valid while inference runs.
- **Component-level cases**: network partition during complete, heartbeat firing after a terminal call, and clock skew are specified in the job-worker ingredient's edge cases; they apply to this composition unchanged.

