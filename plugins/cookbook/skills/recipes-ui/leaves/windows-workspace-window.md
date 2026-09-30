<!-- leaf: recipes-ui/windows-workspace-window · source: recipes/ui/windows/workspace-window.md -->

**Rules** (cite as `recipes-ui/windows-workspace-window#<slug>`):

- `hsplit-sidebar-detail` MUST
- `persist-window-frame` MUST
- `sidebar-default-30pct` MUST
- `resizable-min-size` MUST
- `two-section-sidebar` MUST
- `project-row-display` MUST
- `directory-disclosure-group` MUST
- `directory-row-icon` MUST
- `discovered-project-row` MUST
- `double-click-open` MUST
- `sync-progress-indicator` MUST
- `project-context-menu` MUST
- `directory-context-menu` MUST
- `detail-pane-metadata` MUST
- `welcome-empty-state` MUST
- `workspace-package-format` MUST
- `sqlite-table-schema` MUST
- `sync-on-entry-change` MUST
- `coordinator-pool-manager` MUST
- `aggregate-sync-state` MUST
- `auto-discover-projects` MUST
- `per-entry-cache-dir` MUST
- `entry-type-enum` MUST
- `auto-correct-entry-type` MUST
- `prevent-self-referential` MUST
- `prevent-duplicate-entry` MUST
- `keyboard-sidebar-nav` MUST
- `project-row-label` MUST
- `directory-row-label` MUST
- `discovered-row-label` MUST
- `sync-voiceover-announce` MUST
- `context-menu-labels` MUST
- `tab-focus-transfer` MUST
- `empty-state-accessible` MUST

# Workspace Window

## Overview

A two-pane workspace browser window for managing multiple projects. The window uses a horizontal split view with a sidebar (left) listing project and directory entries, and a detail pane (right) showing the selected entry's information or a welcome/empty state. Workspace state is persisted as a `.catnip-workspace` package containing a SQLite database. Directory entries are auto-scanned for `.catnip-proj` packages via a pool of `DirectoryWatchCoordinator` instances managed by `WorkspaceDirectoryManager`.

## Terminology

| Term | Definition |
|------|-----------|
| Workspace | A `.catnip-workspace` package that groups multiple project and directory references into a single browsable window |
| Entry | A reference to either a project file (`.catnip-proj`) or a directory to scan for projects |
| Project entry | An entry of type `.project` that directly references a `.catnip-proj` package |
| Directory entry | An entry of type `.directory` that references a folder scanned for `.catnip-proj` packages |
| Discovered project | A `.catnip-proj` package automatically found inside a watched directory entry |
| Sidebar proportion | The fractional width of the sidebar relative to the total window width (default 0.3) |
| Workspace document | The `.catnip-workspace` package containing `workspace.db` (SQLite) |
| Self-referential loop | The condition where a workspace's own `.catnip-workspace` package would be added as an entry |

## Behavioral Requirements

### Window

- **hsplit-sidebar-detail**: The window MUST use an `HSplitView` with a sidebar on the left and a detail pane on the right.
- **persist-window-frame**: The window MUST persist its frame (position and size) between sessions using the window frame persistence mechanism described in window-frame-persistence.md. The autosave name MUST be derived from a hash of the workspace file path.
- **sidebar-default-30pct**: The sidebar proportion MUST default to `0.3` and MUST be persisted in the workspace document's `settings` table.
- **resizable-min-size**: The window MUST be resizable with a minimum size sufficient to display the sidebar and detail pane without clipping content.

### Sidebar

- **two-section-sidebar**: The sidebar MUST display two sections: "Projects" (top) and "Directories" (bottom).
- **project-row-display**: The "Projects" section MUST list all entries of type `.project`. Each row MUST display a package icon (`shippingbox.fill`, orange) and the project name, with the file path shown as secondary text.
- **directory-disclosure-group**: The "Directories" section MUST list all entries of type `.directory`. Each directory entry MUST render as a `DisclosureGroup` that expands to show auto-discovered `.catnip-proj` packages within that directory.
- **directory-row-icon**: Each directory entry row MUST display a folder icon (`folder.fill`) and the directory name.
- **discovered-project-row**: Discovered projects within a directory `DisclosureGroup` MUST display a package icon (`shippingbox.fill`, orange) and the project name.
- **double-click-open**: Double-tapping (or double-clicking) a project entry or a discovered project MUST open that project via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **sync-progress-indicator**: A sync progress indicator MUST be displayed at the bottom of the sidebar when any directory coordinator is syncing. Display MUST follow the pattern in directory-sync.md (aggregated `isSyncing` state).

### Context Menus

- **project-context-menu**: Each project entry MUST have a context menu with the following items:
  - "Open Project" — opens the project (same behavior as double-tap, double-click-open)
  - "Remove from Workspace" — removes the entry from the workspace document
- **directory-context-menu**: Each directory entry MUST have a context menu with the following item:
  - "Remove from Workspace" — removes the entry and its associated coordinator from the workspace

### Detail Pane

- **detail-pane-metadata**: When an entry is selected in the sidebar, the detail pane MUST display an entry detail view showing metadata or project information for the selected entry.
- **welcome-empty-state**: When no entry is selected, the detail pane MUST display an empty-state/welcome view as described in empty-state.md, with the following action buttons:
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

- **coordinator-pool-manager**: The `WorkspaceDirectoryManager` MUST manage a pool of `DirectoryWatchCoordinator` instances, one per directory entry, as specified in directory-sync.md coordinator-per-entry through dedicated-cache-directory.
- **aggregate-sync-state**: The manager MUST aggregate `isSyncing` across all coordinators. The workspace-level `isSyncing` MUST be `true` if any coordinator is syncing.
- **auto-discover-projects**: The manager MUST auto-discover `.catnip-proj` packages within each watched directory and report them via an `onDiscoveryChanged` callback for document persistence.
- **per-entry-cache-dir**: Each coordinator MUST use a dedicated cache directory named `cache-{entryID}` within the workspace package.

### Entry Types and Validation

- **entry-type-enum**: Entry type MUST be one of: `.project` (direct reference to a `.catnip-proj` file) or `.directory` (a directory scanned for projects).
- **auto-correct-entry-type**: If an entry has type `.project` but its path does not end with `.catnip-proj`, the type MUST be automatically corrected to `.directory` (entry type migration).
- **prevent-self-referential**: The workspace MUST prevent adding its own `.catnip-workspace` package as an entry (self-referential loop detection). If the user attempts to add a path that resolves to the workspace's own package, the add operation MUST be rejected and a warning MUST be logged.
- **prevent-duplicate-entry**: The workspace MUST prevent adding duplicate entries. If the user attempts to add a path already present as an entry, the add operation MUST be rejected.

## Appearance

```
+-------------------------------------------------------+
| Workspace: MyWorkspace                                |
+------------------+------------------------------------+
|                  |                                    |
| PROJECTS         |                                    |
|  [pkg] App.catnip|    Entry Detail View               |
|  [pkg] Lib.catnip|    or                              |
|                  |    Empty State / Welcome            |
| DIRECTORIES      |    ┌─────────────────────┐         |
|  [dir] ~/Code    |    │ [icon]              │         |
|    [pkg] Found1  |    │ Welcome to Workspace│         |
|    [pkg] Found2  |    │                     │         |
|  [dir] ~/Plugins |    │ [Add Directory]     │         |
|    [pkg] Found3  |    │ [Add Project]       │         |
|                  |    └─────────────────────┘         |
|                  |                                    |
+--[SyncProgressBar]+------------------------------------+
```

- **Layout**: `HSplitView` — sidebar (left), detail pane (right)
- **Sidebar width**: Proportional, default 0.3 of window width, user-adjustable via split divider
- **Section headers**: "Projects" and "Directories", uppercase, secondary color, small font weight
- **Project row**: Package icon (`shippingbox.fill`, orange) + project name (primary text) + path (secondary text, truncated)
- **Directory row**: Folder icon (`folder.fill`, accent) + directory name
- **Discovered project row**: Package icon (`shippingbox.fill`, orange) + project name, indented within disclosure group
- **Sync indicator**: `SyncProgressBar` at the bottom of the sidebar, visible only when syncing
- **Detail pane background**: Standard window background
- **Empty state**: Centered per empty-state.md with folder icon, welcome heading, and action buttons

## Accessibility

- **keyboard-sidebar-nav**: The sidebar MUST be navigable via keyboard — arrow keys to move between entries, Return/Space to select, Right arrow to expand disclosure groups, Left arrow to collapse.
- **project-row-label**: Each project entry row MUST have an accessibility label that includes the project name and "project" role.
- **directory-row-label**: Each directory entry row MUST have an accessibility label that includes the directory name and "directory" role.
- **discovered-row-label**: Discovered project rows MUST have accessibility labels that include the project name and "discovered project" role.
- **sync-voiceover-announce**: The sync progress indicator MUST be announced by VoiceOver when its visibility changes (e.g., "Syncing directories" when it appears, "Sync complete" when it disappears).
- **context-menu-labels**: Context menu items MUST have descriptive accessibility labels matching their visible text.
- **tab-focus-transfer**: Tab key MUST move focus between the sidebar and detail pane.
- **empty-state-accessible**: The empty-state action buttons MUST be accessible per empty-state.md heading-first-announce through decorative-icon.

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Disclosure group expand/collapse transitions are instant (no animation) |
| Reduce Transparency | Sidebar and detail pane use opaque backgrounds |
| Increase Contrast | Section headers, selection highlights, and icon colors use higher-contrast values |
| VoiceOver | Entry rows announce name, type, and status; disclosure state announced on directory entries; sync progress announced on visibility change; context menu items announced |

