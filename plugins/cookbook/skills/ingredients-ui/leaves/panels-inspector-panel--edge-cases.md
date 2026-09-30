<!-- leaf: ingredients-ui/panels-inspector-panel--edge-cases · source: ingredients/ui/panels/inspector-panel.md -->

# Inspector Panel

**Rules** (cite as `ingredients-ui/panels-inspector-panel--edge-cases#<slug>`):

- `very-long-file-name` SHOULD — Name SHOULD truncate with trailing ellipsis rather than overflowing the panel.
- `very-long-path` MUST — Path MUST truncate in the middle (path-caption-truncate), showing the beginning and end of the path.
- `unknown-file-type` SHOULD — Type SHOULD display "Unknown" rather than blank or crashing (uttype-file-type).
- `file-with-no-extension` SHOULD — Type SHOULD display "Document" or "Unknown" based on platform UTType inference.
- `zero-byte-file` SHOULD — Size SHOULD display "Zero bytes" or "0 bytes", not blank.
- `very-large-file` SHOULD — ByteCountFormatter SHOULD handle gracefully (e.g., "1.2 TB").
- `file-deleted-while-inspector-is-open` MUST — Inspector SHOULD clear to empty state or show a "File not found" message. It MUST NOT crash.
- `rapid-selection-changes` MUST — Inspector MUST update without flicker or stale content. Debounce if needed (100ms recommended).
- `git-status-unavailable` MUST — Git Status row MUST NOT appear. No error shown.
- `symlink-selected` SHOULD — SHOULD show the symlink's own metadata, not the target's, unless the platform convention differs.
- `localized-date-number-formatting` MUST — Size and Modified values MUST respect the user's locale settings.

## Edge Cases

- **Very long file name**: Name SHOULD truncate with trailing ellipsis rather than overflowing the panel.
- **Very long path**: Path MUST truncate in the middle (path-caption-truncate), showing the beginning and end of the path.
- **Unknown file type**: Type SHOULD display "Unknown" rather than blank or crashing (uttype-file-type).
- **File with no extension**: Type SHOULD display "Document" or "Unknown" based on platform UTType inference.
- **Zero-byte file**: Size SHOULD display "Zero bytes" or "0 bytes", not blank.
- **Very large file (>1 TB)**: ByteCountFormatter SHOULD handle gracefully (e.g., "1.2 TB").
- **File deleted while inspector is open**: Inspector SHOULD clear to empty state or show a "File not found" message. It MUST NOT crash.
- **Rapid selection changes**: Inspector MUST update without flicker or stale content. Debounce if needed (100ms recommended).
- **Git status unavailable (git not installed)**: Git Status row MUST NOT appear. No error shown.
- **Symlink selected**: SHOULD show the symlink's own metadata, not the target's, unless the platform convention differs.
- **Localized date/number formatting**: Size and Modified values MUST respect the user's locale settings.
