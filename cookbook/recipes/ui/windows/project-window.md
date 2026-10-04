---
id: 338cb220-483c-4f9e-ae9d-e1dd79e59289
title: "Project Window"
domain: agenticdevelopercookbook://recipes/ui/windows/project-window
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
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
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Project Window

## Overview

The primary IDE-style project window that composes multiple sub-components into a four-panel layout. An HSplitView arranges the sessions panel, file tree panel, and detail panel side by side; the detail panel is itself a VSplitView containing the code editor (top) and terminal (bottom). An optional inspector panel slides in from the right. Each pane's visibility and proportions are persisted per-project, and the window frame is auto-saved using a SHA256 hash of the project path.

## Terminology

| Term | Definition |
|------|-----------|
| Sessions panel | The leftmost panel showing a list of sessions for the project |
| File tree panel | The file browser panel displaying the project's directory hierarchy |
| Detail panel | The center/right area containing the editor and terminal in a vertical split |
| Inspector panel | An optional right-side sliding panel showing metadata for the selected item |
| HSplitView | A horizontal split view dividing the window into side-by-side sections |
| VSplitView | A vertical split view dividing the detail panel into top (editor) and bottom (terminal) |
| Proportional sizing | Each pane occupies a fraction of total width, persisted per-project |
| Frame autosave | The platform mechanism for persisting window position and size between sessions |

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

## Behavioral Requirements

### Window structure

- **hsplit-three-panels**: The window MUST use an HSplitView with three main sections: sessions panel (left), file tree panel (center-left), and detail panel (center-right/right).
- **vsplit-editor-terminal**: The detail panel MUST use a VSplitView with the code editor pane on top and the terminal pane on bottom.
- **collapsible-pane-headers**: Each section of the VSplitView (editor and terminal) MUST be preceded by a collapsible pane header (as defined in `ui/collapsible-pane-header.md`).
- **inspector-slide-right**: The inspector panel MUST slide in from the right using the `.inspector` modifier (as defined in `ui/Recipes/inspector-panel.md`).

### Pane sizing and proportions

- **proportional-sizing**: Each HSplitView section MUST use proportional sizing with minimum, ideal, and maximum width frame constraints.
- **sessions-default-15pct**: The sessions panel MUST default to 15% of the window width (`sessionPanelProportion = 0.15`).
- **filetree-default-20pct**: The file tree panel MUST default to 20% of the window width (`fileTreeProportion = 0.20`).
- **detail-fills-remaining**: The detail panel MUST fill the remaining width after sessions and file tree.
- **detail-split-50-50**: The VSplitView within the detail panel MUST default to a 50/50 split between editor and terminal (`detailSplitRatio = 0.5`).
- **persist-layout-proportions**: All layout proportions MUST be persisted per-project in ProjectSettings (see Project Settings section).

### Pane visibility

- **toggle-sessions-panel**: The sessions panel MUST be togglable via a toolbar button. Default: visible (`isSessionPanelVisible = true`).
- **toggle-file-tree**: The file tree panel MUST be togglable. Default: visible (`isFileViewerVisible = true`).
- **toggle-terminal**: The terminal pane MUST be togglable. Default: visible (`isTerminalVisible = true`).
- **toggle-inspector**: The inspector panel MUST be togglable via a toolbar button. Default: hidden (`isInspectorPresented = false`).
- **persist-visibility-state**: Visibility state for all panels MUST be persisted per-project in ProjectSettings.
- **animate-pane-toggle**: Pane visibility changes MUST animate with `.easeInOut(duration: 0.2)`.

### Toolbar

- **toolbar-sessions-button**: The toolbar MUST include a button to toggle the sessions panel.
- **toolbar-inspector-button**: The toolbar MUST include a button to toggle the inspector panel (SF Symbol `sidebar.trailing`).
- **toolbar-gear-button**: The toolbar MUST include a gear button that presents a project settings sheet.

### File tree header

- **folder-header-repo-name**: A folder header MUST be displayed above the file tree showing the repository root directory name.

### Window frame persistence

- **persist-window-frame**: The window frame (position and size) MUST be persisted using the window-frame-persistence component (as defined in `ui/window-frame-persistence.md`).
- **sha256-autosave-id**: The autosave identifier MUST be a SHA256 hash of the project's file path, ensuring uniqueness per project.

### Status bar

- **sync-status-overlay**: During directory sync operations, a status bar overlay MUST appear at the bottom of the file tree panel (as defined in `ui/status-bar.md`).

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

## Appearance

- **Window minimum size**: 800 x 600pt
- **Sessions panel width**: proportional (default 15%), min 120pt, max 250pt
- **File tree panel width**: proportional (default 20%), min 150pt, max 350pt
- **Detail panel width**: fills remaining space, min 300pt
- **Inspector panel width**: 250pt fixed (per inspector-panel spec)
- **Folder header**: Repo root name displayed in a compact header row above the file tree, caption font weight medium
- **Pane headers**: 24-28pt height, system tertiary background (per collapsible-pane-header spec)
- **Pane animation**: `.easeInOut(duration: 0.2)` for all visibility toggles
- **Toolbar style**: Standard macOS toolbar with icon-only buttons

## States

| State | Behavior |
|-------|----------|
| All panels visible | Full four-panel layout: sessions, file tree, editor+terminal, inspector |
| Sessions hidden | Sessions panel collapses; file tree and detail expand to fill |
| File tree hidden | File tree collapses; detail panel expands to fill |
| Terminal collapsed | Terminal pane collapses; editor fills the detail panel, terminal header remains visible |
| Editor collapsed | Editor pane collapses; terminal fills the detail panel, editor header remains visible |
| Both editor and terminal collapsed | Only pane headers visible stacked vertically in the detail area |
| Inspector visible | Inspector slides in from right, narrowing the detail panel |
| Inspector hidden | Detail panel fills width up to the right edge |
| Project settings sheet | Presented as a sheet over the window, triggered by toolbar gear button |
| Window loading | `onAppear` fires: initial data loads, file watcher starts, terminal auto-opens if configured |
| Window closing | `onClose` fires: processes terminated, watcher stopped |

## Project Settings

Layout proportions and pane visibility are persisted per-project in ProjectSettings:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `sessionPanelProportion` | `Double` | `0.15` | Sessions panel width as fraction of window width |
| `fileTreeProportion` | `Double` | `0.20` | File tree panel width as fraction of window width |
| `detailSplitRatio` | `Double` | `0.5` | Vertical split ratio between editor and terminal (0.0 = all terminal, 1.0 = all editor) |
| `isSessionPanelVisible` | `Bool` | `true` | Whether the sessions panel is shown |
| `isFileViewerVisible` | `Bool` | `true` | Whether the file tree panel is shown |
| `isTerminalVisible` | `Bool` | `true` | Whether the terminal pane is shown |
| `isInspectorPresented` | `Bool` | `false` | Whether the inspector panel is shown |

- **persist-project-settings**: All settings in this table MUST be persisted per-project and restored on next open.
- **immediate-settings-save**: Changes to visibility or proportions MUST be written to ProjectSettings immediately (no manual save action).

## Accessibility

- **sessions-toggle-label**: The toolbar sessions toggle button MUST have an accessible label: "Toggle Sessions Panel".
- **inspector-toggle-label**: The toolbar inspector toggle button MUST have an accessible label: "Toggle Inspector" (inherited from inspector-panel spec).
- **gear-button-label**: The toolbar gear button MUST have an accessible label: "Project Settings".
- **pane-header-accessible**: Each collapsible pane header MUST follow the accessibility requirements defined in `ui/collapsible-pane-header.md` (button role, expand/collapse announcement, keyboard toggle).
- **divider-accessible**: The split view dividers MUST be accessible to VoiceOver and MUST announce their purpose (e.g., "Resize sessions panel").
- **keyboard-region-nav**: Keyboard navigation MUST allow moving focus between all major regions: sessions, file tree, editor, terminal, inspector, and toolbar.
- **keyboard-panel-shortcuts**: The window MUST support standard macOS keyboard shortcuts for panel toggling (to be defined at implementation time and recorded as Design Decisions).

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pw-001 | hsplit-three-panels | Open a project window | HSplitView renders with sessions, file tree, and detail panels |
| pw-002 | vsplit-editor-terminal | Inspect detail panel | VSplitView contains editor (top) and terminal (bottom) |
| pw-003 | collapsible-pane-headers | Inspect editor and terminal sections | Each preceded by a collapsible pane header |
| pw-004 | inspector-slide-right | Toggle inspector on | Inspector slides in from right |
| pw-005 | proportional-sizing, sessions-default-15pct, filetree-default-20pct | Open window at 1200pt width | Sessions ~180pt (15%), file tree ~240pt (20%), detail fills remainder |
| pw-006 | detail-split-50-50 | Inspect detail panel at 600pt height | Editor ~300pt, terminal ~300pt (50/50 split) |
| pw-007 | persist-layout-proportions, persist-project-settings | Resize sessions panel to 25%, close project, reopen | Sessions panel restores at 25% |
| pw-008 | toggle-sessions-panel, persist-visibility-state | Hide sessions panel, close project, reopen | Sessions panel remains hidden |
| pw-009 | toggle-terminal, persist-visibility-state | Hide terminal pane, close project, reopen | Terminal pane remains hidden, header still visible |
| pw-010 | animate-pane-toggle | Toggle sessions panel visibility | Panel animates in/out with easeInOut(0.2) |
| pw-011 | toolbar-sessions-button | Click sessions toolbar button | Sessions panel toggles visibility |
| pw-012 | toolbar-inspector-button | Click inspector toolbar button | Inspector panel toggles visibility |
| pw-013 | toolbar-gear-button | Click gear toolbar button | Project settings sheet appears |
| pw-014 | folder-header-repo-name | Open project at `/Users/dev/my-repo` | Folder header shows "my-repo" above file tree |
| pw-015 | persist-window-frame, sha256-autosave-id | Open project, move window, close, reopen | Window restores at saved position; autosave name is SHA256 of project path |
| pw-016 | sync-status-overlay | Trigger directory sync | Status bar overlay appears at bottom of file tree panel |
| pw-017 | load-initial-start-watch | Open a project window | `loadInitial` and `startWatching` called on appear |
| pw-018 | auto-open-terminal | Open project with auto-open-terminal enabled | Terminal pane opens automatically |
| pw-019 | terminate-on-close | Close the project window | `terminateAll` and `stopWatching` called |
| pw-020 | sessions-toggle-label | Enable VoiceOver, focus sessions toolbar button | Announces "Toggle Sessions Panel" |
| pw-021 | keyboard-region-nav | Press Tab repeatedly through window | Focus moves between sessions, file tree, editor, terminal, toolbar |
| pw-022 | immediate-settings-save | Toggle inspector, immediately force-quit app, relaunch | Inspector state matches last toggle (persisted immediately) |

## Edge Cases

- **All side panels hidden**: If sessions and file tree are both hidden, the detail panel fills the full window width. The toolbar toggle buttons remain accessible to restore them.
- **Both editor and terminal collapsed**: Only the two pane headers are visible stacked vertically. The user can re-expand either by clicking its header.
- **Window at minimum size with all panels visible**: Panels MUST respect their minimum width constraints. If the window is too narrow to satisfy all minimums simultaneously, the rightmost resizable panel (detail) SHOULD compress first down to its minimum, and the split view SHOULD prevent further shrinking.
- **Project path changes (rename/move)**: The window frame autosave identifier is based on the original path's SHA256 hash. If the project is moved, the frame will not restore. This is expected — the window opens at default position for the new path.
- **Very long repo root name**: The folder header SHOULD truncate with trailing ellipsis rather than overflowing.
- **No git repository**: File tree renders without git status badges; inspector omits Git Status row. No error displayed.
- **File watcher fails to start**: The window SHOULD log an error and continue operating without live file updates. A manual refresh mechanism SHOULD be available.
- **Terminal process crashes**: The terminal pane SHOULD display an error state. Other panels MUST remain functional.
- **Multiple project windows open**: Each window has its own ProjectSettings and frame autosave identifier. Settings changes in one window MUST NOT affect another.
- **Inspector toggled rapidly**: Animation MUST not stack or glitch. Each toggle SHOULD cancel any in-flight animation and start fresh.
- **Extremely large project (100k+ files)**: Lazy loading in the file tree (delegated to file-tree-browser) mitigates this. The window itself SHOULD remain responsive.
- **visionOS volume placement**: On visionOS, the window renders as a standard window volume. Panel layout is identical but the user cannot resize panes via drag on visionOS — pane proportions are controlled via settings.

## Localization

| String Key | Default (en) | Context |
|-----------|-------------|---------|
| `project_window.sessions_toggle` | Toggle Sessions Panel | Toolbar button accessible label |
| `project_window.inspector_toggle` | Toggle Inspector | Toolbar button accessible label |
| `project_window.settings_button` | Project Settings | Toolbar gear button accessible label |
| `project_window.editor_header` | Editor | Collapsible pane header title for editor |
| `project_window.terminal_header` | Terminal | Collapsible pane header title for terminal |
| `project_window.folder_header` | {{repoName}} | Folder header above file tree (dynamic, not localized) |

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Pane visibility changes are instant (no `.easeInOut` animation). Inspector appears/disappears without slide. |
| Reduce Transparency | Panel backgrounds use opaque materials instead of translucent/blur effects |
| Increase Contrast | Pane header backgrounds, divider lines, and toolbar button outlines use higher-contrast values |
| Differentiate Without Color | No impact — panel structure is spatial, not color-dependent |
| VoiceOver | Toolbar buttons announce labels and toggle state. Pane headers announce expand/collapse state. Split dividers announce resize role. |

## Feature Flags

| Flag Key | Default | Description |
|----------|---------|-------------|
| `{{app_prefix}}.project_window` | `true` | Enables the project window (master toggle) |
| `{{app_prefix}}.project_window.sessions_panel` | `true` | Enables the sessions panel in the project window |

## Analytics

| Event | Properties | When |
|-------|-----------|------|
| `project_window.opened` | `{ project_hash: string }` | Project window opens |
| `project_window.closed` | `{ project_hash: string, duration_seconds: number }` | Project window closes |
| `project_window.panel_toggled` | `{ panel: string, visible: bool }` | Any panel visibility toggled |
| `project_window.settings_opened` | `{}` | Gear button clicked, settings sheet presented |

## Privacy

- **Data collected**: Panel visibility and proportion preferences per project; window frame position/size
- **Storage**: ProjectSettings persisted on-device only (platform standard persistence). Frame autosave via `NSWindow.setFrameAutosaveName` (on-device).
- **Transmission**: None — no layout data leaves the device
- **Retention**: Persisted until the user changes settings or the project is removed. Frame autosave cleaned up by the OS if the app is uninstalled.

## Logging

Subsystem: `{{bundle_id}}` | Category: `ProjectWindow`

| Event | Level | Message |
|-------|-------|---------|
| Window opened | info | `ProjectWindow: opened for "{{projectPath}}"` |
| Window closed | info | `ProjectWindow: closed for "{{projectPath}}"` |
| Load initial started | debug | `ProjectWindow: loadInitial started` |
| Load initial completed | debug | `ProjectWindow: loadInitial completed` |
| File watcher started | debug | `ProjectWindow: startWatching for "{{projectPath}}"` |
| File watcher stopped | debug | `ProjectWindow: stopWatching for "{{projectPath}}"` |
| File watcher failed | error | `ProjectWindow: startWatching failed: {{error}}` |
| Processes terminated | debug | `ProjectWindow: terminateAll called` |
| Sessions panel toggled | debug | `ProjectWindow: sessions panel toggled to {{visible\|hidden}}` |
| File tree toggled | debug | `ProjectWindow: file tree toggled to {{visible\|hidden}}` |
| Terminal toggled | debug | `ProjectWindow: terminal toggled to {{visible\|hidden}}` |
| Inspector toggled | debug | `ProjectWindow: inspector toggled to {{visible\|hidden}}` |
| Proportions saved | debug | `ProjectWindow: proportions saved (sessions={{s}}, fileTree={{f}}, detailSplit={{d}})` |
| Settings sheet presented | debug | `ProjectWindow: settings sheet presented` |
| Frame autosave set | debug | `ProjectWindow: frame autosave name "{{hash}}"` |
| Auto-open terminal | debug | `ProjectWindow: auto-opening terminal per user settings` |

## Platform Notes

- **SwiftUI (macOS)**: Use `HSplitView` for the three-panel horizontal layout. Wrap sessions and file tree panels in conditional `if isSessionPanelVisible` / `if isFileViewerVisible` blocks, animated with `.animation(.easeInOut(duration: 0.2), value:)`. Use `VSplitView` inside the detail panel for editor (top) and terminal (bottom), each preceded by a `CollapsiblePaneHeader`. Apply `.inspector(isPresented: $isInspectorPresented)` on the outer container for the inspector. Use `.frame(minWidth:idealWidth:maxWidth:)` on each panel for proportional sizing. Toolbar via `.toolbar { }` with `ToolbarItem(placement:)` for sessions toggle, inspector toggle, and gear button. Gear button presents a `.sheet` for project settings. Frame persistence via `.background(WindowAccessor(name: sha256Hash(projectPath), onClose: { terminateAll(); stopWatching() }))`. The folder header is an `HStack` with a folder icon and the project root directory name, placed above the file tree `List`. Use `@ObservedObject` or `@EnvironmentObject` for `ProjectSettings` bindings.
- **SwiftUI (visionOS)**: Same layout as macOS. The window opens as a standard visionOS window. `HSplitView` and `VSplitView` render within the window volume. Split view dividers are not user-draggable on visionOS — pane proportions are controlled exclusively through ProjectSettings. Inspector uses the same `.inspector` modifier. Toolbar adapts to visionOS ornament style automatically. Frame persistence is not applicable (visionOS manages window placement).

## Design Decisions

**Fixed 2-pane detail layout**: The current spec uses a fixed VSplitView with editor (top) and terminal (bottom). A future version MAY evolve to a flexible N-pane layout supporting arbitrary pane configurations (file editor, terminal sessions, IDE integration panes). When this ships, the spec should be updated to document `PaneType` enum and `PaneLayout` struct.

**File tree default width**: Currently defaulting to 20% (`fileTreeProportion = 0.20`). Some implementations may prefer 40% for better file name readability. This is configurable per-project — the default can be adjusted based on user feedback.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
