
- `must-instrument-significant-actions-via-provider`: every significant user action calls `track(event, properties)` on an `AnalyticsProvider` interface
- `must-not-couple-to-analytics-backend`: no code outside a provider implementation references an analytics backend
- `should-provide-logging-only-default`: a logging-only implementation of the provider is the default, or the code says why not
- `should-define-events-in-spec`: each spec defines its events in an **Analytics** section, or says why not
- `should-keep-abstraction-same-shape-across-platforms`: on every platform the analytics abstraction is an interface/protocol plus a logging default, or the code says why not
