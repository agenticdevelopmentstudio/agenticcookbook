---
id: 64bdf327-b4ac-4772-a3b6-cbaf7e8e5449
title: "Metrics instrumentation: RED and USE"
domain: agenticdevelopercookbook://guidelines/implementing/observability/metrics-red-use
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Instrument services with RED metrics and resources with USE so signals correlate and feed SLIs/SLOs."
platforms: []
tags:
  - observability
  - metrics
  - monitoring
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/observability/service-level-objectives
references:
  - https://www.brendangregg.com/usemethod.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - logging
  - performance-optimization
---

# Metrics instrumentation: RED and USE

Two complementary methods decide WHAT to measure. Instrument every request-serving **service** with RED (Rate, Errors, Duration) and every consumable **resource** with USE (Utilization, Saturation, Errors). Both derive from Google's Four Golden Signals and feed directly into SLIs/SLOs.

## When to use which

- **RED** — request-handling work: HTTP/gRPC endpoints, message consumers, RPC handlers, queue workers. Measures the caller's experience (external/workload view).
- **USE** — finite resources: CPU, memory, disk, network interfaces, connection pools, thread pools, queues, file descriptors (internal/resource view).
- A single component often needs both: a service emits RED for its endpoints AND USE for its connection pool and worker queue.

## RED — instrument every service

- **rate-metric**: Each service **MUST** emit request rate as a counter (requests over time), labeled by route/operation.
- **errors-metric**: Each service **MUST** emit a count of failed requests as a separate counter (or as an `error`/`status` label on the rate counter) so error ratio is computable.
- **duration-metric**: Each service **MUST** emit request duration as a histogram (not just a mean) so percentiles (p50/p95/p99) are derivable; means hide tail latency.
- **error-definition**: Each service **MUST** document what counts as an error (e.g., HTTP 5xx, gRPC non-OK, business-level failure) — error ratio is meaningless without an explicit definition.
- **cardinality-limit**: Labels **MUST NOT** include unbounded values (raw user IDs, full URLs, request bodies). Use bounded route templates (`/users/{id}`, not `/users/42`) to keep time-series cardinality manageable.

## USE — instrument every resource

For each resource, capture all three:

| Dimension | Meaning | Example signal |
|-----------|---------|----------------|
| **Utilization** | Fraction of time (or capacity) the resource was busy | CPU %, pool in-use / pool size |
| **Saturation** | Degree of queued/unservable extra work | run-queue length, pending tasks, swap activity |
| **Errors** | Count of error events | failed allocations, disk I/O errors, pool timeouts |

- **resource-coverage**: Resources that can become a bottleneck **SHOULD** be monitored with all three USE dimensions; saturation is the most predictive of impending failure and **MUST NOT** be silently omitted.
- **saturation-signal**: Saturation **SHOULD** be a measurable queue depth or wait metric, not inferred solely from high utilization — 100% utilization without saturation is healthy throughput.

## Conventions for correlation

- **naming-convention**: Metric names **SHOULD** follow one consistent scheme across services (the cookbook default is OpenTelemetry semantic conventions, e.g. `http.server.request.duration`) so the same query works everywhere and dashboards compose.
- **unit-discipline**: Durations **SHOULD** be recorded in seconds and sizes in bytes (base units), with the unit stated in metric metadata; mixing `ms` and `s` for the same concept breaks aggregation.
- **shared-labels**: Cross-cutting labels (`service`, `environment`, `version`) **SHOULD** be applied uniformly so RED and USE signals from the same deployment join cleanly during incident analysis.

## Relationship to other methods

- RED ≈ the Four Golden Signals minus Saturation; pair RED (service) with USE (resource) to recover full coverage including saturation.
- RED was adapted from the USE method for the service/request domain — they are intentionally complementary, not alternatives.
- Per-service RED metrics are the natural source for SLIs; see `agenticdevelopercookbook://guidelines/implementing/observability/service-level-objectives`.

## Avoid

- Recording duration as a gauge or average instead of a histogram (loses percentiles).
- High-cardinality labels that explode the time-series count and cost.
- Tracking utilization while ignoring saturation, then being surprised by latency cliffs.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
