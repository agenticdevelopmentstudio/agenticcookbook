
### Workspace Document

- **workspace-package-format**: The workspace MUST be stored as a `.catnip-workspace` package (directory) containing a `workspace.db` SQLite database.
- **sqlite-table-schema**: The SQLite database MUST contain the following tables:
  - `workspace` — metadata (name, creation date, last modified date)
  - `entries` — project and directory references (id, type, path, name, date added)
  - `discovered_projects` — auto-found `.catnip-proj` packages (id, entry_id, path, name)
  - `settings` — key-value settings (key, value), including `sidebarProportion`
- **sync-on-entry-change**: Adding or removing an entry MUST update the workspace document, which MUST trigger `syncEntries` to reconcile the `WorkspaceDirectoryManager` coordinator pool.

### Workspace Directory Manager

- **coordinator-pool-manager**: The `WorkspaceDirectoryManager` MUST manage a pool of `DirectoryWatchCoordinator` instances, one per directory entry, as specified in [directory-sync.md](../../../recipes/infrastructure/directory-sync.md) coordinator-per-entry through dedicated-cache-directory.
- **aggregate-sync-state**: The manager MUST aggregate `isSyncing` across all coordinators. The workspace-level `isSyncing` MUST be `true` if any coordinator is syncing.
- **auto-discover-projects**: The manager MUST auto-discover `.catnip-proj` packages within each watched directory and report them via an `onDiscoveryChanged` callback for document persistence.
- **per-entry-cache-dir**: Each coordinator MUST use a dedicated cache directory named `cache-{entryID}` within the workspace package.

### Entry Types and Validation

- **entry-type-enum**: Entry type MUST be one of: `.project` (direct reference to a `.catnip-proj` file) or `.directory` (a directory scanned for projects).
- **auto-correct-entry-type**: If an entry has type `.project` but its path does not end with `.catnip-proj`, the type MUST be automatically corrected to `.directory` (entry type migration).
- **prevent-self-referential**: The workspace MUST prevent adding its own `.catnip-workspace` package as an entry (self-referential loop detection). If the user attempts to add a path that resolves to the workspace's own package, the add operation MUST be rejected and a warning MUST be logged.
- **prevent-duplicate-entry**: The workspace MUST prevent adding duplicate entries. If the user attempts to add a path already present as an entry, the add operation MUST be rejected.

