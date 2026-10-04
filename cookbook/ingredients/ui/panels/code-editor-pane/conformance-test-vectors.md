
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ced-001 | async-file-load | Select a .swift file | Loading spinner shown, then editor with syntax-highlighted Swift content |
| ced-002 | set-loaded-state | Load a file successfully | `isLoaded` is true, `content` matches file text, `loadGeneration` incremented |
| ced-003 | binary-file-placeholder | Select a .png file | Placeholder "Cannot display this file type" displayed |
| ced-004 | no-file-placeholder | No file selected | Placeholder "Select a file to view its contents" displayed |
| ced-005 | directory-placeholder | Select a directory node | Directory placeholder displayed, no file load attempted |
| ced-006 | load-generation-identity | Load file A, then load file B | `loadGeneration` incremented for each load; editor recreated (no stale state from A) |
| ced-007 | language-detection, supported-language-map | Load file.swift | Language detected as Swift, syntax highlighting applied |
| ced-008 | supported-language-map | Load file.py | Language detected as Python |
| ced-009 | supported-language-map | Load file.yaml | Language detected as YAML |
| ced-010 | plain-text-fallback | Load file.xyz (unknown extension) | Plain text mode, no syntax highlighting |
| ced-011 | system-appearance-theme | System in dark mode | CatnipDark theme applied to editor |
| ced-012 | system-appearance-theme | System in light mode | CatnipLight theme applied to editor |
| ced-013 | system-appearance-theme | Toggle system appearance while editor is open | Theme switches without reloading file |
| ced-014 | gutter-enabled | Load any file | Line numbers visible in gutter |
| ced-015 | minimap-enabled | Load any file | Minimap visible on trailing edge |
| ced-016 | no-line-wrap | Load file with 500-character line | No wrapping; horizontal scroll available |
| ced-017 | default-monospaced-font | Load any file | Font is Menlo 13pt monospaced |
| ced-018 | dirty-state-tracking, is-modified-flag | Type a character in the editor | `isModified` becomes true |
| ced-019 | is-modified-flag | Undo all changes back to saved state | `isModified` becomes false |
| ced-020 | auto-save-on-switch | Edit file A, select file B | File A auto-saved before file B loads |
| ced-021 | manual-save-shortcut | Press Cmd+S with unsaved changes | File saved, `isModified` becomes false |
| ced-022 | atomic-save | Save file | File written atomically (no partial content on disk) |
| ced-023 | reset-modified-after-save | Save file, then check state | `isModified` is false, last-saved snapshot updated |
| ced-024 | debounce-dirty-check | Type rapidly (10 chars in 0.2s) | Dirty comparison fires once after debounce, not per keystroke |
| ced-025 | collapsible-header | View editor pane | Collapsible pane header present at top |
| ced-026 | header-shows-filename | Select ContentView.swift | Header shows file icon + "ContentView.swift" |
| ced-027 | header-generic-title | No file selected | Header shows "Editor" |
| ced-028 | dirty-indicator-in-header | Edit file (make dirty) | Dirty indicator (●) appears in header |
| ced-029 | dirty-indicator-in-header | Save file (clear dirty) | Dirty indicator removed from header |
| ced-030 | dirty-state-a11y | VoiceOver active, file is dirty | Header announces "ContentView.swift, edited" |
| ced-031 | save-menu-discoverable | Open menu bar File menu | "Save" item present with Cmd+S shortcut |

