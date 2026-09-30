# review-observability — leaves

- [`implement-observability/analytics`](../implement-observability/leaves/analytics.md) — Analytics · All significant user actions MUST be instrumented via an `AnalyticsProvider` interface (`track(event, properties)`). ... · platforms: csharp, kotlin, swift, typescript · triggers: logging, ui-implementation · rules: 2 MUST 1 SHOULD
- [`review-observability/logging`](leaves/logging.md) — Instrumented logging · Every component and flow must be instrumented with structured logging using the platform's best-in-class framework: · platforms: csharp, kotlin, python, swift, typescript, web, windows · triggers: error-handling, logging, new-module · rules: 2 MUST 4 SHOULD
