---
id: 865679A9-6631-46E8-84AE-6EF64D2ABF3A
title: "Project Split Layout"
domain: agenticdevelopercookbook://ingredients/ui/windows/project-split-layout
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Four-panel IDE-style split layout with sessions, file tree, editor over terminal, and an optional inspector, with per-project persisted proportions and visibility"
platforms:
  - macos
  - swift
  - web
  - windows
tags:
  - layout
  - project-window
  - ui
  - window
depends-on: []
related:
  - agenticdevelopercookbook://recipes/ui/windows/project-window
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Project Split Layout

## Overview

The split-view layout at the heart of the IDE-style project window. An HSplitView arranges the sessions panel, file tree panel, and detail panel side by side; the detail panel is itself a VSplitView holding the code editor (top) and terminal (bottom). An optional inspector panel slides in from the right. Each pane's visibility and proportions are persisted per-project. This ingredient owns the arrangement, sizing, toggling, toolbar, and persisted layout state only; the content of each pane is supplied by the panel ingredients the Project Window recipe composes with it.

### Terminology

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

## Behavioral Requirements

### Window structure

- **hsplit-three-panels**: The window MUST use an HSplitView with three main sections: sessions panel (left), file tree panel (center-left), and detail panel (center-right/right).
- **vsplit-editor-terminal**: The detail panel MUST use a VSplitView with the code editor pane on top and the terminal pane on bottom.
- **inspector-slide-right**: The inspector panel MUST slide in from the right using the `.inspector` modifier (as defined by the `inspector-panel` ingredient).

### Pane sizing and proportions

- **proportional-sizing**: Each HSplitView section MUST use proportional sizing with minimum, ideal, and maximum width frame constraints.
- **sessions-default-15pct**: The sessions panel MUST default to 15% of the window width (`sessionPanelProportion = 0.15`).
- **filetree-default-20pct**: The file tree panel MUST default to 20% of the window width (`fileTreeProportion = 0.20`).
- **detail-fills-remaining**: The detail panel MUST fill the remaining width after sessions and file tree.
- **detail-split-50-50**: The VSplitView within the detail panel MUST default to a 50/50 split between editor and terminal (`detailSplitRatio = 0.5`).
- **persist-layout-proportions**: All layout proportions MUST be persisted per-project in ProjectSettings (see the Project Settings table under Configuration).

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

### Persistence

- **persist-project-settings**: All settings in the Project Settings table MUST be persisted per-project and restored on next open.
- **immediate-settings-save**: Changes to visibility or proportions MUST be written to ProjectSettings immediately (no manual save action).

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
| Inspector visible | Inspector slides in from right, narrowing the detail panel |
| Inspector hidden | Detail panel fills width up to the right edge |
| Project settings sheet | Presented as a sheet over the window, triggered by toolbar gear button |

## Accessibility

- **sessions-toggle-label**: The toolbar sessions toggle button MUST have an accessible label: "Toggle Sessions Panel".
- **inspector-toggle-label**: The toolbar inspector toggle button MUST have an accessible label: "Toggle Inspector" (matching the `inspector-panel` ingredient).
- **gear-button-label**: The toolbar gear button MUST have an accessible label: "Project Settings".
- **divider-accessible**: The split view dividers MUST be accessible to VoiceOver and MUST announce their purpose (e.g., "Resize sessions panel").
- **keyboard-region-nav**: Keyboard navigation MUST allow moving focus between all major regions: sessions, file tree, editor, terminal, inspector, and toolbar.
- **keyboard-panel-shortcuts**: The window MUST support standard macOS keyboard shortcuts for panel toggling (to be defined at implementation time and recorded as Design Decisions).

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pw-001 | hsplit-three-panels | Open a project window | HSplitView renders with sessions, file tree, and detail panels |
| pw-002 | vsplit-editor-terminal | Inspect detail panel | VSplitView contains editor (top) and terminal (bottom) |
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
| pw-020 | sessions-toggle-label | Enable VoiceOver, focus sessions toolbar button | Announces "Toggle Sessions Panel" |
| pw-021 | keyboard-region-nav | Press Tab repeatedly through window | Focus moves between sessions, file tree, editor, terminal, toolbar |
| pw-022 | immediate-settings-save | Toggle inspector, immediately force-quit app, relaunch | Inspector state matches last toggle (persisted immediately) |

## Edge Cases

- **All side panels hidden**: If sessions and file tree are both hidden, the detail panel fills the full window width. The toolbar toggle buttons remain accessible to restore them.
- **Window at minimum size with all panels visible**: Panels MUST respect their minimum width constraints. If the window is too narrow to satisfy all minimums simultaneously, the rightmost resizable panel (detail) SHOULD compress first down to its minimum, and the split view SHOULD prevent further shrinking.
- **Very long repo root name**: The folder header SHOULD truncate with trailing ellipsis rather than overflowing.
- **Multiple project windows open**: Each window has its own ProjectSettings and frame autosave identifier. Settings changes in one window MUST NOT affect another.
- **Inspector toggled rapidly**: Animation MUST not stack or glitch. Each toggle SHOULD cancel any in-flight animation and start fresh.
- **visionOS volume placement**: On visionOS, the window renders as a standard window volume. Panel layout is identical but the user cannot resize panes via drag on visionOS — pane proportions are controlled via settings.

## Configuration

Layout proportions and pane visibility are persisted per-project in ProjectSettings. Keys SHOULD be declared through the `settings-keys` ingredient.

### Project Settings

| Option | Type | Default | Description |
|---------|------|---------|-------------|
| `sessionPanelProportion` | `Double` | `0.15` | Sessions panel width as fraction of window width |
| `fileTreeProportion` | `Double` | `0.20` | File tree panel width as fraction of window width |
| `detailSplitRatio` | `Double` | `0.5` | Vertical split ratio between editor and terminal (0.0 = all terminal, 1.0 = all editor) |
| `isSessionPanelVisible` | `Bool` | `true` | Whether the sessions panel is shown |
| `isFileViewerVisible` | `Bool` | `true` | Whether the file tree panel is shown |
| `isTerminalVisible` | `Bool` | `true` | Whether the terminal pane is shown |
| `isInspectorPresented` | `Bool` | `false` | Whether the inspector panel is shown |

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
- **Compose**: Use a `Row` of weighted panels (`Modifier.weight`) for sessions, file tree and detail, and a `Column` with draggable divider for editor over terminal. Animate visibility with `AnimatedVisibility`. Persist proportions and visibility in per-project settings storage. The inspector is a trailing `Row` child with a fixed 250dp width.
- **React/Web**: Use CSS grid (or a resizable-panels library) for the three-column layout with a nested vertical split in the detail area. Each panel uses `min-width`/`max-width` constraints; visibility toggles use CSS transitions disabled under `prefers-reduced-motion`. Persist proportions and visibility in `localStorage` keyed by project.

## Design Decisions

**Decision**: Fixed 2-pane detail layout. The layout uses a fixed VSplitView with editor (top) and terminal (bottom). A future version MAY evolve to a flexible N-pane layout supporting arbitrary pane configurations (file editor, terminal sessions, IDE integration panes).
**Rationale**: A fixed two-pane detail area is the smallest layout that serves the current panels. When the flexible layout ships, the spec should be updated to document a `PaneType` enum and `PaneLayout` struct.
**Approved**: pending

**Decision**: File tree default width of 20% (`fileTreeProportion = 0.20`). Some implementations may prefer 40% for better file name readability.
**Rationale**: The proportion is configurable per project, so the default can be adjusted from user feedback without changing the layout contract.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [privacy](agenticdevelopercookbook://guidelines/implementing/security/privacy) | partial | Privacy |
| [localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization) | partial | Localization |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Project Window recipe |
