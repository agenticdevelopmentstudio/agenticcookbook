
# Analytics

All significant user actions MUST be instrumented via an `AnalyticsProvider` interface (`track(event, properties)`). No direct coupling to any analytics backend. Provide a logging-only default; swap in a backend (Mixpanel, Amplitude, PostHog) later.

Each spec SHOULD define events in an **Analytics** section.

---

# Analytics

All significant user actions MUST be instrumented via an `AnalyticsProvider` interface (`track(event, properties)`). No direct coupling to any analytics backend. Provide a logging-only default; swap in a backend (Mixpanel, Amplitude, PostHog) later. Each spec SHOULD define events in an **Analytics** section.

