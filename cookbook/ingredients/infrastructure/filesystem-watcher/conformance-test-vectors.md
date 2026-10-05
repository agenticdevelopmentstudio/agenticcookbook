
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| fs-watcher-001 | debounce-latency | Create 10 files within 0.3 seconds | A single coalesced change event is delivered after the 0.5s debounce |
| fs-watcher-002 | exclude-path-prefixes, filter-excluded-paths | Create a file inside `.git/` | No event is delivered for it; the batch is empty |
| fs-watcher-003 | file-level-granularity | Modify one file in a nested directory | The event names the file path, not only its parent directory |
| fs-watcher-004 | configurable-exclusions | Add a custom prefix to the exclusions and change a file under it | No event is delivered for that file |
| fs-watcher-005 | dispatch-to-main-thread | Change a watched file | The change callback runs on the main thread |
| fs-watcher-006 | start-fsevents-watch | Start the watcher after a full sync | Stream is active and subsequent changes produce events |

