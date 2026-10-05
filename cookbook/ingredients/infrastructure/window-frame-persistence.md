---
id: 85d04a9b-5692-4025-a489-eac8bbb14663
title: "Window Frame Persistence"
domain: agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Invisible view modifier that persists window position and size between sessions via frame autosave"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
  - windows
tags:
  - infrastructure
  - window-frame-persistence
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Window Frame Persistence

## Overview

An invisible view modifier that persists a window's position and size between sessions using the platform's native frame autosave mechanism. Attached as a background modifier to any window's root content. On macOS, accesses the hosting `NSWindow` and calls `setFrameAutosaveName`. Supports a close callback for cleanup.

## Behavioral Requirements

- **persist-frame-autosave**: The component MUST persist the window's frame (origin + size) across app sessions using `NSWindow.setFrameAutosaveName`.
- **unique-autosave-name**: Each window MUST have a unique autosave name. For document windows, this SHOULD be derived from the document's file path (e.g., SHA256 hash prefix).
- **invisible-background-view**: The component MUST NOT be visible — it renders as an empty `NSView` added as a background.
- **delayed-window-access**: The component MUST access the hosting `NSWindow` via the view hierarchy after a brief delay (next main run loop cycle) to ensure the window exists.
- **on-close-callback**: The component MAY accept an `onClose` callback that fires when the window is closed (via `NSWindow.willCloseNotification`).
- **cleanup-observers**: The component MUST clean up notification observers on deinit.
- **default-first-launch**: On first launch (no saved frame), the window SHOULD use its default position/size defined elsewhere.

## Appearance

Not applicable — this component is invisible.

## States

| State | Behavior |
|-------|----------|
| Window appears | Autosave name applied, previous frame restored if saved |
| Window moved/resized | Frame auto-saved by AppKit (no manual intervention needed) |
| Window closed | `onClose` callback fired, observers cleaned up |
| No saved frame | Window uses default layout |

## Accessibility

Not applicable — this component has no visual or interactive surface.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| frame-001 | persist-frame-autosave | Open window, move to (200,300), close, reopen | Window appears at (200,300) |
| frame-002 | persist-frame-autosave | Open window, resize to 800×600, close, reopen | Window appears at 800×600 |
| frame-003 | unique-autosave-name | Open two document windows | Each has unique autosave name, saved independently |
| frame-004 | invisible-background-view | Inspect view hierarchy | No visible NSView from this component |
| frame-005 | on-close-callback | Close window with onClose callback | Callback fires |

## Edge Cases

- **Window opens off-screen** (e.g., saved on external monitor now disconnected): AppKit handles this — `setFrameAutosaveName` adjusts to visible screen area.
- **Duplicate autosave names**: Two windows with the same name will interfere. Use unique identifiers.
- **Rapid open/close**: Observer cleanup in deinit prevents leaks.

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `WindowFrame`

| Event | Level | Message |
|-------|-------|---------|
| Frame autosave set | debug | `WindowFrame: autosave name set to "{{name}}"` |
| Window closed | debug | `WindowFrame: window "{{name}}" closed` |

## Platform Notes

- **SwiftUI (macOS)**: Implement as `NSViewRepresentable`. In `makeNSView`, return an empty `NSView`. In `updateNSView`, dispatch to main queue to access `view.window`, then call `window.setFrameAutosaveName(name)`. Observe `NSWindow.willCloseNotification` for close callback. Attach via `.background(WindowAccessor(name: "...", onClose: { }))`.
- **Other platforms**: Not applicable. iOS, Android, and Web handle window/view positioning differently (iOS has no user-movable windows, Android has activity lifecycle, Web uses CSS/URL state).

## Design Decisions

_None yet._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [state-recovery](agenticdevelopercookbook://compliance/reliability#state-recovery) | partial | Reliability |
| [platform-design-language](agenticdevelopercookbook://compliance/platform-compliance#platform-design-language) | partial | Platform |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
