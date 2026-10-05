
### Sidebar

- **two-section-sidebar**: The sidebar MUST display two sections: "Projects" (top) and "Directories" (bottom).
- **project-row-display**: The "Projects" section MUST list all entries of type `.project`. Each row MUST display a package icon (`shippingbox.fill`, orange) and the project name, with the file path shown as secondary text.
- **directory-disclosure-group**: The "Directories" section MUST list all entries of type `.directory`. Each directory entry MUST render as a `DisclosureGroup` that expands to show auto-discovered `.catnip-proj` packages within that directory.
- **directory-row-icon**: Each directory entry row MUST display a folder icon (`folder.fill`) and the directory name.
- **discovered-project-row**: Discovered projects within a directory `DisclosureGroup` MUST display a package icon (`shippingbox.fill`, orange) and the project name.
- **double-click-open**: Double-tapping (or double-clicking) a project entry or a discovered project MUST open that project via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **sync-progress-indicator**: A sync progress indicator MUST be displayed at the bottom of the sidebar when any directory coordinator is syncing. Display MUST follow the pattern in [directory-sync.md](../../../recipes/infrastructure/directory-sync.md) (aggregated `isSyncing` state).

### Context Menus

- **project-context-menu**: Each project entry MUST have a context menu with the following items:
  - "Open Project" — opens the project (same behavior as double-tap, double-click-open)
  - "Remove from Workspace" — removes the entry from the workspace document
- **directory-context-menu**: Each directory entry MUST have a context menu with the following item:
  - "Remove from Workspace" — removes the entry and its associated coordinator from the workspace

### Detail Pane

- **detail-pane-metadata**: When an entry is selected in the sidebar, the detail pane MUST display an entry detail view showing metadata or project information for the selected entry.
- **welcome-empty-state**: When no entry is selected, the detail pane MUST display an empty-state/welcome view as described in [empty-state.md](../components/empty-state.md), with the following action buttons:
  - "Add Directory" — opens a directory picker to add a new directory entry
  - "Add Project" — opens a file picker (filtered to `.catnip-proj`) to add a new project entry

