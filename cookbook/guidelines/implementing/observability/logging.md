---
id: 0f0c1da3-1c53-417b-890d-0259d7513c65
title: "Instrumented logging"
domain: agenticdevelopercookbook://guidelines/implementing/observability/logging
type: guideline
version: 1.1.2
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Instrument every component and flow with structured logging using the platform's best-in-class framework, at debug level for state transitions, user interactions, async tasks, and branching."
platforms:
  - csharp
  - kotlin
  - python
  - swift
  - typescript
  - web
  - windows
tags:
  - logging
depends-on: []
related: []
references:
  - https://github.com/JakeWharton/timber
  - https://learn.microsoft.com/en-us/visualstudio/profiling/
  - https://opentelemetry.io/blog/2026/otel-graduates/
  - https://www.cncf.io/announcements/2026/05/21/cloud-native-computing-foundation-announces-opentelemetrys-graduation-solidifying-status-as-the-de-facto-observability-standard/
  - https://www.structlog.org/en/stable/logging-best-practices.html
  - https://opentelemetry.io/docs/specs/semconv/
  - https://docs.cloud.google.com/logging/docs/structured-logging
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - logging
  - new-module
  - error-handling
---

# Instrumented logging

Every component and flow must be instrumented with structured logging using the platform's best-in-class framework:

- **Apple**: `os.log` (`Logger` from `os`) — subsystem matching bundle ID, category per component
- **Android**: `Timber` (or `android.util.Log`)
- **Web**: `console` with structured prefixes, or `pino`/`winston` in Node
- **Python**: `logging` module with module-level loggers
- **Windows/.NET**: `ILogger<T>` from `Microsoft.Extensions.Logging` — category per class via generic parameter

Use `debug` level for flow instrumentation. Log state transitions, user interactions, async task start/completion/failure, and branching logic.

---

# Logging

Every component and flow must be instrumented with structured logging using the platform's best-in-class framework. Use `debug` level for flow instrumentation. Log state transitions, user interactions, async task start/completion/failure, and branching logic. Never log personally identifiable information, even at debug level.

## Swift

Use `os.log` via `Logger` from the `os` module:

```swift
import os

private let logger = Logger(
    subsystem: "{{bundle_id}}",
    category: "ComponentName"
)

logger.debug("PrimaryButton: tapped, starting async action")
```

- Subsystem MUST match the bundle ID
- Category MUST be one per component or flow
- Use `debug` level for UI flow instrumentation

## Kotlin

Use [Timber](https://github.com/JakeWharton/timber) for structured logging:

```kotlin
Timber.d("PrimaryButton: tapped, starting async action")
Timber.d("PrimaryButton: async action completed (success, ${duration}ms)")
```

If no dependency is desired, use `android.util.Log` with consistent tags.

## C#

Inject `ILogger<T>` via constructor injection. The generic parameter sets the log category to the consuming class.

- Use structured message templates: `logger.LogInformation("Processing {OrderId}", orderId)`
- **Never** use string interpolation (`$"..."`) in log calls — it bypasses structured logging and prevents log aggregation
- Use the `[LoggerMessage]` source generator attribute for high-performance hot paths
- Configure log levels per category via `appsettings.json`

```csharp
// Standard logging
private readonly ILogger<OrderService> _logger;

_logger.LogInformation("Processing order {OrderId} for {CustomerId}", orderId, customerId);

// High-performance logging via source generator
[LoggerMessage(Level = LogLevel.Debug, Message = "Cache hit for key {Key}")]
static partial void LogCacheHit(ILogger logger, string key);
```

## Windows

`ILogger<T>` (same conventions as C# above). Additionally:

- Use ETW tracing (`EventSource`) for system-level diagnostics and startup timing
- Use XAML Live Visual Tree in Visual Studio for debugging visual tree issues
- Use [Visual Studio Performance Profiler](https://learn.microsoft.com/en-us/visualstudio/profiling/) for CPU, memory, and UI responsiveness analysis

## Python

Use the `logging` module with module-level loggers:

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Starting roadmap sync for %s", roadmap_id)
```

## OpenTelemetry and trace correlation

The per-platform loggers above remain the source of structured log lines; this subsection governs how those lines integrate with distributed telemetry. The PII guidance still applies — never emit personally identifiable information in any field, even at debug level.

- Components **SHOULD** emit telemetry via [OpenTelemetry](https://opentelemetry.io/) and export over OTLP, treating it as the de-facto, CNCF-graduated standard, rather than relying on ad-hoc per-platform logging alone.
- Every log line **SHOULD** carry a trace/correlation ID (e.g., `trace_id` and `span_id`) propagated through the request context, so logs correlate with distributed traces.
- Log and span field names **SHOULD** follow the OpenTelemetry [semantic conventions](https://opentelemetry.io/docs/specs/semconv/) rather than ad-hoc names.
- Production logs **SHOULD** be structured JSON to keep them machine-parseable for aggregation and trace correlation.

See [distributed tracing](agenticdevelopercookbook://guidelines/implementing/observability/distributed-tracing) for span propagation and exporter configuration.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.2 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.1.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Add OpenTelemetry, trace correlation, semantic conventions |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
