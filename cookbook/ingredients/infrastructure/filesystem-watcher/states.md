
| State | Behavior |
|-------|----------|
| Stopped | No stream exists |
| Watching, no changes | Stream is active and idle |
| Debouncing | Changes were received; the watcher waits out the debounce window |
| Delivering | A coalesced, filtered batch is dispatched to the main thread |
| Stopped (root removed) | The watched directory was deleted or unmounted; the stream is stopped |

