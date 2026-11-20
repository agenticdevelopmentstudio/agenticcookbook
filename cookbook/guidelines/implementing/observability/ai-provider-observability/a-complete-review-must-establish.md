
- `structured-request-log`: whether every AI API call logs provider name, model ID, prompt token count, completion token count, total cost, latency in milliseconds, HTTP status, and request ID
- `must-version-prompt-templates`: whether every prompt template is versioned
- `should-reference-prompt-template-in-logs`: whether logs reference the prompt template ID and version rather than the full prompt text
- `cost-attribution`: whether every AI API call log carries a cost-attribution tag
- `rate-limit-tracking`: whether rate limit headers (remaining, reset) are logged
- `error-classification`: whether every AI provider error is classified into rate-limit, context-length-exceeded, content-filter, server-error or timeout
- `no-pii-in-prompt-logs`: whether any production path logs full prompt text
- `may-log-full-prompts-in-controlled-environments`: whether full prompts are logged only in development or staging, and only where that environment is access-controlled
