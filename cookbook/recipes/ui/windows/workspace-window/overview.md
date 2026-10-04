
A two-pane workspace browser window for managing multiple projects. The window uses a horizontal split view with a sidebar (left) listing project and directory entries, and a detail pane (right) showing the selected entry's information or a welcome/empty state. Workspace state is persisted as a `.catnip-workspace` package containing a SQLite database. Directory entries are auto-scanned for `.catnip-proj` packages via a pool of `DirectoryWatchCoordinator` instances managed by `WorkspaceDirectoryManager`.

