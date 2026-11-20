
- **must-instrument-significant-actions-via-provider**: All significant user actions MUST be instrumented via an `AnalyticsProvider` interface (`track(event, properties)`).
- **must-not-couple-to-analytics-backend**: There MUST NOT be direct coupling to any analytics backend.
- **should-provide-logging-only-default**: SHOULD provide a logging-only default, and swap in a backend (Mixpanel, Amplitude, PostHog) later.
- **should-define-events-in-spec**: Each spec SHOULD define events in an **Analytics** section.
- **should-keep-abstraction-same-shape-across-platforms**: The analytics abstraction SHOULD be the same shape across platforms: an interface/protocol plus a logging default.
