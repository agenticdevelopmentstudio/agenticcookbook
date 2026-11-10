
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-002 | configurable-startup-modes, save-restore-urls | Set startup behavior to `restoreSession`, open 3 documents, quit, relaunch | Same 3 documents reopen |
| lifecycle-004 | default-restore-session | Fresh install, launch app with no prior preferences | App behaves as `restoreSession` (and since no URLs saved, falls back to `newWindow` per fallback-to-new-window) |
| lifecycle-016 | multi-window-scenes | (macOS) Inspect app scene declarations | App body contains at least one `WindowGroup` and one `Settings` or `Window` scene |
| lifecycle-017 | per-type-document-group | (macOS) Open a registered document type via Finder | Correct `DocumentGroup` scene handles the file |
| lifecycle-018 | commands-modifier | (macOS) Open app, inspect menu bar | Custom menu commands present from `.commands` modifier |
| lifecycle-020 | mode-gates-restore | Set mode to `newWindow` with saved URLs present, launch | Only the default window opens; no saved document is reopened |
| lifecycle-021 | restore-fallback-uses-new-window, fallback-to-new-window | Mode `restoreSession` with all saved URLs invalid, launch | Exactly one default window opens |
| lifecycle-022 | save-before-cleanup, cleanup-timeout-sigkill | Open 2 documents and a process that ignores SIGHUP, quit | URL list is saved before cleanup starts; after the timeout the process is killed and relaunch restores both documents |
| lifecycle-023 | keys-through-registry | Inspect persisted keys after changing the mode and quitting | Both keys are the ones declared in the settings-keys registry |

