
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-002 | unique-keyboard-shortcuts | Press Cmd-N | "New Project" flow initiates (NSOpenPanel appears) |
| mc-004 | unique-keyboard-shortcuts | Press Cmd-Option-N | "New Workspace" flow initiates (NSSavePanel appears) |
| mc-021 | new-project-invokes-flow, global-commands-always-enabled | With no window focused, press Cmd-N | New Project is enabled and the directory picker appears |
| mc-022 | new-session-stays-in-menu | Press Cmd-Shift-N with a project window focused | A session is created in that project and no picker appears |
| mc-023 | flow-cancel-is-silent | Press Cmd-Option-N and cancel the save panel | No alert, no document, and all three menu items remain in their prior enabled state |
| mc-024 | flow-failures-surface-as-alerts | Trigger New Project on a read-only directory, dismiss the alert, press Cmd-N again | Alert appears once; the second invocation opens the picker normally |
| mc-025 | log-command-events | Run New Project to completion | Logs show initiated, panel presented, validation passed, package creation, and document opened events under `MenuCommands` |

