---
id: 3b83a80f-d170-4ef6-a608-81f3a1476679
title: "Workspace Window"
domain: agenticdevelopercookbook://recipes/ui/windows/workspace-window
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Two-pane workspace browser window for managing multiple projects with auto-discovery of project packages"
platforms:
  - macos
  - swift
  - web
tags:
  - ui
  - window
  - workspace-window
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

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
- **Empty state**: Centered per [empty-state.md](../../../ingredients/ui/components/empty-state.md) with folder icon, welcome heading, and action buttons

## States

| State | Behavior |
|-------|----------|
| No entries | Sidebar shows empty sections, detail pane shows welcome empty state with add buttons (welcome-empty-state) |
| Entries present, none selected | Sidebar lists entries, detail pane shows welcome empty state (welcome-empty-state) |
| Entry selected | Sidebar highlights selection, detail pane shows entry detail (detail-pane-metadata) |
| Directory entry expanded | DisclosureGroup open, discovered projects listed (directory-disclosure-group) |
| Directory entry collapsed | DisclosureGroup closed, discovered projects hidden |
| Syncing | SyncProgressBar visible at sidebar bottom (sync-progress-indicator), `isSyncing` true |
| Sync complete | SyncProgressBar hidden, discovered projects up to date |
| Project opened | Project window opens via NSDocumentController, workspace window remains |
| Entry removed | Entry disappears from sidebar, coordinator stopped (if directory), document updated |
| Entry added | Entry appears in sidebar, coordinator started (if directory), document updated |
| Self-referential add rejected | Add operation silently rejected, warning logged (prevent-self-referential) |
| Entry type migrated | Entry with incorrect type auto-corrected on load (auto-correct-entry-type) |

## Accessibility

- **keyboard-sidebar-nav**: The sidebar MUST be navigable via keyboard — arrow keys to move between entries, Return/Space to select, Right arrow to expand disclosure groups, Left arrow to collapse.
- **project-row-label**: Each project entry row MUST have an accessibility label that includes the project name and "project" role.
- **directory-row-label**: Each directory entry row MUST have an accessibility label that includes the directory name and "directory" role.
- **discovered-row-label**: Discovered project rows MUST have accessibility labels that include the project name and "discovered project" role.
- **sync-voiceover-announce**: The sync progress indicator MUST be announced by VoiceOver when its visibility changes (e.g., "Syncing directories" when it appears, "Sync complete" when it disappears).
- **context-menu-labels**: Context menu items MUST have descriptive accessibility labels matching their visible text.
- **tab-focus-transfer**: Tab key MUST move focus between the sidebar and detail pane.
- **empty-state-accessible**: The empty-state action buttons MUST be accessible per [empty-state.md](../../../ingredients/ui/components/empty-state.md) heading-first-announce through decorative-icon.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ws-001 | hsplit-sidebar-detail | Open a workspace window | HSplitView renders with sidebar (left) and detail pane (right) |
| ws-002 | persist-window-frame | Open workspace, move window to (100, 200), close, reopen | Window appears at (100, 200) |
| ws-003 | sidebar-default-30pct | Open workspace, do not adjust sidebar | Sidebar occupies approximately 30% of window width |
| ws-004 | sidebar-default-30pct | Adjust sidebar proportion to 0.4, close workspace, reopen | Sidebar proportion restored to 0.4 |
| ws-005 | two-section-sidebar | Workspace has 2 project entries and 1 directory entry | Sidebar shows "Projects" section with 2 rows and "Directories" section with 1 row |
| ws-006 | project-row-display | Project entry named "MyApp" at `/path/to/MyApp.catnip-proj` | Row shows orange package icon, "MyApp", and path as secondary text |
| ws-007 | directory-disclosure-group | Directory entry containing 2 `.catnip-proj` packages | DisclosureGroup expands to show 2 discovered project rows |
| ws-008 | double-click-open | Double-click a project entry | Project opens via NSDocumentController |
| ws-009 | double-click-open | Double-click a discovered project within a directory group | Project opens via NSDocumentController |
| ws-010 | sync-progress-indicator | 1 of 2 directory coordinators is syncing | SyncProgressBar visible at sidebar bottom |
| ws-011 | sync-progress-indicator | All coordinators finish syncing | SyncProgressBar hidden |
| ws-012 | project-context-menu | Right-click a project entry | Context menu shows "Open Project" and "Remove from Workspace" |
| ws-013 | directory-context-menu | Right-click a directory entry | Context menu shows "Remove from Workspace" |
| ws-014 | detail-pane-metadata | Select a project entry in sidebar | Detail pane shows project metadata/info |
| ws-015 | welcome-empty-state | No entry selected | Detail pane shows empty state with "Add Directory" and "Add Project" buttons |
| ws-016 | welcome-empty-state | Click "Add Directory" in empty state | Directory picker opens |
| ws-017 | welcome-empty-state | Click "Add Project" in empty state | File picker opens, filtered to .catnip-proj |
| ws-018 | workspace-package-format, sqlite-table-schema | Inspect workspace package on disk | `.catnip-workspace` directory contains `workspace.db` with tables: workspace, entries, discovered_projects, settings |
| ws-019 | sync-on-entry-change | Add a directory entry via UI | Entry appears in `entries` table, `syncEntries` fires, new coordinator created |
| ws-020 | sync-on-entry-change | Remove a directory entry via context menu | Entry removed from `entries` table, coordinator stopped and removed |
| ws-021 | coordinator-pool-manager | Workspace with 3 directory entries | WorkspaceDirectoryManager has 3 coordinators |
| ws-022 | aggregate-sync-state | 1 of 3 coordinators syncing | Workspace-level `isSyncing` is `true` |
| ws-023 | aggregate-sync-state | All 3 coordinators idle | Workspace-level `isSyncing` is `false` |
| ws-024 | auto-discover-projects | Directory entry contains a new `.catnip-proj` package | `onDiscoveryChanged` fires, `discovered_projects` table updated |
| ws-025 | per-entry-cache-dir | Workspace with entry ID "abc" | Cache directory is `cache-abc` within workspace package |
| ws-026 | auto-correct-entry-type | Entry has type `.project` but path is `/Users/me/Code` (no `.catnip-proj` suffix) | Type auto-corrected to `.directory` |
| ws-027 | prevent-self-referential | Attempt to add workspace's own `.catnip-workspace` path as an entry | Add rejected, warning logged |
| ws-028 | prevent-duplicate-entry | Attempt to add `/Users/me/Code` when it already exists as an entry | Add rejected |
| ws-029 | keyboard-sidebar-nav | Focus sidebar, press Down arrow | Selection moves to next entry |
| ws-030 | keyboard-sidebar-nav | Focus on collapsed directory entry, press Right arrow | DisclosureGroup expands |
| ws-031 | tab-focus-transfer | Press Tab from sidebar | Focus moves to detail pane |

## Edge Cases

- **Empty workspace (no entries)**: Both sidebar sections show empty. Detail pane shows welcome empty state with add buttons. The window MUST NOT crash or display broken layout.
- **All entries removed**: Returns to empty workspace state. All coordinators stopped.
- **Directory entry points to non-existent path**: Entry SHOULD display with a warning indicator (e.g., exclamation mark badge). Coordinator SHOULD NOT be created for a missing path. Entry SHOULD remain in the list to allow the user to remove it.
- **Project entry points to non-existent .catnip-proj**: Entry SHOULD display with a warning indicator. Double-tap SHOULD show an error rather than crash.
- **Self-referential add**: prevent-self-referential prevents it. The check MUST resolve symlinks and normalize paths before comparison.
- **Duplicate path add**: prevent-duplicate-entry prevents it. Paths MUST be compared after normalization (resolve symlinks, remove trailing slashes).
- **Very long project/directory name**: Sidebar rows SHOULD truncate with ellipsis. Full path shown in tooltip.
- **Many entries (50+)**: Sidebar MUST scroll. Performance MUST remain acceptable with lazy list rendering.
- **Rapid add/remove**: Document writes MUST be serialized to prevent SQLite contention. `syncEntries` MUST handle the coordinator pool converging to the current entry list without race conditions.
- **Workspace file locked or read-only**: Document operations MUST fail gracefully with a user-visible error. The UI MUST NOT crash.
- **Sidebar proportion at extremes**: If the user drags the split divider to an extreme (< 0.15 or > 0.85), the proportion SHOULD be clamped to maintain usability.
- **Directory entry discovers zero projects**: DisclosureGroup expands but shows no children. SHOULD display a subtle "No projects found" message within the group.
- **Entry type migration on load**: If the workspace database contains entries with incorrect types (auto-correct-entry-type), migration MUST happen silently on load without user intervention.
- **Workspace package corruption**: If `workspace.db` is missing or corrupt within the `.catnip-workspace` package, the document SHOULD attempt to recreate the database with empty tables. A warning MUST be logged.
- **Concurrent workspace access**: If the same workspace is opened in two app instances, SQLite WAL mode SHOULD handle concurrent reads. Writes from one instance SHOULD NOT corrupt the other's state.

## Logging

Subsystem: `{{bundle_id}}` | Category: `WorkspaceWindow`

| Event | Level | Message |
|-------|-------|---------|
| Window opened | debug | `WorkspaceWindow: opened "{{workspacePath}}"` |
| Window closed | debug | `WorkspaceWindow: closed "{{workspacePath}}"` |
| Frame autosave set | debug | `WorkspaceWindow: autosave name "{{hashedName}}"` |
| Sidebar proportion changed | debug | `WorkspaceWindow: sidebar proportion changed to {{value}}` |
| Entry added | info | `WorkspaceWindow: added {{entryType}} entry "{{path}}"` |
| Entry removed | info | `WorkspaceWindow: removed {{entryType}} entry "{{path}}"` |
| Entry selected | debug | `WorkspaceWindow: selected entry "{{name}}" ({{entryType}})` |
| Entry type migrated | warning | `WorkspaceWindow: migrated entry "{{path}}" from .project to .directory (path does not end with .catnip-proj)` |
| Project opened | info | `WorkspaceWindow: opening project "{{path}}"` |
| Project open failed | error | `WorkspaceWindow: failed to open project "{{path}}": {{error}}` |
| Self-referential add rejected | warning | `WorkspaceWindow: rejected self-referential add of "{{path}}"` |
| Duplicate add rejected | warning | `WorkspaceWindow: rejected duplicate entry "{{path}}"` |
| Discovery changed | debug | `WorkspaceWindow: discovery changed for entry "{{entryID}}", {{count}} projects found` |
| Sync entries triggered | debug | `WorkspaceWindow: syncEntries triggered, {{entryCount}} entries` |
| Coordinator created | debug | `WorkspaceWindow: coordinator created for entry "{{entryID}}"` |
| Coordinator removed | debug | `WorkspaceWindow: coordinator removed for entry "{{entryID}}"` |
| Workspace DB opened | debug | `WorkspaceWindow: database opened at "{{dbPath}}"` |
| Workspace DB error | error | `WorkspaceWindow: database error: {{error}}` |
| Workspace DB recreated | warning | `WorkspaceWindow: database recreated due to corruption` |
| Empty state displayed | debug | `WorkspaceWindow: showing welcome empty state` |
| Add directory picker shown | debug | `WorkspaceWindow: showing directory picker` |
| Add project picker shown | debug | `WorkspaceWindow: showing project picker` |
| Non-existent entry path | warning | `WorkspaceWindow: entry "{{path}}" does not exist on disk` |

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Disclosure group expand/collapse transitions are instant (no animation) |
| Reduce Transparency | Sidebar and detail pane use opaque backgrounds |
| Increase Contrast | Section headers, selection highlights, and icon colors use higher-contrast values |
| VoiceOver | Entry rows announce name, type, and status; disclosure state announced on directory entries; sync progress announced on visibility change; context menu items announced |

## Platform Notes

- **SwiftUI (macOS)**: Use `HSplitView` (or `NavigationSplitView` with `.navigationSplitViewStyle(.balanced)`) for the two-pane layout. Sidebar sections use `Section` headers ("Projects", "Directories"). Project rows use `Label` with `Image(systemName: "shippingbox.fill").foregroundStyle(.orange)`. Directory entries use `DisclosureGroup`. Double-click handled via `.onTapGesture(count: 2)` or `List` selection with `onSubmit`. Context menus via `.contextMenu { }`. Open projects via `NSDocumentController.shared.openDocument(withContentsOf:display:completionHandler:)`. Sidebar proportion persisted in workspace SQLite `settings` table. Frame autosave via the `WindowAccessor` pattern from [window-frame-persistence.md](../../../ingredients/infrastructure/window-frame-persistence.md) with the autosave name set to a SHA256 hash prefix of the workspace path. Sync indicator as an overlay or bottom bar within the sidebar column. `WorkspaceDirectoryManager` is `@Observable` (or `ObservableObject`) with `@Published isSyncing`. SQLite access via direct `sqlite3` C API or a lightweight Swift wrapper. Use WAL mode for concurrent read safety.
- **visionOS**: Same SwiftUI implementation as macOS. The window renders in a standard visionOS window volume. `HSplitView` / `NavigationSplitView` adapts to visionOS layout conventions. Double-tap replaces double-click for project opening. Context menus triggered via long press or secondary gesture. `NSDocumentController` is not available on visionOS — project opening must use an alternative mechanism (e.g., custom document handling or `UIDocumentBrowserViewController` equivalent). Frame persistence may not apply in the same way; window placement is managed by the system. The `SyncProgressBar` renders identically.

## Design Decisions

_None yet -- decisions made during implementation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
