
**response-caching**: Identical or semantically equivalent requests MUST be cached. Cache key includes: model, prompt template ID, template variables, temperature (if 0). Cache TTL depends on the use case.

**cost-budgets**: Every AI-powered feature MUST define a per-user and per-request cost budget. The system MUST reject or degrade gracefully when the budget is exhausted.

**tiered-model-selection**: Systems SHOULD route requests to the cheapest model that meets quality requirements. Example: use Haiku for classification, Sonnet for generation, Opus for complex reasoning.

**batch-over-realtime**: Non-latency-sensitive work SHOULD use batch APIs (typically 50% cheaper) rather than real-time endpoints.

**cost-per-request-tracking**: Every API response MUST record actual cost (input tokens times price plus output tokens times price). Aggregate cost SHOULD be available per feature, per user, and per time period.

**provider-fallback**: Systems SHOULD define fallback providers for availability and cost. If the primary provider's costs spike or availability drops, traffic can shift.

**prompt-optimization**: Prompt length directly affects cost. Prompts SHOULD be reviewed for token efficiency. System prompts SHOULD be cached where the API supports it (e.g., Anthropic prompt caching).

