
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-001 | configurable-startup-modes, startup-behavior-setting | Set startup behavior to `newWindow`, launch app | Default window opens |
| lifecycle-002 | configurable-startup-modes, save-restore-urls | Set startup behavior to `restoreSession`, open 3 documents, quit, relaunch | Same 3 documents reopen |
| lifecycle-003 | configurable-startup-modes | Set startup behavior to `nothing`, launch app | No windows open; app is active in menu bar/dock |
| lifecycle-004 | default-restore-session | Fresh install, launch app with no prior preferences | App behaves as `restoreSession` (and since no URLs saved, falls back to `newWindow` per fallback-to-new-window) |
| lifecycle-005 | url-list-storage | Open 2 documents, quit app | UserDefaults contains array of 2 path strings under the correct key |
| lifecycle-006 | filter-registered-types | Save URL list containing a `.txt` file (not a registered type), relaunch in `restoreSession` mode | `.txt` file is skipped; only recognized document types open |
| lifecycle-007 | validate-file-exists | Save URL list containing a path to a deleted file, relaunch in `restoreSession` mode | Deleted file is silently skipped; remaining files open |
| lifecycle-008 | preserve-restore-order | Open documents A, B, C (in that order), quit, relaunch in `restoreSession` mode | Documents open in order A, B, C |
| lifecycle-009 | fallback-to-new-window | Set startup behavior to `restoreSession`, clear all saved URLs, relaunch | App falls back to `newWindow` behavior |
| lifecycle-010 | terminate-child-processes, track-child-handles | Launch app, start 3 terminal sessions, quit | All 3 child processes terminated; no orphaned processes in `ps` output |
| lifecycle-011 | sighup-process-group | (macOS) Launch app, start a child process, quit | `SIGHUP` sent to process group; child process terminated |
| lifecycle-012 | cleanup-timeout-sigkill | Launch app, start a process that ignores SIGHUP, quit | After 5-second timeout, process receives `SIGKILL` |
| lifecycle-013 | suppress-untitled-file, allow-untitled-new-window | (macOS) Set startup behavior to `newWindow` | `applicationShouldOpenUntitledFile` returns `true` |
| lifecycle-014 | suppress-untitled-file | (macOS) Set startup behavior to `nothing` | `applicationShouldOpenUntitledFile` returns `false` |
| lifecycle-015 | suppress-untitled-file | (macOS) Set startup behavior to `restoreSession` | `applicationShouldOpenUntitledFile` returns `false` |
| lifecycle-016 | multi-window-scenes | (macOS) Inspect app scene declarations | App body contains at least one `WindowGroup` and one `Settings` or `Window` scene |
| lifecycle-017 | per-type-document-group | (macOS) Open a registered document type via Finder | Correct `DocumentGroup` scene handles the file |
| lifecycle-018 | commands-modifier | (macOS) Open app, inspect menu bar | Custom menu commands present from `.commands` modifier |
| lifecycle-019 | suppress-untitled-relaunch | (macOS) System restarts with `restoreSession` active | App does not open both restored documents and an untitled window |

