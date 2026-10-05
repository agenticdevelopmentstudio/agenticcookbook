
| State | Behavior |
|-------|----------|
| Quit requested, children running | Cleanup starts: SIGHUP to the process group (macOS), then each tracked handle is terminated (terminate-child-processes, sighup-process-group) |
| Children exited within timeout | Cleanup completes; the app continues terminating (track-child-handles) |
| Timeout elapsed, children remain | Remaining processes receive SIGKILL (cleanup-timeout-sigkill) |

