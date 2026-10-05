
```
┌─────────────────────────────────────────────────────────────────────────┐
│ [Sessions] [Inspector] [⚙]                              Toolbar       │
├──────────┬──────────────┬───────────────────────────────┬──────────────┤
│          │ ▾ repo-name  │ ▾ Editor                      │              │
│          │              │                               │              │
│ Sessions │  📁 Sources  │   (code editor pane)          │  Inspector   │
│   list   │    📄 App... │                               │  (optional)  │
│          │  📁 Tests    │                               │              │
│          │  📄 Package  │                               │              │
│          │              ├───────────────────────────────┤              │
│          │              │ ▾ Terminal                     │              │
│          │              │                               │              │
│          │              │   (terminal pane)              │              │
│          │              │                               │              │
│          │ ┌──────────┐ │                               │              │
│          │ │ Syncing… │ │                               │              │
├──────────┴─┴──────────┴─┴───────────────────────────────┴──────────────┤
```

`[Sessions | FileTree | Editor/Terminal VSplitView] + Inspector(optional)`

- **Sessions panel** (left): Session list, togglable via toolbar button
- **File tree panel**: File browser with folder header showing repo root name; sync status bar overlay at bottom
- **Detail panel** (center): VSplitView with editor (top) and terminal (bottom), each preceded by a collapsible pane header
- **Inspector panel** (right, optional): Slides in from right via `.inspector` modifier

### Composed states

| State | Behavior |
|-------|----------|
| Terminal collapsed | Terminal pane collapses; editor fills the detail panel, terminal header remains visible |
| Editor collapsed | Editor pane collapses; terminal fills the detail panel, editor header remains visible |
| Both editor and terminal collapsed | Only pane headers visible stacked vertically in the detail area |
| Window loading | `onAppear` fires: initial data loads, file watcher starts, terminal auto-opens if configured |
| Window closing | `onClose` fires: processes terminated, watcher stopped |

