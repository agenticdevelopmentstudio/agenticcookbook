
### Window

- **hsplit-sidebar-detail**: The window MUST use an `HSplitView` with a sidebar on the left and a detail pane on the right.
- **persist-window-frame**: The window MUST persist its frame (position and size) between sessions using the window frame persistence mechanism described in [window-frame-persistence.md](../../../ingredients/infrastructure/window-frame-persistence.md). The autosave name MUST be derived from a hash of the workspace file path.
- **sidebar-default-30pct**: The sidebar proportion MUST default to `0.3` and MUST be persisted in the workspace document's `settings` table.
- **resizable-min-size**: The window MUST be resizable with a minimum size sufficient to display the sidebar and detail pane without clipping content.

### Sidebar

- **two-section-sidebar**: The sidebar MUST display two sections: "Projects" (top) and "Directories" (bottom).
- **project-row-display**: The "Projects" section MUST list all entries of type `.project`. Each row MUST display a package icon (`shippingbox.fill`, orange) and the project name, with the file path shown as secondary text.
- **directory-disclosure-group**: The "Directories" section MUST list all entries of type `.directory`. Each directory entry MUST render as a `DisclosureGroup` that expands to show auto-discovered `.catnip-proj` packages within that directory.
- **directory-row-icon**: Each directory entry row MUST display a folder icon (`folder.fill`) and the directory name.
- **discovered-project-row**: Discovered projects within a directory `DisclosureGroup` MUST display a package icon (`shippingbox.fill`, orange) and the project name.
- **double-click-open**: Double-tapping (or double-clicking) a project entry or a discovered project MUST open that project via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **sync-progress-indicator**: A sync progress indicator MUST be displayed at the bottom of the sidebar when any directory coordinator is syncing. Display MUST follow the pattern in [directory-sync.md](../../infrastructure/directory-sync.md) (aggregated `isSyncing` state).

### Context Menus

- **project-context-menu**: Each project entry MUST have a context menu with the following items:
  - "Open Project" — opens the project (same behavior as double-tap, double-click-open)
  - "Remove from Workspace" — removes the entry from the workspace document
- **directory-context-menu**: Each directory entry MUST have a context menu with the following item:
  - "Remove from Workspace" — removes the entry and its associated coordinator from the workspace

### Detail Pane

- **detail-pane-metadata**: When an entry is selected in the sidebar, the detail pane MUST display an entry detail view showing metadata or project information for the selected entry.
- **welcome-empty-state**: When no entry is selected, the detail pane MUST display an empty-state/welcome view as described in [empty-state.md](../../../ingredients/ui/components/empty-state.md), with the following action buttons:
  - "Add Directory" — opens a directory picker to add a new directory entry
  - "Add Project" — opens a file picker (filtered to `.catnip-proj`) to add a new project entry

### Workspace Document

- **workspace-package-format**: The workspace MUST be stored as a `.catnip-workspace` package (directory) containing a `workspace.db` SQLite database.
- **sqlite-table-schema**: The SQLite database MUST contain the following tables:
  - `workspace` — metadata (name, creation date, last modified date)
  - `entries` — project and directory references (id, type, path, name, date added)
  - `discovered_projects` — auto-found `.catnip-proj` packages (id, entry_id, path, name)
  - `settings` — key-value settings (key, value), including `sidebarProportion`
- **sync-on-entry-change**: Adding or removing an entry MUST update the workspace document, which MUST trigger `syncEntries` to reconcile the `WorkspaceDirectoryManager` coordinator pool.

### Workspace Directory Manager

- **coordinator-pool-manager**: The `WorkspaceDirectoryManager` MUST manage a pool of `DirectoryWatchCoordinator` instances, one per directory entry, as specified in [directory-sync.md](../../infrastructure/directory-sync.md) coordinator-per-entry through dedicated-cache-directory.
- **aggregate-sync-state**: The manager MUST aggregate `isSyncing` across all coordinators. The workspace-level `isSyncing` MUST be `true` if any coordinator is syncing.
- **auto-discover-projects**: The manager MUST auto-discover `.catnip-proj` packages within each watched directory and report them via an `onDiscoveryChanged` callback for document persistence.
- **per-entry-cache-dir**: Each coordinator MUST use a dedicated cache directory named `cache-{entryID}` within the workspace package.

### Entry Types and Validation

- **entry-type-enum**: Entry type MUST be one of: `.project` (direct reference to a `.catnip-proj` file) or `.directory` (a directory scanned for projects).
- **auto-correct-entry-type**: If an entry has type `.project` but its path does not end with `.catnip-proj`, the type MUST be automatically corrected to `.directory` (entry type migration).
- **prevent-self-referential**: The workspace MUST prevent adding its own `.catnip-workspace` package as an entry (self-referential loop detection). If the user attempts to add a path that resolves to the workspace's own package, the add operation MUST be rejected and a warning MUST be logged.
- **prevent-duplicate-entry**: The workspace MUST prevent adding duplicate entries. If the user attempts to add a path already present as an entry, the add operation MUST be rejected.

