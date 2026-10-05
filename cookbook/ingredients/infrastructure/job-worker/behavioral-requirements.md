
### Poll-Claim Loop

- **poll-claim**: The node MUST claim work by sending a batch claim request to the backend (pull model), passing the set of job types it supports and a maximum batch size. The backend atomically reserves and returns up to that many matching pending jobs. An empty result (zero jobs returned) MUST be treated as a no-op — the loop continues without producing side effects or logging spurious errors.
- **supported-types-static**: The set of job types a node can handle MUST be declared at startup from configuration and MUST NOT change during a run. The node MUST NOT claim a job whose type it cannot handle.
- **loop-continuity**: The poll-claim loop MUST run continuously. A single job failure, a lease loss, or a handler panic MUST NOT terminate the loop; the node logs the incident and continues to the next poll iteration.
- **poll-interval**: Between claim attempts that return zero jobs, the node SHOULD wait a configurable backoff interval (default 5 seconds) before polling again to avoid hammering an idle queue.

### Lease Heartbeat

- **lease-heartbeat**: While processing a claimed job, the node MUST renew the job's lease by sending a heartbeat to the backend at an interval of approximately one-third of the lease duration. The heartbeat interval MUST be derived from the lease duration returned with the claim response, not hardcoded.
- **lost-lease-abort**: If a heartbeat response indicates the lease is no longer valid (expired, stolen, or cancelled), the node MUST stop all work on that job immediately, discard any partial result, and NOT call the complete or fail endpoint. The job will be re-queued by the backend.
- **heartbeat-stop-on-terminal**: The node MUST stop sending heartbeats as soon as it calls complete or fail for a job.

### Handler Dispatch

- **run-handler**: The node MUST dispatch each claimed job to a handler registered for that job's `type` field. The handler receives the job's `payload` deserialized to the handler's declared input type. The dispatch table MUST be populated at startup from registered handlers; runtime registration is not required.
- **unknown-type-fail**: If no handler is registered for a job's `type`, the node MUST immediately report failure with `retryable: false`. The job MUST NOT be retried and MUST be sent to dead-letter by the backend. The node MUST NOT crash or halt the loop.
- **handler-timeout**: Each handler invocation SHOULD be subject to a configurable per-handler timeout. If a handler exceeds its timeout, the node MUST treat the invocation as a handler error (see `fail-with-backoff`).

### Result Reporting

- **complete-on-success**: On handler success, the node MUST report job completion to the backend, passing the handler's structured result as the job result payload. The node MUST wait for the backend's acknowledgement before releasing the job from local tracking.
- **fail-with-backoff**: On handler error (exception, timeout, or non-recoverable condition), the node MUST report job failure to the backend with `retryable: true`. The backend is solely responsible for applying exponential backoff and enforcing the max-attempts dead-letter policy; the node MUST NOT implement retry logic locally. One failing job MUST NOT halt the poll-claim loop.

### Idempotency

- **idempotency**: Handlers MUST be safe to run more than once for the same job ID and target (leases can expire mid-run and the same job may be re-claimed by any node). A handler MUST produce no duplicate side effects on repeated invocation — if the operation was already applied, the handler MUST detect this and return the same result without re-applying. Calling complete or fail for a job that has already reached a terminal state MUST be accepted gracefully; the node MUST NOT treat such a response as an error.

