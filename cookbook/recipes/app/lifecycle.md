---
id: e56d4b42-9abe-47ac-bd9e-27471bd47b82
title: "App Lifecycle"
domain: agenticdevelopercookbook://recipes/app/lifecycle
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pattern for managing desktop and mobile app startup behavior, session restore, and process cleanup on quit"
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
ingredients:
  - agenticdevelopercookbook://ingredients/app/startup-behavior
  - agenticdevelopercookbook://ingredients/app/session-restore
  - agenticdevelopercookbook://ingredients/app/child-process-cleanup
  - agenticdevelopercookbook://ingredients/infrastructure/settings-keys
  - agenticdevelopercookbook://ingredients/infrastructure/logging
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# App Lifecycle

## Overview

Pattern for managing desktop and mobile app lifecycle: what happens on startup, how sessions and documents are restored, and how processes are cleaned up on quit. Startup Behavior decides what to do at launch, Session Restore reopens the previous documents, and Child Process Cleanup ends child processes at quit; the recipe wires them in launch and quit order and declares the multi-window scenes for SwiftUI apps. Covers UIKit scene delegates, Android activity lifecycle, and Web page lifecycle in the ingredients. Derived from scratching-post CatnipApp.swift and AppDelegate.swift.

### Terminology

| Term | Definition |
|------|-----------|
| Scene | A SwiftUI construct (`WindowGroup`, `DocumentGroup`, `Window`, `Settings`) that declares a window type the app can display |

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Startup Behavior | `agenticdevelopercookbook://ingredients/app/startup-behavior` | Resolves the startup mode and controls untitled-window creation | Yes | Default `restoreSession` |
| Session Restore | `agenticdevelopercookbook://ingredients/app/session-restore` | Saves and reopens document URLs | Yes | Active when mode is `restoreSession` |
| Child Process Cleanup | `agenticdevelopercookbook://ingredients/app/child-process-cleanup` | Terminates child processes on quit | Yes | Timeout 5 seconds |
| Settings Keys | `agenticdevelopercookbook://ingredients/infrastructure/settings-keys` | Central keys for the startup mode and restore list | Yes | Keys in a constants enum or struct |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Logger for lifecycle events | Yes | Category `AppLifecycle` |

## Integration Requirements

- **multi-window-scenes** (macOS/SwiftUI): The app MUST support multiple window types via scene declarations (`WindowGroup`, `DocumentGroup`, `Window`, `Settings`).
- **per-type-document-group**: Each document type SHOULD have its own `DocumentGroup` scene with the appropriate content type and file extensions registered.
- **dedicated-settings-scene**: Settings SHOULD use a dedicated `Settings` scene (macOS 14+) or `Window` scene with `.handlesExternalEvents(matching:)` for older macOS versions.
- **commands-modifier**: Custom menu commands SHOULD be applied via the `.commands` modifier on the primary `WindowGroup`.
- **static-scene-declarations**: The `@main` App struct MUST compose all scene declarations in its `body` property. Scene declarations MUST NOT be generated dynamically at runtime.

### Launch and quit wiring

- **mode-gates-restore**: Session Restore MUST run only when the Startup Behavior mode resolves to `restoreSession`; in `newWindow` and `nothing` modes it MUST NOT open any saved document.
- **restore-fallback-uses-new-window**: When Session Restore finds no valid URLs, it MUST hand control back to Startup Behavior's `newWindow` behavior exactly once, so that only one default window opens.
- **save-before-cleanup**: On quit, the app MUST save the Session Restore URL list before Child Process Cleanup begins, so a slow or timed-out cleanup cannot lose the list.
- **keys-through-registry**: The startup mode and the restore URL list MUST be stored under keys declared through the `settings-keys` ingredient.
- **log-lifecycle-events**: All lifecycle events MUST be logged through the `logging` ingredient with category `AppLifecycle`.

## Layout

```
 Launch                                             Quit
   |                                                  |
   v                                                  v
 Startup Behavior --mode--> newWindow  -> default window
        |                -> nothing    -> no window
        |                -> restoreSession
        v                        |
   Session Restore <-------------+--(no valid URLs)--> newWindow
                                                      |
 [@main App body: WindowGroup | DocumentGroup | Window | Settings scenes]
                                                      |
   Session Restore (save URL list) -> Child Process Cleanup (SIGHUP, 5 s, SIGKILL)
```

Not a visual layout: the diagram shows launch and quit ordering across the ingredients and the scene declarations hosted by the app.

### Composed states

| State | Behavior |
|-------|----------|
| App quitting, documents open | URL list saved to persistence, child processes terminated |
| App quitting, no documents open | Empty URL list saved (clears previous restore list), child processes terminated |
| System logout/restart | Same as app quitting; session restore list saved normally |

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Startup behavior mode | Settings (via settings-keys) | Startup Behavior, Session Restore | one-way | Resolved once at launch |
| Restore URL list | Open document windows at quit | Session Restore on next launch | one-way | Atomic write to platform persistence |
| Child process handles | Subsystems that spawn processes | Child Process Cleanup | one-way | Registered when spawned; cleaned at quit |
| Untitled-window decision | Startup Behavior mode and relaunch state | App delegate | one-way | `applicationShouldOpenUntitledFile` result |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-002 | configurable-startup-modes, save-restore-urls | Set startup behavior to `restoreSession`, open 3 documents, quit, relaunch | Same 3 documents reopen |
| lifecycle-004 | default-restore-session | Fresh install, launch app with no prior preferences | App behaves as `restoreSession` (and since no URLs saved, falls back to `newWindow` per fallback-to-new-window) |
| lifecycle-016 | multi-window-scenes | (macOS) Inspect app scene declarations | App body contains at least one `WindowGroup` and one `Settings` or `Window` scene |
| lifecycle-017 | per-type-document-group | (macOS) Open a registered document type via Finder | Correct `DocumentGroup` scene handles the file |
| lifecycle-018 | commands-modifier | (macOS) Open app, inspect menu bar | Custom menu commands present from `.commands` modifier |
| lifecycle-020 | mode-gates-restore | Set mode to `newWindow` with saved URLs present, launch | Only the default window opens; no saved document is reopened |
| lifecycle-021 | restore-fallback-uses-new-window, fallback-to-new-window | Mode `restoreSession` with all saved URLs invalid, launch | Exactly one default window opens |
| lifecycle-022 | save-before-cleanup, cleanup-timeout-sigkill | Open 2 documents and a process that ignores SIGHUP, quit | URL list is saved before cleanup starts; after the timeout the process is killed and relaunch restores both documents |
| lifecycle-023 | keys-through-registry | Inspect persisted keys after changing the mode and quitting | Both keys are the ones declared in the settings-keys registry |

## Edge Cases

- **Quit during document save**: The app MUST wait for in-progress saves to complete before terminating child processes. This is handled by the document subsystem's save-on-close behavior.
- **Quit with no open documents and children running**: The empty URL list MUST be saved (clearing the previous restore list) and children MUST still be terminated.
- **Mode `nothing` with a relaunch that restores nothing**: No window opens and the empty URL list MUST NOT be treated as a restore failure.

## Platform Notes

- **SwiftUI (macOS) with AppDelegate**: Use `@NSApplicationDelegateAdaptor` to bridge an `AppDelegate` into the SwiftUI app. Scene declarations (`WindowGroup`, `DocumentGroup`, `Settings`) go in the `@main` App struct's `body`. Apply the `.commands` modifier on the primary `WindowGroup` for custom menu items.
- **UIKit (iOS/visionOS) with SceneDelegate**: Scene-level wiring uses the `UISceneDelegate`; the ingredients' platform notes define the per-concern hooks.
- **Compose (Android)**: Scenes correspond to activities; hold lifecycle wiring in the `Application` class and the activity lifecycle callbacks described by the ingredients.
- **React/Web**: There is a single page; scene declarations do not apply. Wire the ingredients from the page's `load`, `visibilitychange`, and `beforeunload` handlers.

## Design Decisions

**Decision**: Split lifecycle into startup behavior, session restore, and child process cleanup.
**Rationale**: Each concern has its own settings, failure modes, and tests; the recipe states only their ordering.
**Approved**: pending

**Decision**: Save the restore list before child process cleanup runs.
**Rationale**: Cleanup can take up to the timeout and can be interrupted; the restore list is the more valuable artifact.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this recipe specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructured into recipe shape: composes startup-behavior, session-restore, and child-process-cleanup |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
