
- **Very large files (1MB+)**: The editor SHOULD load and render without blocking the main thread. If the file exceeds a configurable size threshold (e.g., 5MB), the editor MAY display a warning or truncate rendering. The editor MUST NOT crash.
- **Binary files**: Files that cannot be decoded as UTF-8 MUST show the "Cannot display this file type" placeholder. The editor MUST NOT attempt to render binary data as text.
- **File deleted while editing**: If the file is deleted externally while open in the editor, the editor SHOULD detect this on the next save attempt and present an appropriate error (e.g., "File no longer exists. Save as...?" or re-create the file). The editor MUST NOT crash or silently lose content.
- **File modified externally (concurrent edit)**: If the file is modified by another process while open, the editor SHOULD detect the external change (e.g., via file system events or mtime check on save) and warn the user before overwriting. The editor MUST NOT silently discard external changes without notice.
- **Encoding issues**: Files with mixed encoding, BOM markers, or invalid UTF-8 sequences MUST be handled gracefully. Invalid bytes SHOULD cause the file to be treated as non-displayable (binary-file-placeholder), not crash the editor.
- **Empty file**: A zero-byte file MUST load successfully and display an empty editor (not a placeholder). The file SHOULD be editable.
- **Read-only file**: If the file does not have write permissions, the editor SHOULD indicate read-only status. Save attempts MUST show an error rather than silently failing.
- **File path with special characters**: Paths containing spaces, unicode characters, or shell-special characters MUST be handled correctly for both load and save operations.
- **Rapid file switching**: If the user switches files faster than the async load completes, only the most recently selected file's content MUST be displayed. Stale load results MUST be discarded (the `loadGeneration` mechanism handles this).
- **Save fails (disk full, permissions)**: Save errors MUST be surfaced to the user (e.g., via an alert or inline error) and the dirty state MUST remain true so the user does not lose their changes.
- **Undo after save**: Undo history is per-editor-session. After save, undo SHOULD still work to revert to pre-save content (the dirty indicator reappears if content diverges from the saved snapshot).
- **New file with no extension**: Files without an extension MUST load as plain text with no syntax highlighting.
- **Extremely long lines (10,000+ characters)**: The editor MUST remain responsive. Horizontal scrolling (no-line-wrap) handles display. The minimap SHOULD still render without performance degradation.
- **Tab characters vs spaces**: The editor MUST preserve the original indentation characters in the file. Tab width rendering MAY be configurable (default: 4 spaces).

