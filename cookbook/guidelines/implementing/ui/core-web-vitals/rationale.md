
INP captures the worst (near-worst) interaction latency across the page's lifetime, so a single janky handler fails it. Mitigations, in order of leverage:

1. `should-break-up-long-tasks`
2. `should-yield-to-main-thread` (with `should-prefer-scheduler-yield` and `should-provide-yield-fallback`)
3. `should-move-heavy-computation-to-web-worker`
4. `must-avoid-layout-thrashing`
5. `should-keep-dom-small`
6. `should-defer-non-critical-work`
