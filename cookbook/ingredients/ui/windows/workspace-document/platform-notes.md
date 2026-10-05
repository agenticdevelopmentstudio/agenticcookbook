
- **SwiftUI (macOS)**: `WorkspaceDirectoryManager` is `@Observable` (or `ObservableObject`) with `@Published isSyncing`. SQLite access via direct `sqlite3` C API or a lightweight Swift wrapper. Use WAL mode for concurrent read safety. Sidebar proportion persisted in the workspace SQLite `settings` table.
- **visionOS**: Same implementation as macOS; the data layer has no platform-specific differences.
- **Compose**: Use a `StateFlow<Boolean>` for aggregated `isSyncing` and an SQLite binding (Room or SQLDelight) for the workspace database.
- **React/Web**: The package format maps to a directory-handle-based store; use an in-browser SQLite build or IndexedDB with the same logical tables.

