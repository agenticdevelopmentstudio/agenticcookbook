
The sidebar-and-detail UI for browsing a workspace of projects. A sidebar lists project entries and directory entries (each directory expands to show auto-discovered projects), a detail pane shows the selected entry or a welcome empty state, context menus remove entries, and a sync progress indicator appears while any directory is syncing. This ingredient owns presentation and interaction only; the persisted workspace data and directory-watching pool are the Workspace Document ingredient.

### Terminology

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

