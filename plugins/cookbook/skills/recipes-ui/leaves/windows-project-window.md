<!-- leaf: recipes-ui/windows-project-window · source: recipes/ui/windows/project-window.md -->

**Rules** (cite as `recipes-ui/windows-project-window#<slug>`):

- `hsplit-three-panels` MUST
- `vsplit-editor-terminal` MUST
- `collapsible-pane-headers` MUST
- `inspector-slide-right` MUST
- `proportional-sizing` MUST
- `sessions-default-15pct` MUST
- `filetree-default-20pct` MUST
- `detail-fills-remaining` MUST
- `detail-split-50-50` MUST
- `persist-layout-proportions` MUST
- `toggle-sessions-panel` MUST
- `toggle-file-tree` MUST
- `toggle-terminal` MUST
- `toggle-inspector` MUST
- `persist-visibility-state` MUST
- `animate-pane-toggle` MUST
- `toolbar-sessions-button` MUST
- `toolbar-inspector-button` MUST
- `toolbar-gear-button` MUST
- `folder-header-repo-name` MUST
- `persist-window-frame` MUST
- `sha256-autosave-id` MUST
- `sync-status-overlay` MUST
- `load-initial-start-watch` MUST
- `auto-open-terminal` MUST
- `terminate-on-close` MUST
- `delegate-file-tree` MUST
- `delegate-terminal` MUST
- `delegate-inspector` MUST
- `delegate-editor` MUST
- `delegate-pane-headers` MUST
- `persist-project-settings` MUST
- `immediate-settings-save` MUST
- `sessions-toggle-label` MUST
- `inspector-toggle-label` MUST
- `gear-button-label` MUST
- `pane-header-accessible` MUST
- `divider-accessible` MUST
- `keyboard-region-nav` MUST
- `keyboard-panel-shortcuts` MUST

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

- **delegate-file-tree**: The file tree panel MUST delegate to file-tree-browser.md for all file browsing behavior.
- **delegate-terminal**: The terminal pane MUST delegate to terminal-pane.md for all terminal behavior.
- **delegate-inspector**: The inspector panel MUST delegate to inspector-panel.md for all inspector behavior.
- **delegate-editor**: The code editor pane MUST delegate to code-editor-pane.md for all editor behavior.
- **delegate-pane-headers**: Collapsible pane headers MUST delegate to collapsible-pane-header.md for toggle and animation behavior.

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

