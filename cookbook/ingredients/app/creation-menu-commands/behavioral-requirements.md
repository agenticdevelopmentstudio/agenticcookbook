
### Menu structure

- **replace-default-new-item**: The app MUST replace the default "New" menu item with app-specific creation commands using `CommandGroup(replacing: .newItem)`.
- **creation-command-order**: The menu MUST contain the following creation commands in order: "New Project", "New Session", "New Workspace".
- **unique-keyboard-shortcuts**: Each creation command MUST have a unique keyboard shortcut:
  - New Project: Cmd-N (primary creation action)
  - New Session: Cmd-Shift-N (secondary, within current window)
  - New Workspace: Cmd-Option-N (tertiary)
- **sf-symbol-icons**: Each menu item MUST display an SF Symbol icon on macOS:
  - New Project: a project-appropriate symbol (e.g., `folder.badge.plus`)
  - New Session: a session-appropriate symbol (e.g., `terminal`)
  - New Workspace: a workspace-appropriate symbol (e.g., `square.grid.2x2`)
- **disable-without-focus**: Menu items that require a focused window (e.g., "New Session") MUST be disabled when no window is focused.

### New Session flow

- **create-session-in-window**: "New Session" MUST create a new session within the currently focused project window.
- **focused-object-project-state**: The command MUST use `@FocusedObject` to access the current window's project state.
- **disable-without-project**: If no focused object is available (no project window focused), the menu item MUST be disabled (grayed out).

### Per-window command dispatch

- **focused-object-dispatch**: Commands that operate on the current window MUST use `@FocusedObject` to access per-window state.
- **provide-focused-object**: Views MUST provide their per-window state via the `.focusedObject()` modifier on the view hierarchy.
- **graceful-nil-focused-object**: Commands MUST gracefully handle a `nil` focused object by disabling the menu item, not by crashing or showing an error.

