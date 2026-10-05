
- **start-fsevents-watch**: After full sync completes, the watcher MUST start filesystem monitoring using FSEvents (macOS) with file-level granularity.
- **file-level-granularity**: The FSEvents stream MUST be created with `kFSEventStreamCreateFlagFileEvents` for file-level granularity.
- **debounce-latency**: The FSEvents stream MUST use a debounce latency of `0.5` seconds to coalesce rapid changes.
- **utility-qos-queue**: The FSEvents dispatch queue MUST use utility QoS.
- **exclude-path-prefixes**: The watcher MUST exclude paths matching configurable prefixes from change processing. The default excluded prefixes MUST include `.git` and package directories.
- **configurable-exclusions**: Excluded path prefixes MUST be configurable.
- **filter-excluded-paths**: The FSEvents callback MUST filter changed paths against the excluded prefixes before dispatching.
- **dispatch-to-main-thread**: Change events from the FSEvents callback MUST be dispatched to the main thread for UI updates.

