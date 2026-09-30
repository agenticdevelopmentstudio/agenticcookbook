<!-- leaf: recipes-app/menu-commands · source: recipes/app/menu-commands.md -->

**Rules** (cite as `recipes-app/menu-commands#<slug>`):

- `replace-default-new-item` MUST
- `creation-command-order` MUST
- `unique-keyboard-shortcuts` MUST
- `sf-symbol-icons` MUST
- `disable-without-focus` MUST
- `open-panel-directory-mode` MUST
- `validate-git-directory` MUST
- `open-existing-package` MUST
- `create-new-package` MUST
- `open-via-document-controller` MUST
- `show-creation-error-alert` MUST
- `workspace-save-panel` MUST
- `enforce-workspace-extension` MUST
- `create-workspace-package` MUST
- `open-workspace-document` MUST
- `show-workspace-error-alert` MUST
- `create-session-in-window` MUST
- `focused-object-project-state` MUST
- `disable-without-project` MUST
- `focused-object-dispatch` MUST
- `provide-focused-object` MUST
- `graceful-nil-focused-object` MUST
- `voiceover-menu-access` MUST
- `voiceover-error-announce` MUST
- `disabled-state-assistive` MUST
- `voiceover-shortcut-passthrough` MUST

# Menu Commands

## Overview

Pattern for structuring platform menu commands with keyboard shortcuts, including document creation flows with file/directory pickers and validation. The app replaces the default "New" menu item with app-specific creation commands (New Project, New Session, New Workspace), each with a distinct keyboard shortcut and SF Symbol icon. Document creation commands open platform file pickers (NSOpenPanel for directory selection, NSSavePanel for file creation), validate the selection, and open the resulting document via NSDocumentController. Per-window commands use the `@FocusedObject` pattern to dispatch actions to the currently focused window's state, gracefully disabling menu items when no window is focused.

## Terminology

| Term | Definition |
|------|-----------|
| Menu command | A user-invocable action exposed in the app's menu bar, typically with a keyboard shortcut |
| Keyboard shortcut | A modifier key combination (e.g., Cmd-N) bound to a menu command |
| CommandGroup | A SwiftUI struct that defines or replaces a group of menu items in the app's menu bar |
| @FocusedObject | A SwiftUI property wrapper that reads an observable object provided by the currently focused window via `.focusedObject()` |
| NSOpenPanel | A macOS panel for selecting existing files or directories |
| NSSavePanel | A macOS panel for choosing a save location and filename for a new file |
| NSDocumentController | The macOS singleton that manages the app's open documents and coordinates document lifecycle |
| SF Symbol | A system-provided icon from Apple's SF Symbols library, used for menu item imagery |
| Package document | A directory bundle presented as a single file in Finder, as defined in package-document.md |

## Architecture

```
┌──────────────────────────────────────────────────────┐
│  App (SwiftUI)                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Commands {                                       │ │
│  │    CommandGroup(replacing: .newItem) {             │ │
│  │      ┌─────────────────────────────────────────┐  │ │
│  │      │  "New Project"    Cmd-N                  │  │ │
│  │      │  "New Session"    Cmd-Shift-N            │  │ │
│  │      │  "New Workspace"  Cmd-Option-N           │  │ │
│  │      └─────────────────────────────────────────┘  │ │
│  │    }                                              │ │
│  │  }                                                │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌────────────────────────┐  ┌───────────────────────┐ │
│  │  Window A               │  │  Window B              │ │
│  │  .focusedObject(stateA) │  │  .focusedObject(stateB)│ │
│  └────────────────────────┘  └───────────────────────┘ │
│               ▲                                        │
│               │ @FocusedObject                         │
│  ┌────────────┴─────────────────────────────────────┐ │
│  │  "New Session" reads focused window's state       │ │
│  │  to create session within that window's project   │ │
│  └──────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘

New Project flow:
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌──────────────┐
│ Menu item │───▶│ NSOpenPanel│───▶│ Validate  │───▶│ Create & Open│
│ Cmd-N     │    │ (dir pick) │    │ directory  │    │ document     │
└──────────┘    └───────────┘    └───────────┘    └──────────────┘
                                       │
                                  ┌────▼─────┐
                                  │ .git?    │
                                  │ existing │
                                  │ package? │
                                  └──────────┘

New Workspace flow:
┌──────────┐    ┌───────────┐    ┌──────────────┐
│ Menu item │───▶│ NSSavePanel│───▶│ Create & Open│
│ Cmd-Opt-N │    │ (file save)│    │ document     │
└──────────┘    └───────────┘    └──────────────┘
```

## Behavioral Requirements

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

## Appearance

- **Menu item icons**: SF Symbols rendered at standard menu item size (per system conventions)
- **Keyboard shortcut display**: Standard macOS menu shortcut rendering (modifier glyphs + key character)
- **Error alerts**: Standard `NSAlert` / SwiftUI `.alert` with title, message, and "OK" button
- **NSOpenPanel**: Standard macOS directory picker with prompt text "Select Project Directory"
- **NSSavePanel**: Standard macOS save dialog with prompt text "Create Workspace" and enforced file extension

## Accessibility

- **voiceover-menu-access**: All menu items MUST be accessible via VoiceOver with their full title (e.g., "New Project, Command N").
- **voiceover-error-announce**: Error alerts MUST be announced by VoiceOver when they appear.
- **disabled-state-assistive**: Disabled menu items MUST convey their disabled state to assistive technologies.
- **voiceover-shortcut-passthrough**: All menu keyboard shortcuts MUST be functional when VoiceOver is active, using VoiceOver's pass-through mechanism for keyboard commands.

