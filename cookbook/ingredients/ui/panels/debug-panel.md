---
id: be66e9aa-6c54-4c6c-8026-050eb2286abb
title: "Debug Panel"
domain: agenticdevelopercookbook://ingredients/ui/panels/debug-panel
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Debug-only panel for feature flag overrides, analytics monitoring, and runtime configuration inspection"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - debug-panel
  - panel
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

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

## States

| State | Behavior |
|-------|----------|
| Debug build, panel closed | Gesture/shortcut is active, panel is not visible |
| Debug build, panel open | Modal/overlay showing, app still visible beneath |
| Release build | Panel code is not compiled, gesture has no effect |
| Flag overridden | Flag row shows "override" badge, value reflects override |
| Flag reset | Override cleared, value returns to default/remote |
| Environment switched | All service URLs update, services reconnect |

## Accessibility

- **accessible-labels**: All tabs and controls MUST have accessible labels.
- **keyboard-navigable**: The panel MUST be fully keyboard-navigable.
- **toggle-state-announce**: Toggle switches MUST announce their state (on/off) to screen readers.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| debug-001 | debug-build-only | Build in Release config, attempt shake gesture | No debug panel appears |
| debug-002 | debug-build-only | Build in Debug config, attempt shake gesture | Debug panel appears |
| debug-003 | flag-toggle-persist | Toggle a flag in debug panel, restart app | Override persists after restart |
| debug-004 | reset-all-flags | Override 3 flags, tap Reset All | All flags return to default/remote values |
| debug-005 | live-event-log | Trigger a user action that tracks an event | Event appears in analytics log with correct name and properties |
| debug-006 | manual-variant-picker | Select a different variant for an experiment | Variant assignment changes immediately |
| debug-007 | environment-presets | Switch from Production to Staging | Backend URLs update to staging values |
| debug-008 | copy-env-info | Tap Copy All on environment info | Clipboard contains formatted environment info |
| debug-009 | immediate-effect | Toggle a feature flag | Feature behavior changes immediately without app restart |

## Edge Cases

- **No feature flags registered**: Flags tab SHOULD show "No feature flags registered" rather than empty.
- **No experiments registered**: A/B tab SHOULD show "No experiments registered."
- **Analytics log very long**: Event log SHOULD use a virtualized/recycled list. Cap at 1000 events in memory.
- **Backend unreachable after switch**: SHOULD show connection error inline, not crash. Allow switching back.

## Configuration

This ingredient has no configurable options.

## Privacy

- **Data collected**: Feature flag overrides, experiment variant selections, analytics event log (in-memory only)
- **Storage**: Overrides in platform local storage (UserDefaults / SharedPreferences / localStorage). Event log is in-memory only.
- **Transmission**: None — debug panel data never leaves the device
- **Retention**: Overrides persist until cleared. Event log cleared on app restart.

## Logging

Subsystem: `{{bundle_id}}` | Category: `DebugPanel`

| Event | Level | Message |
|-------|-------|---------|
| Panel opened | debug | `DebugPanel: opened` |
| Panel closed | debug | `DebugPanel: closed` |
| Flag overridden | debug | `DebugPanel: flag "{{key}}" overridden to {{value}}` |
| All flags reset | debug | `DebugPanel: all flag overrides cleared` |
| Variant overridden | debug | `DebugPanel: experiment "{{key}}" set to variant "{{variant}}"` |
| Environment switched | debug | `DebugPanel: switched to {{environment}}` |
| Environment info copied | debug | `DebugPanel: environment info copied to clipboard` |

## Platform Notes

- **SwiftUI (iOS)**: Present as `.sheet`. Trigger via `UIDevice` shake notification. Guard entire file with `#if DEBUG`.
- **SwiftUI (macOS)**: Present as a floating `Window` scene. Add Debug menu item via `.commands`. Guard with `#if DEBUG`.
- **Compose (Android)**: Present as a `ModalBottomSheet` or `Dialog`. Trigger via `ShakeDetector` (accelerometer). Guard with `if (BuildConfig.DEBUG)`.
- **React (Web)**: Render as a slide-in overlay panel. Route to `/debug` in dev mode only. Guard with `process.env.NODE_ENV === 'development'`.

## Design Decisions

_None yet — decisions made during implementation should be recorded here._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [no-pii-in-logs](agenticdevelopercookbook://compliance/privacy-and-data#no-pii-in-logs) | partial | Privacy |
| [secure-log-output](agenticdevelopercookbook://compliance/security#secure-log-output) | partial | Security |
| [screen-reader-support](agenticdevelopercookbook://compliance/accessibility#screen-reader-support) | partial | Accessibility |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
