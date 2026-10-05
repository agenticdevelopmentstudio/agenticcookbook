
| Platform | URL Pattern | Behavior |
|----------|-------------|----------|
| Apple | `{{app_scheme}}://settings` or `{{app_scheme}}://settings/{{category}}` | Opens settings window, optionally navigates to a specific category |
| Windows | Command-line flag `--settings` or `--settings={{category}}` | Opens settings on launch |
| Web/Electron | `/settings` or `/settings/{{category}}` | Routes to settings view |

