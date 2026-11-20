
- Model the agent loop as spans: each model call and each tool/function call **SHOULD** be its own span, nested under the request or agent-step span, so token usage and tool latency are attributable.
- Where applicable, follow the OpenTelemetry GenAI semantic conventions (e.g., `gen_ai.request.model`) for attribute names. *These conventions are still in Development status as of 2026 and may change — record the convention version you target.*
- Capturing prompt/response content on spans **SHOULD** be opt-in and redacted, to avoid leaking sensitive data into the tracing backend.

