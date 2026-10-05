---
id: DE88E58F-7260-4089-B0E3-9485D6B4BC79
title: "Terminal Window Shell"
domain: agenticdevelopercookbook://ingredients/ui/windows/terminal-window-shell
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Session-sidebar and terminal split with a per-window session manager, auto-created default session, and terminate-on-close"
platforms:
  - macos
  - swift
  - windows
tags:
  - session-manager
  - terminal
  - ui
  - window
depends-on:
  - agenticdevelopercookbook://ingredients/ui/panels/terminal-pane
related:
  - agenticdevelopercookbook://recipes/ui/windows/standalone-terminal-window
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Terminal Window Shell

## Overview

A session-sidebar-plus-terminal shell that owns its own session manager. An HSplitView holds the session list (left) and the terminal view (right); the shell creates a default session on first appear, terminates every session when it closes, and publishes its session manager as the focused object so menu commands reach the right window. Terminal behavior itself (PTY sessions, session list rows, rendering, profiles) is delegated to the terminal-pane ingredient; each shell instance is completely independent, with no session sharing between windows.

### Terminology

| Term | Definition |
|------|-----------|
| Standalone terminal window | A top-level window containing only a session sidebar and terminal view, not embedded in a project window |
| Session sidebar | The left panel listing all terminal sessions owned by this window's session manager |
| Session manager | A per-window controller owning an ordered list of sessions — see `terminal-pane` ingredient per-window-manager |
| Terminal view | The rendering surface for the selected session — see `terminal-pane` ingredient nsview-representable through palette-color-structure |
| Active profile | The currently selected color profile applied to terminal rendering — see `color-profile` ingredient single-active-profile |
| Window scene | A SwiftUI `WindowGroup` identified by a string, used to open and manage window instances |

## Behavioral Requirements

### Window structure

- **hsplit-sidebar-terminal**: The window MUST use an HSplitView with two sections: session list sidebar (left) and terminal view (right).
- **sidebar-width-range**: The session list sidebar MUST have a width between 150pt and 200pt.

### Session management

- **own-session-manager**: The window MUST create its own `SessionManager` instance as a `@StateObject`. This instance MUST be independent from any project window's session manager.
- **auto-create-default**: On window appear (`onAppear`), if the session manager contains no sessions, a default session MUST be created automatically by calling `addSession()`.
- **terminate-on-close**: On window close, all sessions MUST be terminated by calling `terminateAll()` on the session manager.
- **focused-object-dispatch**: The session manager MUST be provided as `.focusedObject()` so that menu commands (New Session, Close Session, etc.) can dispatch to the correct window's session manager.

### Relationship to project window

- **independent-sessions**: Each standalone terminal window MUST have its own `SessionManager` instance. Sessions MUST NOT be shared between standalone terminal windows or between standalone terminal windows and project windows.

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
| Window closing | `terminateAll()` called; all PTYs cleaned up |
| Multiple standalone windows open | Each window operates independently with its own session manager |

## Accessibility

- **inherit-pane-accessibility**: The standalone terminal window MUST inherit all accessibility requirements from the terminal-pane spec (keyboard-nav-sessions through terminated-announce), including keyboard-navigable session list, accessible labels, VoiceOver support, and screen reader announcements.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| stw-002 | hsplit-sidebar-terminal | Open a standalone terminal window | HSplitView renders with session sidebar (left) and terminal view (right) |
| stw-003 | sidebar-width-range | Inspect session sidebar width | Width is between 150pt and 200pt |
| stw-006 | own-session-manager | Open a standalone terminal window and a project window | Each has its own SessionManager instance; adding a session in one does not affect the other |
| stw-007 | auto-create-default | Open a standalone terminal window for the first time | A default session ("Session 1") is created automatically; terminal shows shell prompt |
| stw-008 | terminate-on-close | Open window with 3 sessions, close window | All 3 PTYs terminated |
| stw-009 | focused-object-dispatch | Open two standalone terminal windows, focus window 1, invoke "New Session" menu | Session created in window 1's session manager only (via focusedObject dispatch) |
| stw-013 | independent-sessions | Open two standalone terminal windows, create sessions in each | Sessions are independent; removing a session in window A does not affect window B |
| stw-014 | auto-create-default | Open window, remove all sessions, no auto-creation on removal | Empty state displayed; auto-creation only happens on initial appear |
| stw-015 | delegate-session-list, delegate-terminal-view | Open window, create multiple sessions, switch between them | Session list displays rows per terminal-pane spec; reparenting preserves scrollback |

## Edge Cases

- **Last session closed by user**: When the user closes the last session, the empty state is displayed. A new session is NOT automatically created — auto-creation only occurs on initial `onAppear` when the session list is empty. The user must click the "+" button or "New Session" to create a new session.
- **Multiple standalone terminal windows**: Each window has its own `SessionManager` instance. Opening N standalone terminal windows results in N independent session managers. Menu commands dispatch to the focused window's session manager via `.focusedObject()`.
- **Window restored after crash**: Session manager MUST NOT attempt to restore PTY sessions from a previous run. Sessions are ephemeral. On relaunch, the window opens with no sessions, and the `onAppear` auto-creation logic creates a fresh default session.
- **Rapid window open/close**: `terminateAll()` MUST complete cleanly. PTY file descriptors MUST be closed. No zombie processes should remain.
- **Window opened with no shell available**: Falls back to `/bin/zsh` per terminal-pane edge case (shell not found). The standalone terminal window does not add additional fallback logic beyond what terminal-pane provides.
- **Very many sessions in one window (50+)**: Session list MUST remain scrollable and performant (delegated to terminal-pane edge case handling).
- **focusedObject not set**: If menu commands fire before any standalone terminal window is focused, the system's `FocusedValues` will not contain a session manager. Menu commands MUST be disabled when no session manager is available in the focused values.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `sidebarWidthRange` | range (pt) | 150–200 | Resizable width range of the session list sidebar |
| `autoCreateDefaultSession` | Bool | `true` | Create a default session on initial appear when the manager is empty; never on later removal |
| `sessionManagerScope` | enum | per window | Each shell instance owns its own session manager |

## Privacy

- **Data collected**: Terminal output is rendered in-memory by SwiftTerm. No terminal content is stored to disk.
- **Storage**: Active profile ID stored in `@AppStorage` (UserDefaults). Window frame position stored via `NSWindow.setFrameAutosaveName` on macOS.
- **Transmission**: None — terminal content never leaves the device.
- **Retention**: Session data exists only for the lifetime of the window. Profile preference persists until changed. Frame position persists until changed or app is uninstalled.

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

- **SwiftUI (macOS)**: Inside the shell view, create a `@StateObject var sessionManager = SessionManager()`. Use `HSplitView` with the session list sidebar (per terminal-pane sidebar-session-list through row-context-menu) on the left and the terminal view (per terminal-pane nsview-representable through palette-color-structure) on the right. Apply `.frame(minWidth: 150, maxWidth: 200)` on the sidebar and `.frame(maxWidth: .infinity)` on the terminal view. Publish the session manager via `.focusedObject(sessionManager)` so menu commands dispatch correctly. On `onAppear`, check `sessionManager.sessions.isEmpty` and call `sessionManager.addSession()` if true.
- **SwiftUI (visionOS)**: Same view structure. `HSplitView` renders within the window. The session sidebar may use `NavigationSplitView` with the session list in the sidebar column for better visionOS integration, as noted in terminal-pane platform notes.
- **Compose**: Use a `Row` with a fixed-range sidebar `Column` of sessions and a terminal surface. Hold the session manager in a `remember`ed holder scoped to the window and call terminate-all in `DisposableEffect`'s `onDispose`.
- **React/Web**: Use a two-column layout with the session list in a resizable sidebar. Create the session manager in a window-scoped context provider; terminate all sessions on unmount or `beforeunload`.

## Design Decisions

**Decision**: Own the session manager in the shell and delegate every terminal behavior to the terminal-pane ingredient.
**Rationale**: A single terminal-pane spec keeps PTY lifecycle, OSC handling, and rendering identical between the standalone window and the project window (single source of truth).
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [privacy](agenticdevelopercookbook://guidelines/implementing/security/privacy) | partial | Privacy |
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Standalone Terminal Window recipe |
