
# Analytics

All significant user actions MUST be instrumented via an `AnalyticsProvider` interface (`track(event, properties)`), with no direct coupling to any analytics backend.
