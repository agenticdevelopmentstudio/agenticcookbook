
- `must-instrument-significant-actions-via-provider`: a significant user action with no `track(event, properties)` call through the `AnalyticsProvider` interface
- `must-not-couple-to-analytics-backend`: an import of, or call into, an analytics backend SDK (Mixpanel, Amplitude, PostHog) outside the provider's implementation
- `should-provide-logging-only-default`: no logging-only default implementation of the provider (`os.log`, `Timber`, `console` or `ILogger`), or a backend wired in as the only implementation
- `should-define-events-in-spec`: a spec with tracked events and no **Analytics** section defining them
- `must-instrument-significant-actions-via-provider`: Every significant user action goes through an `AnalyticsProvider` interface exposing `track(event, properties)`, not a call wired straight to a concrete vendor;
- `must-not-couple-to-analytics-backend`: flag any direct coupling to an analytics backend (Mixpanel, Amplitude, PostHog and the like) in business or UI code;
- `should-provide-logging-only-default`: a logging-only default implementation must exist so analytics works before any backend is swapped in, and that default is the platform-idiomatic logger — `os.log` behind a protocol on Swift, a `Timber`-backed implementation behind an interface on Kotlin, a `console`-backed implementation behind a TypeScript interface, an `ILogger`-backed implementation behind an interface on C# — never a hard dependency on the vendor SDK;
- `should-keep-abstraction-same-shape-across-platforms`: the abstraction is the same shape across platforms (interface/protocol plus a logging default);

