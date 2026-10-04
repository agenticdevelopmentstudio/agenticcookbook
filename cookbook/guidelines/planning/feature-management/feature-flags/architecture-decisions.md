
1. **Interface first** — define a `FeatureFlagProvider` interface (`isEnabled(key) -> Bool`) early. This is a dependency injection boundary — the provider can be swapped without touching feature code.
2. **Local default** — start with a local storage backend (UserDefaults, SharedPreferences, localStorage, JSON config). Plan for a remote backend (LaunchDarkly, Firebase Remote Config, Azure App Configuration) as a later swap via DI.
3. **Flag inventory** — each feature spec SHOULD list its flag keys in a **Feature Flags** section. Plan the flag naming convention upfront (e.g., `feature.auth.biometric`, `feature.editor.markdown`).

