
- **sessions-toggle-label**: The toolbar sessions toggle button MUST have an accessible label: "Toggle Sessions Panel".
- **inspector-toggle-label**: The toolbar inspector toggle button MUST have an accessible label: "Toggle Inspector" (inherited from inspector-panel spec).
- **gear-button-label**: The toolbar gear button MUST have an accessible label: "Project Settings".
- **pane-header-accessible**: Each collapsible pane header MUST follow the accessibility requirements defined in `ui/collapsible-pane-header.md` (button role, expand/collapse announcement, keyboard toggle).
- **divider-accessible**: The split view dividers MUST be accessible to VoiceOver and MUST announce their purpose (e.g., "Resize sessions panel").
- **keyboard-region-nav**: Keyboard navigation MUST allow moving focus between all major regions: sessions, file tree, editor, terminal, inspector, and toolbar.
- **keyboard-panel-shortcuts**: The window MUST support standard macOS keyboard shortcuts for panel toggling (to be defined at implementation time and recorded as Design Decisions).

