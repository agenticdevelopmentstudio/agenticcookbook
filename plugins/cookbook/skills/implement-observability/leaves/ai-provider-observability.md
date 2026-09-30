<!-- leaf: implement-observability/ai-provider-observability · source: guidelines/implementing/observability/ai-provider-observability.md -->

**Rules** (cite as `implement-observability/ai-provider-observability#<slug>`):

- `ai-provider-api-logged-structured-metadata-cost` MUST — Every call to an AI provider API MUST be logged with structured metadata for cost attribution, debugging, and …
- `structured-request-log` MUST
- `prompt-tracking` MUST
- `cost-attribution` MUST
- `rate-limit-tracking` SHOULD
- `error-classification` MUST
- `no-pii-in-prompt-logs` MUST

# AI Provider Observability

Every call to an AI provider API MUST be logged with structured metadata for cost attribution, debugging, and performance monitoring.

## Requirements

**structured-request-log**: Every AI API call MUST log: provider name, model ID, prompt token count, completion token count, total cost (computed from token counts and per-token price), latency in milliseconds, HTTP status, and request ID.

**prompt-tracking**: Prompt templates MUST be versioned. Logs SHOULD reference the prompt template ID and version, not the full prompt text (which may contain PII).

**cost-attribution**: Logs MUST include a cost-attribution tag (feature name, user action, or batch job ID) so costs can be traced to their source.

**rate-limit-tracking**: Rate limit headers (remaining, reset) SHOULD be logged to enable proactive throttling.

**error-classification**: AI provider errors MUST be classified: rate-limit, context-length-exceeded, content-filter, server-error, timeout. Each category has different retry and fallback behavior.

**no-pii-in-prompt-logs**: Full prompt text MUST NOT be logged in production. Use prompt template IDs. In development or staging, full prompts MAY be logged if the environment is access-controlled.
