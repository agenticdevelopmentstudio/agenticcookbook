
The app's creation menu: it replaces the default "New" menu item with app-specific creation commands (New Project, New Session, New Workspace), each with a distinct keyboard shortcut and an SF Symbol icon. Commands that act on the current window (New Session) use the `@FocusedObject` pattern to reach the focused window's state and disable themselves gracefully when no suitable window is focused. What the document-creating commands do after they are invoked is the Document Creation Flow ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| Menu command | A user-invocable action exposed in the app's menu bar, typically with a keyboard shortcut |
| Keyboard shortcut | A modifier key combination (e.g., Cmd-N) bound to a menu command |
| CommandGroup | A SwiftUI struct that defines or replaces a group of menu items in the app's menu bar |
| @FocusedObject | A SwiftUI property wrapper that reads an observable object provided by the currently focused window via `.focusedObject()` |
| SF Symbol | A system-provided icon from Apple's SF Symbols library, used for menu item imagery |

