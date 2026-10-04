---
id: 85d90939-4047-4b69-a76c-716de9fd5d38
title: "Instrumented logging"
domain: agenticdevelopercookbook://guidelines/reviewing/observability/logging
type: guideline
version: 1.1.1
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
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
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

Logs SHOULD be emitted through [OpenTelemetry](agenticdevelopercookbook://guidelines/implementing/observability/distributed-tracing) and exported over OTLP, the de-facto cross-vendor standard for telemetry. Prefer this over per-platform-only logging frameworks so logs, traces, and metrics share one pipeline and one backend.

- Every log line SHOULD carry the active trace ID and span ID (a trace/correlation ID), so a log can be pivoted to its trace and vice versa. OpenTelemetry-aware logging integrations inject these automatically when a span is in scope.
- Field names SHOULD follow OpenTelemetry semantic conventions (e.g. `service.name`, `trace_id`, `http.request.method`) rather than ad-hoc keys, so telemetry is portable across backends.
- Production logs SHOULD be emitted as structured JSON, not free-form text, to keep them machine-parseable and aggregable.

The per-platform frameworks above remain the local emission layer; route their output through an OpenTelemetry appender/bridge rather than replacing them. PII guidance still applies — never log personally identifiable information at any level, including trace-correlated logs.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Add OpenTelemetry, trace correlation, semantic conventions |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
