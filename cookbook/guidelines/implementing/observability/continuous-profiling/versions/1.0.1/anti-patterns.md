
- **You MUST NOT** treat continuous profiling as a substitute for RED/USE metrics or distributed tracing — it complements them; start there.
- **You MUST NOT** ship a profiler whose overhead you have not measured, especially on latency-critical services.
- **You SHOULD NOT** store full-resolution profiles indefinitely; cost grows fast with no marginal diagnostic value.

