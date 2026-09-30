<!-- leaf: implement-ui/android-predictive-back · source: guidelines/implementing/ui/android-predictive-back.md -->

**Rules** (cite as `implement-ui/android-predictive-back#<slug>`):

- `user-commits-apps-migrate-off-unsupported-onbackpressed` MUST — The predictive back gesture (introduced in Android 13 / API 33, enabled by default for opted-in apps from Android 15) …
- `longer-supported-code-not-rely-either-official-docs` MUST — Activity.onBackPressed() and Dialog.onBackPressed() are deprecated; intercepting KeyEvent.KEYCODE_BACK is no longer …
- `custom-back-logic-register-onbackpressedcallback-activity-onbackpresseddispatcher` MUST — Custom back logic MUST register an OnBackPressedCallback on the activity's OnBackPressedDispatcher, tied to a …
- `callback-isenabled-derived-from-observable-ui` MUST — The callback's isEnabled MUST be derived from observable UI state (a StateFlow or Compose State), not toggled …
- `per-application-flag-overridden-per-activity-gradual` MAY — The android:enableOnBackInvokedCallback flag controls predictive back during migration. It is a per-<application> flag …
- `step-flows-guidance-animate-gesture-rather-than` SHOULD — For custom transitions (sheets, drawers, multi-step flows), guidance SHOULD animate with the gesture rather than …
- `consuming-side-effects-not-alter-navigation` MUST — Android 16 (API 36) adds PRIORITY_SYSTEM_NAVIGATION_OBSERVER for callbacks that watch Back without consuming it (e.g. …

# Android predictive back

The predictive back gesture (introduced in Android 13 / API 33, enabled by default for opted-in apps from Android 15) shows a peek of where Back will go before the user commits. Apps MUST migrate off the unsupported `onBackPressed()` and `KEYCODE_BACK` interception to `OnBackPressedDispatcher` and SHOULD drive in-app transitions from the gesture's progress.

## Migrate off unsupported back handling

- `Activity.onBackPressed()` and `Dialog.onBackPressed()` are deprecated; intercepting `KeyEvent.KEYCODE_BACK` is no longer supported. Code MUST NOT rely on either — official docs warn of "unexpected behavior in a future release."
- Custom back logic MUST register an `OnBackPressedCallback` on the activity's `OnBackPressedDispatcher`, tied to a `LifecycleOwner` so it is removed automatically.
- Prefer the AndroidX `androidx.activity` APIs over the platform `OnBackInvokedCallback` — AndroidX is backward compatible across versions and is the recommended path. Use the platform `OnBackInvokedCallback` directly ONLY when you have no AndroidX dependency.
- The callback's `isEnabled` MUST be derived from observable UI state (a `StateFlow` or Compose `State`), not toggled imperatively, so the system knows whether the app or the system handles Back.
- Keep callbacks single-responsibility: one callback per back-consuming UI state, ordered by registration. The most recently added enabled callback wins.

```kotlin
val callback = object : OnBackPressedCallback(enabled = uiState.hasUnsavedChanges) {
    override fun handleOnBackPressed() { showDiscardConfirmation() }
}
requireActivity().onBackPressedDispatcher.addCallback(viewLifecycleOwner, callback)
```

## Opt in via the manifest

- The `android:enableOnBackInvokedCallback` flag controls predictive back during migration. It is a per-`<application>` flag and MAY be overridden per `<activity>` for gradual rollout of multi-activity apps.
- Setting it `false` disables system predictive animations and ignores the platform `OnBackInvokedCallback`; AndroidX `OnBackPressedCallback` still works. Set it `true` (or omit it where the default is on) to receive system animations.
- FORECAST: default-on behavior and removal of any opt-out are tied to evolving target-SDK rules across Android 15/16 (API 35/36). Pin the exact behavior to your `targetSdk` and re-check the linked doc before shipping — do not assume a fixed default across versions.

## Drive in-app animations from gesture progress

- For custom transitions (sheets, drawers, multi-step flows), guidance SHOULD animate with the gesture rather than snapping at release.
- Compose: use `PredictiveBackHandler`, collecting the `Flow<BackEventCompat>` and reading `progress` (0f..1f). Commit the navigation when the flow completes; reset UI on `CancellationException` (gesture cancelled).
- Views: extend `OnBackPressedCallback` and implement `handleOnBackStarted` / `handleOnBackProgressed` / `handleOnBackCancelled` (API 34+) to animate, with `handleOnBackPressed` committing the result.

```kotlin
PredictiveBackHandler(enabled = sheetIsOpen) { progress: Flow<BackEventCompat> ->
    try {
        progress.collect { event -> sheetOffset = event.progress }
        closeSheet() // committed
    } catch (e: CancellationException) {
        resetSheetOffset() // cancelled
    }
}
```

## Observer-only callbacks

- Android 16 (API 36) adds `PRIORITY_SYSTEM_NAVIGATION_OBSERVER` for callbacks that watch Back without consuming it (e.g. analytics). Use it ONLY for non-consuming side effects; it MUST NOT alter navigation.
