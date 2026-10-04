
Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Cache load started | debug | `DirectorySync: loading cache from "{{path}}"` |
| Cache load succeeded | debug | `DirectorySync: cache loaded, {{count}} entries` |
| Cache load failed | warning | `DirectorySync: cache load failed: {{error}}` |
| Cache not found | debug | `DirectorySync: no cache file found, starting fresh` |
| Full sync started | info | `DirectorySync: full sync started for "{{rootPath}}"` |
| Full sync completed | info | `DirectorySync: full sync completed, {{nodeCount}} nodes in {{duration}}s` |
| Cache save started | debug | `DirectorySync: saving cache ({{count}} entries)` |
| Cache save succeeded | debug | `DirectorySync: cache saved to "{{path}}"` |
| Cache save failed | warning | `DirectorySync: cache save failed: {{error}}` |
| Watch started | info | `DirectorySync: FSEvents watch started for "{{rootPath}}"` |
| Watch stopped | info | `DirectorySync: FSEvents watch stopped` |
| Change event received | debug | `DirectorySync: {{changeCount}} changes received, {{affectedDirCount}} directories affected` |
| Surgical update started | debug | `DirectorySync: surgical update for {{dirCount}} directories` |
| Surgical update completed | debug | `DirectorySync: surgical update completed in {{duration}}s` |
| Directory skipped (permission) | warning | `DirectorySync: skipped "{{path}}" — permission denied` |
| Excluded path filtered | debug | `DirectorySync: filtered {{count}} excluded paths` |
| Workspace coordinator created | debug | `DirectorySync: workspace coordinator created for entry "{{entryID}}"` |
| Workspace syncing state changed | debug | `DirectorySync: workspace isSyncing={{value}}` |
| Project auto-discovered | info | `DirectorySync: discovered .catnip-proj at "{{path}}"` |
| Scan worker count | debug | `DirectorySync: maxScanWorkers={{count}}` |

