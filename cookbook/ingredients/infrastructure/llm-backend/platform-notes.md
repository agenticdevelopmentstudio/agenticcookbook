
SwiftUI, Compose, and React/Web do not apply: an LLM backend has no view layer.

- **Swift macOS (development node)**: Read the backend from a `.env` file or the `UserDefaults` key `com.adh.node.llmBackend`. A local model server (e.g., Ollama via its OpenAI-compatible endpoint) is the default for development. Use the `/v1/chat/completions` endpoint with `response_format: { type: "json_schema", json_schema: { schema: ... } }` when the model supports it; fall back to a `json_object` response type with system-prompt schema injection.
- **TypeScript (production node)**: Read `LLM_BACKEND_KIND` and `LLM_BACKEND_URL` environment variables. Production uses a hosted API (e.g., the Anthropic API via an OpenAI-compatible shim, or the native Anthropic SDK). Use the provider's native structured-output parameter (`response_format` or `tools` with a single schema-constrained tool) to avoid parsing free text.

