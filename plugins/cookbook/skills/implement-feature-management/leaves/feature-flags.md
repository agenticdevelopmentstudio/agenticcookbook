<!-- leaf: implement-feature-management/feature-flags · source: guidelines/implementing/feature-management/feature-flags.md -->

**Rules** (cite as `implement-feature-management/feature-flags#<slug>`):

- `features-gated-behind-feature-flags` MUST — All features MUST be gated behind feature flags from initial implementation. Define a FeatureFlagProvider interface …
- `spec-list-flag-keys-feature` SHOULD — Each spec SHOULD list flag keys in a Feature Flags section.
- `features-gated-behind-feature-flags-2` MUST — All features MUST be gated behind feature flags from initial implementation. Define a FeatureFlagProvider interface …

# Feature flags

All features MUST be gated behind feature flags from initial implementation. Define a `FeatureFlagProvider` interface (`isEnabled(key) -> Bool`), provide a local default implementation (UserDefaults/SharedPreferences/localStorage), swap in a backend implementation later via DI.

Each spec SHOULD list flag keys in a **Feature Flags** section.

---

# Feature Flags

All features MUST be gated behind feature flags from initial implementation. Define a `FeatureFlagProvider` interface (`isEnabled(key) -> Bool`), provide a local default implementation, and swap in a backend implementation later via dependency injection. Each spec SHOULD list flag keys in a **Feature Flags** section.

## Swift

Protocol + `UserDefaults`-backed implementation as the default.

## Kotlin

Interface + `SharedPreferences`-backed implementation as the default.

## TypeScript

TypeScript interface + `localStorage`-backed implementation as the default.

## C#

`IFeatureManager` interface + local JSON config as the default. Use the `Microsoft.FeatureManagement` NuGet package. Swap in Azure App Configuration for server-side flag evaluation later.
