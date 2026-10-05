
### Load

- **load-cached-tree**: On startup, the cache loader MUST attempt to load a cached tree from the JSON file `file-tree-cache.json` for instant display.
- **background-cache-load**: The cache MUST be loaded synchronously on a background queue so the main thread is never blocked.
- **handle-missing-cache**: If no cache file exists or the file cannot be read, the loader MUST present an empty or loading state. It MUST NOT crash or block.

### Format

- **json-cache-format**: The cache MUST be stored as a JSON file using the following entry structure:
  ```
  FileTreeCacheEntry {
    path: String
    parentPath: String?   // nil for root
    name: String
    isDirectory: Bool
    isPackage: Bool
    fileSize: Int?
    modificationDate: Date?   // ISO 8601 encoded
  }
  ```
- **flattened-cache-array**: The cache MUST be a flattened array of `FileTreeCacheEntry` values. Parent-child relationships MUST be reconstructed from `path` / `parentPath` on load.
- **atomic-cache-writes**: Cache writes MUST be atomic — write to a temporary file first, then rename into place. This prevents corruption from interrupted writes.

### Save

- **cache-save-nonblocking**: A cache save MUST be a fire-and-forget operation on a background queue. A save failure MUST NOT block or crash the caller.

