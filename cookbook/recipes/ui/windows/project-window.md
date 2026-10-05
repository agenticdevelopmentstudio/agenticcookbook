---
id: 338cb220-483c-4f9e-ae9d-e1dd79e59289
title: "Project Window"
domain: agenticdevelopercookbook://recipes/ui/windows/project-window
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "IDE-style four-panel project window composing file tree, editor, terminal, and inspector in split views"
platforms:
  - macos
  - swift
  - web
  - windows
tags:
  - project-window
  - ui
  - window
ingredients:
  - agenticdevelopercookbook://ingredients/ui/windows/project-split-layout
  - agenticdevelopercookbook://ingredients/ui/panels/file-tree-browser
  - agenticdevelopercookbook://ingredients/ui/panels/code-editor-pane
  - agenticdevelopercookbook://ingredients/ui/panels/terminal-pane
  - agenticdevelopercookbook://ingredients/ui/panels/inspector-panel
  - agenticdevelopercookbook://ingredients/ui/components/collapsible-pane-header
  - agenticdevelopercookbook://ingredients/ui/components/status-bar
  - agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence
  - agenticdevelopercookbook://ingredients/infrastructure/logging
  - agenticdevelopercookbook://ingredients/infrastructure/settings-keys
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Project Window

## Overview

The primary IDE-style project window, composed from a split layout and the panels that fill it. The Project Split Layout ingredient arranges a sessions panel, file tree, and a detail area (code editor over terminal) with an optional inspector; the panel ingredients supply each pane's behavior, collapsible pane headers fold the editor and terminal sections, a status bar reports directory sync, and window frame persistence remembers the window per project using a SHA256 hash of the project path. Use this recipe to build the main window of a project-based development tool.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Project Split Layout | `agenticdevelopercookbook://ingredients/ui/windows/project-split-layout` | Arranges the panels, owns proportions, visibility, toolbar and persisted ProjectSettings | Yes | Defaults: sessions 15%, file tree 20%, detail split 0.5; inspector hidden |
| File Tree Browser | `agenticdevelopercookbook://ingredients/ui/panels/file-tree-browser` | File tree panel content, selection, and directory sync | Yes | Root = project repository directory |
| Code Editor Pane | `agenticdevelopercookbook://ingredients/ui/panels/code-editor-pane` | Editor content in the top section of the detail area | Yes | Default |
| Terminal Pane | `agenticdevelopercookbook://ingredients/ui/panels/terminal-pane` | Terminal content in the bottom section of the detail area; owns sessions and processes | Yes | Auto-open per user setting |
| Inspector Panel | `agenticdevelopercookbook://ingredients/ui/panels/inspector-panel` | Right-side metadata panel for the selected item | No | Hidden by default; 250pt fixed width |
| Collapsible Pane Header | `agenticdevelopercookbook://ingredients/ui/components/collapsible-pane-header` | Header above the editor and terminal sections that collapses or expands each | Yes | Two instances: "Editor" and "Terminal" |
| Status Bar | `agenticdevelopercookbook://ingredients/ui/components/status-bar` | Sync-status overlay at the bottom of the file tree panel | Yes | Visible only during directory sync |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Persists window position and size per project | Yes | Autosave name = SHA256 of the project path |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Per-category logger for window-level events | Yes | Category `ProjectWindow` |
| Settings Keys | `agenticdevelopercookbook://ingredients/infrastructure/settings-keys` | Central registry for the ProjectSettings keys and user-setting keys | No | Keys for the Project Settings table |

## Integration Requirements

### Pane composition

- **collapsible-pane-headers**: Each section of the VSplitView (editor and terminal) MUST be preceded by a collapsible pane header (the `collapsible-pane-header` ingredient).

### Window frame persistence

- **persist-window-frame**: The window frame (position and size) MUST be persisted using the window-frame-persistence component (the `window-frame-persistence` ingredient).
- **sha256-autosave-id**: The autosave identifier MUST be a SHA256 hash of the project's file path, ensuring uniqueness per project.

### Status bar

- **sync-status-overlay**: During directory sync operations, a status bar overlay MUST appear at the bottom of the file tree panel (the `status-bar` ingredient).

### Lifecycle

- **load-initial-start-watch**: On `onAppear`, the window MUST load initial project data (`loadInitial`) and start file system watching (`startWatching`).
- **auto-open-terminal**: On `onAppear`, if the user's settings enable auto-open terminal, the terminal pane MUST be opened automatically.
- **terminate-on-close**: On window close (`onClose` / `onDisappear`), the window MUST terminate all running processes (`terminateAll`) and stop file system watching (`stopWatching`).

### Delegation to sub-components

- **delegate-file-tree**: The file tree panel MUST delegate to [file-tree-browser.md](../../../ingredients/ui/panels/file-tree-browser.md) for all file browsing behavior.
- **delegate-terminal**: The terminal pane MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) for all terminal behavior.
- **delegate-inspector**: The inspector panel MUST delegate to [inspector-panel.md](../../../ingredients/ui/panels/inspector-panel.md) for all inspector behavior.
- **delegate-editor**: The code editor pane MUST delegate to [code-editor-pane.md](../../../ingredients/ui/panels/code-editor-pane.md) for all editor behavior.
- **delegate-pane-headers**: Collapsible pane headers MUST delegate to [collapsible-pane-header.md](../../../ingredients/ui/components/collapsible-pane-header.md) for toggle and animation behavior.

- **pane-header-accessible**: Each collapsible pane header MUST follow the accessibility requirements defined by the `collapsible-pane-header` ingredient (button role, expand/collapse announcement, keyboard toggle).

### Wiring

- **layout-hosts-panel-ingredients**: The sessions, file tree, editor, terminal, and inspector slots of the Project Split Layout MUST be filled by the panel ingredients named in the Ingredients table. The layout MUST NOT reimplement any panel's own behavior.
- **header-collapse-drives-detail-area**: Collapsing or expanding a collapsible pane header MUST resize the detail area per the composed states in Layout (the other section fills the space; the collapsed section's header stays visible).
- **settings-keys-central**: The ProjectSettings keys (proportions and visibility) SHOULD be declared through the `settings-keys` ingredient rather than as scattered string literals.
- **log-via-shared-logger**: All window-level log events MUST use the `logging` ingredient's per-category logger with category `ProjectWindow`.

## Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│ [Sessions] [Inspector] [⚙]                              Toolbar       │
├──────────┬──────────────┬───────────────────────────────┬──────────────┤
│          │ ▾ repo-name  │ ▾ Editor                      │              │
│          │              │                               │              │
│ Sessions │  📁 Sources  │   (code editor pane)          │  Inspector   │
│   list   │    📄 App... │                               │  (optional)  │
│          │  📁 Tests    │                               │              │
│          │  📄 Package  │                               │              │
│          │              ├───────────────────────────────┤              │
│          │              │ ▾ Terminal                     │              │
│          │              │                               │              │
│          │              │   (terminal pane)              │              │
│          │              │                               │              │
│          │ ┌──────────┐ │                               │              │
│          │ │ Syncing… │ │                               │              │
├──────────┴─┴──────────┴─┴───────────────────────────────┴──────────────┤
```

`[Sessions | FileTree | Editor/Terminal VSplitView] + Inspector(optional)`

- **Sessions panel** (left): Session list, togglable via toolbar button
- **File tree panel**: File browser with folder header showing repo root name; sync status bar overlay at bottom
- **Detail panel** (center): VSplitView with editor (top) and terminal (bottom), each preceded by a collapsible pane header
- **Inspector panel** (right, optional): Slides in from right via `.inspector` modifier

### Composed states

| State | Behavior |
|-------|----------|
| Terminal collapsed | Terminal pane collapses; editor fills the detail panel, terminal header remains visible |
| Editor collapsed | Editor pane collapses; terminal fills the detail panel, editor header remains visible |
| Both editor and terminal collapsed | Only pane headers visible stacked vertically in the detail area |
| Window loading | `onAppear` fires: initial data loads, file watcher starts, terminal auto-opens if configured |
| Window closing | `onClose` fires: processes terminated, watcher stopped |

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| ProjectSettings (proportions, visibility) | Project Split Layout | Project Split Layout, Collapsible Pane Header | two-way | Per-project settings written immediately; restored on open |
| Pane collapsed state | Collapsible Pane Header | Project Split Layout (detail area) | two-way | Binding on each header; terminal visibility mirrors `isTerminalVisible` |
| Selected item | File Tree Browser | Inspector Panel | one-way | Selection binding feeding the inspector |
| Directory sync status | File Tree Browser | Status Bar | one-way | Sync-in-progress flag drives the overlay at the bottom of the file tree panel |
| Window frame autosave name | Project path (SHA256) | Window Frame Persistence | one-way | Hash of the project path set as the frame autosave name |
| Running processes and file watcher | Terminal Pane, File Tree Browser | Window close handler | one-way | `terminateAll` and `stopWatching` called on close |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pw-003 | collapsible-pane-headers | Inspect editor and terminal sections | Each preceded by a collapsible pane header |
| pw-015 | persist-window-frame, sha256-autosave-id | Open project, move window, close, reopen | Window restores at saved position; autosave name is SHA256 of project path |
| pw-016 | sync-status-overlay | Trigger directory sync | Status bar overlay appears at bottom of file tree panel |
| pw-017 | load-initial-start-watch | Open a project window | `loadInitial` and `startWatching` called on appear |
| pw-018 | auto-open-terminal | Open project with auto-open-terminal enabled | Terminal pane opens automatically |
| pw-019 | terminate-on-close | Close the project window | `terminateAll` and `stopWatching` called |
| pw-023 | header-collapse-drives-detail-area, collapsible-pane-headers | Collapse the terminal pane header | Terminal collapses, editor fills the detail area, terminal header remains visible |
| pw-024 | layout-hosts-panel-ingredients, delegate-inspector | Select a file in the file tree, then toggle the inspector on | Inspector slides in and shows metadata for the selected file |
| pw-025 | settings-keys-central, persist-window-frame | Open two projects, resize one window and toggle panels in it | The other window's frame, proportions and visibility are unchanged |

## Edge Cases

- **Both editor and terminal collapsed**: Only the two pane headers are visible stacked vertically. The user can re-expand either by clicking its header.
- **Project path changes (rename/move)**: The window frame autosave identifier is based on the original path's SHA256 hash. If the project is moved, the frame will not restore. This is expected — the window opens at default position for the new path.
- **No git repository**: File tree renders without git status badges; inspector omits Git Status row. No error displayed.
- **File watcher fails to start**: The window SHOULD log an error and continue operating without live file updates. A manual refresh mechanism SHOULD be available.
- **Terminal process crashes**: The terminal pane SHOULD display an error state. Other panels MUST remain functional.
- **Extremely large project (100k+ files)**: Lazy loading in the file tree (delegated to file-tree-browser) mitigates this. The window itself SHOULD remain responsive.

## Platform Notes

- **SwiftUI (macOS)**: Compose the Project Split Layout with the panel ingredients inside one `HSplitView`/`VSplitView`. Frame persistence via `.background(WindowAccessor(name: sha256Hash(projectPath), onClose: { terminateAll(); stopWatching() }))`. Call `loadInitial` and `startWatching` from `onAppear`, and open the terminal if the auto-open setting is on. Supply the folder header and status bar overlay inside the file tree column. Use `@ObservedObject` or `@EnvironmentObject` for `ProjectSettings` bindings.
- **SwiftUI (visionOS)**: Same composition. The window opens as a standard visionOS window; frame persistence is not applicable and pane proportions are controlled through ProjectSettings only.
- **Compose**: Compose the layout from the panel composables in a `Row`/`Column` split. Key the window state and frame persistence by a hash of the project path. Start the file watcher in a `LaunchedEffect` and stop it (and terminate sessions) in `DisposableEffect`'s `onDispose`.
- **React/Web**: Compose the panels in a resizable-panels layout; key persisted layout state in `localStorage` by a hash of the project path. Start file watching on mount and terminate sessions and stop watching on unmount or `beforeunload`.

## Design Decisions

**Decision**: Compose the project window from a dedicated split-layout ingredient plus the existing panel, header, status-bar, frame-persistence, and logging ingredients instead of one monolithic window spec.
**Rationale**: Each panel keeps a single owner (design-for-deletion); the window recipe states only how they wire together, so a panel can be replaced without touching the layout.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |

> Status is `partial`: this recipe specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructured into recipe shape: composes project-split-layout and existing panel ingredients |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
