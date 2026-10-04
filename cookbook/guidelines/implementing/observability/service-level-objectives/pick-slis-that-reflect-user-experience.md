
An SLI is a ratio: **good events / valid events**, expressed as a percentage.

- **measure-at-the-journey**: SLIs SHOULD be measured at the boundary closest to the user (load balancer, API gateway, or client telemetry), not at an internal subsystem. CPU and memory are causes, not user experience.
- **cover-the-failure-modes**: For each user-facing service you SHOULD define SLIs across the relevant categories:
  - **Availability** — fraction of requests that succeed (e.g. non-5xx).
  - **Latency** — fraction of requests faster than a threshold, at a percentile.
  - **Correctness / freshness / coverage** — for data and async pipelines.
- **latency-uses-percentiles**: Latency SLIs MUST be stated as a percentile bound, not a mean (a mean hides tail pain). Define **multiple thresholds** to capture both typical and tail experience, e.g. *90% of requests < 100 ms AND 99% < 400 ms*.
- **define-valid-events**: You MUST state which events count toward the denominator (exclude health checks, internal warmup, client-aborted requests) and document it alongside the SLI.

