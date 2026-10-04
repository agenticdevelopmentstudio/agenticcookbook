
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

