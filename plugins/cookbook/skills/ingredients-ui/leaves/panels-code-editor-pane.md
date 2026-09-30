<!-- leaf: ingredients-ui/panels-code-editor-pane · source: ingredients/ui/panels/code-editor-pane.md -->

**Rules** (cite as `ingredients-ui/panels-code-editor-pane#<slug>`):

- `async-file-load` MUST
- `set-loaded-state` MUST
- `binary-file-placeholder` MUST
- `no-file-placeholder` MUST
- `directory-placeholder` MUST
- `load-generation-identity` MUST
- `language-detection` MUST
- `supported-language-map` MUST
- `plain-text-fallback` MUST
- `system-appearance-theme` MUST
- `gutter-enabled` MUST
- `minimap-enabled` MUST
- `no-line-wrap` MUST
- `default-monospaced-font` MUST
- `dirty-state-tracking` MUST
- `is-modified-flag` MUST
- `auto-save-on-switch` MUST
- `manual-save-shortcut` MUST
- `atomic-save` MUST
- `reset-modified-after-save` MUST
- `editor-state-properties` MUST
- `debounce-dirty-check` MUST
- `collapsible-header` MUST
- `header-shows-filename` MUST
- `header-generic-title` MUST
- `dirty-indicator-in-header` SHOULD
- `text-editor-a11y-role` MUST
- `header-a11y-compliance` MUST
- `dirty-state-a11y` MUST
- `placeholder-a11y` MUST
- `save-menu-discoverable` MUST
- `decorative-line-numbers` MUST

# Code Editor Pane

## Overview

A text editor pane for viewing and editing source code files with syntax highlighting, line numbers, minimap, dirty state tracking, and auto-save. Loads file contents asynchronously and provides language-aware editing via CodeEditSourceEditor on Apple platforms. Derived from scratching-post FileEditorView and EditorState.

## Terminology

| Term | Definition |
|------|-----------|
| EditorState | An ObservableObject that manages the loaded file content, modification tracking, load state, and save operations for a single file |
| Dirty state | The editor has unsaved modifications — determined by comparing current content to last-saved content |
| loadGeneration | A monotonically increasing counter that forces the SourceEditor to be recreated when a new file is loaded, preventing stale editor state |
| Syntax highlighting | Colorized rendering of source code tokens (keywords, strings, comments, etc.) based on the detected language |
| Minimap | A scaled-down overview of the entire file shown as a narrow column on the trailing edge of the editor |
| Gutter | The column to the left of the editing area that displays line numbers |
| Auto-save | Automatic persistence of modified content when the user switches to a different file |

## Behavioral Requirements

### File loading

- **async-file-load**: The editor MUST load file contents asynchronously as UTF-8 text. During loading, a progress spinner MUST be displayed.
- **set-loaded-state**: On successful load, the editor MUST set `isLoaded` to true, populate `content` with the file text, and increment `loadGeneration` to force the SourceEditor to recreate.
- **binary-file-placeholder**: If the file cannot be read as UTF-8 text (binary file, encoding error), the editor MUST display a placeholder: "Cannot display this file type".
- **no-file-placeholder**: If no file is selected, the editor MUST display a placeholder: "Select a file to view its contents".
- **directory-placeholder**: If a directory is selected (rather than a file), the editor MUST display a directory-appropriate placeholder rather than attempting to load.
- **load-generation-identity**: The `loadGeneration` counter MUST be incremented each time a new file is loaded. The SourceEditor view MUST use this value as an identity key (e.g., SwiftUI `.id(loadGeneration)`) so that the editor is fully recreated for each file, preventing stale content or cursor position from the previous file.

### Syntax highlighting and language detection

- **language-detection**: The editor MUST detect the programming language from the file extension and apply syntax highlighting accordingly.
- **supported-language-map**: Language detection MUST support at minimum the following mappings:

| Extension(s) | Language |
|--------------|----------|
| `.swift` | Swift |
| `.json` | JSON |
| `.md`, `.markdown` | Markdown |
| `.py` | Python |
| `.js` | JavaScript |
| `.ts` | TypeScript |
| `.jsx` | JSX |
| `.tsx` | TSX |
| `.yaml`, `.yml` | YAML |
| `.toml` | TOML |
| `.html`, `.htm` | HTML |
| `.css` | CSS |
| `.sh`, `.bash`, `.zsh` | Shell |
| `.rb` | Ruby |
| `.rs` | Rust |
| `.go` | Go |
| `.c`, `.h` | C |
| `.cpp`, `.hpp`, `.cc` | C++ |
| `.java` | Java |
| `.kt`, `.kts` | Kotlin |
| `.xml`, `.plist` | XML |
| `.sql` | SQL |
| `.r`, `.R` | R |
| `.lua` | Lua |
| `.dockerfile`, `Dockerfile` | Dockerfile |
| `.gitignore` | Git Ignore |

- **plain-text-fallback**: If the file extension is unrecognized, the editor MUST fall back to plain text (no syntax highlighting).
- **system-appearance-theme**: The editor MUST follow the system appearance to select a dark or light theme. On Apple platforms, use CatnipDark for dark mode and CatnipLight for light mode, or equivalent named themes from the syntax highlighting library.

### Editor configuration

- **gutter-enabled**: The gutter (line numbers) MUST be enabled by default.
- **minimap-enabled**: The minimap MUST be enabled by default.
- **no-line-wrap**: Line wrapping MUST be disabled. Horizontal scrolling MUST be used for long lines.
- **default-monospaced-font**: The default font MUST be Menlo 13pt (monospaced). The font MAY be configurable via project or app settings.

### Dirty state and saving

- **dirty-state-tracking**: The editor MUST track dirty state by subscribing to content changes (via Combine or equivalent reactive mechanism) and comparing the current content to the last-saved content.
- **is-modified-flag**: When the content differs from the last-saved content, `isModified` MUST be set to true. When they match, `isModified` MUST be set to false.
- **auto-save-on-switch**: When the user switches to a different file and `isModified` is true, the editor MUST auto-save the current file before loading the new file.
- **manual-save-shortcut**: The user MUST be able to trigger a manual save via Cmd+S (macOS) or the platform-equivalent keyboard shortcut.
- **atomic-save**: Save MUST write the content atomically to disk to prevent data loss from partial writes.
- **reset-modified-after-save**: After a successful save, `isModified` MUST be reset to false and the last-saved content snapshot MUST be updated.

### EditorState

- **editor-state-properties**: EditorState MUST be implemented as an ObservableObject (or platform equivalent) with the following published properties:
  - `content: String` — the current text in the editor
  - `isModified: Bool` — whether the content has unsaved changes
  - `loadError: String?` — an error message if the file could not be loaded
  - `isLoaded: Bool` — whether the file has been successfully loaded
  - `loadGeneration: Int` — incremented to force editor recreation on file change
- **debounce-dirty-check**: EditorState MUST debounce dirty-state comparison by a short interval (e.g., 0.3s) to avoid excessive comparisons during rapid typing.

### Pane header

- **collapsible-header**: The editor pane MUST use the collapsible-pane-header component at the top.
- **header-shows-filename**: When a file is selected, the header MUST display a file icon and the filename.
- **header-generic-title**: When no file is selected, the header MUST display a generic title (e.g., "Editor").
- **dirty-indicator-in-header**: When the file is modified (dirty), the header SHOULD display a dirty indicator (e.g., a dot or bullet adjacent to the filename, or the standard macOS edited-document indicator).

## Appearance

### Editor pane layout

```
┌────────────────────────────────────────────────────────┐
│  ▼  📄 ContentView.swift  ●                           │  ← pane header (collapsible)
├──────────────────────────────────────────────────┬─────┤
│ 1  import SwiftUI                                │▓▓▓▓▓│
│ 2                                                │▓░░▓▓│
│ 3  struct ContentView: View {                    │▓░░▓▓│
│ 4      var body: some View {                     │▓░░▓▓│
│ 5          VStack {                              │▓░░▓▓│
│ 6              Image(systemName: "globe")        │▓░░▓▓│
│ 7                  .imageScale(.large)           │▓▓▓▓▓│
│ 8                  .foregroundStyle(.tint)       │▓▓▓▓▓│
│ 9              Text("Hello, world!")             │▓▓▓▓▓│
│10          }                                     │▓▓▓▓▓│
│11          .padding()                            │▓▓▓▓▓│
│12      }                                         │     │
│13  }                                             │     │
│14                                                │     │
│                                                  │     │
└──────────────────────────────────────────────────┴─────┘
 ↑ gutter (line numbers)   ↑ editor area            ↑ minimap
```

### No file selected (empty state)

```
┌────────────────────────────────────────────────────────┐
│  ▼  Editor                                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│                                                        │
│                      📄                                │
│           Select a file to view its contents           │
│                                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Binary file placeholder

```
┌────────────────────────────────────────────────────────┐
│  ▼  📄 image.png                                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│                                                        │
│                      ⚠️                                │
│           Cannot display this file type                │
│                                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

- **Gutter**: Monospaced, right-aligned line numbers, secondary text color, subtle separator from editor area
- **Editor area**: Monospaced font (Menlo 13pt default), themed background per color-profile
- **Minimap**: ~60pt wide trailing column, scaled-down representation of the file
- **Dirty indicator**: Small filled circle (●) adjacent to the filename in the pane header, or platform-standard edited-document indicator

## Accessibility

- **text-editor-a11y-role**: The editor MUST be accessible as a text editor role to screen readers and MUST support standard text navigation (by character, word, line).
- **header-a11y-compliance**: The pane header MUST follow collapsible-pane-header accessibility requirements (button role, expand/collapse announced).
- **dirty-state-a11y**: The dirty indicator MUST be communicated to assistive technologies — e.g., the header's accessibility label SHOULD include "edited" or "modified" when `isModified` is true.
- **placeholder-a11y**: Empty state and error placeholders MUST follow empty-state accessibility requirements (heading announced first, icon decorative).
- **save-menu-discoverable**: The Cmd+S save shortcut MUST be discoverable via the app's menu bar (File > Save) on macOS.
- **decorative-line-numbers**: Line numbers in the gutter MUST be decorative and not announced individually by screen readers.

## Configuration

This ingredient has no configurable options.

