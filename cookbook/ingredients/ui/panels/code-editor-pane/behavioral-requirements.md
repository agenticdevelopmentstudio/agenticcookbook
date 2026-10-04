
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

