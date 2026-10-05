---
id: 18FDFDAD-E9DA-4B84-80DB-23B00FEF5D77
title: "Creation Menu Commands"
domain: agenticdevelopercookbook://ingredients/app/creation-menu-commands
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Replaces the default New menu item with New Project, New Session, and New Workspace commands with shortcuts, icons, and focused-window dispatch"
platforms:
  - macos
  - swift
  - windows
tags:
  - app
  - commands
  - menu
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/app/document-creation-flow
  - agenticdevelopercookbook://recipes/app/menu-commands
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Creation Menu Commands

## Overview

The app's creation menu: it replaces the default "New" menu item with app-specific creation commands (New Project, New Session, New Workspace), each with a distinct keyboard shortcut and an SF Symbol icon. Commands that act on the current window (New Session) use the `@FocusedObject` pattern to reach the focused window's state and disable themselves gracefully when no suitable window is focused. What the document-creating commands do after they are invoked is the Document Creation Flow ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| Menu command | A user-invocable action exposed in the app's menu bar, typically with a keyboard shortcut |
| Keyboard shortcut | A modifier key combination (e.g., Cmd-N) bound to a menu command |
| CommandGroup | A SwiftUI struct that defines or replaces a group of menu items in the app's menu bar |
| @FocusedObject | A SwiftUI property wrapper that reads an observable object provided by the currently focused window via `.focusedObject()` |
| SF Symbol | A system-provided icon from Apple's SF Symbols library, used for menu item imagery |

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

## States

| State | Behavior |
|-------|----------|
| No window focused | Per-window commands (New Session) are disabled. Global commands (New Project, New Workspace) remain enabled |
| Project window focused | All commands are enabled. New Session operates on the focused window's project |
| Workspace window focused | New Session is disabled (sessions belong to projects). New Project and New Workspace remain enabled |

## Accessibility

- **voiceover-menu-access**: All menu items MUST be accessible via VoiceOver with their full title (e.g., "New Project, Command N").
- **disabled-state-assistive**: Disabled menu items MUST convey their disabled state to assistive technologies.
- **voiceover-shortcut-passthrough**: All menu keyboard shortcuts MUST be functional when VoiceOver is active, using VoiceOver's pass-through mechanism for keyboard commands.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-001 | replace-default-new-item, creation-command-order | Open the File menu | Default "New" item is replaced with "New Project", "New Session", "New Workspace" in that order |
| mc-003 | unique-keyboard-shortcuts | Press Cmd-Shift-N with a project window focused | "New Session" creates a session in the focused project |
| mc-005 | sf-symbol-icons | Open the File menu on macOS | Each creation command displays its SF Symbol icon |
| mc-006 | disable-without-focus, disable-without-project, graceful-nil-focused-object | Press Cmd-Shift-N with no window focused | Menu item is disabled; nothing happens |
| mc-016 | create-session-in-window, focused-object-project-state | Press Cmd-Shift-N with project window focused | New session created in the focused project |
| mc-017 | focused-object-dispatch, provide-focused-object | Focus Window A, press Cmd-Shift-N, then focus Window B, press Cmd-Shift-N | Session created in Window A's project first, then in Window B's project |
| mc-018 | graceful-nil-focused-object | Focus a non-project window (e.g., settings), press Cmd-Shift-N | Menu item is disabled; no action taken |
| mc-019 | voiceover-menu-access | Enable VoiceOver, navigate to File menu | VoiceOver announces each menu item with title and shortcut |

## Edge Cases

- **No window focused**: Global commands (New Project, New Workspace) remain enabled. Per-window commands (New Session) are disabled via `@FocusedObject` returning nil. This is the expected state at app launch before any document is opened.
- **Workspace window focused when pressing Cmd-Shift-N**: The @FocusedObject for project state is nil (workspace windows do not provide project state), so the menu item is disabled.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `newProjectShortcut` | key combination | Cmd-N | Primary creation action |
| `newSessionShortcut` | key combination | Cmd-Shift-N | Secondary, within the current window |
| `newWorkspaceShortcut` | key combination | Cmd-Option-N | Tertiary creation action |
| `menuIcons` | map | `folder.badge.plus`, `terminal`, `square.grid.2x2` | SF Symbol per command (examples) |

## Logging

Subsystem: `{{bundle_id}}` | Category: `MenuCommands`

| Event | Level | Message |
|-------|-------|---------|
| New Session initiated | info | `MenuCommands: "New Session" initiated for project "{{projectName}}"` |
| New Session — no focused project | debug | `MenuCommands: "New Session" skipped — no focused project window` |

## Platform Notes

- **macOS (SwiftUI)**: Use `Commands { CommandGroup(replacing: .newItem) { ... } }` in the `App` struct to replace the default New menu item. Each `Button` within the command group defines a menu item with `.keyboardShortcut()` for the shortcut binding and `Label("Title", systemImage: "sf.symbol.name")` for the icon. Use `@FocusedObject var projectState: ProjectWindowState?` at the command level; the menu item is disabled when `projectState` is nil. Each project window view must apply `.focusedObject(windowState)` to make its state available.
- **macOS (AppKit)**: Menu items are defined in `NSMenu` via `NSMenuItem` with `action`, `keyEquivalent`, and `keyEquivalentModifierMask`. `NSMenuItem.image` is set to an `NSImage(systemSymbolName:accessibilityDescription:)` for SF Symbol icons. Per-window dispatch uses the responder chain — the `NSWindow`'s `windowController` or content view controller implements the action method. If no responder handles the action, the menu item auto-disables (`autoenablesItems = true`). `validateMenuItem(_:)` provides fine-grained enable/disable logic.
- **Windows**: Menu bar items are defined via the platform's menu API (e.g., Win32 `HMENU` or a UI framework equivalent). Keyboard shortcuts are registered as accelerators. SF Symbols are not available — use equivalent icons from the app's asset catalog or platform icon set. Per-window command dispatch uses the active window handle or equivalent focus mechanism.
- **Compose and React/Web**: Not applicable — these requirements concern the native platform menu bar; Compose Desktop `MenuBar` and Electron menus follow the Windows approach of accelerators and focused-window dispatch.

## Design Decisions

**Decision**: Replace the default New item with explicit creation commands rather than adding to it.
**Rationale**: The default New item is document-type agnostic; app-specific commands carry distinct shortcuts and meanings.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Menu Commands recipe |
