
### Window structure

- **window-group-terminal**: The window MUST use a `WindowGroup(id: "terminal")` scene declaration.
- **persist-window-frame**: The window frame MUST be persisted using the window-frame-persistence component (the `window-frame-persistence` ingredient). The autosave name MUST be `"terminal-window"`.
- **min-size-constraints**: The window MUST enforce minimum size constraints: minWidth 600pt, minHeight 400pt.

### Terminal view and profile

- **apply-active-profile**: The terminal view MUST apply the active color profile (colors, font, cursor style) from `TerminalProfile.activeProfile()`.
- **global-profile-storage**: The active profile ID MUST be read from `@AppStorage`. This is a global setting shared across all terminal windows.
- **profile-fallback-default**: If the stored active profile ID is invalid (not found among available profiles), the window MUST fall back to the first built-in profile (Solarized Dark), as specified in `color-profile` ingredient fallback-to-default.

### Relationship to project window

- **shared-terminal-spec**: The standalone terminal window and the project window's embedded terminal pane MUST share the same terminal-pane spec (`terminal-pane` ingredient) for all terminal behavior — PTY lifecycle, session management, terminal rendering, OSC handling, and session list display.

### Delegation to sub-components

- **delegate-session-list**: The session list sidebar MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) sidebar-session-list through row-context-menu for session list behavior (row display, selection binding, add button, context menu).
- **delegate-terminal-view**: The terminal view MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) nsview-representable through palette-color-structure for terminal rendering, reparenting, and profile application.
- **delegate-empty-state**: The empty state MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) empty-state-no-sessions for display when no sessions exist.

### Wiring

- **scene-hosts-shell**: The `WindowGroup(id: "terminal")` scene MUST host the Terminal Window Shell as its only content.
- **profile-reaches-terminal-view**: The profile resolved through the color-profile ingredient MUST be passed to the terminal-pane terminal view, and a profile change MUST update colors and font without reparenting the view.
- **frame-key-fixed**: The window frame autosave name MUST be the fixed string `"terminal-window"` regardless of how many shells are open.

### Accessibility

- **accessible-window-title**: The window MUST have an accessible window title that distinguishes it from project windows (e.g., "Terminal" or "Terminal — Session Name").

