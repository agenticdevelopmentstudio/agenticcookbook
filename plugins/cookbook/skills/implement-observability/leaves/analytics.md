<!-- leaf: implement-observability/analytics · source: guidelines/implementing/observability/analytics.md -->

**Rules** (cite as `implement-observability/analytics#<slug>`):

- `significant-user-actions-instrumented-via-analyticsprovider-interface` MUST — All significant user actions MUST be instrumented via an AnalyticsProvider interface (track(event, properties)). No …
- `spec-define-events-analytics-section` SHOULD — Each spec SHOULD define events in an Analytics section.
- `significant-user-actions-instrumented-via-analyticsprovider-interface-2` MUST — All significant user actions MUST be instrumented via an AnalyticsProvider interface (track(event, properties)). No …

# Analytics

All significant user actions MUST be instrumented via an `AnalyticsProvider` interface (`track(event, properties)`). No direct coupling to any analytics backend. Provide a logging-only default; swap in a backend (Mixpanel, Amplitude, PostHog) later.

Each spec SHOULD define events in an **Analytics** section.

---

# Analytics

All significant user actions MUST be instrumented via an `AnalyticsProvider` interface (`track(event, properties)`). No direct coupling to any analytics backend. Provide a logging-only default; swap in a backend (Mixpanel, Amplitude, PostHog) later. Each spec SHOULD define events in an **Analytics** section.

## Swift

Protocol + `os.log`-backed implementation as the default.

## Kotlin

Interface + `Timber`-backed implementation as the default.

## TypeScript

TypeScript interface + `console`-backed implementation as the default.

## C#

Interface + `ILogger`-backed implementation as the default. Same pattern as other platforms: no direct coupling to any analytics backend.
