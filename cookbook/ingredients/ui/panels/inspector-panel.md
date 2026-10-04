---
id: 6af1d30a-c2ee-4a6d-97ec-50c67f01a243
title: "Inspector Panel"
domain: agenticdevelopercookbook://ingredients/ui/panels/inspector-panel
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-05
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Right-side sliding panel that shows metadata for the currently selected item in the workspace"
platforms:
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - inspector-panel
  - panel
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Inspector Panel

## Overview

A right-side sliding panel that shows metadata for the currently selected item in the workspace. Toggled via a toolbar button using the standard inspector icon. Uses a `Form` with `LabeledContent` for structured key-value display. Shows an empty state when nothing is selected. Derived from scratching-post `ProjectInspectorView` and `ContentViewerView`.

## Terminology

| Term | Definition |
|------|-----------|
| Inspector | A right-side auxiliary panel that displays detail/metadata about the current selection |
| Selected item | The file or folder currently highlighted in the file tree or content area |
| Metadata row | A single key-value pair displayed via `LabeledContent` inside a `Form` |

## Behavioral Requirements

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

## Appearance

```
┌──────────────────────┐
│ Inspector        [×] │
├──────────────────────┤
│                      │
│ Name     README.md   │
│ Path     src/...md   │
│ Type     Markdown    │
│ Size     4.2 KB      │
│ Modified Mar 25, ... │
│ Git      M Modified  │
│                      │
└──────────────────────┘
```

Empty state:

```
┌──────────────────────┐
│ Inspector        [×] │
├──────────────────────┤
│                      │
│                      │
│     📄🔍             │
│  Select a file       │
│  to inspect          │
│                      │
│                      │
└──────────────────────┘
```

- **Panel width**: 250pt fixed
- **Form style**: Grouped
- **Path font**: Caption, secondary color, truncation middle
- **Git status**: Monospaced bold character + color + label (per git-status-indicator spec)
- **Empty state**: Centered vertically and horizontally within panel

## States

| State | Behavior |
|-------|----------|
| Panel hidden | Main content area fills available width; toolbar toggle button visible |
| Panel visible, item selected | Panel slides in from right; form displays metadata for selected item |
| Panel visible, nothing selected | Panel slides in from right; empty state displayed |
| Selection changes | Form content updates immediately to reflect newly selected item |
| Panel toggled off | Panel slides out to the right; state persisted |
| Panel toggled on | Panel slides in from the right; state persisted |

## Accessibility

- **toggle-accessible-label**: The toolbar toggle button MUST have an accessible label: "Toggle Inspector" (or platform-localized equivalent).
- **toggle-state-announce**: The toggle button MUST announce its state to screen readers (e.g., "Inspector, showing" / "Inspector, hidden").
- **row-label-accessible**: Each metadata row label MUST be the accessible label for its corresponding value.
- **path-full-announce**: The selectable Path text MUST be accessible to screen readers with the full path announced, not the truncated display.
- **git-accessible-label**: The Git Status badge MUST have an accessibility label with the full status name (e.g., "Git Status: Modified"), not just the character. This is inherited from the git-status-indicator spec (git-status-badge).
- **empty-state-accessible**: The empty state MUST follow the empty-state accessibility requirements (heading announced first, icon decorative).
- **keyboard-navigable**: The inspector panel MUST be fully keyboard-navigable — Tab key should move focus through metadata rows and the close/toggle button.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| inspector-001 | slide-in-right | Toggle inspector on | Panel slides in from the right side |
| inspector-002 | fixed-width-250 | Measure panel width | Panel width is 250pt |
| inspector-003 | toolbar-toggle-button | Click toolbar inspector button | Panel visibility toggles |
| inspector-004 | persist-visibility | Show inspector, quit app, relaunch | Inspector is visible on relaunch |
| inspector-005 | persist-visibility | Hide inspector, quit app, relaunch | Inspector is hidden on relaunch |
| inspector-006 | form-metadata-display, uttype-file-type | Select a Markdown file (README.md) | Name shows "README.md", Type shows "Markdown" or UTType description |
| inspector-007 | size-files-only, byte-count-format | Select a 4,200-byte file | Size row shows "4.2 KB" (or locale-appropriate equivalent) |
| inspector-008 | size-files-only | Select a directory | Size row is not displayed |
| inspector-009 | date-format-medium | Select a file modified on 2026-03-25 at 14:30 | Modified shows "Mar 25, 2026 at 2:30 PM" (or locale equivalent) |
| inspector-010 | git-status-indicator, hide-clean-git-status | Select a modified file in a git repo | Git Status row shows orange "M" badge with label "Modified" |
| inspector-011 | hide-clean-git-status | Select a clean/committed file in a git repo | Git Status row is not displayed |
| inspector-012 | hide-clean-git-status | Select a file in a non-git project | Git Status row is not displayed |
| inspector-013 | empty-state-display | No file selected, inspector visible | Empty state shows icon and "Select a file to inspect" |
| inspector-014 | selectable-path-text | Select a file, attempt to select the path text | Path text is selectable and copyable |
| inspector-015 | path-caption-truncate | Select a file with a very long path | Path truncates in the middle with ellipsis |
| inspector-016 | grouped-form-style | Inspect form style | Form uses grouped style |
| inspector-017 | toggle-accessible-label, toggle-state-announce | Enable VoiceOver, activate toolbar toggle | Button announces "Toggle Inspector" and state |
| inspector-018 | keyboard-navigable | Press Tab repeatedly while inspector is open | Focus moves through metadata rows and toggle button |

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

## Configuration

This ingredient has no configurable options.

## Localization

| String Key | Default (en) | Context |
|-----------|-------------|---------|
| `inspector.title` | Inspector | Panel title |
| `inspector.toggle` | Toggle Inspector | Toolbar button accessible label |
| `inspector.name` | Name | Metadata row label |
| `inspector.path` | Path | Metadata row label |
| `inspector.type` | Type | Metadata row label |
| `inspector.size` | Size | Metadata row label |
| `inspector.modified` | Modified | Metadata row label |
| `inspector.git_status` | Git Status | Metadata row label |
| `inspector.empty_heading` | Select a file to inspect | Empty state heading |
| `inspector.type_unknown` | Unknown | Fallback file type |

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Panel appears/disappears instantly (no slide animation) |
| Reduce Transparency | Panel background uses opaque material |
| Increase Contrast | Metadata labels and values use higher-contrast colors |
| Differentiate Without Color | Git status character provides differentiation (inherited from git-status-indicator) |

## Logging

Subsystem: `{{bundle_id}}` | Category: `InspectorPanel`

| Event | Level | Message |
|-------|-------|---------|
| Panel shown | debug | `InspectorPanel: shown` |
| Panel hidden | debug | `InspectorPanel: hidden` |
| Visibility state persisted | debug | `InspectorPanel: visibility persisted as {{visible}}` |
| Item inspected | debug | `InspectorPanel: inspecting "{{name}}" at "{{path}}"` |
| Empty state displayed | debug | `InspectorPanel: no selection, showing empty state` |
| Type detection failed | debug | `InspectorPanel: could not determine type for "{{name}}", showing "Unknown"` |

## Platform Notes

- **SwiftUI (macOS / iPadOS / visionOS)**: Use the `.inspector(isPresented:)` modifier on the main content view. Bind `isPresented` to a `@SceneStorage` or `@AppStorage` boolean for persistence. Inside the inspector, use `Form { ... }.formStyle(.grouped)` with `LabeledContent` for each metadata row. Path text: `Text(path).textSelection(.enabled).font(.caption).lineLimit(1).truncationMode(.middle)`. Size: `ByteCountFormatter` with `.countStyle = .file`. Date: `DateFormatter` with `dateStyle = .medium`, `timeStyle = .short`. Git status: use the git-status-indicator view with `.detailed` style. Empty state: `ContentUnavailableView("Select a file to inspect", systemImage: "doc.text.magnifyingglass")`. Set `.inspectorColumnWidth(250)` for fixed width. Toolbar button: `Button { isInspectorPresented.toggle() } label: { Label("Toggle Inspector", systemImage: "sidebar.trailing") }`.
- **Compose (Android / Desktop)**: Use a `ModalDrawer` or side sheet anchored to the right with `drawerContent`. Fixed width via `Modifier.width(250.dp)`. Use `LazyColumn` with labeled rows. Date formatting via `java.time.format.DateTimeFormatter`. File size via custom formatter or `Formatter.formatFileSize()`. Persist visibility in `DataStore` or `SharedPreferences`.
- **React / Web**: CSS sidebar with `position: fixed; right: 0; width: 250px; transition: transform 0.2s`. Toggle by translating off-screen. Use a `<dl>` (description list) for key-value pairs. File size via `filesize` npm package. Date via `Intl.DateTimeFormat`. Persist visibility in `localStorage`.

## Privacy

- **Data collected**: None — the inspector only reads and displays file metadata already available on the local filesystem
- **Storage**: Inspector visibility state stored in platform standard persistence (UserDefaults / SharedPreferences / localStorage)
- **Transmission**: None — no data leaves the device
- **Retention**: Visibility preference persisted until changed; file metadata is read on demand, never cached

## Design Decisions

_None yet — decisions made during implementation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
