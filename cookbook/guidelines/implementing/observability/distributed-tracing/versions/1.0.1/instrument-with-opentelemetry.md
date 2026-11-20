
- Code **MUST** create spans through the OpenTelemetry API rather than vendor-specific SDKs, so the backend stays swappable.
- Each unit of work (an HTTP handler, a DB query, an outbound call, a model invocation) **SHOULD** be one span with a clear name and status.
- Spans **SHOULD** record errors via `span.record_exception` / set status to `ERROR` rather than only logging, so failures are visible in the trace tree.
- Prefer auto-instrumentation for common frameworks/clients; reserve manual spans for domain-specific work.

