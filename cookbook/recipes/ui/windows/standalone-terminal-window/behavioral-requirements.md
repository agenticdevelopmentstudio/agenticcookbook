
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

