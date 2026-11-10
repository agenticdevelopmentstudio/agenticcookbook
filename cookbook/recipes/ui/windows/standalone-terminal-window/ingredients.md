
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Terminal Window Shell | [adc.ingredient.ui.windows.terminal-window-shell](cookbook:de88e58f-7260-4089-b0e3-9485d6b4bc79) | Sidebar and terminal split, per-window session manager, default session, terminate on close | Yes | Sidebar 150-200pt |
| Terminal Pane | [adc.ingredient.ui.panels.terminal-pane](cookbook:4a2898cf-34ed-4153-8d06-c795f80c19cd) | Session list rows, terminal rendering, PTY lifecycle, empty state | Yes | Shared with the project window |
| Color Profile | [adc.ingredient.ui.components.color-profile](cookbook:bdc920ab-fde0-445a-a62a-c2f6d23da8a8) | Active profile colors, font and cursor style; fallback to Solarized Dark | Yes | Active profile ID in global app storage |
| Window Frame Persistence | [adc.ingredient.infrastructure.window-frame-persistence](cookbook:85d04a9b-5692-4025-a489-eac8bbb14663) | Persists window frame | Yes | Autosave name `"terminal-window"` |
| Logging | [adc.ingredient.infrastructure.logging](cookbook:7c2049c7-89d9-4135-b657-dbd03cdd19a0) | Window-level logging | Yes | Category `StandaloneTerminalWindow` (events defined by the shell) |

