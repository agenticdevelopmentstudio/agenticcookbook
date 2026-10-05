
Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Cache load started | debug | `DirectorySync: loading cache from "{{path}}"` |
| Cache load succeeded | debug | `DirectorySync: cache loaded, {{count}} entries` |
| Cache load failed | warning | `DirectorySync: cache load failed: {{error}}` |
| Cache not found | debug | `DirectorySync: no cache file found, starting fresh` |
| Cache save started | debug | `DirectorySync: saving cache ({{count}} entries)` |
| Cache save succeeded | debug | `DirectorySync: cache saved to "{{path}}"` |
| Cache save failed | warning | `DirectorySync: cache save failed: {{error}}` |

