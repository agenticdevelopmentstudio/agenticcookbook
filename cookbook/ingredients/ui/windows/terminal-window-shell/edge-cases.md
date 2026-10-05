
- **Last session closed by user**: When the user closes the last session, the empty state is displayed. A new session is NOT automatically created — auto-creation only occurs on initial `onAppear` when the session list is empty. The user must click the "+" button or "New Session" to create a new session.
- **Multiple standalone terminal windows**: Each window has its own `SessionManager` instance. Opening N standalone terminal windows results in N independent session managers. Menu commands dispatch to the focused window's session manager via `.focusedObject()`.
- **Window restored after crash**: Session manager MUST NOT attempt to restore PTY sessions from a previous run. Sessions are ephemeral. On relaunch, the window opens with no sessions, and the `onAppear` auto-creation logic creates a fresh default session.
- **Rapid window open/close**: `terminateAll()` MUST complete cleanly. PTY file descriptors MUST be closed. No zombie processes should remain.
- **Window opened with no shell available**: Falls back to `/bin/zsh` per terminal-pane edge case (shell not found). The standalone terminal window does not add additional fallback logic beyond what terminal-pane provides.
- **Very many sessions in one window (50+)**: Session list MUST remain scrollable and performant (delegated to terminal-pane edge case handling).
- **focusedObject not set**: If menu commands fire before any standalone terminal window is focused, the system's `FocusedValues` will not contain a session manager. Menu commands MUST be disabled when no session manager is available in the focused values.

