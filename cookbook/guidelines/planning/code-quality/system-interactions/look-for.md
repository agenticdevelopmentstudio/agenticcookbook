
- `should-anchor-groups-on-lifecycle-callbacks`: `UIApplicationDelegate`, `SceneDelegate`, `Application`/`Activity` lifecycle or equivalent implementations, and whether groups are anchored on them
- `should-treat-each-os-integration-point-as-distinct`: push notification handling, URL scheme or deep-link routing and other OS integration points folded into unrelated groups
- `should-give-background-code-own-group`: `BGTaskScheduler`, `WorkManager`, `JobScheduler`, background sync or `IBackgroundTask` code with no group of its own
- `should-not-mix-background-with-foreground-ui`: background-context code in the same group as foreground UI code
- `should-group-ipc-with-infrastructure`: shared-container, XPC, `Intent`, named-pipe or `postMessage` IPC code grouped with the feature it serves
- `should-place-composition-roots-in-bootstrap-group`: an `AppDelegate` or similar callback calling many services, placed in a feature group
