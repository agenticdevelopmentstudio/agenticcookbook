
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

