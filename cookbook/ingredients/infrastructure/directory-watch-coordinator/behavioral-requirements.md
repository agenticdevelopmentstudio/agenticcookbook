
### Coordinator

- **publish-before-sync**: A loaded cache MUST be published to the UI before the full sync begins, so users see an instant tree.
- **publish-syncing-state**: The coordinator MUST publish an `isSyncing` boolean state that is `true` during the full sync and `false` after it completes. The UI SHOULD use this to display a status bar indicator.
- **save-cache-after-sync**: After the full sync completes, the coordinator MUST save the updated cache to disk as a fire-and-forget operation on a background queue. A save failure MUST NOT block or crash the coordinator.
- **save-cache-after-update**: After a surgical update, the coordinator MUST save the updated cache to disk (fire-and-forget on a background queue).
- **apply-on-main-thread**: The updated children MUST be applied to the in-memory tree on the main thread.

### Workspace Variant

- **coordinator-per-entry**: `WorkspaceDirectoryManager` MUST manage a pool of coordinators, one per workspace directory entry.
- **aggregate-syncing-state**: `WorkspaceDirectoryManager` MUST aggregate the `isSyncing` state across all coordinators. The workspace-level `isSyncing` MUST be `true` if any coordinator is syncing.
- **auto-discover-packages**: `WorkspaceDirectoryManager` MUST additionally scan for `.catnip-proj` packages for auto-discovery of projects.
- **dedicated-cache-directory**: Each coordinator in the workspace MUST use a dedicated cache directory named `cache-{entryID}`.

