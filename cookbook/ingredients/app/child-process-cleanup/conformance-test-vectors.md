
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-010 | terminate-child-processes, track-child-handles | Launch app, start 3 terminal sessions, quit | All 3 child processes terminated; no orphaned processes in `ps` output |
| lifecycle-011 | sighup-process-group | (macOS) Launch app, start a child process, quit | `SIGHUP` sent to process group; child process terminated |
| lifecycle-012 | cleanup-timeout-sigkill | Launch app, start a process that ignores SIGHUP, quit | After 5-second timeout, process receives `SIGKILL` |

