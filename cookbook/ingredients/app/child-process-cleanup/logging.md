
Subsystem: `{{bundle_id}}` | Category: `AppLifecycle`

| Event | Level | Message |
|-------|-------|---------|
| Child process cleanup started | info | `AppLifecycle: terminating {{count}} child process(es)` |
| SIGHUP sent | debug | `AppLifecycle: sent SIGHUP to process group {{pgid}}` |
| Child process terminated | debug | `AppLifecycle: child process {{pid}} ("{{name}}") terminated` |
| Child process cleanup timeout | warning | `AppLifecycle: child process {{pid}} ("{{name}}") did not terminate within {{timeout}}s, sending SIGKILL` |
| All child processes cleaned up | info | `AppLifecycle: all child processes terminated` |
| App terminating | info | `AppLifecycle: applicationWillTerminate` |

