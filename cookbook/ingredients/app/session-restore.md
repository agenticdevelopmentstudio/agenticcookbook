---
id: A7C4168E-2F0A-40BB-B38F-0F81AD6A9CF0
title: "Session Restore"
domain: agenticdevelopercookbook://ingredients/app/session-restore
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Saves open document URLs on quit and reopens them on launch, filtering by type and existence with a new-window fallback"
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
  - restore
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/app/startup-behavior
  - agenticdevelopercookbook://recipes/app/lifecycle
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Session Restore

## Overview

Saves the list of open document URLs on quit and reopens them on the next launch. On restore, saved URLs are filtered to registered document types, validated against the file system, deduplicated, and opened in their original order; if nothing valid remains the app falls back to opening a new window. Writes are atomic so a crash never corrupts the list.

### Terminology

| Term | Definition |
|------|-----------|
| Session restore | The process of reopening previously open documents or windows from a saved URL list |

## Behavioral Requirements

### Session restore

- **save-restore-urls**: When startup behavior is `restoreSession`, the app MUST save the list of open document URLs on quit and reopen them on the next launch.
- **url-list-storage**: The URL list SHOULD be stored in `UserDefaults` (or platform equivalent) as an array of path strings, under a centralized settings key.
- **filter-registered-types**: On restore, the app SHOULD filter saved URLs to only include files whose extensions match the app's registered document types. Unrecognized extensions MUST be silently skipped.
- **validate-file-exists**: On restore, the app MUST validate that each saved URL points to an existing file. Missing files MUST be silently skipped and removed from the saved list.
- **preserve-restore-order**: On restore, the app SHOULD open documents in the same order they were saved (matching the order they were open at quit time).
- **fallback-to-new-window**: If no saved URLs exist (first launch in `restoreSession` mode, or all saved URLs are invalid), the app SHOULD fall back to the `newWindow` behavior.

## Appearance

Not applicable — session restore has no visual appearance of its own; the restored windows are defined by the window and component recipes.

## States

| State | Behavior |
|-------|----------|
| Cold launch, mode = restoreSession, saved URLs exist | App opens each saved document in order |
| Cold launch, mode = restoreSession, no saved URLs | App falls back to newWindow behavior |
| Force quit / crash | Saved URL list from previous clean quit preserved; no new save occurs |

## Accessibility

N/A — Session restore has no direct user-facing UI elements. Accessibility requirements for the restored windows are covered by their respective specs.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-005 | url-list-storage | Open 2 documents, quit app | UserDefaults contains array of 2 path strings under the correct key |
| lifecycle-006 | filter-registered-types | Save URL list containing a `.txt` file (not a registered type), relaunch in `restoreSession` mode | `.txt` file is skipped; only recognized document types open |
| lifecycle-007 | validate-file-exists | Save URL list containing a path to a deleted file, relaunch in `restoreSession` mode | Deleted file is silently skipped; remaining files open |
| lifecycle-008 | preserve-restore-order | Open documents A, B, C (in that order), quit, relaunch in `restoreSession` mode | Documents open in order A, B, C |
| lifecycle-009 | fallback-to-new-window | Set startup behavior to `restoreSession`, clear all saved URLs, relaunch | App falls back to `newWindow` behavior |

## Edge Cases

- **No saved URLs on restore**: The app MUST fall back to `newWindow` behavior (fallback-to-new-window). It MUST NOT show an error or empty state.
- **Saved URL points to deleted file**: The file MUST be silently skipped (validate-file-exists). The remaining valid URLs MUST still open. The invalid entry MUST be removed from the saved list.
- **Saved URL points to moved/renamed file**: Treated as a missing file — silently skipped. File-system-level bookmarks (Security-Scoped Bookmarks on macOS) MAY be used in a future version to track moved files, but this is out of scope for v1.
- **All saved URLs are invalid**: Falls back to `newWindow` behavior per fallback-to-new-window.
- **Crash during quit**: The saved URL list from the previous clean quit is preserved. The app MUST NOT corrupt the list during a partial write — writing SHOULD be atomic (write to temp file, then rename).
- **Crash during startup restore**: If the app crashes while opening a restored document, the next launch SHOULD still attempt to restore. A crash counter MAY be implemented to break infinite crash-restore loops (e.g., skip restore after 3 consecutive crashes).
- **Very large number of saved URLs (100+)**: The app SHOULD open documents asynchronously to avoid blocking the main thread. A progress indicator MAY be shown.
- **Duplicate URLs in saved list**: The app SHOULD deduplicate URLs before restoring. Each document SHOULD be opened at most once.
- **Read-only file restored**: The document SHOULD open in read-only mode. This is handled by the document subsystem, not lifecycle.
- **Multiple app instances**: Each instance MUST manage its own URL list independently. On macOS, the system typically enforces single-instance for bundled apps.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `restoreUrlList` | array of path strings | empty | Saved document URLs, under a centralized settings key |
| `registeredDocumentTypes` | list of extensions | app-defined | Extensions kept when filtering saved URLs on restore |
| `crashLoopThreshold` | integer | `3` | Consecutive crashes after which restore MAY be skipped |

## Privacy

- **Data collected**: Paths of the documents open at quit time.
- **Storage**: Platform persistence (`UserDefaults`, `SharedPreferences`, `localStorage`), on-device only.
- **Transmission**: None — the URL list never leaves the device.
- **Retention**: Until replaced by the next quit; an empty list is saved when no documents are open.

## Logging

Subsystem: `{{bundle_id}}` | Category: `AppLifecycle`

| Event | Level | Message |
|-------|-------|---------|
| Session restore started | info | `AppLifecycle: restoring {{count}} document(s)` |
| Document restored | debug | `AppLifecycle: restored "{{path}}"` |
| Document restore skipped (missing) | warning | `AppLifecycle: skipping missing file "{{path}}"` |
| Document restore skipped (unrecognized type) | debug | `AppLifecycle: skipping unrecognized file type "{{path}}" (extension: "{{ext}}")` |
| Session restore completed | info | `AppLifecycle: restore complete, opened {{opened}} of {{total}} document(s)` |
| Session restore fell back to newWindow | debug | `AppLifecycle: no valid URLs to restore, falling back to newWindow` |
| URL list saved | debug | `AppLifecycle: saved {{count}} document URL(s) for restore` |
| URL list save failed | error | `AppLifecycle: failed to save document URLs: {{error}}` |

## Platform Notes

- **SwiftUI (macOS) with AppDelegate**: Use `NSApp.windows` to enumerate open document windows and collect their file URLs before quit. Use `NSDocumentController.shared.recentDocumentURLs` as a reference but maintain the restore list separately in `UserDefaults`.
- **UIKit (iOS/visionOS) with SceneDelegate**: Use `NSUserActivity` or `UserDefaults` to persist and restore the document URL list. In `sceneDidDisconnect(_:)`, save the current document state.
- **Android (Activity lifecycle, Compose)**: Store the document URL list in `SharedPreferences`. In `onStop` or `onDestroy`, save the current state. Use `ProcessLifecycleOwner` to detect app-level lifecycle events. Android's activity back stack provides some built-in restore behavior, but explicit URL list management is needed for document-centric apps.
- **Web (SPA with beforeunload)**: Use the `beforeunload` event to save the document URL list to `localStorage`. On page load, check `localStorage` for saved URLs and restore them. Use `navigator.sendBeacon` or synchronous `localStorage` writes in the `beforeunload` handler to ensure data is saved. The `visibilitychange` event with `document.visibilityState === 'hidden'` is more reliable than `beforeunload` on mobile browsers.

## Design Decisions

**Decision**: Maintain the restore list separately from the platform recent-documents list.
**Rationale**: The recent list is user-visible and clearable independently; the restore list must reflect exactly what was open at quit.
**Approved**: pending

**Decision**: Skip missing, moved, or renamed files silently instead of tracking moved files. File-system-level bookmarks (Security-Scoped Bookmarks on macOS) MAY be used in a future version to track moved files, but this is out of scope for v1.
**Rationale**: Silent skipping keeps restore non-blocking; bookmark tracking adds complexity not yet needed.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [privacy](agenticdevelopercookbook://guidelines/implementing/security/privacy) | partial | Privacy |
| [error-responses](agenticdevelopercookbook://guidelines/implementing/networking/error-responses) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the App Lifecycle recipe |
