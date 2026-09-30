<!-- leaf: recipes-ui/windows-standalone-terminal-window · source: recipes/ui/windows/standalone-terminal-window.md -->

**Rules** (cite as `recipes-ui/windows-standalone-terminal-window#<slug>`):

- `window-group-terminal` MUST
- `hsplit-sidebar-terminal` MUST
- `sidebar-width-range` MUST
- `persist-window-frame` MUST
- `min-size-constraints` MUST
- `own-session-manager` MUST
- `auto-create-default` MUST
- `terminate-on-close` MUST
- `focused-object-dispatch` MUST
- `apply-active-profile` MUST
- `global-profile-storage` MUST
- `profile-fallback-default` MUST
- `shared-terminal-spec` MUST
- `independent-sessions` MUST
- `delegate-session-list` MUST
- `delegate-terminal-view` MUST
- `delegate-empty-state` MUST
- `inherit-pane-accessibility` MUST
- `accessible-window-title` MUST

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

- **delegate-session-list**: The session list sidebar MUST delegate to terminal-pane.md sidebar-session-list through row-context-menu for session list behavior (row display, selection binding, add button, context menu).
- **delegate-terminal-view**: The terminal view MUST delegate to terminal-pane.md nsview-representable through palette-color-structure for terminal rendering, reparenting, and profile application.
- **delegate-empty-state**: The empty state MUST delegate to terminal-pane.md empty-state-no-sessions for display when no sessions exist.

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

## Accessibility

- **inherit-pane-accessibility**: The standalone terminal window MUST inherit all accessibility requirements from the terminal-pane spec (keyboard-nav-sessions through terminated-announce), including keyboard-navigable session list, accessible labels, VoiceOver support, and screen reader announcements.
- **accessible-window-title**: The window MUST have an accessible window title that distinguishes it from project windows (e.g., "Terminal" or "Terminal — Session Name").

## Platform Notes

- **SwiftUI (macOS)**: Declare the window scene as `WindowGroup(id: "terminal") { StandaloneTerminalView() }`. Inside `StandaloneTerminalView`, create a `@StateObject var sessionManager = SessionManager()`. Use `HSplitView` with the session list sidebar (per terminal-pane sidebar-session-list through row-context-menu) on the left and the terminal view (per terminal-pane nsview-representable through palette-color-structure) on the right. Apply `.frame(minWidth: 150, maxWidth: 200)` on the sidebar and `.frame(maxWidth: .infinity)` on the terminal view. Set `.frame(minWidth: 600, minHeight: 400)` on the window content. Attach `.background(WindowAccessor(name: "terminal-window", onClose: { sessionManager.terminateAll() }))` for frame persistence and close handling. Publish the session manager via `.focusedObject(sessionManager)` so menu commands dispatch correctly. Read the active profile ID from `@AppStorage("activeProfileId")` and resolve the profile via `TerminalProfile.activeProfile()` with Solarized Dark fallback. On `onAppear`, check `sessionManager.sessions.isEmpty` and call `sessionManager.addSession()` if true.
- **SwiftUI (visionOS)**: Same scene and view structure as macOS. The window opens as a standard visionOS window volume. `HSplitView` renders within the window. Frame persistence is not applicable — visionOS manages window placement. Minimum size constraints are respected by the system. Session sidebar may use `NavigationSplitView` with the session list in the sidebar column for better visionOS integration, as noted in terminal-pane platform notes.

## Privacy

- **Data collected**: Terminal output is rendered in-memory by SwiftTerm. No terminal content is stored to disk.
- **Storage**: Active profile ID stored in `@AppStorage` (UserDefaults). Window frame position stored via `NSWindow.setFrameAutosaveName` on macOS.
- **Transmission**: None — terminal content never leaves the device.
- **Retention**: Session data exists only for the lifetime of the window. Profile preference persists until changed. Frame position persists until changed or app is uninstalled.
