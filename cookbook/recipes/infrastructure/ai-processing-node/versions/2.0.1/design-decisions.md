
**Decision**: Pull model (node polls for jobs) rather than push model (backend pushes to node).
**Rationale**: Pull tolerates node restarts without message loss, scales horizontally without a broker, and lets each node self-throttle by controlling its batch size. At the scale of a development or small production node, the polling overhead is negligible.
**Approved**: pending

**Decision**: Lease + heartbeat rather than a one-shot acknowledgement.
**Rationale**: Long-running LLM inference can take tens of seconds to minutes. A one-shot ack with no keepalive would require the backend to set an unrealistically long timeout or risk never detecting a crashed node. Heartbeats let the backend detect node loss in one heartbeat interval.
**Approved**: pending

**Decision**: Heartbeat interval is one-third of the lease duration (not one-half or fixed).
**Rationale**: One-third gives two missed heartbeats before the lease expires, tolerating transient network hiccups without prematurely losing the lease. One-half leaves only one miss, which is too tight; fixed intervals couple the node to backend config.
**Approved**: pending

**Decision**: `retryable: false` on unknown job type (immediate dead-letter).
**Rationale**: An unknown type means no handler will ever exist on this node for that job. Retrying would exhaust the max-attempts counter with no chance of success and delay the operator seeing the misconfiguration. Dead-letter with a clear error is faster feedback.
**Approved**: pending

**Decision**: LLM backend selected by configuration, not by handler code.
**Rationale**: The `categorize_and_tag` handler (and future handlers) must run unmodified on both the Swift dev node (local model) and the TypeScript prod node (hosted API). Injecting the backend as a configured dependency keeps handler code platform-agnostic and testable with a stub.
**Approved**: pending

**Decision**: Idempotency is a handler contract, not enforced by the node framework.
**Rationale**: Only the handler knows what constitutes a duplicate side effect for its domain. The node framework can detect a duplicate job ID (already in terminal state on the backend) and skip re-running, but fine-grained deduplication (e.g., "did I already write this category?") requires handler-level logic.
**Approved**: pending

