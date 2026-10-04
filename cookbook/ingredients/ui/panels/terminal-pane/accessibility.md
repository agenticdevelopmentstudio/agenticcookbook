
- **keyboard-nav-sessions**: The session list MUST be keyboard-navigable. Arrow keys MUST move selection between sessions.
- **add-button-label**: The add button MUST have an accessible label: "New Terminal Session".
- **row-announce-details**: Each session row MUST announce: session name, working directory, git branch (if present), and foreground process via a combined accessibility label.
- **keyboard-context-menu**: The context menu MUST be accessible via keyboard (e.g., Shift+F10 or Control+Click equivalent).
- **voiceover-terminal-nav**: The terminal view MUST support VoiceOver cursor navigation for reading terminal output.
- **empty-state-accessible**: The empty state MUST follow empty-state accessibility requirements (heading announced first, icon decorative).
- **terminated-announce**: The `.terminated` state MUST be announced to screen readers when a session's shell exits.

