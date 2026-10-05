
- **Self-referential add**: prevent-self-referential prevents it. The check MUST resolve symlinks and normalize paths before comparison.
- **Duplicate path add**: prevent-duplicate-entry prevents it. Paths MUST be compared after normalization (resolve symlinks, remove trailing slashes).
- **Rapid add/remove**: Document writes MUST be serialized to prevent SQLite contention. `syncEntries` MUST handle the coordinator pool converging to the current entry list without race conditions.
- **Workspace file locked or read-only**: Document operations MUST fail gracefully with a user-visible error. The UI MUST NOT crash.
- **Entry type migration on load**: If the workspace database contains entries with incorrect types (auto-correct-entry-type), migration MUST happen silently on load without user intervention.
- **Workspace package corruption**: If `workspace.db` is missing or corrupt within the `.catnip-workspace` package, the document SHOULD attempt to recreate the database with empty tables. A warning MUST be logged.
- **Concurrent workspace access**: If the same workspace is opened in two app instances, SQLite WAL mode SHOULD handle concurrent reads. Writes from one instance SHOULD NOT corrupt the other's state.

