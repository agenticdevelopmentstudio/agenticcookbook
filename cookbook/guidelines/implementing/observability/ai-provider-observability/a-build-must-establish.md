
- `structured-request-log`: every AI API call logs provider name, model ID, prompt token count, completion token count, total cost (computed from token counts and per-token price), latency in milliseconds, HTTP status, and request ID
- `must-version-prompt-templates`: every prompt template carries a version
- `should-reference-prompt-template-in-logs`: every log of a call references the prompt template ID and version, not the full prompt text, or the code says why
- `cost-attribution`: every AI API call log carries a cost-attribution tag (feature name, user action, or batch job ID)
- `rate-limit-tracking`: rate limit headers (remaining, reset) are logged, or the code says why not
- `error-classification`: every AI provider error is classified as rate-limit, context-length-exceeded, content-filter, server-error or timeout
- `no-pii-in-prompt-logs`: no production path logs full prompt text
- `may-log-full-prompts-in-controlled-environments`: full prompts are logged only in development or staging environments that are access-controlled
