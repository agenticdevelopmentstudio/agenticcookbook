
| Event | Properties | When |
|-------|-----------|------|
| `project_window.opened` | `{ project_hash: string }` | Project window opens |
| `project_window.closed` | `{ project_hash: string, duration_seconds: number }` | Project window closes |
| `project_window.panel_toggled` | `{ panel: string, visible: bool }` | Any panel visibility toggled |
| `project_window.settings_opened` | `{}` | Gear button clicked, settings sheet presented |

