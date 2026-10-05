
- **phase-ordering**: The coordinator MUST run the phases in this order: cache load, full sync, watch, surgical update. Watch MUST NOT start before the full sync completes, and a surgical update MUST NOT run before the watch has delivered a change.
- **cache-feeds-first-publish**: The tree produced by the directory tree cache MUST be handed to the coordinator and published before the scanner begins its full sync, so a valid cache always displays before the scan finishes.
- **sync-result-replaces-cache-tree**: When the scanner completes its full sync, the coordinator MUST replace the published tree with the scanned tree and then trigger a cache save of that tree.
- **watch-events-drive-surgical-update**: The changed paths the filesystem watcher delivers (after debounce and exclusion filtering) MUST be passed to the scanner's path index so only the affected directories are reloaded, and the coordinator MUST then apply the result and trigger a cache save.
- **shared-exclusion-policy**: The watcher's excluded prefixes and the scanner's treatment of package directories MUST agree: a path the watcher excludes MUST NOT cause a surgical update, and a package directory the scanner treats as opaque MUST NOT have its children reported as changed nodes.
- **failure-isolation**: A cache load failure, a cache save failure, or a permission-denied directory MUST NOT prevent the remaining phases from running; the coordinator MUST continue from the next phase.
- **main-thread-boundary**: Cache load, scanning, and cache saves MUST run off the main thread; only the application of updated nodes to the published tree and the `isSyncing` publication MUST occur on the main thread.

