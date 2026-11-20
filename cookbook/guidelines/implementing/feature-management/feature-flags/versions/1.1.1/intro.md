
# Feature flags

Read flags through a provider interface injected via DI, with a local default implementation on each platform and a backend swapped in later. Give every flag an in-code default that keeps the existing behaviour, keep evaluation from failing the app, and treat each flag as inventory: given a type and a lifetime, named once, tested on and off, and removed when its job is done.

Plan for feature flag architecture from the start. All features MUST be gated behind flags from initial implementation.

Before shipping, verify that all new features are properly gated behind feature flags and that flag configuration is correct.
