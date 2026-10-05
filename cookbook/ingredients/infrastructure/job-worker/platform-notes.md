
SwiftUI, Compose, and React/Web do not apply: a job worker has no view layer. Two implementations satisfy this ingredient simultaneously.

### Swift macOS Daemon (Development Node)

- Implemented as a launchd-managed background process (`launchd` plist, `KeepAlive: true`).
- The poll-claim loop runs on a dedicated `Task` (Swift Concurrency). Each job is processed in its own child `Task`, bounded by a `TaskGroup` limited to the configured concurrency ceiling.
- Lease heartbeat: a `Task` that loops `try await Task.sleep(for: heartbeatInterval)` until cancelled. Cancel it by calling `.cancel()` on the heartbeat task before reporting complete or fail.
- Logging: use `os.Logger` with subsystem `com.adh.node` and category per handler.

### TypeScript Service (Production Node)

- Implemented as a Node.js long-running process, containerized and managed by the deployment platform (e.g., Docker / Kubernetes Deployment).
- The poll-claim loop runs as an `async` loop with `await`-based polling. Each job is dispatched to a `Promise`-based handler; a `p-limit` semaphore or equivalent caps concurrency.
- Lease heartbeat: a `setInterval` timer started immediately after claim, cleared in a `finally` block that fires whether complete, fail, or error terminates the handler.
- Logging: structured JSON to stdout (`pino` or equivalent), consumed by the deployment platform's log aggregator.

