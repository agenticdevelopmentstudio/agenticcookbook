
- **SwiftUI / Compose / React/Web**: Not applicable. The node is a background worker with no view layer. The two implementations are a Swift macOS daemon and a TypeScript service.
- **Swift macOS daemon (development node)**: Runs as a launchd-managed background process with a local model server as the default LLM backend. Detailed daemon, heartbeat, structured-output, and logging guidance is in the job-worker and llm-backend ingredients.
- **TypeScript service (production node)**: Runs as a containerized Node.js process using a hosted API as the LLM backend. The backend is selected by the `LLM_BACKEND_KIND` and `LLM_BACKEND_URL` environment variables; see the llm-backend ingredient and the Design Decision on LLM backend selection below.

