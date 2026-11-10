
### Command-to-flow wiring

- **new-project-invokes-flow**: The "New Project" command MUST start the Document Creation Flow's project flow (directory picker first) and MUST NOT perform any document work itself.
- **new-workspace-invokes-flow**: The "New Workspace" command MUST start the Document Creation Flow's workspace flow (save panel first) and MUST NOT perform any document work itself.
- **new-session-stays-in-menu**: The "New Session" command MUST be fully handled through the focused window's state (Creation Menu Commands) and MUST NOT invoke a document creation flow.
- **global-commands-always-enabled**: "New Project" and "New Workspace" MUST be enabled whether or not any window is focused, because they do not depend on focused-window state.
- **flow-failures-surface-as-alerts**: A failure inside a creation flow MUST surface as the flow's error alert and MUST NOT disable or alter the menu commands afterwards.
- **flow-cancel-is-silent**: Cancelling a picker MUST return the app to its prior state with no alert, log error, or change to menu enablement.
- **log-command-events**: Command events from both ingredients MUST be logged through the `logging` ingredient with category `MenuCommands`.

