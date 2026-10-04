
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

### New Project flow

- **open-panel-directory-mode**: "New Project" MUST open an `NSOpenPanel` configured for directory selection (`canChooseDirectories = true`, `canChooseFiles = false`).
- **validate-git-directory**: The selected directory MUST be validated to contain a `.git` directory. If the `.git` directory is not present, the command MUST show an error alert with a clear message (e.g., "The selected folder is not a Git repository. Please select a folder that contains a .git directory.").
- **open-existing-package**: If a project package already exists at the expected path (`{selected_dir}/{dir_name}.{extension}`), the command MUST open the existing package instead of creating a duplicate.
- **create-new-package**: If no existing package is found, the command MUST create a new project package at `{selected_dir}/{dir_name}.{extension}` following the package-document spec (see dependency `package-document.md@1.0.0`).
- **open-via-document-controller**: After creation or discovery of an existing package, the command MUST open the document via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **show-creation-error-alert**: If document creation or opening fails, the command MUST show an error alert with the failure reason.

### New Workspace flow

- **workspace-save-panel**: "New Workspace" MUST open an `NSSavePanel` for file creation.
- **enforce-workspace-extension**: The save panel MUST enforce the workspace file extension (e.g., `.catnip-workspace`) via `allowedContentTypes` set to the workspace UTType.
- **create-workspace-package**: After the user confirms the save location, the command MUST create a new workspace package at the chosen path following the package-document spec.
- **open-workspace-document**: After creation, the command MUST open the new document via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **show-workspace-error-alert**: If document creation or opening fails, the command MUST show an error alert with the failure reason.

### New Session flow

- **create-session-in-window**: "New Session" MUST create a new session within the currently focused project window.
- **focused-object-project-state**: The command MUST use `@FocusedObject` to access the current window's project state.
- **disable-without-project**: If no focused object is available (no project window focused), the menu item MUST be disabled (grayed out).

### Per-window command dispatch

- **focused-object-dispatch**: Commands that operate on the current window MUST use `@FocusedObject` to access per-window state.
- **provide-focused-object**: Views MUST provide their per-window state via the `.focusedObject()` modifier on the view hierarchy.
- **graceful-nil-focused-object**: Commands MUST gracefully handle a `nil` focused object by disabling the menu item, not by crashing or showing an error.

