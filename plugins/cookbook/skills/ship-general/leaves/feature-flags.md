<!-- leaf: ship-general/feature-flags · source: guidelines/shipping/feature-flags.md -->

**Rules** (cite as `ship-general/feature-flags#<slug>`):

- `defaults-are-correct` SHOULD — new features SHOULD default to false (disabled) in production. Verify the default value in the FeatureFlagProvider …
- `flag-keys-are-documented` SHOULD — each feature spec SHOULD list its flag keys in a Feature Flags section. Verify the keys match between the spec and the …
- `no-flag-leaks` MUST — features behind a disabled flag MUST NOT be visible in the UI, accessible via deep links, or discoverable through the …

# Feature flags

Before shipping, verify that all new features are properly gated behind feature flags and that flag configuration is correct.

## Pre-ship verification checklist

1. **Every new feature is gated** — no new user-visible behavior should ship without a feature flag. Verify by searching for UI or behavior changes that lack a flag check.
2. **Defaults are correct** — new features SHOULD default to `false` (disabled) in production. Verify the default value in the `FeatureFlagProvider` implementation.
3. **Flag keys are documented** — each feature spec SHOULD list its flag keys in a **Feature Flags** section. Verify the keys match between the spec and the code.
4. **Kill switch works** — for critical features, verify the flag can be toggled off remotely (or via local config) without a code deploy.
5. **No flag leaks** — features behind a disabled flag MUST NOT be visible in the UI, accessible via deep links, or discoverable through the API.
