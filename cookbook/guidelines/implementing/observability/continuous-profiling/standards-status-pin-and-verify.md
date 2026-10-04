
- The **OpenTelemetry Profiles signal entered public Alpha on 2026-03-26**; the OTLP profiles signal is still in **Development/unstable** while traces, metrics, and logs are Stable. Treat profiles wire format and semantic conventions as moving targets — **you MUST** pin the collector/SDK version and re-verify on upgrade.
- OTLP Profiles is an independent standard inspired by `pprof`, with lossless round-trip conversion to/from `pprof`. (FORECAST: production-ready OTLP-Profiles backends are still emerging; **prefer** a profiler whose data you can convert if the backend changes.)

