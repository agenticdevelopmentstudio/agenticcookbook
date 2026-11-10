
| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| ProjectSettings (proportions, visibility) | Project Split Layout | Project Split Layout, Collapsible Pane Header | two-way | Per-project settings written immediately; restored on open |
| Pane collapsed state | Collapsible Pane Header | Project Split Layout (detail area) | two-way | Binding on each header; terminal visibility mirrors `isTerminalVisible` |
| Selected item | File Tree Browser | Inspector Panel | one-way | Selection binding feeding the inspector |
| Directory sync status | File Tree Browser | Status Bar | one-way | Sync-in-progress flag drives the overlay at the bottom of the file tree panel |
| Window frame autosave name | Project path (SHA256) | Window Frame Persistence | one-way | Hash of the project path set as the frame autosave name |
| Running processes and file watcher | Terminal Pane, File Tree Browser | Window close handler | one-way | `terminateAll` and `stopWatching` called on close |

