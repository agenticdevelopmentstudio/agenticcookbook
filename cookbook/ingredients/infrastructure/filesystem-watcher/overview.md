
A filesystem watcher delivers coalesced, file-level change notifications for a directory subtree. On macOS it wraps an FSEvents stream created with file-level granularity, debounces rapid changes into a single batch, filters out paths under excluded prefixes (such as `.git` and package directories), and hands the surviving paths to the main thread. Use it to drive live updates of an in-memory tree after the initial scan has finished.

### Terminology

| Term | Definition |
|------|-----------|
| FSEvents | The macOS kernel subsystem that delivers file-level change notifications |
| Debounce latency | The coalescing window during which rapid changes are batched into one event |
| Excluded prefix | A path prefix whose changes are ignored |

