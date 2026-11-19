---
id: ac616d81-16c2-4f33-9ae4-139d5c24318d
title: "Feature flags"
type: guideline
version: 1.0.4
status: accepted
language: en
created: 2026-03-27
modified: 2026-11-07
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Read flags through an injected FeatureFlagProvider with a local default; every evaluation takes a default and never throws; flags are typed, tested and removed."
platforms:
  - csharp
  - kotlin
  - swift
  - typescript
tags:
  - feature-flags
  - feature-management
depends-on: []
related:
  - d991b992-07aa-47b9-9d36-4fd1ca81435f
  - e446ee3e-b8f2-40e7-b93d-3113e6a95e5d
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - feature-flags
  - new-module
---

# Feature flags

Read every flag through an injected `FeatureFlagProvider` interface with a local default implementation, so a backend can be swapped in later without touching call sites. Every evaluation takes an in-code default, returns it instead of throwing, and leaves the existing behaviour in place (or, for a security- or compliance-sensitive flag, the restrictive one) when the flag is off or the flag service is gone. A flag is inventory: give it a type, a lifetime and a unique name, test both of its states, never let it bring in downloaded code that changes the app, and remove it when its rollout is done.

## Rules

- **gate-all-features**: All features MUST be gated behind feature flags from initial implementation. (claim: gate-all-features-prior)
- **flag-only-when-needed**: A change SHOULD get a flag only when it cannot ship safely as smaller increments or needs a runtime switch (an experiment, an operational toggle or a permission); a release flag SHOULD be the last choice, not the default, and the count of live flags SHOULD be kept low. (claims: not-every-change-needs-a-flag, toggles-are-inventory)
- **feature-flag-provider-interface**: Code MUST read flags through a `FeatureFlagProvider` interface supplied by dependency injection, never by calling a vendor SDK or a storage API at the call site (in C#, `FeatureGateAttribute` aside, per `csharp-feature-gate`). (claims: openfeature-provider-abstraction, decouple-decision-point-from-logic)
- **ship-a-local-default-provider**: The app MUST ship a local default implementation of the `FeatureFlagProvider` interface, which it runs with when no backend is registered. (claims: openfeature-noop-provider, ms-json-to-app-configuration)
- **backend-provider-is-swappable**: A backend implementation of the `FeatureFlagProvider` interface (a vendor SDK, an OpenFeature provider or Azure App Configuration) MUST be swappable in for the local default without changing call sites. (claims: openfeature-provider-abstraction, ms-json-to-app-configuration)
- **evaluation-takes-a-default-and-never-throws**: Every flag evaluation MUST take a default value at the call site and MUST NOT throw: when the provider is not ready, the flag service is unreachable, the key is missing or evaluation fails, it MUST return that default, and it SHOULD report the error (an error code or a log entry). (claims: openfeature-default-required-no-throw, vendor-sdks-default-on-error, default-at-every-evaluation)
- **fail-at-setup-not-at-evaluation**: A flag failure MAY stop the app only at setup, when the provider is registered or configured; a missing or unreadable flag at evaluation MUST NOT stop it, and flags SHOULD NOT be loaded through the fail-fast path that deploy configuration uses. (claims: setup-may-fail-evaluation-may-not, flags-are-not-config)
- **fail-fast-on-missing-config**: The app MUST do this: Read every value that varies per deploy from the environment, coerce all required config into a typed object once at startup, and halt on a missing or malformed value rather than falling back to a silent default (fail-fast). (claim: fail-fast-on-missing-config-prior)
- **typed-flag-evaluation**: The provider interface SHOULD evaluate typed values (boolean, number, string and structured object), each with a default of the same type, rather than booleans only. (claims: openfeature-typed-evaluation, openfeature-vendor-agnostic)
- **off-means-existing-behaviour**: A flag's off state and its default SHOULD be the existing, known-working behaviour, with on as the new behaviour; a flag guarding a security- or compliance-sensitive path SHOULD default to the more restrictive behaviour instead. (claims: off-is-existing-behaviour, restrictive-fallback-for-security)
- **no-dependency-on-flag-service**: The app MUST keep working when the flag service is unavailable, using the in-code defaults; it SHOULD serve the last-known values from a local cache first. (claims: no-dependency-on-flag-service, sdks-cache-in-local-storage, openfeature-default-required-no-throw, default-at-every-evaluation)
- **flag-has-a-type-and-lifetime**: Each flag SHOULD be declared with its type (release, experiment, operational, or permission/kill switch) and that type's expected lifetime, temporary or permanent, and be managed by it; a flag that outlives its expected lifetime SHOULD be reported as stale. (claims: categories-managed-differently, flag-types-and-lifetimes, stale-flag-detection)
- **plan-flag-removal-at-creation**: A temporary flag SHOULD have its removal planned when it is created: an expiry date, a backlog item or a removal pull request. (claim: removal-planned-at-creation)
- **remove-flags-when-done**: Once a temporary flag's rollout is complete, the flag and its losing code path SHOULD be removed from the code. (claims: flags-short-lived-removed, toggles-are-inventory)
- **remove-code-before-archive**: A flag MUST be removed from the code before it is archived or retired in the flag service. (claims: remove-code-before-archive, vendor-sdks-default-on-error, openfeature-default-required-no-throw)
- **review-live-flags-regularly**: The team SHOULD review its live flags on a regular cadence, such as each sprint. (claim: regular-flag-review)
- **unique-never-reused-flag-names**: A flag's name MUST be unique across the system and MUST NOT be reused for new behaviour once its flag is retired; each flag SHOULD follow a shared naming convention and carry a description. (claims: naming-and-descriptions, never-repurpose-a-flag)
- **test-both-flag-states**: Tests MUST cover each flag's on and off states, and MUST keep covering a long-lived flag's off path while it can still be switched; rather than every combination of flags, the suite SHOULD test the configuration going live and the fallback with the new flags off. (claims: test-both-states, test-the-release-combinations)
- **decouple-toggle-points**: Business logic SHOULD receive the flag's decision (an injected value or strategy) rather than query the flag system itself, and a long-lived or multi-point toggle SHOULD select its code path through a strategy, not scattered conditionals. (claims: decouple-decision-point-from-logic, strategy-over-conditionals)
- **flags-never-hide-features-from-review**: In an app submitted to Apple's App Review, a flag MUST NOT hide a feature or leave it dormant or undocumented (guideline 2.5.19), and every new feature MUST be accessible for review and described in the Notes for Review (guideline 2.3.1(a)). (claims: apple-no-hidden-features, apple-features-accessible-for-review)
- **flags-switch-only-shipped-code**: In an app distributed through the App Store or Google Play, a flag MUST NOT download, install or execute code that introduces or changes the app's features, and SHOULD switch only between code already in the reviewed binary. (claim: store-no-downloaded-code)
- **swift-userdefaults-default**: In Swift, the local default SHOULD be a protocol with a `UserDefaults`-backed implementation. (claims: apple-userdefaults-for-config, apple-userdefaults-not-sensitive)
- **kotlin-sharedpreferences-default**: In Kotlin, the local default SHOULD be: Interface + `SharedPreferences`-backed implementation as the default. (claim: kotlin-sharedpreferences-default-prior)
- **kotlin-datastore-default**: In Kotlin, new local flag storage SHOULD use Jetpack DataStore, in a DataStore file of its own for flags, rather than `SharedPreferences`. (claims: android-sharedpreferences-not-for-new, android-datastore-holds-feature-flags)
- **typescript-localstorage-default**: In TypeScript, the local default SHOULD be an interface with a `localStorage`-backed implementation, which MUST store values as strings, parse them on read, and return the defaults when `localStorage` is unavailable or throws. (claims: sdks-cache-in-local-storage, web-localstorage-semantics, openfeature-default-required-no-throw)
- **csharp-feature-management**: In C#, the `FeatureFlagProvider` interface (`IFeatureFlagProvider`) SHOULD be implemented over `IFeatureManager` (or `IVariantFeatureManager` for variants) from the `Microsoft.FeatureManagement` NuGet package, registered through dependency injection, reading local JSON configuration (`appsettings.json`) by default, with Azure App Configuration swapped in later for server-side flags. (claims: ms-featuremanager-interface, ms-json-to-app-configuration)
- **csharp-missing-flag-returns-default**: Because `IsEnabledAsync` takes no default, and ignores a missing flag rather than throwing unless `IgnoreMissingFeatures` is turned off, the C# provider SHOULD keep missing flags ignored and return the call site's default for a flag that is not configured. (claims: ms-featuremanager-interface, setup-may-fail-evaluation-may-not)
- **csharp-feature-gate**: ASP.NET Core MAY gate whole controllers, actions and Razor pages with `FeatureGateAttribute`, the one place a C# flag is read outside the provider. (claim: ms-feature-gate)
- **local-flag-store-is-untrusted**: A flag value stored or overridden on the client MUST NOT be the only gate on a security, payment or entitlement decision, because the user can change it. (claims: client-side-override-risk, apple-userdefaults-not-sensitive, web-localstorage-semantics)
- **no-secrets-in-userdefaults**: A `UserDefaults` store that holds flags MUST NOT hold secrets or personal data. (claim: apple-userdefaults-not-sensitive)
- **no-secrets-in-client-flag-store**: A client-side flag store other than `UserDefaults` (a DataStore file, `localStorage` or the like) SHOULD NOT hold secrets or personal data. (claims: android-datastore-holds-feature-flags, client-side-override-risk)
- **no-personal-data-in-flag-service**: Flag contexts sent to a flag service, and server-side flag stores, SHOULD NOT carry personal data. (claim: client-side-override-risk)
- **no-mid-session-ui-flip**: A flag that changes visible UI SHOULD NOT switch it while the user is using it; newly fetched values SHOULD take effect at the next app start or another natural boundary. (claim: firebase-activate-next-start)
- **monitor-flag-rollout**: While a flag widens exposure, the team SHOULD watch usage and system-health metrics for the flagged path. (claim: monitor-flag-rollout)
- **prefer-static-flag-configuration**: Flag configuration SHOULD be static and source-controlled, with dynamic, runtime-changed configuration used only for the flags that need it, such as operational toggles. (claim: static-config-preferred)
- **prefer-a-standard-flag-api**: A project SHOULD put a standard flag API (OpenFeature) or an existing flag platform behind the provider interface rather than build its own flag service. (claims: openfeature-vendor-agnostic, build-vs-buy)
- **spec-lists-flag-keys**: Each spec SHOULD list flag keys in a **Feature Flags** section. (claim: spec-lists-flag-keys-prior)

## How to keep the rules

- Before adding a flag, ask whether the change can ship dark as smaller safe increments; reach for a flag only when it cannot, or when the switch itself is the feature (an experiment, a kill switch, an entitlement).
- Shape the provider interface on OpenFeature's evaluation API: one typed method per value type, each taking a key and a default. Make the local default the provider the app runs with when nothing else is registered, and let tests reset to it.
- Choose each flag's default as the code path that runs today. Write the default once, at the call site, not in a lookup table far from it.
- Put setup failures where they belong: an invalid provider configuration may halt startup; a flag that is missing, mistyped or unreachable at runtime returns its default and logs.
- Keep flags out of the typed deploy-configuration object. That object fails fast; flags never do.
- With the flag service unreachable, run on the in-code defaults. Better still, cache the last-known flag values locally, read the cache on launch before the network, and fall back to the in-code defaults when the cache is empty.
- Record for every flag its name, type, description and expected lifetime, and for every temporary flag its removal plan. Let tooling report flags that outlive their lifetime.
- To retire a flag: remove the call sites and the losing path from code, ship that, then archive the flag in the flag service. Retire the name with it.
- Review the live flags on a regular cadence, such as each sprint, and keep their count low: retire before adding.
- Test each new flag twice (on and off), and run the release configuration plus the all-new-flags-off fallback in CI; skip the exhaustive combination matrix.
- Pass the decision into business logic: the composition root reads the flag and injects a strategy, so the feature code never imports the flag provider.
- For Apple review, ship the build with every new feature reachable by the reviewer and described in the Notes for Review; do not use a flag to keep a feature dark through review.
- Apply fetched values on the next launch, or at a screen boundary, never under the user's finger.
- Treat a client-side override (a `UserDefaults`, DataStore or `localStorage` value, a query parameter or a cookie) as input the user controls; check entitlements on the server.

## Examples

Swift, a typed provider with call-site defaults and a `UserDefaults` local default:

```swift
protocol FeatureFlagProvider {
    func bool(_ key: String, default value: Bool) -> Bool
    func string(_ key: String, default value: String) -> String
}

struct UserDefaultsFlagProvider: FeatureFlagProvider {
    let defaults: UserDefaults
    let log = Logger(subsystem: "{{bundle_id}}", category: "FeatureFlags")

    func bool(_ key: String, default value: Bool) -> Bool {
        read(key, default: value)
    }

    func string(_ key: String, default value: String) -> String {
        read(key, default: value)
    }

    private func read<T>(_ key: String, default value: T) -> T {
        guard let raw = defaults.object(forKey: "{{app_prefix}}.\(key)") else { return value }
        if let typed = raw as? T { return typed }
        log.warning("Flag \(key) is not a \(String(describing: T.self)); using default \(String(describing: value))")
        return value
    }
}
```

Kotlin, flags in their own Preferences DataStore file:

```kotlin
interface FeatureFlagProvider {
    suspend fun bool(key: String, default: Boolean): Boolean
}

private val Context.flagStore by preferencesDataStore(name = "feature_flags")

class DataStoreFlagProvider(private val context: Context) : FeatureFlagProvider {
    override suspend fun bool(key: String, default: Boolean): Boolean =
        try {
            // Preferences.get casts unchecked, so read the raw value and check its type
            val raw = context.flagStore.data.first().asMap()[booleanPreferencesKey(key)]
            (raw as? Boolean) ?: default.also {
                if (raw != null) Log.w("FeatureFlags", "Flag $key is not a Boolean; using default $default")
            }
        } catch (e: CancellationException) {
            throw e // never swallow coroutine cancellation
        } catch (e: Exception) { // IOException (DataStore's documented read failure) or anything else
            Log.w("FeatureFlags", "Flag $key unreadable; using default $default", e)
            default
        }
}
```

TypeScript, a `localStorage` default that never throws:

```typescript
export interface FeatureFlagProvider {
  bool(key: string, defaultValue: boolean): boolean;
}

export class LocalStorageFlagProvider implements FeatureFlagProvider {
  bool(key: string, defaultValue: boolean): boolean {
    try {
      const raw = window.localStorage.getItem(`{{app_prefix}}.${key}`);
      if (raw === "true") return true;
      if (raw === "false") return false;
      if (raw !== null) console.warn(`Flag ${key} malformed; using default ${defaultValue}`);
      return defaultValue;
    } catch (error) {
      // storage blocked (SecurityError): report it, then use the default
      console.warn(`Flag ${key} unreadable; using default ${defaultValue}`, error);
      return defaultValue;
    }
  }
}
```

C#, an `IFeatureFlagProvider` over `Microsoft.FeatureManagement` from `appsettings.json`, with call-site defaults and a gated controller:

```csharp
public interface IFeatureFlagProvider
{
    Task<bool> BoolAsync(string key, bool defaultValue);
}

public sealed class FeatureManagerFlagProvider(IFeatureManager features, ILogger<FeatureManagerFlagProvider> log)
    : IFeatureFlagProvider
{
    public async Task<bool> BoolAsync(string key, bool defaultValue)
    {
        try
        {
            // IsEnabledAsync takes no default: a flag that is not configured returns the caller's.
            await foreach (var name in features.GetFeatureNamesAsync())
                if (string.Equals(name, key, StringComparison.OrdinalIgnoreCase)) return await features.IsEnabledAsync(key);
            return defaultValue;
        }
        catch (Exception e)
        {
            log.LogWarning(e, "Flag {Key} failed; using default {Default}", key, defaultValue);
            return defaultValue;
        }
    }
}

builder.Services.AddFeatureManagement();
builder.Services.AddSingleton<IFeatureFlagProvider, FeatureManagerFlagProvider>();

[FeatureGate("NewCheckout")]
public class CheckoutV2Controller : Controller { /* ... */ }

public class CheckoutService(IFeatureFlagProvider flags)
{
    public async Task<ICheckoutFlow> FlowAsync() =>
        await flags.BoolAsync("NewCheckout", defaultValue: false) ? new CheckoutV2() : new CheckoutV1();
}
```

```json
{ "feature_management": { "feature_flags": [ { "id": "NewCheckout", "enabled": false } ] } }
```

Decoupled toggle point: the composition root decides, the feature takes a strategy:

```kotlin
suspend fun buildCart(flags: FeatureFlagProvider): Cart {
    val pricing: PricingStrategy =
        if (flags.bool("new-pricing", default = false)) TieredPricing() else FlatPricing()
    return Cart(pricing) // Cart never sees the flag
}
```

## What a reviewer looks for

- A change that adds a feature without a flag, against `gate-all-features`; and a flag added where the change could have shipped as smaller increments, against `flag-only-when-needed`
- Call sites that read a vendor SDK, `UserDefaults`, `SharedPreferences`, DataStore or `localStorage` directly instead of the injected provider (a C# `FeatureGateAttribute` aside)
- A provider interface with no local default implementation, or call sites that would change if a backend provider replaced the local one
- An evaluation with no call-site default, or one that can throw, crash or block on a missing key, an unready provider or an unreachable service
- An evaluation that returns its default on a failure without reporting the error (error code or log), with no reason given
- Flags loaded through the deploy-configuration path with no reason given, so a missing flag halts startup, or deploy configuration that falls back to a silent default instead of halting
- A provider interface that offers only booleans where the code needs a number, string or structured value
- A default that turns on the new path, or a security- or compliance-sensitive flag whose fallback is the permissive behaviour
- Startup or rendering that depends on the flag service being reachable, with no in-code defaults to fall back on; or no local cache of last-known values, with no reason given
- A new flag with no recorded type, lifetime or description
- Flags with no way to report the ones that have outlived their expected lifetime as stale
- A new temporary flag with no removal plan (expiry date, backlog item or removal pull request)
- A finished rollout whose flag and losing code path are still in the code
- A flag archived in the flag service while code still reads it
- No regular review of live flags, or a live-flag count that only grows
- A flag name that duplicates an existing name or reuses a retired one
- Tests that cover only one state of a flag, or a long-lived flag whose off path has no tests
- Business logic that queries the flag system directly, or the same flag checked in scattered `if` statements across modules
- A flag that keeps a feature hidden or dormant through App Review, or a new feature missing from the Notes for Review
- In an App Store or Google Play app, a flag that downloads, installs or executes code that introduces or changes the app's features, or a flagged path that is not in the reviewed binary
- A Swift local default that is not a protocol with a `UserDefaults`-backed implementation, with no reason given
- Kotlin flags stored in `SharedPreferences` (against `kotlin-datastore-default`) or in DataStore (against `kotlin-sharedpreferences-default`)
- Kotlin flags kept in a DataStore file shared with other data instead of a file of their own
- `localStorage` reads that are not wrapped against a throw or that store non-string values
- A C# project that hand-rolls flag reading instead of `Microsoft.FeatureManagement` and DI, with no reason given
- A C# provider that throws on, or turns off, a flag that is not configured instead of returning the call-site default, with no reason given
- A `FeatureGateAttribute` on anything other than a controller, an action or a Razor page
- A client-side flag value that is the only gate on a security, payment or entitlement decision
- Secrets or personal data in `UserDefaults` alongside flags
- Secrets or personal data in any other client-side flag store (a DataStore file, `localStorage`), with no reason given
- Personal data in a flag context or a server-side flag store, with no reason given
- Visible UI that changes in place when newly fetched flag values arrive
- A rollout widening exposure with no usage or health metrics watched
- Dynamic, runtime-changed configuration for a flag that never needs to change at runtime
- A hand-built flag service where a standard API or existing platform would serve
- A spec with flags but no **Feature Flags** section listing their keys

## A complete review must establish

- Every new feature and every new flag in the change was checked against `gate-all-features` and `flag-only-when-needed`, and each conflict between the two was reported for the owner
- Every flag read in the change was traced to the injected provider (or, in C#, to a `FeatureGateAttribute`)
- The provider's local default implementation was found, and the call sites were checked for depending on nothing a backend provider would change
- Every evaluation was checked for a call-site default, for a path that can throw, crash or block, and for the error being reported when the default is returned (or a reason given)
- The startup path was checked: a flag failure may stop the app only at provider setup, flags are not loaded through the fail-fast deploy configuration (or the code says why), and deploy configuration halts on a missing or malformed value
- The provider interface was checked for the value types the change needs
- Each flag's default was compared with the existing behaviour, and each security- or compliance-sensitive flag's fallback was checked for the restrictive choice
- The app's behaviour with the flag service unreachable was established, from the in-code defaults and any local cache of last-known values
- Each new flag's type, lifetime, name and description were checked, and its name against existing and retired names, and whether flags that outlive their expected lifetime can be reported as stale
- Each new temporary flag was checked for a removal plan made at its creation
- Every flag whose rollout is complete was checked for removal, with its losing path, from the code
- Every flag archived or retired in the flag service was checked for remaining code references
- The team's review of live flags on a set cadence was established, and the live-flag count was checked for being kept low
- Tests were found for both states of each flag, for each long-lived flag's off path, and for the release configuration and the new-flags-off fallback
- Toggle points were checked for injected decisions or strategies, and for flags checked in scattered conditionals
- For apps on the App Store or Google Play, each flagged path was checked for being in the reviewed binary and for downloaded code that changes features; for apps sent to App Review, each new feature was also checked for being reachable by the reviewer and described in the Notes for Review
- Each platform's local store was checked against its rule (`swift-userdefaults-default`, `kotlin-datastore-default` and `kotlin-sharedpreferences-default`, `typescript-localstorage-default`, `csharp-feature-management`), and each conflict between the two Kotlin rules was reported for the owner
- Each C# provider was checked for returning the call-site default for a flag that is not configured, and each `FeatureGateAttribute` for gating only controllers, actions or Razor pages
- Every client-side flag value was checked for gating security, payment or entitlement alone
- `UserDefaults` holding flags was checked for secrets and personal data
- Every other client-side flag store was checked for secrets and personal data
- Every flag context sent to a flag service, and every server-side flag store, was checked for personal data
- Flags that change visible UI were checked for when fetched values take effect
- Each widening rollout was checked for the metrics watched
- Each flag's configuration was checked for being static where the flag does not need to change at runtime
- The flag implementation was checked for a standard API or existing platform behind the provider
- Each spec touched by the change was checked for a **Feature Flags** section listing its keys
- Each finding names the rule it breaks

## A build must establish

- `gate-all-features`: every feature the build adds is behind a feature flag from its first commit
- `flag-only-when-needed`: each flag the build adds is one the change needs (it cannot ship as smaller safe increments, or it is an experiment, operational toggle or permission), or the code says why it was added; the live-flag count is kept low, or the code says why not
- `feature-flag-provider-interface`: every flag is read through an injected `FeatureFlagProvider`, and no call site names a vendor SDK or storage API, `FeatureGateAttribute` on C# controllers, actions and Razor pages aside
- `ship-a-local-default-provider`: a local default implementation of the provider ships, and the app runs with it when no backend is registered
- `backend-provider-is-swappable`: a backend provider can replace the local default with no call site changed
- `evaluation-takes-a-default-and-never-throws`: every evaluation passes a default, and a missing key, unready provider or unreachable service returns that default without throwing; the error is reported, or the code says why not
- `fail-at-setup-not-at-evaluation`: no flag failure stops the app except at provider setup; no flag is loaded through the fail-fast deploy-configuration path, or the code says why not
- `fail-fast-on-missing-config`: every per-deploy value is read from the environment into a typed object once at startup, and a missing or malformed value halts startup
- `typed-flag-evaluation`: the provider evaluates each value type the code needs, each with a default of that type, or the code says why not
- `off-means-existing-behaviour`: each flag's off state and default are the existing behaviour, and each security- or compliance-sensitive flag falls back to the restrictive behaviour, or the code says why not
- `no-dependency-on-flag-service`: with the flag service unreachable the app keeps working on the in-code defaults; it serves cached last-known values first, or the code says why not
- `flag-has-a-type-and-lifetime`: each new flag records its type and expected lifetime, and stale flags can be reported, or the code says why not
- `plan-flag-removal-at-creation`: each new temporary flag records its removal plan (an expiry date, a backlog item or a removal pull request), or the code says why not
- `remove-flags-when-done`: each flag whose rollout is complete is gone from the code with its losing path, or the code says why not
- `remove-code-before-archive`: no flag archived or retired in the flag service is still read by the code
- `review-live-flags-regularly`: the team reviews its live flags on a set cadence, or the code says why not
- `unique-never-reused-flag-names`: each new flag name is unique and not a retired name; it follows the naming convention and has a description, or the code says why not
- `test-both-flag-states`: tests run each flag on and off, and keep running each long-lived flag's off path; they cover the release configuration and the new-flags-off fallback, or the code says why not
- `decouple-toggle-points`: business logic receives the flag's decision or a strategy and does not query the flag system, and each long-lived or multi-point toggle selects its path through a strategy, not scattered conditionals, or the code says why not
- `flags-never-hide-features-from-review`: in an app submitted to App Review, no flag hides a feature, and every new feature is reachable by the reviewer and listed in the Notes for Review
- `flags-switch-only-shipped-code`: in an app distributed through the App Store or Google Play, no flag downloads, installs or executes code that introduces or changes the app's features, and every flagged path is code in the reviewed binary, or the code says why not
- `swift-userdefaults-default`: the Swift local default is a protocol with a `UserDefaults`-backed implementation, or the code says why not
- `kotlin-sharedpreferences-default`: the Kotlin local default is an interface with a `SharedPreferences`-backed implementation, or the code says why not
- `kotlin-datastore-default`: new Kotlin flag storage uses its own Jetpack DataStore file, or the code says why not
- `typescript-localstorage-default`: the TypeScript local default is `localStorage`-backed, or the code says why not; it stores strings, parses on read and returns the defaults when storage is unavailable or throws
- `csharp-feature-management`: C# flags are read through an `IFeatureFlagProvider` implemented over `IFeatureManager` or `IVariantFeatureManager` registered by DI, reading `appsettings.json` locally, or the code says why not
- `csharp-missing-flag-returns-default`: the C# provider keeps missing flags ignored and returns the call-site default for a flag that is not configured, or the code says why not
- `csharp-feature-gate`: any `FeatureGateAttribute` gates only a controller, an action or a Razor page
- `local-flag-store-is-untrusted`: no client-side flag value alone gates a security, payment or entitlement decision
- `no-secrets-in-userdefaults`: no `UserDefaults` that holds flags holds secrets or personal data
- `no-secrets-in-client-flag-store`: no other client-side flag store (a DataStore file, `localStorage`) holds secrets or personal data, or the code says why not
- `no-personal-data-in-flag-service`: no flag context sent to a flag service, and no server-side flag store, carries personal data, or the code says why not
- `no-mid-session-ui-flip`: newly fetched values that change visible UI take effect at the next start or a natural boundary, or the code says why not
- `monitor-flag-rollout`: each widening rollout names the usage and health metrics watched, or the code says why not
- `prefer-static-flag-configuration`: flag configuration is static and source-controlled except for flags that must change at runtime, or the code says why not
- `prefer-a-standard-flag-api`: the provider wraps OpenFeature or an existing flag platform, or the code says why it does not
- `spec-lists-flag-keys`: each spec for a flagged feature lists its flag keys in a **Feature Flags** section, or the spec says why not

## Rationale

- `gate-all-features`, `flag-only-when-needed`: Kept as written for the owner to decide: Microsoft's DevOps guidance says not every change needs a flag, Fowler calls a release flag the last choice after breaking the feature into safe increments, and both Fowler and LaunchDarkly treat live flags as inventory with a carrying cost. `flag-only-when-needed` states the research's position; the two rules conflict until the owner rules.
- `feature-flag-provider-interface`, `ship-a-local-default-provider`, `backend-provider-is-swappable`: OpenFeature separates the evaluation API from a provider set at startup, which may wrap a vendor SDK or read a local file, and falls back to a no-op provider that returns the caller's default; Microsoft.FeatureManagement reads flags through `IConfiguration` from `appsettings.json` up to Azure App Configuration and registers through DI. The rule's shape is a call-site default on every evaluation (`evaluation-takes-a-default-and-never-throws`) and typed values (`typed-flag-evaluation`), the standard shape the research finds in OpenFeature, so it fixes no boolean-only, default-free signature.
- `evaluation-takes-a-default-and-never-throws`, `no-dependency-on-flag-service`: OpenFeature requires a default and forbids evaluation from throwing, returning the default with an error code; LaunchDarkly, ConfigCat and Flagsmith each return the caller's default on their documented failures (unreachable service, missing key, unexpected error); Firebase, Flagsmith and LaunchDarkly all tell callers to carry an in-code default, and Unleash says the app should not depend on the flag service being available. The MUST that the app keeps working without the flag service rests on OpenFeature's MUST that evaluation returns the default rather than failing: an evaluation that always yields its in-code default leaves nothing that needs the service. LaunchDarkly's client SDKs cache flags locally and read them before the network, vendor practice and so a SHOULD.
- `fail-at-setup-not-at-evaluation`, `fail-fast-on-missing-config`: `fail-fast-on-missing-config` is kept as written for the owner to decide. Applied to deploy configuration it holds; applied to flags it is contradicted, since OpenFeature allows failure at provider registration but never at evaluation, and Unleash says flags are not configuration: configuration is static and loaded at startup, flags change at runtime and favour availability. `fail-at-setup-not-at-evaluation` makes failure at evaluation a MUST NOT, from OpenFeature's MUST; keeping flags off the fail-fast deploy-configuration path rests on Unleash alone ("Avoid using feature flags for static application configuration"), so it is a SHOULD NOT.
- `typed-flag-evaluation`, `prefer-a-standard-flag-api`: OpenFeature, a CNCF specification, evaluates booleans, numbers, strings and structures behind one vendor-agnostic API; Microsoft recommends adopting an existing platform over building one, a single-source SHOULD.
- `off-means-existing-behaviour`: Fowler and LaunchDarkly both make off the known-working path, so an outage or a missing flag falls back to code already in production; LaunchDarkly alone advises the restrictive fallback for security and compliance flags.
- `flag-has-a-type-and-lifetime`, `plan-flag-removal-at-creation`, `remove-flags-when-done`, `remove-code-before-archive`, `review-live-flags-regularly`: Fowler's toggle categories differ in longevity and dynamism; Unleash and LaunchDarkly classify flags as temporary or permanent, and Unleash marks a flag stale once it outlives its expected lifetime. Unleash, LaunchDarkly and Microsoft all remove release flags when rollout completes, and Fowler and LaunchDarkly plan the removal at creation (an expiry date, a removal pull request). LaunchDarkly serves the in-code fallback once a flag is archived, and this is not LaunchDarkly's alone: OpenFeature requires evaluation to return the default on any abnormal execution, and LaunchDarkly, ConfigCat and Flagsmith each return the caller's default when the flag cannot be served, so with any flag service a retired flag that code still reads flips to its in-code default. Code must lose the flag first: a MUST, because archiving first silently flips the behaviour. Microsoft alone advises a regular flag review, such as at the start of each sprint, a single-source SHOULD.
- `unique-never-reused-flag-names`: The SEC's order on Knight Capital records that repurposing an old flag with the dead code still deployed caused a $460 million loss; that order and Unleash's "ensure that all flags ... have unique names across your entire system" make uniqueness and the reuse ban MUSTs, while the shared naming convention and the description are vendor practice and so SHOULDs.
- `test-both-flag-states`: Fowler, Microsoft and LaunchDarkly test both states; Fowler advises testing the live configuration and the all-off fallback rather than every combination.
- `decouple-toggle-points`: Fowler keeps the toggle point apart from the decision logic, and prefers a strategy to scattered conditionals for long-lived toggles.
- `flags-never-hide-features-from-review`, `flags-switch-only-shipped-code`: Apple's guideline 2.5.19 forbids hidden, dormant or undocumented features and 2.3.1(a) requires new features to be accessible for review (the hidden-features rule is 2.5.19, not 2.3.1); Apple 2.5.2 forbids downloading, installing or executing code that introduces or changes features, and Google Play's Device and Network Abuse policy forbids downloading executable code such as dex, JAR or .so files. Google exempts interpreted code such as JavaScript in a webview, so the MUST binds only code that changes the app's features, and staying inside the reviewed binary is a SHOULD. Whether a feature switched off during review counts as hidden is not stated by Apple.
- `swift-userdefaults-default`, `no-secrets-in-userdefaults`: Apple describes `UserDefaults` as the store for nonsensitive configuration, including temporary feature overrides, and notes it is unencrypted on disk.
- `kotlin-sharedpreferences-default`, `kotlin-datastore-default`: `kotlin-sharedpreferences-default` is kept as written for the owner to decide: the Android team strongly recommends against `SharedPreferences` for new storage and points to Jetpack DataStore, whose guide names feature flags as preferences to keep in a DataStore file of their own. The two rules conflict until the owner rules.
- `typescript-localstorage-default`: `localStorage` is per-origin, persists across sessions, holds only strings and throws `SecurityError` when storage is blocked, so the implementation parses and guards every read, returning the call-site default that `evaluation-takes-a-default-and-never-throws` requires; LaunchDarkly's web SDK caches flags there.
- `csharp-feature-management`, `csharp-missing-flag-returns-default`, `csharp-feature-gate`: Microsoft.FeatureManagement still ships `IFeatureManager.IsEnabledAsync`, though its docs now lead with `IVariantFeatureManager`; `IsEnabledAsync` takes only the flag name, and missing flags are ignored by default (`IgnoreMissingFeatures`) but can be set to throw, so the provider over it supplies the call-site default the evaluation rule requires; it reads `appsettings.json` and Azure App Configuration through `IConfiguration`, and `FeatureGateAttribute` gates controllers, actions and Razor pages.
- `local-flag-store-is-untrusted`, `no-secrets-in-userdefaults`, `no-secrets-in-client-flag-store`, `no-personal-data-in-flag-service`: Fowler warns that client-side and per-request overrides let curious or malicious users change flag state, Apple records that `UserDefaults` sits unencrypted on disk, and MDN that `localStorage` persists on the device for the page's origin. A gate that rests on such a value alone can therefore be opened by the user, so it MUST NOT be the only gate on a security, payment or entitlement decision. Apple's "Don't store personal or sensitive information" makes secrets and personal data a MUST NOT for `UserDefaults`. For other client-side stores no source makes it a MUST NOT: Android's DataStore guide keeps sensitive data in a DataStore file apart from feature flags, and Unleash keeps personal data out of flag systems, so it is a SHOULD NOT there. Unleash says personal data should stay confined to the application, vendor practice and so a SHOULD NOT for flag contexts and server-side flag stores. Guarding the overrides themselves is [adc.guideline.implementing.feature-management.debug-mode](cookbook:e446ee3e-b8f2-40e7-b93d-3113e6a95e5d).
- `no-mid-session-ui-flip`: Firebase Remote Config advises against switching UI while the user is using it and offers activation on the next start.
- `monitor-flag-rollout`: Microsoft watches usage and system-health metrics as exposure widens, a single-source SHOULD.
- `prefer-static-flag-configuration`: Fowler prefers static, source-controlled toggle configuration and reserves dynamic configuration for ops toggles.
- `spec-lists-flag-keys`: Kept as written for the owner to decide: no source covers listing flag keys in a specification; the nearest practice is the naming convention, description and removal plan each flag records.

## References

- [Feature Toggles (aka Feature Flags) (Pete Hodgson, martinfowler.com)](https://martinfowler.com/articles/feature-toggles.html)
- [FeatureFlag (bliki) (Martin Fowler)](https://martinfowler.com/bliki/FeatureFlag.html)
- [Introduction | OpenFeature](https://openfeature.dev/docs/reference/intro)
- [OpenFeature Specification, 1. Flag Evaluation API](https://openfeature.dev/specification/sections/flag-evaluation)
- [OpenFeature Specification, 2. Provider](https://openfeature.dev/specification/sections/providers)
- [OpenFeature Specification, 01-flag-evaluation.md (source)](https://raw.githubusercontent.com/open-feature/spec/main/specification/sections/01-flag-evaluation.md)
- [OpenFeature Specification, 02-providers.md (source)](https://raw.githubusercontent.com/open-feature/spec/main/specification/sections/02-providers.md)
- [Resilient architecture patterns for LaunchDarkly SDKs](https://launchdarkly.com/docs/guides/sdk/resilience)
- [Flag variation evaluation (LaunchDarkly)](https://launchdarkly.com/docs/sdk/features/evaluating)
- [Reducing technical debt from feature flags (LaunchDarkly)](https://launchdarkly.com/docs/guides/flags/technical-debt)
- [Archiving and restoring flags (LaunchDarkly)](https://launchdarkly.com/docs/home/flags/archive)
- [Caching contexts to local storage (LaunchDarkly)](https://launchdarkly.com/docs/sdk/features/local-storage)
- [Feature Flag Evaluation (ConfigCat)](https://configcat.com/docs/targeting/feature-flag-evaluation/)
- [Defensive Coding and Designing for Failure (Flagsmith)](https://docs.flagsmith.com/best-practices/defensive-coding)
- [11 feature flag best practices for scale (Unleash)](https://docs.getunleash.io/topics/feature-flags/feature-flag-best-practices)
- [Feature flags (Unleash)](https://docs.getunleash.io/concepts/feature-flags)
- [Technical debt (Unleash)](https://docs.getunleash.io/reference/technical-debt)
- [Firebase Remote Config loading strategies](https://firebase.google.com/docs/remote-config/loading)
- [Progressive experimentation with feature flags (Microsoft)](https://learn.microsoft.com/en-us/devops/operate/progressive-experimentation-feature-flags)
- [.NET Feature Flag Management - Azure App Configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/feature-management-dotnet-reference)
- [Feature Management Overview - Azure App Configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/feature-management-overview)
- [IFeatureManager.cs (FeatureManagement-Dotnet, main)](https://raw.githubusercontent.com/microsoft/FeatureManagement-Dotnet/main/src/Microsoft.FeatureManagement/IFeatureManager.cs)
- [FeatureManagementOptions.cs (FeatureManagement-Dotnet, main)](https://raw.githubusercontent.com/microsoft/FeatureManagement-Dotnet/main/src/Microsoft.FeatureManagement/FeatureManagementOptions.cs)
- [App Review Guidelines (Apple)](https://developer.apple.com/app-store/review/guidelines/)
- [Device and Network Abuse - Play Console Help](https://support.google.com/googleplay/android-developer/answer/16273414)
- [UserDefaults (Apple)](https://developer.apple.com/documentation/foundation/userdefaults)
- [SharedPreferences (Android API reference)](https://developer.android.com/reference/android/content/SharedPreferences)
- [DataStore (Android App Architecture: Data Layer)](https://developer.android.com/topic/libraries/architecture/datastore)
- [Window: localStorage property (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- [In the Matter of Knight Capital Americas LLC, Release No. 34-70694 (SEC)](https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.4 | 2026-11-07 | Mike Fullerton | Remove the duplicated intro block |
| 1.0.3 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
