
### Visibility and toggling

- **slide-in-right**: The inspector panel MUST slide in from the right side of the window using the platform's native inspector mechanism (SwiftUI `.inspector` modifier or equivalent).
- **fixed-width-250**: The inspector panel MUST have a fixed width of 250pt.
- **toolbar-toggle-button**: The inspector panel MUST be toggled via a toolbar button using the standard inspector icon (SF Symbol `sidebar.trailing` on Apple platforms).
- **persist-visibility**: The inspector visibility state MUST be persisted in project/app settings so that it is restored on next launch.
- **toggle-always-accessible**: When the inspector is hidden, the toolbar toggle button MUST remain accessible.

### Content — item selected

- **form-metadata-display**: When an item is selected, the inspector MUST display a `Form` with grouped style containing the following metadata rows using `LabeledContent`:

  | Label | Value | Notes |
  |-------|-------|-------|
  | Name | File or folder name | Display name only, not full path |
  | Path | Relative path from project root | Selectable text, truncated middle, caption font |
  | Type | File type description | Derived from file extension / UTType |
  | Size | Human-readable file size | Files only; use `ByteCountFormatter` / equivalent |
  | Modified | Last modification date | Formatted via `DateFormatter`, medium date + short time |
  | Git Status | Colored badge + label | Uses git-status-indicator component (character + color + label) |

- **selectable-path-text**: The Path value MUST be displayed as selectable text so the user can copy it.
- **path-caption-truncate**: The Path value MUST use a caption-sized font and MUST truncate in the middle when it exceeds the available width.
- **size-files-only**: The Size row MUST only appear for files, not directories.
- **byte-count-format**: The Size value MUST be formatted using `ByteCountFormatter` (Apple) or equivalent locale-aware byte formatting on other platforms.
- **date-format-medium**: The Modified date MUST be formatted using a medium date style and short time style (e.g., "Mar 25, 2026 at 2:30 PM").
- **git-status-indicator**: The Git Status row MUST use the git-status-indicator component (as defined in `ui/git-status-indicator.md`), showing the status character, color, and full label (e.g., "M Modified").
- **hide-clean-git-status**: The Git Status row MUST NOT appear if the file has no git status (clean/committed) or the project is not a git repository.
- **uttype-file-type**: The Type value MUST be derived from the file extension using `UTType` on Apple platforms or MIME type lookup on other platforms. If the type cannot be determined, it SHOULD display "Unknown".

### Content — nothing selected

- **empty-state-display**: When no item is selected, the inspector MUST display an empty state (as defined in `ui/empty-state.md`) with:
  - Icon: `doc.text.magnifyingglass` (SF Symbol) or equivalent
  - Heading: "Select a file to inspect"
  - No action buttons

### Form layout

- **grouped-form-style**: The form MUST use grouped style (`.formStyle(.grouped)` on SwiftUI or equivalent).
- **vertical-scroll**: The form MUST scroll vertically if content exceeds the panel height.

