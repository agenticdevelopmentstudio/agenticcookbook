<!-- leaf: recipes-infrastructure/ai-processing-node--part-2 · source: recipes/infrastructure/ai-processing-node.md -->

# AI Processing Node — continued (part 2)

## Platform Notes

### Swift macOS Daemon (Development Node)

- Implemented as a launchd-managed background process (`launchd` plist, `KeepAlive: true`).
- The poll-claim loop runs on a dedicated `Task` (Swift Concurrency). Each job is processed in its own child `Task`, bounded by a `TaskGroup` limited to the configured concurrency ceiling.
- Lease heartbeat: a `Task` that loops `try await Task.sleep(for: heartbeatInterval)` until cancelled. Cancel it by calling `.cancel()` on the heartbeat task before reporting complete/fail.
- LLM backend selection: read from a `.env` file or `UserDefaults` key `com.adh.node.llmBackend`. A local model server (e.g., Ollama via OpenAI-compat endpoint) is the default for development.
- Structured output: use the `/v1/chat/completions` endpoint with `response_format: { type: "json_schema", json_schema: { schema: ... } }` when the model supports it; fall back to a `json_object` response type with system-prompt schema injection.
- Logging: use `os.Logger` with subsystem `com.adh.node` and category per handler.

### TypeScript Service (Production Node)

- Implemented as a Node.js long-running process, containerized and managed by the deployment platform (e.g., Docker / Kubernetes Deployment).
- The poll-claim loop runs as an `async` loop with `await`-based polling. Each job is dispatched to a `Promise`-based handler; a `p-limit` semaphore or equivalent caps concurrency.
- Lease heartbeat: a `setInterval` timer started immediately after claim, cleared in a `finally` block that fires whether complete, fail, or error terminates the handler.
- LLM backend selection: `LLM_BACKEND_KIND` and `LLM_BACKEND_URL` environment variables. Production uses a hosted API (e.g., Anthropic API via OpenAI-compatible shim, or the native Anthropic SDK). See `agenticdevelopercookbook://recipes/infrastructure/ai-processing-node#design-decisions/llm-backend-env`.
- Structured output: use the provider's native structured-output parameter (`response_format` or `tools` with a single schema-constrained tool) to avoid parsing free text.
- Logging: structured JSON to stdout (`pino` or equivalent), consumed by the deployment platform's log aggregator.

## Design Decisions

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
