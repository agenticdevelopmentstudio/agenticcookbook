<!-- leaf: recipes-ui/windows-workspace-window--test-vectors · source: recipes/ui/windows/workspace-window.md -->

# Workspace Window

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
