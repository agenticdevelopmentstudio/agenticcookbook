
### Process cleanup

- **terminate-child-processes**: On app termination, the app MUST terminate all child processes (terminal sessions, background tasks, language servers, build processes).
- **sighup-process-group** (macOS): The app SHOULD send `SIGHUP` to its process group on `applicationWillTerminate` to ensure child processes receive a termination signal.
- **track-child-handles**: The app MUST NOT leave orphaned processes after quitting. All child process handles MUST be tracked and cleaned up.
- **cleanup-timeout-sigkill**: Child process cleanup MUST complete within a reasonable timeout (5 seconds). After the timeout, remaining processes SHOULD be sent `SIGKILL`.

