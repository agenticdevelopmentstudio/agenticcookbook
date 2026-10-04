
| State | Behavior |
|-------|----------|
| Window opened, no sessions | Default session created automatically on appear; terminal view shows shell prompt |
| One or more sessions, one selected | Selected session's terminal view reparented into container; sidebar highlights selected row |
| Session added | New session appended, selected, terminal view shown |
| Session removed | PTY terminated, smart selection applied (previous > next > nil per terminal-pane remove-smart-select) |
| All sessions removed | Empty state displayed (per terminal-pane empty-state-no-sessions); next session creation re-populates |
| Profile changed | Colors/font applied to terminal view without reparenting |
| Profile deleted while in use | Falls back to Solarized Dark (per color-profile fallback-to-default) |
| Window closing | `terminateAll()` called; all PTYs cleaned up |
| Multiple standalone windows open | Each window operates independently with its own session manager |

