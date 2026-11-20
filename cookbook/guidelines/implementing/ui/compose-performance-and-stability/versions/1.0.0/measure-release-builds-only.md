
- Profile **release** builds with R8 enabled and a **Baseline Profile** applied. Debug builds run unoptimized Compose and produce misleading numbers — never tune against them.
- Use **Layout Inspector** recomposition counts to find composables recomposing more than expected; a high count signals an unstable parameter or an un-deferred read. The Compose compiler can also emit stability metrics/reports to identify unstable parameters.
- For regression gates, use Macrobenchmark (frame timing, `recompositionCount`) on representative journeys. Optimize a hotspot **only** after a measurement justifies it (per make-it-work-make-it-right-make-it-fast); do not pre-optimize composables that are not hot.

