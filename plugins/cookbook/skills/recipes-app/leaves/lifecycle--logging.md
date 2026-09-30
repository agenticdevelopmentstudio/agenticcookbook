<!-- leaf: recipes-app/lifecycle--logging · source: recipes/app/lifecycle.md -->

# App Lifecycle

## Logging

Subsystem: `{{bundle_id}}` | Category: `AppLifecycle`

| Event | Level | Message |
|-------|-------|---------|
| App launched | info | `AppLifecycle: launched, startup behavior = "{{mode}}"` |
| Startup behavior resolved | debug | `AppLifecycle: resolved startup behavior to "{{mode}}" (setting: "{{setting}}", fallback: {{fallback}})` |
| Session restore started | info | `AppLifecycle: restoring {{count}} document(s)` |
| Document restored | debug | `AppLifecycle: restored "{{path}}"` |
| Document restore skipped (missing) | warning | `AppLifecycle: skipping missing file "{{path}}"` |
| Document restore skipped (unrecognized type) | debug | `AppLifecycle: skipping unrecognized file type "{{path}}" (extension: "{{ext}}")` |
| Session restore completed | info | `AppLifecycle: restore complete, opened {{opened}} of {{total}} document(s)` |
| Session restore fell back to newWindow | debug | `AppLifecycle: no valid URLs to restore, falling back to newWindow` |
| URL list saved | debug | `AppLifecycle: saved {{count}} document URL(s) for restore` |
| URL list save failed | error | `AppLifecycle: failed to save document URLs: {{error}}` |
| Untitled file suppressed | debug | `AppLifecycle: applicationShouldOpenUntitledFile returning false (mode = "{{mode}}")` |
| Untitled file allowed | debug | `AppLifecycle: applicationShouldOpenUntitledFile returning true` |
| Child process cleanup started | info | `AppLifecycle: terminating {{count}} child process(es)` |
| SIGHUP sent | debug | `AppLifecycle: sent SIGHUP to process group {{pgid}}` |
| Child process terminated | debug | `AppLifecycle: child process {{pid}} ("{{name}}") terminated` |
| Child process cleanup timeout | warning | `AppLifecycle: child process {{pid}} ("{{name}}") did not terminate within {{timeout}}s, sending SIGKILL` |
| All child processes cleaned up | info | `AppLifecycle: all child processes terminated` |
| App terminating | info | `AppLifecycle: applicationWillTerminate` |
