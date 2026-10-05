
### Full Sync

- **rebuild-from-filesystem**: The scanner MUST rebuild the entire file tree from the filesystem on a background queue.
- **parallel-top-level-scan**: Top-level directories MUST be scanned in parallel via an `OperationQueue`.
- **configurable-scan-workers**: Parallel scan concurrency MUST be controlled by a configurable `maxScanWorkers` property. The default value MUST be `3`. Valid range MUST be `1` to `8` inclusive. Values outside this range MUST be clamped.
- **file-tree-node-fields**: Each file tree node MUST contain the following fields:
  - `path` — absolute filesystem path (`String`)
  - `name` — display name (`String`)
  - `isDirectory` — whether the node is a directory (`Bool`)
  - `isPackage` — whether the node is a package directory (`Bool`)
  - `fileSize` — size in bytes (`Int?`, nil for directories)
  - `modificationDate` — last modification timestamp (`Date?`)
  - `children` — ordered child nodes (`[FileTreeNode]?`, nil for files)

### Surgical Update

- **surgical-reload-affected**: On receiving filesystem change events, the scanner MUST only reload the children of the affected directories — not rebuild the full tree.
- **build-path-index**: The scanner MUST build a path index from the changed file paths to identify the set of affected parent directories.
- **background-load-children**: New children for affected directories MUST be loaded on a background queue.

