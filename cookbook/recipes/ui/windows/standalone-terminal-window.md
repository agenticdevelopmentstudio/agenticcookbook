---
id: 08f87323-4043-432f-8f29-936cfb4ed2e2
title: "Standalone Terminal Window"
domain: agenticdevelopercookbook://recipes/ui/windows/standalone-terminal-window
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Standalone terminal window with session sidebar and independent session manager for non-project terminal use"
platforms:
  - macos
  - swift
  - windows
tags:
  - standalone-terminal-window
  - ui
  - window
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Standalone Terminal Window

## Overview

A standalone terminal window with a session sidebar and terminal view — distinct from the project window's embedded terminal. This is the primary window for non-project terminal usage. The window uses an HSplitView with a session list on the left and a terminal view on the right, and creates its own independent SessionManager instance. It shares the same terminal-pane spec for terminal behavior (PTY sessions, session list, terminal rendering, profiles) but operates as a completely independent instance with no session sharing between windows.

## Terminology

| Term | Definition |
|------|-----------|
| Standalone terminal window | A top-level window containing only a session sidebar and terminal view, not embedded in a project window |
| Session sidebar | The left panel listing all terminal sessions owned by this window's session manager |
| Session manager | A per-window controller owning an ordered list of sessions — see `ui/Recipes/terminal-pane.md` per-window-manager |
| Terminal view | The rendering surface for the selected session — see `ui/Recipes/terminal-pane.md` nsview-representable through palette-color-structure |
| Active profile | The currently selected color profile applied to terminal rendering — see `ui/color-profile.md` single-active-profile |
| Window scene | A SwiftUI `WindowGroup` identified by a string, used to open and manage window instances |

## Behavioral Requirements

### Window structure

- **window-group-terminal**: The window MUST use a `WindowGroup(id: "terminal")` scene declaration.
- **hsplit-sidebar-terminal**: The window MUST use an HSplitView with two sections: session list sidebar (left) and terminal view (right).
- **sidebar-width-range**: The session list sidebar MUST have a width between 150pt and 200pt.
- **persist-window-frame**: The window frame MUST be persisted using the window-frame-persistence component (as defined in `ui/window-frame-persistence.md`). The autosave name MUST be `"terminal-window"`.
- **min-size-constraints**: The window MUST enforce minimum size constraints: minWidth 600pt, minHeight 400pt.

### Session management

- **own-session-manager**: The window MUST create its own `SessionManager` instance as a `@StateObject`. This instance MUST be independent from any project window's session manager.
- **auto-create-default**: On window appear (`onAppear`), if the session manager contains no sessions, a default session MUST be created automatically by calling `addSession()`.
- **terminate-on-close**: On window close, all sessions MUST be terminated by calling `terminateAll()` on the session manager.
- **focused-object-dispatch**: The session manager MUST be provided as `.focusedObject()` so that menu commands (New Session, Close Session, etc.) can dispatch to the correct window's session manager.

### Terminal view and profile

- **apply-active-profile**: The terminal view MUST apply the active color profile (colors, font, cursor style) from `TerminalProfile.activeProfile()`.
- **global-profile-storage**: The active profile ID MUST be read from `@AppStorage`. This is a global setting shared across all terminal windows.
- **profile-fallback-default**: If the stored active profile ID is invalid (not found among available profiles), the window MUST fall back to the first built-in profile (Solarized Dark), as specified in `ui/color-profile.md` fallback-to-default.

### Relationship to project window

- **shared-terminal-spec**: The standalone terminal window and the project window's embedded terminal pane MUST share the same terminal-pane spec (`ui/Recipes/terminal-pane.md`) for all terminal behavior — PTY lifecycle, session management, terminal rendering, OSC handling, and session list display.
- **independent-sessions**: Each standalone terminal window MUST have its own `SessionManager` instance. Sessions MUST NOT be shared between standalone terminal windows or between standalone terminal windows and project windows.

### Delegation to sub-components

- **delegate-session-list**: The session list sidebar MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) sidebar-session-list through row-context-menu for session list behavior (row display, selection binding, add button, context menu).
- **delegate-terminal-view**: The terminal view MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) nsview-representable through palette-color-structure for terminal rendering, reparenting, and profile application.
- **delegate-empty-state**: The empty state MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) empty-state-no-sessions for display when no sessions exist.

## Appearance

### Window layout

```
┌──────────────┬─────────────────────────────────────────┐
│ Sessions [+] │                                         │
├──────────────┤                                         │
│              │                                         │
│ ● Session 1  │  user@host ~ %                          │
│   ~/projects │  ls -la                                 │
│   main       │  total 42                               │
│   zsh        │  drwxr-xr-x  5 user staff  160 ...     │
│              │  -rw-r--r--  1 user staff  230 ...     │
│ ○ Session 2  │                                         │
│   ~/docs     │                                         │
│   bash       │                                         │
│              │                                         │
│              │                                         │
│              │                                         │
└──────────────┴─────────────────────────────────────────┘
```

- **Window minimum size**: 600 x 400pt
- **Session sidebar width**: 150–200pt, resizable within that range
- **Terminal view**: Fills remaining width
- **Terminal background**: Determined by active color profile
- **Terminal font**: Determined by active color profile (monospaced)
- **Sidebar appearance**: Standard sidebar material, matching the terminal-pane session list style

## States

| State | Behavior |
|-------|----------|
| Window opened, no sessions | Default session created automatically on appear; terminal view shows shell prompt |
| One or more sessions, one selected | Selected session's terminal view reparented into container; sidebar highlights selected row |
| Session added | New session appended, selected, terminal view shown |
| Session removed | PTY terminated, smart selection applied (previous > next > nil per terminal-pane remove-smart-select) |
| All sessions removed | Empty state displayed (per terminal-pane empty-state-no-sessions); next session creation re-populates |
| Profile changed | Colors/font applied to terminal view without reparenting |
| Profile deleted while in use | Falls back to Solarized Dark (per color-profile fallback-to-default) |
| Window closing | `terminateAll()` called; all PTYs cleaned up |
| Multiple standalone windows open | Each window operates independently with its own session manager |

## Accessibility

- **inherit-pane-accessibility**: The standalone terminal window MUST inherit all accessibility requirements from the terminal-pane spec (keyboard-nav-sessions through terminated-announce), including keyboard-navigable session list, accessible labels, VoiceOver support, and screen reader announcements.
- **accessible-window-title**: The window MUST have an accessible window title that distinguishes it from project windows (e.g., "Terminal" or "Terminal — Session Name").

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| stw-001 | window-group-terminal | Inspect SwiftUI scene declaration | `WindowGroup(id: "terminal")` is registered |
| stw-002 | hsplit-sidebar-terminal | Open a standalone terminal window | HSplitView renders with session sidebar (left) and terminal view (right) |
| stw-003 | sidebar-width-range | Inspect session sidebar width | Width is between 150pt and 200pt |
| stw-004 | persist-window-frame | Open terminal window, move to (300, 200), close, reopen | Window restores at (300, 200); autosave name is "terminal-window" |
| stw-005 | min-size-constraints | Attempt to resize window below 600x400 | Window enforces minimum size constraints |
| stw-006 | own-session-manager | Open a standalone terminal window and a project window | Each has its own SessionManager instance; adding a session in one does not affect the other |
| stw-007 | auto-create-default | Open a standalone terminal window for the first time | A default session ("Session 1") is created automatically; terminal shows shell prompt |
| stw-008 | terminate-on-close | Open window with 3 sessions, close window | All 3 PTYs terminated |
| stw-009 | focused-object-dispatch | Open two standalone terminal windows, focus window 1, invoke "New Session" menu | Session created in window 1's session manager only (via focusedObject dispatch) |
| stw-010 | apply-active-profile, global-profile-storage | Set active profile to Dracula, open terminal window | Terminal renders with Dracula colors (#282a36 background, #f8f8f2 foreground) |
| stw-011 | profile-fallback-default | Set active profile ID in AppStorage to an invalid UUID, open terminal window | Terminal falls back to Solarized Dark (#002b36 background, #839496 foreground) |
| stw-012 | shared-terminal-spec | Compare terminal behavior in standalone window vs. project window terminal pane | Identical PTY lifecycle, OSC handling, session list, and rendering behavior |
| stw-013 | independent-sessions | Open two standalone terminal windows, create sessions in each | Sessions are independent; removing a session in window A does not affect window B |
| stw-014 | auto-create-default | Open window, remove all sessions, no auto-creation on removal | Empty state displayed; auto-creation only happens on initial appear |
| stw-015 | delegate-session-list, delegate-terminal-view | Open window, create multiple sessions, switch between them | Session list displays rows per terminal-pane spec; reparenting preserves scrollback |
| stw-016 | accessible-window-title | Enable VoiceOver, open terminal window | Window title announced as "Terminal" (or similar), distinguishable from project windows |

## Edge Cases

- **Last session closed by user**: When the user closes the last session, the empty state is displayed. A new session is NOT automatically created — auto-creation only occurs on initial `onAppear` when the session list is empty. The user must click the "+" button or "New Session" to create a new session.
- **Profile deleted while in use**: If the active profile is a custom profile that gets deleted while a standalone terminal window is open, the window MUST fall back to Solarized Dark immediately (per color-profile fallback-to-default). Terminal colors update without reparenting.
- **Multiple standalone terminal windows**: Each window has its own `SessionManager` instance. Opening N standalone terminal windows results in N independent session managers. Menu commands dispatch to the focused window's session manager via `.focusedObject()`.
- **Standalone window and project window open simultaneously**: Both function independently. Changing the active color profile affects all terminal views across both window types (since profile ID is stored in `@AppStorage`, a global setting).
- **Window restored after crash**: Session manager MUST NOT attempt to restore PTY sessions from a previous run. Sessions are ephemeral. On relaunch, the window opens with no sessions, and the `onAppear` auto-creation logic creates a fresh default session.
- **Rapid window open/close**: `terminateAll()` MUST complete cleanly. PTY file descriptors MUST be closed. No zombie processes should remain.
- **Window opened with no shell available**: Falls back to `/bin/zsh` per terminal-pane edge case (shell not found). The standalone terminal window does not add additional fallback logic beyond what terminal-pane provides.
- **Very many sessions in one window (50+)**: Session list MUST remain scrollable and performant (delegated to terminal-pane edge case handling).
- **Frame persistence for multiple standalone windows**: All standalone terminal windows share the autosave name `"terminal-window"`. This means only one window's frame is persisted. If multiple standalone windows are needed with independent frame persistence, a future revision MAY introduce per-window identifiers.
- **visionOS window placement**: On visionOS, the system manages window placement. Frame persistence (persist-window-frame) is a no-op on visionOS. Minimum size constraints still apply.
- **focusedObject not set**: If menu commands fire before any standalone terminal window is focused, the system's `FocusedValues` will not contain a session manager. Menu commands MUST be disabled when no session manager is available in the focused values.

## Logging

Subsystem: `{{bundle_id}}` | Category: `StandaloneTerminalWindow`

| Event | Level | Message |
|-------|-------|---------|
| Window opened | info | `StandaloneTerminalWindow: opened` |
| Window closed | info | `StandaloneTerminalWindow: closed` |
| Default session created | debug | `StandaloneTerminalWindow: created default session on appear` |
| All sessions terminated | debug | `StandaloneTerminalWindow: all sessions terminated (window closing)` |
| Profile applied | debug | `StandaloneTerminalWindow: applied profile "{{profileName}}" ({{profileId}})` |
| Profile fallback | debug | `StandaloneTerminalWindow: invalid active profile ID, falling back to Solarized Dark` |
| Focused object set | debug | `StandaloneTerminalWindow: session manager set as focusedObject` |
| Frame autosave set | debug | `StandaloneTerminalWindow: frame autosave name "terminal-window"` |

## Platform Notes

- **SwiftUI (macOS)**: Declare the window scene as `WindowGroup(id: "terminal") { StandaloneTerminalView() }`. Inside `StandaloneTerminalView`, create a `@StateObject var sessionManager = SessionManager()`. Use `HSplitView` with the session list sidebar (per terminal-pane sidebar-session-list through row-context-menu) on the left and the terminal view (per terminal-pane nsview-representable through palette-color-structure) on the right. Apply `.frame(minWidth: 150, maxWidth: 200)` on the sidebar and `.frame(maxWidth: .infinity)` on the terminal view. Set `.frame(minWidth: 600, minHeight: 400)` on the window content. Attach `.background(WindowAccessor(name: "terminal-window", onClose: { sessionManager.terminateAll() }))` for frame persistence and close handling. Publish the session manager via `.focusedObject(sessionManager)` so menu commands dispatch correctly. Read the active profile ID from `@AppStorage("activeProfileId")` and resolve the profile via `TerminalProfile.activeProfile()` with Solarized Dark fallback. On `onAppear`, check `sessionManager.sessions.isEmpty` and call `sessionManager.addSession()` if true.
- **SwiftUI (visionOS)**: Same scene and view structure as macOS. The window opens as a standard visionOS window volume. `HSplitView` renders within the window. Frame persistence is not applicable — visionOS manages window placement. Minimum size constraints are respected by the system. Session sidebar may use `NavigationSplitView` with the session list in the sidebar column for better visionOS integration, as noted in terminal-pane platform notes.

## Privacy

- **Data collected**: Terminal output is rendered in-memory by SwiftTerm. No terminal content is stored to disk.
- **Storage**: Active profile ID stored in `@AppStorage` (UserDefaults). Window frame position stored via `NSWindow.setFrameAutosaveName` on macOS.
- **Transmission**: None — terminal content never leaves the device.
- **Retention**: Session data exists only for the lifetime of the window. Profile preference persists until changed. Frame position persists until changed or app is uninstalled.

## Design Decisions

_None yet — decisions made during implementation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
