
```
 Launch                                             Quit
   |                                                  |
   v                                                  v
 Startup Behavior --mode--> newWindow  -> default window
        |                -> nothing    -> no window
        |                -> restoreSession
        v                        |
   Session Restore <-------------+--(no valid URLs)--> newWindow
                                                      |
 [@main App body: WindowGroup | DocumentGroup | Window | Settings scenes]
                                                      |
   Session Restore (save URL list) -> Child Process Cleanup (SIGHUP, 5 s, SIGKILL)
```

Not a visual layout: the diagram shows launch and quit ordering across the ingredients and the scene declarations hosted by the app.

### Composed states

| State | Behavior |
|-------|----------|
| App quitting, documents open | URL list saved to persistence, child processes terminated |
| App quitting, no documents open | Empty URL list saved (clears previous restore list), child processes terminated |
| System logout/restart | Same as app quitting; session restore list saved normally |

