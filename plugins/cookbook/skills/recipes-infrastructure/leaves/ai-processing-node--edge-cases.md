<!-- leaf: recipes-infrastructure/ai-processing-node--edge-cases · source: recipes/infrastructure/ai-processing-node.md -->

# AI Processing Node

**Rules** (cite as `recipes-infrastructure/ai-processing-node--edge-cases#<slug>`):

- `network-partition-during-complete` SHOULD — if the complete or fail call fails with a transient network error, the node SHOULD retry that specific HTTP call with …
- `handler-returns-before-first-heartbeat-interval` MUST — heartbeat goroutine/timer MUST be cancelled before calling complete so no heartbeat fires after the terminal call.
- `llm-backend-returns-invalid-schema` MUST — the handler MUST fail the job with retryable: true rather than passing a malformed result to complete.
- `startup-with-empty-handler-registry` MUST — the node MUST log a warning and start normally; it will claim no jobs (no supported types), poll an empty result, and …
- `clock-skew-between-node-and-backend` MUST — heartbeat interval MUST be derived from the backend-reported lease duration, not the node's wall clock, to tolerate …
- `large-batch-with-mixed-types` SHOULD — the node SHOULD process jobs in the batch concurrently up to a configurable concurrency limit, with each job's …

## Edge Cases

- **Network partition during complete**: if the complete or fail call fails with a transient network error, the node SHOULD retry that specific HTTP call with limited exponential backoff before giving up. Abandoning without reporting is preferable to a tight retry storm; the job will eventually be re-queued when the lease expires.
- **Handler returns before first heartbeat interval**: heartbeat goroutine/timer MUST be cancelled before calling complete so no heartbeat fires after the terminal call.
- **LLM backend returns invalid schema**: the handler MUST fail the job with `retryable: true` rather than passing a malformed result to complete.
- **Startup with empty handler registry**: the node MUST log a warning and start normally; it will claim no jobs (no supported types), poll an empty result, and idle.
- **Clock skew between node and backend**: heartbeat interval MUST be derived from the backend-reported lease duration, not the node's wall clock, to tolerate moderate skew.
- **Large batch with mixed types**: the node SHOULD process jobs in the batch concurrently up to a configurable concurrency limit, with each job's heartbeat running independently.
