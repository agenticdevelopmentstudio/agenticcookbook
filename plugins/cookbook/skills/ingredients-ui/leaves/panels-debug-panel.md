<!-- leaf: ingredients-ui/panels-debug-panel · source: ingredients/ui/panels/debug-panel.md -->

**Rules** (cite as `ingredients-ui/panels-debug-panel#<slug>`):

- `configuration-environment-info-not-accessible-compiled-into-release` MUST — A debug-only configuration panel for inspecting and overriding runtime behavior during development. Provides access to …
- `debug-build-only` MUST
- `platform-access-gesture` MUST
- `display-flag-states` MUST
- `flag-toggle-persist` MUST
- `reset-all-flags` MUST
- `flag-row-details` MUST
- `live-event-log` MUST
- `event-row-details` MUST
- `clear-event-log` MUST
- `event-log-ephemeral` MUST
- `display-experiments` MUST
- `manual-variant-picker` MUST
- `variant-override-persist` MUST
- `reset-all-variants` MUST
- `environment-presets` MUST
- `environment-url-update` MUST
- `display-backend-urls` MUST
- `custom-url-entry` SHOULD
- `display-env-info` MUST
- `copy-env-info` MUST
- `modal-presentation` MUST
- `immediate-effect` MUST
- `accessible-labels` MUST
- `keyboard-navigable` MUST
- `toggle-state-announce` MUST

# Debug Panel

## Overview

A debug-only configuration panel for inspecting and overriding runtime behavior during development. Provides access to feature flag overrides, analytics event monitoring, A/B test variant selection, backend configuration, and environment info. MUST NOT be accessible or compiled into release builds.

## Behavioral Requirements

### Access

- **debug-build-only**: The debug panel MUST only be accessible in debug/development builds. It MUST NOT be compiled into release builds.
- **platform-access-gesture**: The debug panel MUST be accessible via a platform-appropriate gesture or action:
  - iOS: Shake gesture
  - macOS: Menu item (Debug menu) or keyboard shortcut `⌘⇧D`
  - watchOS: Force-press or long-press on app icon
  - tvOS: Button sequence on remote (e.g., Play/Pause ×3)
  - visionOS: Long-press on a hidden debug zone
  - Android: Shake gesture or long-press on app version in settings
  - Web: `/debug` route or `Ctrl+Shift+D`

### Feature Flags tab

- **display-flag-states**: MUST display all registered feature flags with their current state (enabled/disabled).
- **flag-toggle-persist**: Each flag MUST be toggleable. Overrides MUST persist across app restarts (stored locally).
- **reset-all-flags**: MUST provide a "Reset All" action that clears all overrides and returns to default/remote values.
- **flag-row-details**: Each flag row MUST show: flag key, current value (on/off), source (default / remote / override).

### Analytics Event Log tab

- **live-event-log**: MUST display a live, scrollable list of analytics events as they are tracked.
- **event-row-details**: Each event row MUST show: timestamp, event name, and properties (expandable).
- **clear-event-log**: MUST provide a "Clear" action to reset the event log.
- **event-log-ephemeral**: The event log MUST be in-memory only — it does not persist across app restarts.

### A/B Test Variants tab

- **display-experiments**: MUST display all registered experiments with their current variant assignment.
- **manual-variant-picker**: Each experiment MUST allow manual variant selection from a picker showing all possible variants.
- **variant-override-persist**: Manual overrides MUST persist across app restarts (stored locally).
- **reset-all-variants**: MUST provide a "Reset All" action that clears overrides and returns to default/remote assignments.

### Backend Configuration tab

- **environment-presets**: MUST allow switching between environment presets: Local, Staging, Production.
- **environment-url-update**: Switching environments MUST update the base URLs for feature flags, analytics, and experiment services.
- **display-backend-urls**: MUST display the current backend URL for each service.
- **custom-url-entry**: Custom URL entry SHOULD be supported for ad-hoc testing.

### Environment Info tab

- **display-env-info**: MUST display: app name, version, build number, OS name and version, device model, screen size/resolution.
- **copy-env-info**: MUST provide a "Copy All" action that copies environment info to the clipboard.

### General

- **modal-presentation**: The debug panel MUST be presented modally (sheet on iOS, floating window on macOS, overlay on Android/Web) and MUST NOT interfere with the app's navigation state.
- **immediate-effect**: Changes made in the debug panel MUST take effect immediately — no restart required.

## Appearance

The debug panel uses platform-native styling — no custom theming. It should look like a developer tool, not a polished user feature.

```
┌──────────────────────────────────────────────┐
│ Debug Panel                            [Done]│
├──────────────────────────────────────────────┤
│ [Flags] [Analytics] [A/B] [Backend] [Info]   │
├──────────────────────────────────────────────┤
│                                              │
│ feature.new_onboarding      ON   [override]  │
│ feature.dark_mode           OFF  [default]   │
│ feature.community           ON   [remote]    │
│                                              │
│                        [Reset All Overrides]  │
└──────────────────────────────────────────────┘
```

## Accessibility

- **accessible-labels**: All tabs and controls MUST have accessible labels.
- **keyboard-navigable**: The panel MUST be fully keyboard-navigable.
- **toggle-state-announce**: Toggle switches MUST announce their state (on/off) to screen readers.

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI (iOS)**: Present as `.sheet`. Trigger via `UIDevice` shake notification. Guard entire file with `#if DEBUG`.
- **SwiftUI (macOS)**: Present as a floating `Window` scene. Add Debug menu item via `.commands`. Guard with `#if DEBUG`.
- **Compose (Android)**: Present as a `ModalBottomSheet` or `Dialog`. Trigger via `ShakeDetector` (accelerometer). Guard with `if (BuildConfig.DEBUG)`.
- **React (Web)**: Render as a slide-in overlay panel. Route to `/debug` in dev mode only. Guard with `process.env.NODE_ENV === 'development'`.

## Privacy

- **Data collected**: Feature flag overrides, experiment variant selections, analytics event log (in-memory only)
- **Storage**: Overrides in platform local storage (UserDefaults / SharedPreferences / localStorage). Event log is in-memory only.
- **Transmission**: None — debug panel data never leaves the device
- **Retention**: Overrides persist until cleared. Event log cleared on app restart.
