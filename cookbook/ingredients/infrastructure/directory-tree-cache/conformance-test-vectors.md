
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| tree-cache-001 | load-cached-tree, background-cache-load | Launch with a valid `file-tree-cache.json` on disk | Cached tree is loaded on a background queue and returned without blocking the main thread |
| tree-cache-002 | handle-missing-cache | Launch with no cache file on disk | Empty/loading state is returned; no error |
| tree-cache-003 | handle-missing-cache | Launch with a corrupt (invalid JSON) cache file | Empty/loading state is returned; no error |
| tree-cache-004 | atomic-cache-writes | Kill the process during a cache write | On next launch, the cache file is either the old valid version or the new valid version — never partial or corrupt |
| tree-cache-005 | flattened-cache-array | Load a cache with 100 entries and verify parent-child wiring | All entries with `parentPath` matching another entry's `path` are wired as children |
| tree-cache-006 | json-cache-format | Save a tree containing a file and a directory | The file on disk is valid JSON whose entries have all `FileTreeCacheEntry` fields |
| tree-cache-007 | cache-save-nonblocking | Make the cache location read-only and request a save | The save fails with a warning; the caller is not blocked and does not crash |

