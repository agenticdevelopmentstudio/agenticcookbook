---
id: 81410d5e-e3df-4feb-a9b1-bbc97abfc798
title: "Menu Commands"
domain: agenticdevelopercookbook://recipes/app/menu-commands
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pattern for platform menu commands with keyboard shortcuts and document creation flows via file pickers"
platforms:
  - macos
  - swift
  - windows
tags:
  - app
  - menu-commands
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

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

## States

| State | Behavior |
|-------|----------|
| No window focused | Per-window commands (New Session) are disabled. Global commands (New Project, New Workspace) remain enabled |
| Project window focused | All commands are enabled. New Session operates on the focused window's project |
| Workspace window focused | New Session is disabled (sessions belong to projects). New Project and New Workspace remain enabled |
| NSOpenPanel displayed | User is selecting a directory for New Project. Other menu commands are blocked by the modal panel |
| NSSavePanel displayed | User is choosing a save location for New Workspace. Other menu commands are blocked by the modal panel |
| Directory validation failed | Error alert displayed with reason. User can dismiss and retry |
| Existing package found | Package at expected path is opened instead of creating a duplicate |
| Document creation in progress | Package is being created on disk. Menu command is non-reentrant (no double-creation) |
| Document open failed | Error alert displayed with failure reason. No document window opens |

## Accessibility

- **voiceover-menu-access**: All menu items MUST be accessible via VoiceOver with their full title (e.g., "New Project, Command N").
- **voiceover-error-announce**: Error alerts MUST be announced by VoiceOver when they appear.
- **disabled-state-assistive**: Disabled menu items MUST convey their disabled state to assistive technologies.
- **voiceover-shortcut-passthrough**: All menu keyboard shortcuts MUST be functional when VoiceOver is active, using VoiceOver's pass-through mechanism for keyboard commands.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-001 | replace-default-new-item, creation-command-order | Open the File menu | Default "New" item is replaced with "New Project", "New Session", "New Workspace" in that order |
| mc-002 | unique-keyboard-shortcuts | Press Cmd-N | "New Project" flow initiates (NSOpenPanel appears) |
| mc-003 | unique-keyboard-shortcuts | Press Cmd-Shift-N with a project window focused | "New Session" creates a session in the focused project |
| mc-004 | unique-keyboard-shortcuts | Press Cmd-Option-N | "New Workspace" flow initiates (NSSavePanel appears) |
| mc-005 | sf-symbol-icons | Open the File menu on macOS | Each creation command displays its SF Symbol icon |
| mc-006 | disable-without-focus, disable-without-project, graceful-nil-focused-object | Press Cmd-Shift-N with no window focused | Menu item is disabled; nothing happens |
| mc-007 | open-panel-directory-mode | Trigger "New Project" | NSOpenPanel opens with directory selection enabled and file selection disabled |
| mc-008 | validate-git-directory | Select a directory without a .git subdirectory | Error alert appears: "The selected folder is not a Git repository." |
| mc-009 | validate-git-directory | Select a directory containing a .git subdirectory | Validation passes; flow proceeds to package creation or opening |
| mc-010 | open-existing-package, open-via-document-controller | Select a directory that already contains `dirname.catnip-proj` | Existing package is opened; no new package created |
| mc-011 | create-new-package, open-via-document-controller | Select a valid git directory with no existing package | New package created at `{dir}/{dirname}.{ext}`; document opens |
| mc-012 | show-creation-error-alert | Select a directory where package creation fails (e.g., read-only filesystem) | Error alert displayed with failure reason |
| mc-013 | workspace-save-panel, enforce-workspace-extension | Trigger "New Workspace" | NSSavePanel opens with workspace file extension enforced |
| mc-014 | create-workspace-package, open-workspace-document | Confirm save location in NSSavePanel | Workspace package created at chosen path; document opens |
| mc-015 | show-workspace-error-alert | Confirm save location on a read-only volume | Error alert displayed with failure reason |
| mc-016 | create-session-in-window, focused-object-project-state | Press Cmd-Shift-N with project window focused | New session created in the focused project |
| mc-017 | focused-object-dispatch, provide-focused-object | Focus Window A, press Cmd-Shift-N, then focus Window B, press Cmd-Shift-N | Session created in Window A's project first, then in Window B's project |
| mc-018 | graceful-nil-focused-object | Focus a non-project window (e.g., settings), press Cmd-Shift-N | Menu item is disabled; no action taken |
| mc-019 | voiceover-menu-access | Enable VoiceOver, navigate to File menu | VoiceOver announces each menu item with title and shortcut |
| mc-020 | voiceover-error-announce | Trigger validation error with VoiceOver enabled | VoiceOver announces the error alert |

## Edge Cases

- **No window focused**: Global commands (New Project, New Workspace) remain enabled. Per-window commands (New Session) are disabled via `@FocusedObject` returning nil. This is the expected state at app launch before any document is opened.
- **Directory without .git**: Validation fails with a clear error alert. The user is not prevented from dismissing the alert and retrying with a different directory.
- **Duplicate project package**: If `{dir}/{dirname}.{ext}` already exists, the existing package is opened. This prevents creating multiple packages for the same project directory.
- **Permissions denied**: If the app lacks read permission on the selected directory, the validation step MUST fail gracefully with an error alert (e.g., "Cannot access the selected folder. Check Finder permissions."). If write permission is denied when creating a package, the creation step MUST fail with an error alert.
- **NSOpenPanel cancelled**: If the user clicks Cancel in the NSOpenPanel, the command MUST silently abort with no error or side effect.
- **NSSavePanel cancelled**: If the user clicks Cancel in the NSSavePanel, the command MUST silently abort with no error or side effect.
- **Rapid repeated invocation**: If the user presses Cmd-N multiple times quickly, the command MUST NOT open multiple NSOpenPanels simultaneously. The panel is modal, so subsequent invocations are blocked until the current panel is dismissed.
- **Selected directory is a symlink**: The command SHOULD resolve the symlink to its canonical path before checking for `.git` and existing packages, to avoid creating duplicate packages for symlinked directories.
- **Project directory on a network volume**: File operations (validation, package creation) MAY be slower. The command SHOULD NOT block the main thread during I/O. Asynchronous execution with appropriate UI feedback is RECOMMENDED.
- **Extremely long directory name**: The package filename (`{dirname}.{ext}`) inherits the directory name. If the resulting path exceeds filesystem limits, the creation MUST fail with an error alert rather than silently truncating.
- **Workspace window focused when pressing Cmd-Shift-N**: The @FocusedObject for project state is nil (workspace windows do not provide project state), so the menu item is disabled.
- **Multiple screens / spaces**: NSOpenPanel and NSSavePanel SHOULD appear on the same screen as the app's key window. This is default system behavior.
- **Sandboxed app**: If the app is sandboxed, the NSOpenPanel and NSSavePanel provide security-scoped URLs. The command MUST call `startAccessingSecurityScopedResource()` before accessing the selected URL and `stopAccessingSecurityScopedResource()` when done.

## Logging

Subsystem: `{{bundle_id}}` | Category: `MenuCommands`

| Event | Level | Message |
|-------|-------|---------|
| New Project initiated | info | `MenuCommands: "New Project" initiated` |
| NSOpenPanel presented | debug | `MenuCommands: NSOpenPanel presented for directory selection` |
| NSOpenPanel cancelled | debug | `MenuCommands: NSOpenPanel cancelled by user` |
| Directory selected | debug | `MenuCommands: directory selected: "{{path}}"` |
| Directory validation passed | debug | `MenuCommands: directory validation passed for "{{path}}"` |
| Directory validation failed (no .git) | warning | `MenuCommands: directory validation failed — no .git found in "{{path}}"` |
| Directory validation failed (permissions) | warning | `MenuCommands: directory validation failed — cannot access "{{path}}": {{error}}` |
| Existing package found | info | `MenuCommands: existing package found at "{{packagePath}}", opening instead of creating` |
| Package creation started | debug | `MenuCommands: creating project package at "{{packagePath}}"` |
| Package creation succeeded | info | `MenuCommands: project package created at "{{packagePath}}"` |
| Package creation failed | error | `MenuCommands: failed to create project package at "{{packagePath}}": {{error}}` |
| Document opened | info | `MenuCommands: opened document at "{{path}}"` |
| Document open failed | error | `MenuCommands: failed to open document at "{{path}}": {{error}}` |
| New Session initiated | info | `MenuCommands: "New Session" initiated for project "{{projectName}}"` |
| New Session — no focused project | debug | `MenuCommands: "New Session" skipped — no focused project window` |
| New Workspace initiated | info | `MenuCommands: "New Workspace" initiated` |
| NSSavePanel presented | debug | `MenuCommands: NSSavePanel presented for workspace creation` |
| NSSavePanel cancelled | debug | `MenuCommands: NSSavePanel cancelled by user` |
| Workspace creation started | debug | `MenuCommands: creating workspace package at "{{path}}"` |
| Workspace creation succeeded | info | `MenuCommands: workspace package created at "{{path}}"` |
| Workspace creation failed | error | `MenuCommands: failed to create workspace package at "{{path}}": {{error}}` |
| Error alert presented | debug | `MenuCommands: error alert presented — "{{title}}": "{{message}}"` |

## Platform Notes

- **macOS (SwiftUI)**: Use `Commands { CommandGroup(replacing: .newItem) { ... } }` in the `App` struct to replace the default New menu item. Each `Button` within the command group defines a menu item with `.keyboardShortcut()` for the shortcut binding and `Label("Title", systemImage: "sf.symbol.name")` for the icon. Use `@FocusedObject var projectState: ProjectWindowState?` at the command level; the menu item is disabled when `projectState` is nil. Each project window view must apply `.focusedObject(windowState)` to make its state available. `NSOpenPanel` and `NSSavePanel` are called from the button action via `await panel.begin()` (or `panel.runModal()` on the main actor). After directory selection, validate by checking `FileManager.default.fileExists(atPath: selectedURL.appendingPathComponent(".git").path)`. Create the package document per `package-document.md` and open it via `NSDocumentController.shared.openDocument(withContentsOf: url, display: true)`.
- **macOS (AppKit)**: Menu items are defined in `NSMenu` via `NSMenuItem` with `action`, `keyEquivalent`, and `keyEquivalentModifierMask`. `NSMenuItem.image` is set to an `NSImage(systemSymbolName:accessibilityDescription:)` for SF Symbol icons. Per-window dispatch uses the responder chain — the `NSWindow`'s `windowController` or content view controller implements the action method. If no responder handles the action, the menu item auto-disables (`autoenablesItems = true`). `validateMenuItem(_:)` provides fine-grained enable/disable logic.
- **Windows**: Menu bar items are defined via the platform's menu API (e.g., Win32 `HMENU` or a UI framework equivalent). Keyboard shortcuts are registered as accelerators. SF Symbols are not available — use equivalent icons from the app's asset catalog or platform icon set. Per-window command dispatch uses the active window handle or equivalent focus mechanism. File/directory pickers use `IFileOpenDialog` (directory mode) and `IFileSaveDialog` respectively. Validation logic (checking for `.git` directory) uses standard filesystem APIs.

## Design Decisions

_None yet — decisions made during implementation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
