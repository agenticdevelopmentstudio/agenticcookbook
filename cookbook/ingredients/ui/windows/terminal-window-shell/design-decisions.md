
**Decision**: Own the session manager in the shell and delegate every terminal behavior to the terminal-pane ingredient.
**Rationale**: A single terminal-pane spec keeps PTY lifecycle, OSC handling, and rendering identical between the standalone window and the project window (single source of truth).
**Approved**: pending

