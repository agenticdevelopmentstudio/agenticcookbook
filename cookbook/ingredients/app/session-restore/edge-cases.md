
- **No saved URLs on restore**: The app MUST fall back to `newWindow` behavior (fallback-to-new-window). It MUST NOT show an error or empty state.
- **Saved URL points to deleted file**: The file MUST be silently skipped (validate-file-exists). The remaining valid URLs MUST still open. The invalid entry MUST be removed from the saved list.
- **Saved URL points to moved/renamed file**: Treated as a missing file — silently skipped. File-system-level bookmarks (Security-Scoped Bookmarks on macOS) MAY be used in a future version to track moved files, but this is out of scope for v1.
- **All saved URLs are invalid**: Falls back to `newWindow` behavior per fallback-to-new-window.
- **Crash during quit**: The saved URL list from the previous clean quit is preserved. The app MUST NOT corrupt the list during a partial write — writing SHOULD be atomic (write to temp file, then rename).
- **Crash during startup restore**: If the app crashes while opening a restored document, the next launch SHOULD still attempt to restore. A crash counter MAY be implemented to break infinite crash-restore loops (e.g., skip restore after 3 consecutive crashes).
- **Very large number of saved URLs (100+)**: The app SHOULD open documents asynchronously to avoid blocking the main thread. A progress indicator MAY be shown.
- **Duplicate URLs in saved list**: The app SHOULD deduplicate URLs before restoring. Each document SHOULD be opened at most once.
- **Read-only file restored**: The document SHOULD open in read-only mode. This is handled by the document subsystem, not lifecycle.
- **Multiple app instances**: Each instance MUST manage its own URL list independently. On macOS, the system typically enforces single-instance for bundled apps.

