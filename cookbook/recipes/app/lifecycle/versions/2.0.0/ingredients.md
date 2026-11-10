
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Startup Behavior | `agenticdevelopercookbook://ingredients/app/startup-behavior` | Resolves the startup mode and controls untitled-window creation | Yes | Default `restoreSession` |
| Session Restore | `agenticdevelopercookbook://ingredients/app/session-restore` | Saves and reopens document URLs | Yes | Active when mode is `restoreSession` |
| Child Process Cleanup | `agenticdevelopercookbook://ingredients/app/child-process-cleanup` | Terminates child processes on quit | Yes | Timeout 5 seconds |
| Settings Keys | `agenticdevelopercookbook://ingredients/infrastructure/settings-keys` | Central keys for the startup mode and restore list | Yes | Keys in a constants enum or struct |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Logger for lifecycle events | Yes | Category `AppLifecycle` |

