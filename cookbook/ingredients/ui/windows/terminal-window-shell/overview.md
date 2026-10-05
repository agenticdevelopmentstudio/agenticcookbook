
A session-sidebar-plus-terminal shell that owns its own session manager. An HSplitView holds the session list (left) and the terminal view (right); the shell creates a default session on first appear, terminates every session when it closes, and publishes its session manager as the focused object so menu commands reach the right window. Terminal behavior itself (PTY sessions, session list rows, rendering, profiles) is delegated to the terminal-pane ingredient; each shell instance is completely independent, with no session sharing between windows.

### Terminology

| Term | Definition |
|------|-----------|
| Standalone terminal window | A top-level window containing only a session sidebar and terminal view, not embedded in a project window |
| Session sidebar | The left panel listing all terminal sessions owned by this window's session manager |
| Session manager | A per-window controller owning an ordered list of sessions — see `terminal-pane` ingredient per-window-manager |
| Terminal view | The rendering surface for the selected session — see `terminal-pane` ingredient nsview-representable through palette-color-structure |
| Active profile | The currently selected color profile applied to terminal rendering — see `color-profile` ingredient single-active-profile |
| Window scene | A SwiftUI `WindowGroup` identified by a string, used to open and manage window instances |

