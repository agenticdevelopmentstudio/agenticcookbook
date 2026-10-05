
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-005 | url-list-storage | Open 2 documents, quit app | UserDefaults contains array of 2 path strings under the correct key |
| lifecycle-006 | filter-registered-types | Save URL list containing a `.txt` file (not a registered type), relaunch in `restoreSession` mode | `.txt` file is skipped; only recognized document types open |
| lifecycle-007 | validate-file-exists | Save URL list containing a path to a deleted file, relaunch in `restoreSession` mode | Deleted file is silently skipped; remaining files open |
| lifecycle-008 | preserve-restore-order | Open documents A, B, C (in that order), quit, relaunch in `restoreSession` mode | Documents open in order A, B, C |
| lifecycle-009 | fallback-to-new-window | Set startup behavior to `restoreSession`, clear all saved URLs, relaunch | App falls back to `newWindow` behavior |

