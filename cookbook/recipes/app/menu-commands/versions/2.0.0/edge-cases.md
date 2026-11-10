
- **Cmd-N while a creation flow is open**: The open panel or save panel is modal; the command MUST NOT start a second flow until the first is dismissed, and the other creation commands are blocked by the same modal.
- **Flow invoked from a workspace window**: New Project and New Workspace MUST work from a workspace window, while New Session MUST stay disabled there (no project state is provided).
- **Window focus changes while a picker is open**: The flow MUST complete against the app, not the window that was focused at invocation, and MUST NOT change which window supplies New Session state afterward.
- **Document opened by a flow gains focus**: After a flow opens a project window, New Session MUST become enabled for that window without any further user action.

