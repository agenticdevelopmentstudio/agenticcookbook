
Setting up the provider: define a `FeatureFlagProvider` interface (`isEnabled(key) -> Bool`), provide a local default implementation, backed by `UserDefaults` in Swift, `SharedPreferences` in Kotlin and `localStorage` in TypeScript, and swap in a backend implementation later via DI (`feature-flag-provider-interface`, `swift-userdefaults-default`, `kotlin-sharedpreferences-default`, `typescript-localstorage-default`). On Android, `kotlin-datastore-default` points the Kotlin store to Jetpack DataStore instead; the owner has not yet settled which of the two Kotlin rules stands; see Rationale.

Adding a flag:

1. Ask whether the change can ship in safe increments without one (`flag-only-when-needed`). The owner has not yet settled how this sits with `gate-all-features`; see Rationale.
2. Give the flag a name from the shared convention, prefixed `{{app_prefix}}.`, a description, a type and its expected lifetime, and plan its removal now: open the removal pull request beside the one that adds it, or set an expiration date (`name-and-describe-flags`, `flag-has-a-type-and-lifetime`, `remove-flags-when-done`).
3. Register its in-code default in the local default implementation, set to today's behaviour, or to the restrictive behaviour for a security-sensitive flag (`evaluation-takes-a-default-and-never-throws`, `off-means-existing-behaviour`).
4. Read the flag once, where the object is composed, and pass the decision in; avoid letting deep code ask the provider (`decouple-toggle-points`).
5. Test both states, and test the release configuration and its fallback (`test-both-flag-states`, `test-release-and-fallback-configurations`).
6. For an App Store build, describe the feature in the Notes for Review and make it reachable for review (`flags-never-hide-features-from-review`).

Rolling it out: widen exposure in steps, watching usage and health metrics (`monitor-flag-rollout`); apply values fetched mid-session at the next launch when they change UI (`no-mid-session-ui-flip`).

Retiring it: delete the flag check and the old code path, ship that, then archive the flag in the flag service; never give its name to another flag (`remove-flags-when-done`, `unique-never-reused-flag-names`).

