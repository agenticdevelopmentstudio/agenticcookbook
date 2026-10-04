---
id: 36825f6a-eedc-4cc5-a857-e107133f7ce5
title: "Distributed tracing and context propagation"
domain: agenticdevelopercookbook://guidelines/implementing/observability/distributed-tracing
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Propagate W3C trace context across every service hop and async boundary, and correlate logs/metrics/traces via a shared trace_id."
platforms: []
tags:
  - observability
  - tracing
  - opentelemetry
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/observability/metrics-red-use
references:
  - https://opentelemetry.io/
  - https://www.w3.org/TR/trace-context/
  - https://opentelemetry.io/docs/concepts/context-propagation/
  - https://opentelemetry.io/blog/2025/sampling-milestones/
  - https://uptrace.dev/opentelemetry/distributed-tracing
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - logging
  - networking
---

# Distributed tracing and context propagation

A distributed trace stitches the spans produced by every service that handles one logical request into a single causal tree. Standardize instrumentation on OpenTelemetry (OTel) and propagation on W3C Trace Context so traces work across vendors and language boundaries. The durable payoff: when something is slow or broken, you can follow one `trace_id` from the edge through every hop.

## Instrument with OpenTelemetry

- Code **MUST** create spans through the OpenTelemetry API rather than vendor-specific SDKs, so the backend stays swappable.
- Each unit of work (an HTTP handler, a DB query, an outbound call, a model invocation) **SHOULD** be one span with a clear name and status.
- Spans **SHOULD** record errors via `span.record_exception` / set status to `ERROR` rather than only logging, so failures are visible in the trace tree.
- Prefer auto-instrumentation for common frameworks/clients; reserve manual spans for domain-specific work.

## Propagate context across boundaries

- A request crossing a service boundary **SHOULD** propagate W3C Trace Context: the `traceparent` header (and `tracestate` when present). This is the W3C Trace Context Recommendation (Level 1, dated 6 February 2020). *Level 2 is a Candidate Recommendation Draft as of 2026 — treat its additions as a forecast and pin to Level 1 for interop.*
- Header names **MUST** be treated as ASCII case-insensitive; emit `traceparent` in lowercase.
- Services **MUST NOT** drop an incoming `traceparent`; continue the trace instead of starting a new root, or the trace fragments.
- Inject and extract context at the transport edge (middleware/interceptors), not scattered through business logic.

### Async and messaging boundaries

- Trace context **MUST** travel with the message, not just synchronous calls — inject `traceparent` into message/event metadata when publishing.
- For queues, pub/sub, and event streams, the consumer span **SHOULD** use a **span link** to the producer rather than a parent-child edge. A single message may fan out to many consumers, and processing is often decoupled in time; links express that causal-but-not-nested relationship.

## Correlate logs, metrics, and traces

- Log records **SHOULD** carry the active `trace_id` (and `span_id`) so a log line can be pivoted to its trace and back. See `agenticdevelopercookbook://guidelines/implementing/observability/metrics-red-use` for the metric side.
- Use the same `trace_id` field name across services; agents grep on it to correlate signals.
- Exemplars (linking a metric data point to a sample `trace_id`) **MAY** be emitted to jump from a latency spike to a representative trace.

## Control cost with sampling

- Prefer **tail-based sampling** at the OpenTelemetry Collector over head-based sampling in the SDK: the full trace is buffered and the keep/drop decision is made after completion, so interesting traces survive.
- A sane default policy: keep 100% of traces containing an error or high latency, and sample a fraction (e.g., ~10%) of successful traces. Tune the rate from what proves useful — do not treat any one number as a fixed rule.
- A consistent sampling decision **MUST** be propagated via `traceparent` trace-flags so all services in one trace agree, avoiding partial traces.

## Agentic and GenAI systems

- Model the agent loop as spans: each model call and each tool/function call **SHOULD** be its own span, nested under the request or agent-step span, so token usage and tool latency are attributable.
- Where applicable, follow the OpenTelemetry GenAI semantic conventions (e.g., `gen_ai.request.model`) for attribute names. *These conventions are still in Development status as of 2026 and may change — record the convention version you target.*
- Capturing prompt/response content on spans **SHOULD** be opt-in and redacted, to avoid leaking sensitive data into the tracing backend.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
