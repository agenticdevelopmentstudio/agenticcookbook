---
id: EE72734E-2CFF-41BE-9D1A-813B64AA0FD2
title: "Startup Behavior"
domain: agenticdevelopercookbook://ingredients/app/startup-behavior
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "User-configurable startup behavior (new window, restore session, or nothing) with untitled-window suppression"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - web
  - windows
tags:
  - app
  - lifecycle
  - startup
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/app/session-restore
  - agenticdevelopercookbook://recipes/app/lifecycle
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Startup Behavior

## Overview

The configurable action an app takes when it first becomes active after launch, and the control of automatic untitled-window creation that goes with it. Three modes are supported: open the default window, restore the previous session, or launch silently with no window. The mode is a user setting stored through the platform's standard persistence layer under a centralized key and defaults to restoring the session. This ingredient decides what to do at launch; reopening documents is the Session Restore ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| Startup behavior | The configurable action the app takes when it first becomes active after launch |
| Untitled file | A new, unsaved document window that macOS may open automatically on launch |

## Behavioral Requirements

### Startup behavior

- **configurable-startup-modes**: The app MUST support configurable startup behavior with at least the following modes:
  - `newWindow` — open the default window (e.g., new document or welcome screen)
  - `restoreSession` — reopen previously open documents/windows
  - `nothing` — launch silently to the menu bar (macOS) or dock/background without opening any window
- **startup-behavior-setting**: Startup behavior MUST be a user-configurable setting stored via the platform's standard persistence layer (per the `abstract-persistence` requirement of the `settings-category-browser` ingredient). The setting key MUST be centralized in the app's settings key constants (per the `centralized-keys` requirement of the Settings Window recipe).
- **default-restore-session**: The startup behavior setting MUST default to `restoreSession` on first launch (no prior user preference).

### Untitled window suppression

- **suppress-untitled-file** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `false` when startup behavior is `nothing` or `restoreSession`.
- **allow-untitled-new-window** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `true` when startup behavior is `newWindow`.
- **suppress-untitled-relaunch** (macOS): This method MUST also return `false` when the app is being relaunched by the system after a logout/restart and `restoreSession` is active, to avoid duplicating restored windows with an additional untitled window.

## Appearance

Not applicable — app lifecycle management has no visual appearance. UI is defined by the window and component recipes.

## States

| State | Behavior |
|-------|----------|
| Cold launch, mode = newWindow | App opens default window immediately |
| Cold launch, mode = nothing | App activates with no windows; only menu bar and dock icon visible |
| App becoming active (already running) | No automatic window creation; user activates existing windows |

## Accessibility

N/A — App lifecycle management has no direct user-facing UI elements. Accessibility requirements for any windows or views opened during startup are covered by their respective specs.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-001 | configurable-startup-modes, startup-behavior-setting | Set startup behavior to `newWindow`, launch app | Default window opens |
| lifecycle-003 | configurable-startup-modes | Set startup behavior to `nothing`, launch app | No windows open; app is active in menu bar/dock |
| lifecycle-013 | suppress-untitled-file, allow-untitled-new-window | (macOS) Set startup behavior to `newWindow` | `applicationShouldOpenUntitledFile` returns `true` |
| lifecycle-014 | suppress-untitled-file | (macOS) Set startup behavior to `nothing` | `applicationShouldOpenUntitledFile` returns `false` |
| lifecycle-015 | suppress-untitled-file | (macOS) Set startup behavior to `restoreSession` | `applicationShouldOpenUntitledFile` returns `false` |
| lifecycle-019 | suppress-untitled-relaunch | (macOS) System restarts with `restoreSession` active | App does not open both restored documents and an untitled window |

## Edge Cases

- **Stored mode is unrecognized**: If the persisted startup behavior value is not one of `newWindow`, `restoreSession`, or `nothing`, the app MUST resolve to the default (`restoreSession`) rather than failing, and the resolution SHOULD be logged with the fallback flag set (see the "Startup behavior resolved" log event).
- **Mode `nothing` on a platform without a menu bar**: The app MUST launch without opening any window and remain reachable through its dock, launcher, or background entry; it MUST NOT quit itself.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `startupBehavior` | enum (`newWindow`, `restoreSession`, `nothing`) | `restoreSession` | Action taken when the app first becomes active after launch; stored under a centralized settings key |

## Logging

Subsystem: `{{bundle_id}}` | Category: `AppLifecycle`

| Event | Level | Message |
|-------|-------|---------|
| App launched | info | `AppLifecycle: launched, startup behavior = "{{mode}}"` |
| Startup behavior resolved | debug | `AppLifecycle: resolved startup behavior to "{{mode}}" (setting: "{{setting}}", fallback: {{fallback}})` |
| Untitled file suppressed | debug | `AppLifecycle: applicationShouldOpenUntitledFile returning false (mode = "{{mode}}")` |
| Untitled file allowed | debug | `AppLifecycle: applicationShouldOpenUntitledFile returning true` |

## Platform Notes

- **SwiftUI (macOS) with AppDelegate**: Implement `applicationShouldOpenUntitledFile(_:)` in the `AppDelegate` to control untitled window creation based on the startup behavior setting.
- **UIKit (iOS/visionOS) with SceneDelegate**: Implement `scene(_:willConnectTo:options:)` in the `UISceneDelegate` to handle startup behavior.
- **Android (Activity lifecycle, Compose)**: Map startup behavior to `onCreate` / `onRestoreInstanceState`.
- **Web (React/SPA)**: Resolve the startup behavior from `localStorage` on page load before rendering the first view.

## Design Decisions

**Decision**: The default startup behavior is `restoreSession`, falling back to `newWindow` when there is nothing to restore.
**Rationale**: Returning users see their work again, and first-time users still get a window.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the App Lifecycle recipe |
