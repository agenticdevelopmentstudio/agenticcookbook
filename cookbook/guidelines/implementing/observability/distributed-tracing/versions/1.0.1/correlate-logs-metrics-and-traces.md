
- Log records **SHOULD** carry the active `trace_id` (and `span_id`) so a log line can be pivoted to its trace and back. See [adc.guideline.implementing.observability.metrics-red-use](cookbook:64bdf327-b4ac-4772-a3b6-cbaf7e8e5449) for the metric side.
- Use the same `trace_id` field name across services; agents grep on it to correlate signals.
- Exemplars (linking a metric data point to a sample `trace_id`) **MAY** be emitted to jump from a latency spike to a representative trace.

