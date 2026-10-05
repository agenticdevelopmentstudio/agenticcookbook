
A directory tree cache persists an in-memory file tree to a JSON file so the next launch can show a tree instantly, before any filesystem scan has finished. The tree is stored as a flattened array of entries whose parent-child relationships are rebuilt on load, and every write is atomic so an interrupted write can never leave a corrupt cache. Use it wherever a UI shows a potentially large directory tree and must not wait for a scan to display something.

### Terminology

| Term | Definition |
|------|-----------|
| Cache | A JSON file (`file-tree-cache.json`) containing a flattened array of `FileTreeCacheEntry` values |
| File tree node | An in-memory representation of a single file or directory: path, name, metadata, and children |

