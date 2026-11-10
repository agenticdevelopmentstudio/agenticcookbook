
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

- **delegate-file-tree**: The file tree panel MUST delegate to [adc.ingredient.ui.panels.file-tree-browser](cookbook:a1845427-a2cd-4744-96bf-f6c6f2380982) for all file browsing behavior.
- **delegate-terminal**: The terminal pane MUST delegate to [adc.ingredient.ui.panels.terminal-pane](cookbook:4a2898cf-34ed-4153-8d06-c795f80c19cd) for all terminal behavior.
- **delegate-inspector**: The inspector panel MUST delegate to [adc.ingredient.ui.panels.inspector-panel](cookbook:6af1d30a-c2ee-4a6d-97ec-50c67f01a243) for all inspector behavior.
- **delegate-editor**: The code editor pane MUST delegate to [adc.ingredient.ui.panels.code-editor-pane](cookbook:954e559c-e2bf-494c-a37e-de0b88bec89a) for all editor behavior.
- **delegate-pane-headers**: Collapsible pane headers MUST delegate to [adc.ingredient.ui.components.collapsible-pane-header](cookbook:1dd2111a-eb05-40e4-b469-1aecd79c5863) for toggle and animation behavior.

- **pane-header-accessible**: Each collapsible pane header MUST follow the accessibility requirements defined by the `collapsible-pane-header` ingredient (button role, expand/collapse announcement, keyboard toggle).

### Wiring

- **layout-hosts-panel-ingredients**: The sessions, file tree, editor, terminal, and inspector slots of the Project Split Layout MUST be filled by the panel ingredients named in the Ingredients table. The layout MUST NOT reimplement any panel's own behavior.
- **header-collapse-drives-detail-area**: Collapsing or expanding a collapsible pane header MUST resize the detail area per the composed states in Layout (the other section fills the space; the collapsed section's header stays visible).
- **settings-keys-central**: The ProjectSettings keys (proportions and visibility) SHOULD be declared through the `settings-keys` ingredient rather than as scattered string literals.
- **log-via-shared-logger**: All window-level log events MUST use the `logging` ingredient's per-category logger with category `ProjectWindow`.

