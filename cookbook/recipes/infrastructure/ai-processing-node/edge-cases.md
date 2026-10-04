
- **Network partition during complete**: if the complete or fail call fails with a transient network error, the node SHOULD retry that specific HTTP call with limited exponential backoff before giving up. Abandoning without reporting is preferable to a tight retry storm; the job will eventually be re-queued when the lease expires.
- **Handler returns before first heartbeat interval**: heartbeat goroutine/timer MUST be cancelled before calling complete so no heartbeat fires after the terminal call.
- **LLM backend returns invalid schema**: the handler MUST fail the job with `retryable: true` rather than passing a malformed result to complete.
- **Startup with empty handler registry**: the node MUST log a warning and start normally; it will claim no jobs (no supported types), poll an empty result, and idle.
- **Clock skew between node and backend**: heartbeat interval MUST be derived from the backend-reported lease duration, not the node's wall clock, to tolerate moderate skew.
- **Large batch with mixed types**: the node SHOULD process jobs in the batch concurrently up to a configurable concurrency limit, with each job's heartbeat running independently.

