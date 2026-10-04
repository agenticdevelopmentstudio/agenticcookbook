---
id: 3890e8fb-9d2d-42db-9753-cf60b95152cc
title: "AI Provider Observability"
domain: agenticdevelopercookbook://guidelines/implementing/observability/ai-provider-observability
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-04-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Every call to an AI provider API MUST be logged with structured metadata for cost attribution, debugging, and performance monitoring."
platforms: []
tags:
  - observability
  - ai
  - llm
  - logging
depends-on:
  - agenticdevelopercookbook://guidelines/implementing/observability/logging
related:
  - agenticdevelopercookbook://guidelines/implementing/networking/ai-cost-management
references:
  - https://opentelemetry.io/docs/
  - https://docs.anthropic.com/en/api/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ai-api-integration
  - logging
  - api-integration
---

# AI Provider Observability

Every call to an AI provider API MUST be logged with structured metadata for cost attribution, debugging, and performance monitoring.

## Requirements

**structured-request-log**: Every AI API call MUST log: provider name, model ID, prompt token count, completion token count, total cost (computed from token counts and per-token price), latency in milliseconds, HTTP status, and request ID.

**prompt-tracking**: Prompt templates MUST be versioned. Logs SHOULD reference the prompt template ID and version, not the full prompt text (which may contain PII).

**cost-attribution**: Logs MUST include a cost-attribution tag (feature name, user action, or batch job ID) so costs can be traced to their source.

**rate-limit-tracking**: Rate limit headers (remaining, reset) SHOULD be logged to enable proactive throttling.

**error-classification**: AI provider errors MUST be classified: rate-limit, context-length-exceeded, content-filter, server-error, timeout. Each category has different retry and fallback behavior.

**no-pii-in-prompt-logs**: Full prompt text MUST NOT be logged in production. Use prompt template IDs. In development or staging, full prompts MAY be logged if the environment is access-controlled.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-04-09 | Mike Fullerton | Initial creation |
