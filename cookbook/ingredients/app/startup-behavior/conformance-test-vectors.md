
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-001 | configurable-startup-modes, startup-behavior-setting | Set startup behavior to `newWindow`, launch app | Default window opens |
| lifecycle-003 | configurable-startup-modes | Set startup behavior to `nothing`, launch app | No windows open; app is active in menu bar/dock |
| lifecycle-013 | suppress-untitled-file, allow-untitled-new-window | (macOS) Set startup behavior to `newWindow` | `applicationShouldOpenUntitledFile` returns `true` |
| lifecycle-014 | suppress-untitled-file | (macOS) Set startup behavior to `nothing` | `applicationShouldOpenUntitledFile` returns `false` |
| lifecycle-015 | suppress-untitled-file | (macOS) Set startup behavior to `restoreSession` | `applicationShouldOpenUntitledFile` returns `false` |
| lifecycle-019 | suppress-untitled-relaunch | (macOS) System restarts with `restoreSession` active | App does not open both restored documents and an untitled window |

