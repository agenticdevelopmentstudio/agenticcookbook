
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

**Decision**: The `claude-code` provider runs with no tools (`--tools ""`, `--strict-mcp-config`, `--safe-mode`, `--permission-mode dontAsk`), pinned flags and an empty working directory.
**Rationale**: Tools for a step come only from the hub's `/mcp` under the acting token, where the persona's grants apply. Letting the CLI use its own tools, its MCP servers or the owner's settings and hooks would act with the machine user's full access outside those grants. `--allowedTools ""` is not enough, because it only pre-approves tools and the read-only ones run without asking in `-p` mode. The empty working directory gives the CLI no project to read, and a flag taken from the step would let a template author turn tools back on.
**Approved**: pending

**Decision**: Script steps run only on a machine whose owner set `AI_NODE_ALLOW_SCRIPTS=1`.
**Rationale**: A script is arbitrary code. On the owner's own machine, with the owner's explicit opt-in, it runs with the owner's own authority; on a shared hub pool node it would run one customer's code beside another's.
**Approved**: pending

**Decision**: The tool loop is capped at 20 tool calls per step and the cap is a non-retryable failure.
**Rationale**: A model that keeps asking for tools would otherwise hold the lease and spend tokens without end; retrying the same prompt would loop the same way.
**Approved**: pending
