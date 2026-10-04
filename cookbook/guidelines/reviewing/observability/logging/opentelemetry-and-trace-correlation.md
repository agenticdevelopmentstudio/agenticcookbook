
Logs SHOULD be emitted through [OpenTelemetry](agenticdevelopercookbook://guidelines/implementing/observability/distributed-tracing) and exported over OTLP, the de-facto cross-vendor standard for telemetry. Prefer this over per-platform-only logging frameworks so logs, traces, and metrics share one pipeline and one backend.

- Every log line SHOULD carry the active trace ID and span ID (a trace/correlation ID), so a log can be pivoted to its trace and vice versa. OpenTelemetry-aware logging integrations inject these automatically when a span is in scope.
- Field names SHOULD follow OpenTelemetry semantic conventions (e.g. `service.name`, `trace_id`, `http.request.method`) rather than ad-hoc keys, so telemetry is portable across backends.
- Production logs SHOULD be emitted as structured JSON, not free-form text, to keep them machine-parseable and aggregable.

The per-platform frameworks above remain the local emission layer; route their output through an OpenTelemetry appender/bridge rather than replacing them. PII guidance still applies — never log personally identifiable information at any level, including trace-correlated logs.

