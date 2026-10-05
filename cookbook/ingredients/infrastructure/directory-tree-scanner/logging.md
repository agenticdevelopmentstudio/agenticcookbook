
Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Full sync started | info | `DirectorySync: full sync started for "{{rootPath}}"` |
| Full sync completed | info | `DirectorySync: full sync completed, {{nodeCount}} nodes in {{duration}}s` |
| Surgical update started | debug | `DirectorySync: surgical update for {{dirCount}} directories` |
| Surgical update completed | debug | `DirectorySync: surgical update completed in {{duration}}s` |
| Directory skipped (permission) | warning | `DirectorySync: skipped "{{path}}" — permission denied` |
| Scan worker count | debug | `DirectorySync: maxScanWorkers={{count}}` |

