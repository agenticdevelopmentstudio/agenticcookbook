
- **toggle-accessible-label**: The toolbar toggle button MUST have an accessible label: "Toggle Inspector" (or platform-localized equivalent).
- **toggle-state-announce**: The toggle button MUST announce its state to screen readers (e.g., "Inspector, showing" / "Inspector, hidden").
- **row-label-accessible**: Each metadata row label MUST be the accessible label for its corresponding value.
- **path-full-announce**: The selectable Path text MUST be accessible to screen readers with the full path announced, not the truncated display.
- **git-accessible-label**: The Git Status badge MUST have an accessibility label with the full status name (e.g., "Git Status: Modified"), not just the character. This is inherited from the git-status-indicator spec (git-status-badge).
- **empty-state-accessible**: The empty state MUST follow the empty-state accessibility requirements (heading announced first, icon decorative).
- **keyboard-navigable**: The inspector panel MUST be fully keyboard-navigable — Tab key should move focus through metadata rows and the close/toggle button.

