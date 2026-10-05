
- **SwiftUI (macOS)**: Frame autosave via the `WindowAccessor` pattern from [window-frame-persistence.md](../../../ingredients/infrastructure/window-frame-persistence.md) with the autosave name set to a SHA256 hash prefix of the workspace path. Compose the Workspace Browser inside an `HSplitView` (or `NavigationSplitView`) and bind it to the Workspace Document model.
- **SwiftUI (visionOS)**: Frame persistence may not apply in the same way; window placement is managed by the system. The composition is otherwise identical to macOS.
- **Compose**: Use a `Window` with `rememberWindowState` keyed by a hash of the workspace path; bind the browser to a document view model.
- **React/Web**: Persist window layout in `localStorage` keyed by a hash of the workspace path; bind the browser to a document store.

