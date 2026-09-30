<!-- leaf: plan-feature-management/feature-flags · source: guidelines/planning/feature-management/feature-flags.md -->

**Rules** (cite as `plan-feature-management/feature-flags#<slug>`):

- `from-start-features-gated-behind-flags-from` MUST — Plan for feature flag architecture from the start. All features MUST be gated behind flags from initial implementation.
- `flag-inventory` SHOULD — each feature spec SHOULD list its flag keys in a Feature Flags section. Plan the flag naming convention upfront (e.g., …

# Feature flags

Plan for feature flag architecture from the start. All features MUST be gated behind flags from initial implementation.

## Architecture decisions

1. **Interface first** — define a `FeatureFlagProvider` interface (`isEnabled(key) -> Bool`) early. This is a dependency injection boundary — the provider can be swapped without touching feature code.
2. **Local default** — start with a local storage backend (UserDefaults, SharedPreferences, localStorage, JSON config). Plan for a remote backend (LaunchDarkly, Firebase Remote Config, Azure App Configuration) as a later swap via DI.
3. **Flag inventory** — each feature spec SHOULD list its flag keys in a **Feature Flags** section. Plan the flag naming convention upfront (e.g., `feature.auth.biometric`, `feature.editor.markdown`).

## What to gate

- All new user-visible features (default: off in production)
- Major refactors that change behavior (gradual rollout)
- Integrations with external services (kill switch)
- NOT: bug fixes, internal refactors, or non-behavioral changes
