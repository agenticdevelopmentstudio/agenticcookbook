<!-- leaf: recipes-infrastructure/directory-sync--edge-cases · source: recipes/infrastructure/directory-sync.md -->

# Directory Sync / Watch Lifecycle

**Rules** (cite as `recipes-infrastructure/directory-sync--edge-cases#<slug>`):

- `large-repository` MUST — Full sync SHOULD complete within a reasonable time. Parallel scanning (parallel-top-level-scan) and configurable …
- `rapid-filesystem-changes` SHOULD — The 0.5s debounce (debounce-latency) coalesces rapid changes into a single surgical update. If changes arrive faster …
- `corrupt-cache-file` MUST — The coordinator MUST handle malformed JSON gracefully (handle-missing-cache) — log a warning and proceed with full sync …
- `network-remote-drives` SHOULD — FSEvents may not work reliably on network-mounted volumes. The coordinator SHOULD fall back to periodic polling or …
- `directory-deleted-while-watching` MUST — The coordinator MUST handle the root directory being deleted or unmounted. It SHOULD publish an empty tree and stop the …
- `permission-denied-on-subdirectory` MUST — The coordinator MUST skip inaccessible directories during scan and log a warning. It MUST NOT crash or abort the entire …
- `symlink-cycles` MUST — The coordinator MUST NOT follow symlinks recursively into cycles. It SHOULD detect symlinks and either skip or …
- `package-directories` SHOULD — Directories identified as packages (file-tree-node-fields isPackage) SHOULD NOT have their children scanned by default. …
- `concurrent-cache-writes` SHOULD — If a surgical update triggers a cache save while a previous save is still in progress, the coordinator SHOULD coalesce …
- `empty-directory` MUST — A directory with no children MUST be represented as a node with an empty children array, not nil.

## Edge Cases

- **Large repository (100k+ files)**: Full sync SHOULD complete within a reasonable time. Parallel scanning (parallel-top-level-scan) and configurable concurrency (configurable-scan-workers) mitigate this. The UI MUST remain responsive during sync — all scanning is off the main thread.
- **Rapid filesystem changes**: The 0.5s debounce (debounce-latency) coalesces rapid changes into a single surgical update. If changes arrive faster than the update cycle, the coordinator SHOULD batch them rather than queueing unbounded updates.
- **Corrupt cache file**: The coordinator MUST handle malformed JSON gracefully (handle-missing-cache) — log a warning and proceed with full sync as if no cache exists.
- **Cache file missing or unreadable**: Same behavior as corrupt cache — empty/loading state, then full sync.
- **Network/remote drives**: FSEvents may not work reliably on network-mounted volumes. The coordinator SHOULD fall back to periodic polling or disable watch mode for non-local filesystems. Implementors SHOULD detect volume type and adapt.
- **Directory deleted while watching**: The coordinator MUST handle the root directory being deleted or unmounted. It SHOULD publish an empty tree and stop the FSEvents stream.
- **Permission denied on subdirectory**: The coordinator MUST skip inaccessible directories during scan and log a warning. It MUST NOT crash or abort the entire sync.
- **Symlink cycles**: The coordinator MUST NOT follow symlinks recursively into cycles. It SHOULD detect symlinks and either skip or represent them as leaf nodes.
- **Package directories**: Directories identified as packages (file-tree-node-fields `isPackage`) SHOULD NOT have their children scanned by default. They are treated as opaque files.
- **Concurrent cache writes**: If a surgical update triggers a cache save while a previous save is still in progress, the coordinator SHOULD coalesce or serialize writes to avoid conflicts.
- **Empty directory**: A directory with no children MUST be represented as a node with an empty `children` array, not `nil`.
