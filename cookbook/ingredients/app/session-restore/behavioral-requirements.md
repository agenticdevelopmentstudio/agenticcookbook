
### Session restore

- **save-restore-urls**: When startup behavior is `restoreSession`, the app MUST save the list of open document URLs on quit and reopen them on the next launch.
- **url-list-storage**: The URL list SHOULD be stored in `UserDefaults` (or platform equivalent) as an array of path strings, under a centralized settings key.
- **filter-registered-types**: On restore, the app SHOULD filter saved URLs to only include files whose extensions match the app's registered document types. Unrecognized extensions MUST be silently skipped.
- **validate-file-exists**: On restore, the app MUST validate that each saved URL points to an existing file. Missing files MUST be silently skipped and removed from the saved list.
- **preserve-restore-order**: On restore, the app SHOULD open documents in the same order they were saved (matching the order they were open at quit time).
- **fallback-to-new-window**: If no saved URLs exist (first launch in `restoreSession` mode, or all saved URLs are invalid), the app SHOULD fall back to the `newWindow` behavior.

