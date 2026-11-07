
The per-platform loggers above remain the source of structured log lines; this subsection governs how those lines integrate with distributed telemetry. The PII guidance still applies — never emit personally identifiable information in any field, even at debug level.

- Components **SHOULD** emit telemetry via [OpenTelemetry](https://opentelemetry.io/) and export over OTLP, treating it as the de-facto, CNCF-graduated standard, rather than relying on ad-hoc per-platform logging alone.
- Every log line **SHOULD** carry a trace/correlation ID (e.g., `trace_id` and `span_id`) propagated through the request context, so logs correlate with distributed traces.
- Log and span field names **SHOULD** follow the OpenTelemetry [semantic conventions](https://opentelemetry.io/docs/specs/semconv/) rather than ad-hoc names.
- Production logs **SHOULD** be structured JSON to keep them machine-parseable for aggregation and trace correlation.

See [distributed tracing](agenticdevelopercookbook://guidelines/implementing/observability/distributed-tracing) for span propagation and exporter configuration.

