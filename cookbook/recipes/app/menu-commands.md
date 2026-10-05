---
id: 81410d5e-e3df-4feb-a9b1-bbc97abfc798
title: "Menu Commands"
domain: agenticdevelopercookbook://recipes/app/menu-commands
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
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
ingredients:
  - agenticdevelopercookbook://ingredients/app/creation-menu-commands
  - agenticdevelopercookbook://ingredients/app/document-creation-flow
  - agenticdevelopercookbook://ingredients/infrastructure/logging
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/package-document
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Menu Commands

## Overview

Pattern for structuring platform menu commands with keyboard shortcuts, including document creation flows with file and directory pickers and validation. The Creation Menu Commands ingredient defines the menu and per-window dispatch; the Document Creation Flow ingredient defines what New Project and New Workspace do once invoked. The recipe wires each menu command to its flow and defines how failures and cancellations surface.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Creation Menu Commands | `agenticdevelopercookbook://ingredients/app/creation-menu-commands` | Replaced New menu, shortcuts, icons, New Session, focused-object dispatch | Yes | Shortcuts Cmd-N, Cmd-Shift-N, Cmd-Option-N |
| Document Creation Flow | `agenticdevelopercookbook://ingredients/app/document-creation-flow` | New Project and New Workspace pickers, validation, package creation | Yes | Extensions app-defined |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Logger for command events | Yes | Category `MenuCommands` |

## Integration Requirements

### Command-to-flow wiring

- **new-project-invokes-flow**: The "New Project" command MUST start the Document Creation Flow's project flow (directory picker first) and MUST NOT perform any document work itself.
- **new-workspace-invokes-flow**: The "New Workspace" command MUST start the Document Creation Flow's workspace flow (save panel first) and MUST NOT perform any document work itself.
- **new-session-stays-in-menu**: The "New Session" command MUST be fully handled through the focused window's state (Creation Menu Commands) and MUST NOT invoke a document creation flow.
- **global-commands-always-enabled**: "New Project" and "New Workspace" MUST be enabled whether or not any window is focused, because they do not depend on focused-window state.
- **flow-failures-surface-as-alerts**: A failure inside a creation flow MUST surface as the flow's error alert and MUST NOT disable or alter the menu commands afterwards.
- **flow-cancel-is-silent**: Cancelling a picker MUST return the app to its prior state with no alert, log error, or change to menu enablement.
- **log-command-events**: Command events from both ingredients MUST be logged through the `logging` ingredient with category `MenuCommands`.

## Layout

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

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Focused window state | Focused window (`.focusedObject()`) | Creation Menu Commands | one-way | `@FocusedObject` read at the command level |
| Selected directory or save location | File picker | Document Creation Flow | one-way | Picker result passed to validation or package creation |
| Created document | Document Creation Flow | Document controller | one-way | Opened via `NSDocumentController.shared.openDocument(withContentsOf:display:)` |
| Flow in progress | Document Creation Flow | Creation Menu Commands | one-way | Commands that start a flow are non-reentrant while a flow runs |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-002 | unique-keyboard-shortcuts | Press Cmd-N | "New Project" flow initiates (NSOpenPanel appears) |
| mc-004 | unique-keyboard-shortcuts | Press Cmd-Option-N | "New Workspace" flow initiates (NSSavePanel appears) |
| mc-021 | new-project-invokes-flow, global-commands-always-enabled | With no window focused, press Cmd-N | New Project is enabled and the directory picker appears |
| mc-022 | new-session-stays-in-menu | Press Cmd-Shift-N with a project window focused | A session is created in that project and no picker appears |
| mc-023 | flow-cancel-is-silent | Press Cmd-Option-N and cancel the save panel | No alert, no document, and all three menu items remain in their prior enabled state |
| mc-024 | flow-failures-surface-as-alerts | Trigger New Project on a read-only directory, dismiss the alert, press Cmd-N again | Alert appears once; the second invocation opens the picker normally |
| mc-025 | log-command-events | Run New Project to completion | Logs show initiated, panel presented, validation passed, package creation, and document opened events under `MenuCommands` |

## Edge Cases

- **Cmd-N while a creation flow is open**: The open panel or save panel is modal; the command MUST NOT start a second flow until the first is dismissed, and the other creation commands are blocked by the same modal.
- **Flow invoked from a workspace window**: New Project and New Workspace MUST work from a workspace window, while New Session MUST stay disabled there (no project state is provided).
- **Window focus changes while a picker is open**: The flow MUST complete against the app, not the window that was focused at invocation, and MUST NOT change which window supplies New Session state afterward.
- **Document opened by a flow gains focus**: After a flow opens a project window, New Session MUST become enabled for that window without any further user action.

## Platform Notes

- **macOS (SwiftUI)**: Declare the menu with `Commands { CommandGroup(replacing: .newItem) { ... } }`; each Button calls into the Document Creation Flow (New Project, New Workspace) or the focused window state (New Session). Keep flow code out of the `App` struct so it stays testable.
- **macOS (AppKit)**: Route menu actions through the responder chain; flow actions live on the app delegate or a document controller, and New Session on the window controller.
- **Windows**: Register accelerators for the three commands and route them to the same flow entry points; New Session dispatches to the active window.
- **Compose and React/Web**: Not applicable — this recipe composes native menu bar and document controller behavior; Compose Desktop and Electron apps follow the Windows approach.

## Design Decisions

**Decision**: Separate the menu (what the user can invoke) from the creation flows (what happens next).
**Rationale**: Menus change with product shape while flows change with document formats; keeping them apart lets either change alone.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [error-responses](agenticdevelopercookbook://guidelines/implementing/networking/error-responses) | partial | Best Practices |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this recipe specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructured into recipe shape: composes creation-menu-commands and document-creation-flow |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
