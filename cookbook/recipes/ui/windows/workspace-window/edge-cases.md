
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

