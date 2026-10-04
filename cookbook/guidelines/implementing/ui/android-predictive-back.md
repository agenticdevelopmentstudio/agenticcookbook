---
id: 8a39c784-a101-434f-afe6-c92187ccf576
title: "Android predictive back"
domain: agenticdevelopercookbook://guidelines/implementing/ui/android-predictive-back
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Migrate off deprecated back handling to OnBackPressedDispatcher and support the predictive back gesture with progress-driven animations."
platforms:
  - kotlin
tags:
  - android
  - navigation
  - ui
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/ui/android-edge-to-edge
references:
  - https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ui-implementation
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
