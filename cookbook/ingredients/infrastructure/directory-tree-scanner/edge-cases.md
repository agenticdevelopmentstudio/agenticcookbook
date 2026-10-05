
- **Large repository (100k+ files)**: Full sync SHOULD complete within a reasonable time. Parallel scanning (parallel-top-level-scan) and configurable concurrency (configurable-scan-workers) mitigate this. The UI MUST remain responsive during sync — all scanning is off the main thread.
- **Permission denied on subdirectory**: The scanner MUST skip inaccessible directories during scan and log a warning. It MUST NOT crash or abort the entire sync.
- **Symlink cycles**: The scanner MUST NOT follow symlinks recursively into cycles. It SHOULD detect symlinks and either skip or represent them as leaf nodes.
- **Package directories**: Directories identified as packages (file-tree-node-fields `isPackage`) SHOULD NOT have their children scanned by default. They are treated as opaque files.
- **Empty directory**: A directory with no children MUST be represented as a node with an empty `children` array, not `nil`.

