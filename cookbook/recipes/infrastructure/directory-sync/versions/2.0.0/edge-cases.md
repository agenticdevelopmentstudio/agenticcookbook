
- **Large repository (100k+ files)**: Full sync SHOULD complete within a reasonable time. Parallel scanning and configurable concurrency mitigate this. The UI MUST remain responsive during sync — all scanning is off the main thread (main-thread-boundary).
- **Rapid filesystem changes**: The debounce coalesces rapid changes into a single surgical update. If changes arrive faster than the update cycle, the coordinator SHOULD batch them rather than queueing unbounded updates.
- **Corrupt or missing cache file**: Handled as in the directory tree cache ingredient: log a warning and proceed with full sync as if no cache exists (failure-isolation).
- **Network/remote drives**: FSEvents may not work reliably on network-mounted volumes. The coordinator SHOULD fall back to periodic polling or disable watch mode for non-local filesystems. Implementors SHOULD detect volume type and adapt.
- **Directory deleted while watching**: The coordinator MUST handle the root directory being deleted or unmounted. It SHOULD publish an empty tree and stop the FSEvents stream.
- **Permission denied on subdirectory**: The coordinator MUST skip inaccessible directories during scan and log a warning. It MUST NOT crash or abort the entire sync.
- **Symlink cycles**: The coordinator MUST NOT follow symlinks recursively into cycles. It SHOULD detect symlinks and either skip or represent them as leaf nodes.
- **Package directories**: Directories identified as packages (`isPackage`) SHOULD NOT have their children scanned by default. They are treated as opaque files (shared-exclusion-policy).
- **Concurrent cache writes**: If a surgical update triggers a cache save while a previous save is still in progress, the coordinator SHOULD coalesce or serialize writes to avoid conflicts.
- **Empty directory**: A directory with no children MUST be represented as a node with an empty `children` array, not `nil`.

