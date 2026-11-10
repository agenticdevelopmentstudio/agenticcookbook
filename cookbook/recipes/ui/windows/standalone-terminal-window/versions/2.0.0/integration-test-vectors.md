
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| stw-001 | window-group-terminal | Inspect SwiftUI scene declaration | `WindowGroup(id: "terminal")` is registered |
| stw-004 | persist-window-frame | Open terminal window, move to (300, 200), close, reopen | Window restores at (300, 200); autosave name is "terminal-window" |
| stw-005 | min-size-constraints | Attempt to resize window below 600x400 | Window enforces minimum size constraints |
| stw-010 | apply-active-profile, global-profile-storage | Set active profile to Dracula, open terminal window | Terminal renders with Dracula colors (#282a36 background, #f8f8f2 foreground) |
| stw-011 | profile-fallback-default | Set active profile ID in AppStorage to an invalid UUID, open terminal window | Terminal falls back to Solarized Dark (#002b36 background, #839496 foreground) |
| stw-012 | shared-terminal-spec | Compare terminal behavior in standalone window vs. project window terminal pane | Identical PTY lifecycle, OSC handling, session list, and rendering behavior |
| stw-016 | accessible-window-title | Enable VoiceOver, open terminal window | Window title announced as "Terminal" (or similar), distinguishable from project windows |
| stw-017 | scene-hosts-shell, window-group-terminal | Open the terminal window | The scene content is the Terminal Window Shell and nothing else |
| stw-018 | profile-reaches-terminal-view | Change the active profile while a session is running | Terminal colors and font update; the scrollback and view are not reparented |
| stw-019 | frame-key-fixed | Open two standalone windows, move one, close both, reopen | Frame is restored from the single `"terminal-window"` entry |

