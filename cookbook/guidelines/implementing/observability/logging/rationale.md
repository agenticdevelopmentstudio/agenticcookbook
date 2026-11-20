
- `should-emit-telemetry-via-opentelemetry`, `should-carry-trace-id-on-log-lines`, `should-follow-otel-semantic-conventions`, `should-use-structured-json-in-production`: The per-platform loggers remain the source of structured log lines; these rules govern how those lines integrate with distributed telemetry. The PII guidance (`must-not-log-pii`) still applies to them.
- `should-use-etw-for-system-diagnostics`, `should-use-xaml-live-visual-tree`, `should-use-vs-performance-profiler`: Windows uses `ILogger<T>` with the same conventions as C#; these tools apply additionally.
