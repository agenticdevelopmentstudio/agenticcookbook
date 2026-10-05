
| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Session manager | Terminal Window Shell | Terminal Pane, menu commands | one-way | Window-scoped instance; published as the focused object |
| Active profile ID | Global app storage | Color Profile, every terminal window | one-way | Read from `@AppStorage`; shared across all terminal windows and project windows |
| Window frame | Window | Window Frame Persistence | two-way | Autosave name `"terminal-window"` |
| Focused session manager | Focused window | Menu commands | one-way | `.focusedObject()` dispatch |

