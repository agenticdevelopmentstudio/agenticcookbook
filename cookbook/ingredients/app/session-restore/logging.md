
Subsystem: `{{bundle_id}}` | Category: `AppLifecycle`

| Event | Level | Message |
|-------|-------|---------|
| Session restore started | info | `AppLifecycle: restoring {{count}} document(s)` |
| Document restored | debug | `AppLifecycle: restored "{{path}}"` |
| Document restore skipped (missing) | warning | `AppLifecycle: skipping missing file "{{path}}"` |
| Document restore skipped (unrecognized type) | debug | `AppLifecycle: skipping unrecognized file type "{{path}}" (extension: "{{ext}}")` |
| Session restore completed | info | `AppLifecycle: restore complete, opened {{opened}} of {{total}} document(s)` |
| Session restore fell back to newWindow | debug | `AppLifecycle: no valid URLs to restore, falling back to newWindow` |
| URL list saved | debug | `AppLifecycle: saved {{count}} document URL(s) for restore` |
| URL list save failed | error | `AppLifecycle: failed to save document URLs: {{error}}` |

