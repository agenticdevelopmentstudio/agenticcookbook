
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| tree-scanner-001 | rebuild-from-filesystem, parallel-top-level-scan | Full sync on a directory with 5 top-level subdirectories | All 5 subdirectories are scanned and the tree matches the filesystem |
| tree-scanner-002 | configurable-scan-workers | Set `maxScanWorkers` to 0 | Value is clamped to 1; the scan proceeds with 1 worker |
| tree-scanner-003 | configurable-scan-workers | Set `maxScanWorkers` to 10 | Value is clamped to 8; the scan proceeds with 8 workers |
| tree-scanner-004 | file-tree-node-fields | Scan a directory containing a file (100 bytes, modified 2026-01-15) and a subdirectory | File node has correct `fileSize`, `modificationDate`, `isDirectory: false`; directory node has `isDirectory: true` and `children` populated |
| tree-scanner-005 | surgical-reload-affected, build-path-index | Create a new file in subdirectory `src/` | Only `src/` children are reloaded; sibling directories are untouched |
| tree-scanner-006 | background-load-children | Trigger a surgical update | Children are loaded on a background queue, not the main thread |

