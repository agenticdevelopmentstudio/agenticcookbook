
- `must-instrument-significant-actions-via-provider`: whether every significant user action is instrumented through the `AnalyticsProvider` interface
- `must-not-couple-to-analytics-backend`: whether any code couples directly to an analytics backend
- `should-provide-logging-only-default`: whether a logging-only default implementation of the provider exists
- `should-define-events-in-spec`: whether each spec defines its events in an **Analytics** section
- `must-not-couple-to-analytics-backend`: no direct imports of or calls to Mixpanel/Amplitude/PostHog (or any analytics SDK) appear in business or UI logic;
- `should-provide-logging-only-default`: a logging-only default implementation is present and backed by the platform-idiomatic logger (`os.log` on Swift, `Timber` on Kotlin, `console` on TypeScript, `ILogger` on C#);
- `should-keep-abstraction-same-shape-across-platforms`, `must-not-couple-to-analytics-backend`: the analytics abstraction is interface/protocol-based on every platform with no hard vendor coupling;
