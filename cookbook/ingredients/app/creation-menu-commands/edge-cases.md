
- **No window focused**: Global commands (New Project, New Workspace) remain enabled. Per-window commands (New Session) are disabled via `@FocusedObject` returning nil. This is the expected state at app launch before any document is opened.
- **Workspace window focused when pressing Cmd-Shift-N**: The @FocusedObject for project state is nil (workspace windows do not provide project state), so the menu item is disabled.

