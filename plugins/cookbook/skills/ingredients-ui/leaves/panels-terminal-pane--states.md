<!-- leaf: ingredients-ui/panels-terminal-pane--states · source: ingredients/ui/panels/terminal-pane.md -->

# Terminal Pane

## States

| State | Behavior |
|-------|----------|
| No sessions | Empty state displayed in main area; sidebar shows only the + button |
| One or more sessions, one selected | Selected session's terminal view reparented into container; sidebar highlights selected row |
| Session added | New session appended, selected, terminal view shown |
| Session removed | PTY terminated, smart selection applied (previous > next > nil) |
| Session terminated (shell exited) | State transitions to `.terminated`; row may show visual indicator |
| Profile changed | Colors/font applied to terminal view without reparenting |
| Working directory changed (OSC 7) | Sidebar row updates directory metadata line; git branch detection triggered |
| Terminal title changed (OSC 2) | `terminalTitle` property updated |
| Foreground process changed | Sidebar row updates process metadata line |
| Custom OSC 7770 received | Dot color or subtitle updated on session; sidebar row reflects change |
| Window closing | `terminateAll()` called; all PTYs cleaned up |
