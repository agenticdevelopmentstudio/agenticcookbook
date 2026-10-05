
Subsystem: `{{bundle_id}}` | Category: `AppLifecycle`

| Event | Level | Message |
|-------|-------|---------|
| App launched | info | `AppLifecycle: launched, startup behavior = "{{mode}}"` |
| Startup behavior resolved | debug | `AppLifecycle: resolved startup behavior to "{{mode}}" (setting: "{{setting}}", fallback: {{fallback}})` |
| Untitled file suppressed | debug | `AppLifecycle: applicationShouldOpenUntitledFile returning false (mode = "{{mode}}")` |
| Untitled file allowed | debug | `AppLifecycle: applicationShouldOpenUntitledFile returning true` |

