
- `structured-request-log`: an AI API call site whose log record lacks any of provider name, model ID, prompt and completion token counts, computed total cost, latency in milliseconds, HTTP status, or request ID
- `must-version-prompt-templates`: a prompt template with no version, or a prompt built inline with no template
- `should-reference-prompt-template-in-logs`: a log record that carries full prompt text instead of the prompt template ID and version
- `cost-attribution`: an AI API call logged with no cost-attribution tag (feature name, user action, or batch job ID)
- `rate-limit-tracking`: rate limit headers (remaining, reset) read from the response but not logged
- `error-classification`: an AI provider error handled without being classified as rate-limit, context-length-exceeded, content-filter, server-error or timeout
- `no-pii-in-prompt-logs`: full prompt text written to logs on a production path
- `may-log-full-prompts-in-controlled-environments`: full prompt logging enabled in development or staging without access control on that environment
