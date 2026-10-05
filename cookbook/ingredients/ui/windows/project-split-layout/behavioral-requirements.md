
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

