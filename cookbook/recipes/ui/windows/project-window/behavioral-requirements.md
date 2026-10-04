
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

