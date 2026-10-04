
Per YAGNI and make-it-work-make-it-right-make-it-fast, **you MUST NOT** add a continuous-profiling pipeline by default. **Adopt it ONLY when** a concrete, measured need justifies the added pipeline, storage, and operational cost:

- A recurring or hard-to-reproduce production CPU/memory/allocation regression that metrics and traces localize to a service but not to a function or line.
- A cloud-cost or efficiency mandate where shaving CPU/memory directly reduces spend.
- Latency outliers whose hot path is not visible from span timings alone.

If a one-off `pprof`/perf capture or a load-test profile answers the question, **prefer that** over standing infrastructure (small-reversible-decisions).

