---
id: 967fe6f8-aa3a-4bcf-8415-7f996042c245
title: "Continuous profiling"
domain: agenticdevelopercookbook://guidelines/implementing/observability/continuous-profiling
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Adopt always-on, low-overhead production profiling correlated with traces only when measured perf/cost debugging justifies the pipeline."
platforms: []
tags:
  - observability
  - profiling
  - performance
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/observability/metrics-red-use
  - agenticdevelopercookbook://guidelines/implementing/observability/distributed-tracing
references:
  - https://opentelemetry.io/blog/2024/profiling/
  - https://www.datadoghq.com/blog/continuous-profiling-fourth-pillar/
  - https://charity.wtf/2025/10/30/the-pillar-is-a-lie/
  - https://opentelemetry.io/docs/specs/status/
  - https://thenewstack.io/elastic-profiling-agent-offers-a-4th-pillar-of-observability/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - performance-optimization
  - logging
---

# Continuous profiling

Continuous profiling samples CPU, memory, and allocation stacks continuously in production and renders them as flame graphs — a fourth observability signal alongside metrics, logs, and traces. Treat it as a maturity addition for diagnosing production performance and cost regressions, not a day-one default.

## When to adopt (MEASURED-NEED guardrail)

Per YAGNI and make-it-work-make-it-right-make-it-fast, **you MUST NOT** add a continuous-profiling pipeline by default. **Adopt it ONLY when** a concrete, measured need justifies the added pipeline, storage, and operational cost:

- A recurring or hard-to-reproduce production CPU/memory/allocation regression that metrics and traces localize to a service but not to a function or line.
- A cloud-cost or efficiency mandate where shaving CPU/memory directly reduces spend.
- Latency outliers whose hot path is not visible from span timings alone.

If a one-off `pprof`/perf capture or a load-test profile answers the question, **prefer that** over standing infrastructure (small-reversible-decisions).

## How to do it

- **You MUST** choose a low-overhead, sampling profiler. eBPF whole-system profilers and runtime samplers commonly report well under 1% CPU overhead; **you MUST** validate overhead in your own environment rather than trusting a single vendor's published figure.
- **You SHOULD** prefer whole-system eBPF profiling on Linux (no per-app instrumentation; supports mixed runtimes) when targets are diverse, and **MAY** use in-runtime profilers (Go `runtime/pprof`, JFR, async-profiler, .NET `dotnet-trace`) when you need language-level detail.
- **You SHOULD** emit profiles in a `pprof`-compatible or OTLP-Profiles-convertible format so data is portable across backends (explicit-over-implicit).
- **You MUST** attach resource attributes (`service.name`, `service.version`, deployment, region) so profiles join the rest of your telemetry.
- **You SHOULD** correlate profiles with traces by recording `trace_id`/`span_id` on profile samples where the profiler and runtime support it; this lets you jump from a slow span to the code that ran inside it. (FORECAST: automatic span-level correlation is uneven across profilers/runtimes as of 2026 — verify support per language before relying on it.)
- **You SHOULD** retain profiles at a shorter window than metrics/logs (volume is high) and downsample or aggregate older data.

## Standards status (pin and verify)

- The **OpenTelemetry Profiles signal entered public Alpha on 2026-03-26**; the OTLP profiles signal is still in **Development/unstable** while traces, metrics, and logs are Stable. Treat profiles wire format and semantic conventions as moving targets — **you MUST** pin the collector/SDK version and re-verify on upgrade.
- OTLP Profiles is an independent standard inspired by `pprof`, with lossless round-trip conversion to/from `pprof`. (FORECAST: production-ready OTLP-Profiles backends are still emerging; **prefer** a profiler whose data you can convert if the backend changes.)

## Anti-patterns

- **You MUST NOT** treat continuous profiling as a substitute for RED/USE metrics or distributed tracing — it complements them; start there.
- **You MUST NOT** ship a profiler whose overhead you have not measured, especially on latency-critical services.
- **You SHOULD NOT** store full-resolution profiles indefinitely; cost grows fast with no marginal diagnostic value.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
