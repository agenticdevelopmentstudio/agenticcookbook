<!-- leaf: recipes-ui/windows-project-window--part-2 · source: recipes/ui/windows/project-window.md -->

# Project Window — continued (part 2)

**Rules** (cite as `recipes-ui/windows-project-window--part-2#<slug>`):

- `fixed-2-pane-detail-layout` MAY — The current spec uses a fixed VSplitView with editor (top) and terminal (bottom). A future version MAY evolve to a …

## Localization

| String Key | Default (en) | Context |
|-----------|-------------|---------|
| `project_window.sessions_toggle` | Toggle Sessions Panel | Toolbar button accessible label |
| `project_window.inspector_toggle` | Toggle Inspector | Toolbar button accessible label |
| `project_window.settings_button` | Project Settings | Toolbar gear button accessible label |
| `project_window.editor_header` | Editor | Collapsible pane header title for editor |
| `project_window.terminal_header` | Terminal | Collapsible pane header title for terminal |
| `project_window.folder_header` | {{repoName}} | Folder header above file tree (dynamic, not localized) |

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Pane visibility changes are instant (no `.easeInOut` animation). Inspector appears/disappears without slide. |
| Reduce Transparency | Panel backgrounds use opaque materials instead of translucent/blur effects |
| Increase Contrast | Pane header backgrounds, divider lines, and toolbar button outlines use higher-contrast values |
| Differentiate Without Color | No impact — panel structure is spatial, not color-dependent |
| VoiceOver | Toolbar buttons announce labels and toggle state. Pane headers announce expand/collapse state. Split dividers announce resize role. |

## Feature Flags

| Flag Key | Default | Description |
|----------|---------|-------------|
| `{{app_prefix}}.project_window` | `true` | Enables the project window (master toggle) |
| `{{app_prefix}}.project_window.sessions_panel` | `true` | Enables the sessions panel in the project window |

## Analytics

| Event | Properties | When |
|-------|-----------|------|
| `project_window.opened` | `{ project_hash: string }` | Project window opens |
| `project_window.closed` | `{ project_hash: string, duration_seconds: number }` | Project window closes |
| `project_window.panel_toggled` | `{ panel: string, visible: bool }` | Any panel visibility toggled |
| `project_window.settings_opened` | `{}` | Gear button clicked, settings sheet presented |

## Privacy

- **Data collected**: Panel visibility and proportion preferences per project; window frame position/size
- **Storage**: ProjectSettings persisted on-device only (platform standard persistence). Frame autosave via `NSWindow.setFrameAutosaveName` (on-device).
- **Transmission**: None — no layout data leaves the device
- **Retention**: Persisted until the user changes settings or the project is removed. Frame autosave cleaned up by the OS if the app is uninstalled.

## Platform Notes

- **SwiftUI (macOS)**: Use `HSplitView` for the three-panel horizontal layout. Wrap sessions and file tree panels in conditional `if isSessionPanelVisible` / `if isFileViewerVisible` blocks, animated with `.animation(.easeInOut(duration: 0.2), value:)`. Use `VSplitView` inside the detail panel for editor (top) and terminal (bottom), each preceded by a `CollapsiblePaneHeader`. Apply `.inspector(isPresented: $isInspectorPresented)` on the outer container for the inspector. Use `.frame(minWidth:idealWidth:maxWidth:)` on each panel for proportional sizing. Toolbar via `.toolbar { }` with `ToolbarItem(placement:)` for sessions toggle, inspector toggle, and gear button. Gear button presents a `.sheet` for project settings. Frame persistence via `.background(WindowAccessor(name: sha256Hash(projectPath), onClose: { terminateAll(); stopWatching() }))`. The folder header is an `HStack` with a folder icon and the project root directory name, placed above the file tree `List`. Use `@ObservedObject` or `@EnvironmentObject` for `ProjectSettings` bindings.
- **SwiftUI (visionOS)**: Same layout as macOS. The window opens as a standard visionOS window. `HSplitView` and `VSplitView` render within the window volume. Split view dividers are not user-draggable on visionOS — pane proportions are controlled exclusively through ProjectSettings. Inspector uses the same `.inspector` modifier. Toolbar adapts to visionOS ornament style automatically. Frame persistence is not applicable (visionOS manages window placement).

## Design Decisions

**Fixed 2-pane detail layout**: The current spec uses a fixed VSplitView with editor (top) and terminal (bottom). A future version MAY evolve to a flexible N-pane layout supporting arbitrary pane configurations (file editor, terminal sessions, IDE integration panes). When this ships, the spec should be updated to document `PaneType` enum and `PaneLayout` struct.

**File tree default width**: Currently defaulting to 20% (`fileTreeProportion = 0.20`). Some implementations may prefer 40% for better file name readability. This is configurable per-project — the default can be adjusted based on user feedback.
