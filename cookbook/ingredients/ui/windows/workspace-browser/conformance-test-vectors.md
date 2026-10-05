
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
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
| ws-029 | keyboard-sidebar-nav | Focus sidebar, press Down arrow | Selection moves to next entry |
| ws-030 | keyboard-sidebar-nav | Focus on collapsed directory entry, press Right arrow | DisclosureGroup expands |
| ws-031 | tab-focus-transfer | Press Tab from sidebar | Focus moves to detail pane |

