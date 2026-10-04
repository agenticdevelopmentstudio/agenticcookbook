
- **You MUST** choose a low-overhead, sampling profiler. eBPF whole-system profilers and runtime samplers commonly report well under 1% CPU overhead; **you MUST** validate overhead in your own environment rather than trusting a single vendor's published figure.
- **You SHOULD** prefer whole-system eBPF profiling on Linux (no per-app instrumentation; supports mixed runtimes) when targets are diverse, and **MAY** use in-runtime profilers (Go `runtime/pprof`, JFR, async-profiler, .NET `dotnet-trace`) when you need language-level detail.
- **You SHOULD** emit profiles in a `pprof`-compatible or OTLP-Profiles-convertible format so data is portable across backends (explicit-over-implicit).
- **You MUST** attach resource attributes (`service.name`, `service.version`, deployment, region) so profiles join the rest of your telemetry.
- **You SHOULD** correlate profiles with traces by recording `trace_id`/`span_id` on profile samples where the profiler and runtime support it; this lets you jump from a slow span to the code that ran inside it. (FORECAST: automatic span-level correlation is uneven across profilers/runtimes as of 2026 — verify support per language before relying on it.)
- **You SHOULD** retain profiles at a shorter window than metrics/logs (volume is high) and downsample or aggregate older data.

