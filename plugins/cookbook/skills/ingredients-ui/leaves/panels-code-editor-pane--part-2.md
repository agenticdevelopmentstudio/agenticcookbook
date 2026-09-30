<!-- leaf: ingredients-ui/panels-code-editor-pane--part-2 · source: ingredients/ui/panels/code-editor-pane.md -->

# Code Editor Pane — continued (part 2)

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Pane collapse/expand transitions are instant (per collapsible-pane-header) |
| Increase Contrast | Editor uses higher-contrast syntax theme variant; gutter separator more prominent |
| Differentiate Without Color | Syntax highlighting uses bold/italic/underline styles in addition to color to differentiate token types |
| VoiceOver | Editor text navigable by character/word/line; header announces filename, modified state, and collapse state; placeholders announced per empty-state requirements |
| Dynamic Type | Editor font size SHOULD respect the system font size preference while maintaining monospaced rendering |

## Platform Notes

- **SwiftUI (macOS)**: Use `CodeEditSourceEditor` (from the CodeEditSourceEditor package) as the primary editor component, wrapped in an `NSViewRepresentable` if needed. Set language via `CodeLanguage` enum mapped from file extension. Configure: `lineNumbers: true`, `minimap: true`, `wrapLines: false`, font: `NSFont.monospacedSystemFont(ofSize: 13, weight: .regular)` or `NSFont(name: "Menlo", size: 13)`. Theme: use `EditorTheme` conforming types — CatnipDark and CatnipLight — switching based on `@Environment(\.colorScheme)`. Bind editor text to `EditorState.content` as a `Binding<String>`. Use `.id(editorState.loadGeneration)` on the editor view to force recreation when a new file loads. Dirty state tracking: subscribe to `editorState.$content` via Combine, debounce 0.3s, compare to `lastSavedContent` snapshot. Save: use `Data(content.utf8).write(to: fileURL, options: .atomic)` or `String.write(to:atomically:encoding:)`. Auto-save: in the file-selection `onChange` handler, call `save()` if `isModified` before loading the new file. Cmd+S: register via `.keyboardShortcut("s", modifiers: .command)` on a hidden button or via the `commands` modifier on the scene. Pane header: use collapsible-pane-header with the filename as title and a file-type SF Symbol as the icon.
- **SwiftUI (iOS / visionOS)**: CodeEditSourceEditor may not be available on iOS. Use a `UITextView`-based editor with custom syntax highlighting (e.g., Highlightr or a tree-sitter wrapper) inside a `UIViewRepresentable`. Line numbers and minimap may need custom drawing. On visionOS, the editor pane appears within the workspace window's detail area. Keyboard shortcut Cmd+S is available when an external keyboard is connected.
- **Compose (Android)**: Use a code editor library such as CodeView or Sora Editor. Configure syntax highlighting via language grammars. Line numbers and minimap depend on library capabilities. Dirty state tracking via `MutableState<String>` observation. Save with `File.writeText()` using `createTempFile` + `renameTo` for atomic writes. Auto-save triggered in `onDispose` or selection-change callback.
- **Web (React)**: Use Monaco Editor or CodeMirror 6. Monaco provides built-in language support, minimap, line numbers, and theme switching. Bind editor value to React state. Dirty tracking via `onChange` callback comparing to saved snapshot. Save via backend API or File System Access API. Cmd+S / Ctrl+S intercepted via `editor.addCommand` or `onKeyDown` handler. Theme: configure `vs-dark` / `vs` based on `prefers-color-scheme` media query.

## Privacy

- **Data collected**: File contents are loaded into memory for editing. No content is transmitted off-device.
- **Storage**: File contents are persisted only to their original file path on save. No copies or caches are created.
- **Transmission**: None — file content never leaves the device.
- **Retention**: Editor content exists in memory only for the lifetime of the editing session. Closing the file releases memory.
