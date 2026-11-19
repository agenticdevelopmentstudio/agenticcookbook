
# Feature flags

All features MUST be gated behind feature flags from initial implementation. Define a `FeatureFlagProvider` interface (`isEnabled(key) -> Bool`), provide a local default implementation (UserDefaults/SharedPreferences/localStorage), swap in a backend implementation later via DI.

Each spec SHOULD list flag keys in a **Feature Flags** section.
