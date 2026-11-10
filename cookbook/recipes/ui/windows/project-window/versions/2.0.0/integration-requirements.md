
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

