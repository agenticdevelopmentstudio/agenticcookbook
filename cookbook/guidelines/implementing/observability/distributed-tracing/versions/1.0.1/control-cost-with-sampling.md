
- Prefer **tail-based sampling** at the OpenTelemetry Collector over head-based sampling in the SDK: the full trace is buffered and the keep/drop decision is made after completion, so interesting traces survive.
- A sane default policy: keep 100% of traces containing an error or high latency, and sample a fraction (e.g., ~10%) of successful traces. Tune the rate from what proves useful — do not treat any one number as a fixed rule.
- A consistent sampling decision **MUST** be propagated via `traceparent` trace-flags so all services in one trace agree, avoiding partial traces.

