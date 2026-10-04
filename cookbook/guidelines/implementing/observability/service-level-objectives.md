---
id: 6b8715f1-ece0-4db6-b691-19e9d0367ef3
title: "Service-level objectives and error budgets"
domain: agenticdevelopercookbook://guidelines/implementing/observability/service-level-objectives
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Define user-centric SLIs, set SLOs, derive an error budget, and alert on multi-window burn rate rather than resource thresholds."
platforms: []
tags:
  - observability
  - sre
  - reliability
depends-on: []
related:
  - agenticdevelopercookbook://principles/tight-feedback-loops
  - agenticdevelopercookbook://guidelines/implementing/observability/logging
references:
  - https://sre.google/workbook/implementing-slos/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - logging
  - performance-optimization
---

# Service-level objectives and error budgets

Define reliability targets from the user's perspective: pick service-level indicators (SLIs), set service-level objectives (SLOs) against them, and derive an error budget (`1 - SLO`) that licenses change velocity. Alert on error-budget *burn*, not on raw resource thresholds.

## Pick SLIs that reflect user experience

An SLI is a ratio: **good events / valid events**, expressed as a percentage.

- **measure-at-the-journey**: SLIs SHOULD be measured at the boundary closest to the user (load balancer, API gateway, or client telemetry), not at an internal subsystem. CPU and memory are causes, not user experience.
- **cover-the-failure-modes**: For each user-facing service you SHOULD define SLIs across the relevant categories:
  - **Availability** — fraction of requests that succeed (e.g. non-5xx).
  - **Latency** — fraction of requests faster than a threshold, at a percentile.
  - **Correctness / freshness / coverage** — for data and async pipelines.
- **latency-uses-percentiles**: Latency SLIs MUST be stated as a percentile bound, not a mean (a mean hides tail pain). Define **multiple thresholds** to capture both typical and tail experience, e.g. *90% of requests < 100 ms AND 99% < 400 ms*.
- **define-valid-events**: You MUST state which events count toward the denominator (exclude health checks, internal warmup, client-aborted requests) and document it alongside the SLI.

## Set SLOs

An SLO is the target value for an SLI over a rolling window (commonly 28 or 30 days).

- **SLOs-are-targets-not-100**: SLOs MUST be below 100%. 100% is the wrong target — it forbids all change and is unobservable. Choose the lowest reliability users won't notice.
- **user-facing-needs-an-SLO**: Every user-facing service SHOULD have at least one SLO with an owner.
- **start-from-data**: Set the initial SLO from observed performance, then tighten deliberately. Do not promise a number you have never measured.

## Derive and spend the error budget

The error budget is `1 - SLO` — the allowed unreliability over the window. A 99.9% SLO over 30 days permits ~43 min of downtime-equivalent.

- **budget-governs-velocity**: A healthy budget SHOULD license shipping faster; an exhausted budget SHOULD trigger an agreed response (freeze risky changes, prioritize reliability work) until it recovers.
- **agree-the-policy-first**: The consequences of budget exhaustion MUST be agreed by both product and engineering owners *before* a breach, not negotiated during an incident.

## Alert on burn rate, not thresholds

**Burn rate** is how fast you are consuming the error budget relative to the SLO window: burn rate `1` exhausts the budget exactly at the window's end; burn rate `14.4` exhausts it in ~2 hours for a 30-day window.

- **alert-on-symptom-not-cause**: Alerting MUST target budget burn (the user-visible symptom), not resource thresholds (CPU > 80%, queue depth). Threshold alerts are noisy proxies that fire without user impact and miss impact that doesn't touch the watched resource.
- **use-multi-window-multi-burn-rate**: Burn-rate alerts SHOULD require BOTH a long and a short window to exceed the threshold. The long window gives recall (catches sustained burn); the short window cuts reset time so the alert clears soon after the burn stops, reducing false positives.
- **tier-by-severity**: Page on fast burn; open a ticket on slow burn. A common starting set for a 99.9% SLO (per Google SRE; tune to your window and tolerance):

  | Severity | Long window | Short window | Burn rate | Budget consumed |
  |----------|-------------|--------------|-----------|-----------------|
  | Page     | 1 hour      | 5 minutes    | 14.4      | ~2%             |
  | Page     | 6 hours     | 30 minutes   | 6         | ~5%             |
  | Ticket   | 3 days      | 6 hours      | 1         | ~10%            |

- **scale-windows-to-your-SLO**: These windows and rates assume a 30-day, 99.9% SLO. You MUST recompute them when your window or target differs — the burn-rate-to-time mapping changes with the window length.

## Anti-patterns

- Alerting on a single fixed error-count threshold (no relation to budget; floods or misses).
- One global SLO covering unrelated journeys (masks a broken critical path behind healthy traffic).
- SLOs measured only inside the service, missing client-side and edge failures.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
