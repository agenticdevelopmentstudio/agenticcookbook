
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Terminal Window Shell | `agenticdevelopercookbook://ingredients/ui/windows/terminal-window-shell` | Sidebar and terminal split, per-window session manager, default session, terminate on close | Yes | Sidebar 150-200pt |
| Terminal Pane | `agenticdevelopercookbook://ingredients/ui/panels/terminal-pane` | Session list rows, terminal rendering, PTY lifecycle, empty state | Yes | Shared with the project window |
| Color Profile | `agenticdevelopercookbook://ingredients/ui/components/color-profile` | Active profile colors, font and cursor style; fallback to Solarized Dark | Yes | Active profile ID in global app storage |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Persists window frame | Yes | Autosave name `"terminal-window"` |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Window-level logging | Yes | Category `StandaloneTerminalWindow` (events defined by the shell) |

