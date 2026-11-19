
- Every flag read goes through the injected provider interface, and toggle points receive their decision rather than query the flag system; a toggle expected to outlive a release flag's lifetime, or needed at several points, selects its path through a strategy rather than scattered conditionals
- Flags are evaluated through a vendor-agnostic standard API such as OpenFeature, and an existing flag platform is adopted rather than flag infrastructure built in-house, or the change says why; where the in-house provider interface and its local default stand in, a review records it
- Each new flag is for a change that could not ship safely in smaller increments, and the live flag count is held down by the team's recorded limit or by expiration dates; where neither the limit nor the dates are in the code, a review states that it could not establish them
- Every flag has an in-code default; its off state is the existing behaviour, or the restrictive one for security- or compliance-sensitive flags
- No flag evaluation can throw or halt the app, and the app keeps working with the flag service unreachable
- Provider setup failures surface at registration; no flag carries static application configuration
- Flags with non-boolean values are evaluated as their own type
- Flag configuration is static and source-controlled, changed at runtime only where it must be, such as for operational toggles
- Each platform's local store matches its rule: UserDefaults (nonsensitive only), the Android store per the Kotlin rules, localStorage handling strings and a blocked-storage error, Microsoft.FeatureManagement with appsettings.json
- The local flag store holds no personal or sensitive data, and nothing trusts a flag value the user could have changed
- Each new flag has a unique, never-reused name under the shared convention, a description, a type and lifetime, and a planned removal, and a flag past its type's lifetime is marked stale
- Both states of each flag are tested, along with the release configuration and its fallback
- Runtime flag changes do not switch UI the user is using
- A rollout that widens a flag's exposure has usage and system-health metrics to watch; a review cannot see from the code that they are watched, and states that it could not establish it
- Flags whose rollout is done are removed with their old code path, before they are archived in the flag service; whether the live flags are reviewed on a regular cadence is a team practice a review cannot establish from the code, and it says so
- No feature in a build submitted to App Review is hidden behind a flag from review, and in an app distributed through the App Store or Google Play no flag turns on code downloaded after release
- The change is checked against each owner-list rule as written: `gate-all-features`, `spec-lists-flag-keys`, `kotlin-sharedpreferences-default` and `fail-fast-on-missing-config`

