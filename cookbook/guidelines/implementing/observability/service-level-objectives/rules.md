
- **measure-at-the-journey**: SLIs SHOULD be measured at the boundary closest to the user (load balancer, API gateway, or client telemetry), not at an internal subsystem. CPU and memory are causes, not user experience.
- **cover-the-failure-modes**: For each user-facing service you SHOULD define SLIs across the relevant categories:
  - **Availability** — fraction of requests that succeed (e.g. non-5xx).
  - **Latency** — fraction of requests faster than a threshold, at a percentile.
  - **Correctness / freshness / coverage** — for data and async pipelines.
- **latency-uses-percentiles**: Latency SLIs MUST be stated as a percentile bound, not a mean (a mean hides tail pain).
- **define-multiple-latency-thresholds**: Latency SLIs SHOULD define **multiple thresholds** to capture both typical and tail experience, e.g. *90% of requests < 100 ms AND 99% < 400 ms*.
- **define-valid-events**: You MUST state which events count toward the denominator (exclude health checks, internal warmup, client-aborted requests) and document it alongside the SLI.
- **slos-are-targets-not-100**: SLOs are targets not 100 percent: SLOs MUST be below 100%. 100% is the wrong target — it forbids all change and is unobservable.
- **choose-lowest-unnoticed-reliability**: You SHOULD choose the lowest reliability users won't notice.
- **user-facing-needs-an-slo**: Every user-facing service SHOULD have at least one SLO with an owner.
- **start-from-data**: You SHOULD start from data: set the initial SLO from observed performance, then tighten deliberately, and SHOULD NOT promise a number you have never measured.
- **budget-governs-velocity**: A healthy budget SHOULD license shipping faster; an exhausted budget SHOULD trigger an agreed response (freeze risky changes, prioritize reliability work) until it recovers.
- **agree-the-policy-first**: The consequences of budget exhaustion MUST be agreed by both product and engineering owners *before* a breach, not negotiated during an incident.
- **alert-on-symptom-not-cause**: Alerting MUST target budget burn (the user-visible symptom), not resource thresholds (CPU > 80%, queue depth). Threshold alerts are noisy proxies that fire without user impact and miss impact that doesn't touch the watched resource.
- **use-multi-window-multi-burn-rate**: Burn-rate alerts SHOULD require BOTH a long and a short window to exceed the threshold. The long window gives recall (catches sustained burn); the short window cuts reset time so the alert clears soon after the burn stops, reducing false positives.
- **tier-by-severity**: Alerts SHOULD page on fast burn and open a ticket on slow burn. A common starting set for a 99.9% SLO (per Google SRE; tune to your window and tolerance):

  | Severity | Long window | Short window | Burn rate | Budget consumed |
  |----------|-------------|--------------|-----------|-----------------|
  | Page     | 1 hour      | 5 minutes    | 14.4      | ~2%             |
  | Page     | 6 hours     | 30 minutes   | 6         | ~5%             |
  | Ticket   | 3 days      | 6 hours      | 1         | ~10%            |

- **scale-windows-to-your-slo**: These windows and rates assume a 30-day, 99.9% SLO. You MUST recompute them when your window or target differs — the burn-rate-to-time mapping changes with the window length.
- **should-not-alert-on-fixed-error-count**: Alerting SHOULD NOT rest on a single fixed error-count threshold (no relation to budget; floods or misses).
- **should-not-use-one-global-slo**: You SHOULD NOT have one global SLO covering unrelated journeys (masks a broken critical path behind healthy traffic).
- **should-not-measure-slos-only-inside-service**: SLOs SHOULD NOT be measured only inside the service, missing client-side and edge failures.
