---
id: e5799ba8-98b0-4df9-9413-cdad03e76aab
title: "AI Cost Management"
domain: agenticdevelopercookbook://guidelines/implementing/networking/ai-cost-management
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-04-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "AI API calls cost $0.01-$0.10+ each. Systems MUST treat AI calls as a managed resource with budgets, caching, and fallback strategies."
platforms: []
tags:
  - cost-management
  - ai
  - caching
  - rate-limiting
depends-on:
  - agenticdevelopercookbook://guidelines/implementing/networking/caching
  - agenticdevelopercookbook://guidelines/implementing/networking/rate-limiting
related:
  - agenticdevelopercookbook://guidelines/implementing/observability/ai-provider-observability
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ai-api-integration
  - networking
  - performance-optimization
---

# AI Cost Management

AI API calls cost $0.01-$0.10+ each. Systems MUST treat AI calls as a managed resource with budgets, caching, and fallback strategies.

## Requirements

**response-caching**: Identical or semantically equivalent requests MUST be cached. Cache key includes: model, prompt template ID, template variables, temperature (if 0). Cache TTL depends on the use case.

**cost-budgets**: Every AI-powered feature MUST define a per-user and per-request cost budget. The system MUST reject or degrade gracefully when the budget is exhausted.

**tiered-model-selection**: Systems SHOULD route requests to the cheapest model that meets quality requirements. Example: use Haiku for classification, Sonnet for generation, Opus for complex reasoning.

**batch-over-realtime**: Non-latency-sensitive work SHOULD use batch APIs (typically 50% cheaper) rather than real-time endpoints.

**cost-per-request-tracking**: Every API response MUST record actual cost (input tokens times price plus output tokens times price). Aggregate cost SHOULD be available per feature, per user, and per time period.

**provider-fallback**: Systems SHOULD define fallback providers for availability and cost. If the primary provider's costs spike or availability drops, traffic can shift.

**prompt-optimization**: Prompt length directly affects cost. Prompts SHOULD be reviewed for token efficiency. System prompts SHOULD be cached where the API supports it (e.g., Anthropic prompt caching).

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-04-09 | Mike Fullerton | Initial creation |
