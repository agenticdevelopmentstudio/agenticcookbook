
| State | Behavior |
|-------|----------|
| All panels visible | Full four-panel layout: sessions, file tree, editor+terminal, inspector |
| Sessions hidden | Sessions panel collapses; file tree and detail expand to fill |
| File tree hidden | File tree collapses; detail panel expands to fill |
| Terminal collapsed | Terminal pane collapses; editor fills the detail panel, terminal header remains visible |
| Editor collapsed | Editor pane collapses; terminal fills the detail panel, editor header remains visible |
| Both editor and terminal collapsed | Only pane headers visible stacked vertically in the detail area |
| Inspector visible | Inspector slides in from right, narrowing the detail panel |
| Inspector hidden | Detail panel fills width up to the right edge |
| Project settings sheet | Presented as a sheet over the window, triggered by toolbar gear button |
| Window loading | `onAppear` fires: initial data loads, file watcher starts, terminal auto-opens if configured |
| Window closing | `onClose` fires: processes terminated, watcher stopped |

