<!-- leaf: ingredients-ui/panels-code-editor-pane--states · source: ingredients/ui/panels/code-editor-pane.md -->

# Code Editor Pane

## States

| State | Behavior |
|-------|----------|
| No file selected | Empty state placeholder: "Select a file to view its contents" |
| Loading file | ProgressView spinner centered in the editor area |
| File loaded | Editor displayed with syntax highlighting, line numbers, minimap |
| Binary / non-UTF-8 file | Placeholder: "Cannot display this file type" |
| Directory selected | Placeholder appropriate for directory (e.g., "Select a file to view its contents") |
| Modified (dirty) | Dirty indicator shown in pane header; `isModified` is true |
| Unmodified (clean) | No dirty indicator; `isModified` is false |
| Save in progress | Content written atomically; on completion, dirty state cleared |
| Load error | Error placeholder displayed with the load error message |
| Pane collapsed | Header visible (via collapsible-pane-header), editor content hidden |
