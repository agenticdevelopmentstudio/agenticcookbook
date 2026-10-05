---
id: E53B1FD3-3E7A-490D-BC5D-83EE9C5CE351
title: "Document Creation Flow"
domain: agenticdevelopercookbook://ingredients/app/document-creation-flow
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "New Project and New Workspace flows: file pickers, Git validation, package creation, document opening, and error alerts"
platforms:
  - macos
  - swift
  - windows
tags:
  - app
  - documents
  - file-picker
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/app/creation-menu-commands
  - agenticdevelopercookbook://recipes/app/menu-commands
  - agenticdevelopercookbook://recipes/infrastructure/package-document
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Document Creation Flow

## Overview

The flows that create and open documents from the "New Project" and "New Workspace" menu commands. New Project opens a directory picker, validates the selection is a Git repository, then opens an existing project package or creates a new one; New Workspace opens a save panel with the workspace extension enforced and creates a workspace package. Both flows open the result through the document controller and show an error alert on failure. Package contents follow the package-document recipe.

### Terminology

| Term | Definition |
|------|-----------|
| NSOpenPanel | A macOS panel for selecting existing files or directories |
| NSSavePanel | A macOS panel for choosing a save location and filename for a new file |
| NSDocumentController | The macOS singleton that manages the app's open documents and coordinates document lifecycle |
| Package document | A directory bundle presented as a single file in Finder, as defined in package-document.md |

## Behavioral Requirements

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

## Appearance

- **Error alerts**: Standard `NSAlert` / SwiftUI `.alert` with title, message, and "OK" button
- **NSOpenPanel**: Standard macOS directory picker with prompt text "Select Project Directory"
- **NSSavePanel**: Standard macOS save dialog with prompt text "Create Workspace" and enforced file extension

## States

| State | Behavior |
|-------|----------|
| NSOpenPanel displayed | User is selecting a directory for New Project. Other menu commands are blocked by the modal panel |
| NSSavePanel displayed | User is choosing a save location for New Workspace. Other menu commands are blocked by the modal panel |
| Directory validation failed | Error alert displayed with reason. User can dismiss and retry |
| Existing package found | Package at expected path is opened instead of creating a duplicate |
| Document creation in progress | Package is being created on disk. Menu command is non-reentrant (no double-creation) |
| Document open failed | Error alert displayed with failure reason. No document window opens |

## Accessibility

- **voiceover-error-announce**: Error alerts MUST be announced by VoiceOver when they appear.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-007 | open-panel-directory-mode | Trigger "New Project" | NSOpenPanel opens with directory selection enabled and file selection disabled |
| mc-008 | validate-git-directory | Select a directory without a .git subdirectory | Error alert appears: "The selected folder is not a Git repository." |
| mc-009 | validate-git-directory | Select a directory containing a .git subdirectory | Validation passes; flow proceeds to package creation or opening |
| mc-010 | open-existing-package, open-via-document-controller | Select a directory that already contains `dirname.catnip-proj` | Existing package is opened; no new package created |
| mc-011 | create-new-package, open-via-document-controller | Select a valid git directory with no existing package | New package created at `{dir}/{dirname}.{ext}`; document opens |
| mc-012 | show-creation-error-alert | Select a directory where package creation fails (e.g., read-only filesystem) | Error alert displayed with failure reason |
| mc-013 | workspace-save-panel, enforce-workspace-extension | Trigger "New Workspace" | NSSavePanel opens with workspace file extension enforced |
| mc-014 | create-workspace-package, open-workspace-document | Confirm save location in NSSavePanel | Workspace package created at chosen path; document opens |
| mc-015 | show-workspace-error-alert | Confirm save location on a read-only volume | Error alert displayed with failure reason |
| mc-020 | voiceover-error-announce | Trigger validation error with VoiceOver enabled | VoiceOver announces the error alert |

## Edge Cases

- **Directory without .git**: Validation fails with a clear error alert. The user is not prevented from dismissing the alert and retrying with a different directory.
- **Duplicate project package**: If `{dir}/{dirname}.{ext}` already exists, the existing package is opened. This prevents creating multiple packages for the same project directory.
- **Permissions denied**: If the app lacks read permission on the selected directory, the validation step MUST fail gracefully with an error alert (e.g., "Cannot access the selected folder. Check Finder permissions."). If write permission is denied when creating a package, the creation step MUST fail with an error alert.
- **NSOpenPanel cancelled**: If the user clicks Cancel in the NSOpenPanel, the command MUST silently abort with no error or side effect.
- **NSSavePanel cancelled**: If the user clicks Cancel in the NSSavePanel, the command MUST silently abort with no error or side effect.
- **Rapid repeated invocation**: If the user presses Cmd-N multiple times quickly, the command MUST NOT open multiple NSOpenPanels simultaneously. The panel is modal, so subsequent invocations are blocked until the current panel is dismissed.
- **Selected directory is a symlink**: The command SHOULD resolve the symlink to its canonical path before checking for `.git` and existing packages, to avoid creating duplicate packages for symlinked directories.
- **Project directory on a network volume**: File operations (validation, package creation) MAY be slower. The command SHOULD NOT block the main thread during I/O. Asynchronous execution with appropriate UI feedback is RECOMMENDED.
- **Extremely long directory name**: The package filename (`{dirname}.{ext}`) inherits the directory name. If the resulting path exceeds filesystem limits, the creation MUST fail with an error alert rather than silently truncating.
- **Multiple screens / spaces**: NSOpenPanel and NSSavePanel SHOULD appear on the same screen as the app's key window. This is default system behavior.
- **Sandboxed app**: If the app is sandboxed, the NSOpenPanel and NSSavePanel provide security-scoped URLs. The command MUST call `startAccessingSecurityScopedResource()` before accessing the selected URL and `stopAccessingSecurityScopedResource()` when done.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `openPanelPrompt` | string | `Select Project Directory` | Prompt text of the directory picker |
| `savePanelPrompt` | string | `Create Workspace` | Prompt text of the workspace save panel |
| `projectExtension` | string | app-defined (e.g., `catnip-proj`) | Extension of the project package |
| `workspaceExtension` | string | app-defined (e.g., `catnip-workspace`) | Extension enforced through `allowedContentTypes` |

## Privacy

- **Data collected**: Paths the user selects in the directory and save panels.
- **Storage**: Packages are created on the user's disk at the chosen path; the app does not retain the selection beyond opening the document.
- **Transmission**: None.
- **Retention**: Until the user deletes the package.

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
| New Workspace initiated | info | `MenuCommands: "New Workspace" initiated` |
| NSSavePanel presented | debug | `MenuCommands: NSSavePanel presented for workspace creation` |
| NSSavePanel cancelled | debug | `MenuCommands: NSSavePanel cancelled by user` |
| Workspace creation started | debug | `MenuCommands: creating workspace package at "{{path}}"` |
| Workspace creation succeeded | info | `MenuCommands: workspace package created at "{{path}}"` |
| Workspace creation failed | error | `MenuCommands: failed to create workspace package at "{{path}}": {{error}}` |
| Error alert presented | debug | `MenuCommands: error alert presented — "{{title}}": "{{message}}"` |

## Platform Notes

- **macOS (SwiftUI)**: `NSOpenPanel` and `NSSavePanel` are called from the button action via `await panel.begin()` (or `panel.runModal()` on the main actor). After directory selection, validate by checking `FileManager.default.fileExists(atPath: selectedURL.appendingPathComponent(".git").path)`. Create the package document per `package-document.md` and open it via `NSDocumentController.shared.openDocument(withContentsOf: url, display: true)`.
- **macOS (AppKit)**: Present the panels with `begin(completionHandler:)` on the key window; the document controller call is identical to the SwiftUI path.
- **Windows**: File/directory pickers use `IFileOpenDialog` (directory mode) and `IFileSaveDialog` respectively. Validation logic (checking for `.git` directory) uses standard filesystem APIs.
- **Compose and React/Web**: Not applicable — the flows use native OS pickers and the macOS document controller; Compose Desktop and Electron use their platform file dialogs with the same validation steps.

## Design Decisions

**Decision**: Open an existing project package instead of creating a duplicate when one exists at the expected path.
**Rationale**: One project directory maps to one package; creating duplicates would split project state.
**Approved**: pending

**Decision**: Require a `.git` directory for New Project.
**Rationale**: A Git repository is the unit a project package wraps; failing early with a clear alert avoids creating a package around a non-repository.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [error-responses](agenticdevelopercookbook://guidelines/implementing/networking/error-responses) | partial | Best Practices |
| [privacy](agenticdevelopercookbook://guidelines/implementing/security/privacy) | partial | Privacy |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Menu Commands recipe |
