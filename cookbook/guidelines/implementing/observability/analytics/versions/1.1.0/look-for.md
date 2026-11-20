
- `must-instrument-significant-actions-via-provider`: a significant user action with no `track(event, properties)` call through the `AnalyticsProvider` interface
- `must-not-couple-to-analytics-backend`: an import of, or call into, an analytics backend SDK (Mixpanel, Amplitude, PostHog) outside the provider's implementation
- `should-provide-logging-only-default`: no logging-only default implementation of the provider (`os.log`, `Timber`, `console` or `ILogger`), or a backend wired in as the only implementation
- `should-define-events-in-spec`: a spec with tracked events and no **Analytics** section defining them
