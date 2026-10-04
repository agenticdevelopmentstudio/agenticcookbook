
- **text-editor-a11y-role**: The editor MUST be accessible as a text editor role to screen readers and MUST support standard text navigation (by character, word, line).
- **header-a11y-compliance**: The pane header MUST follow collapsible-pane-header accessibility requirements (button role, expand/collapse announced).
- **dirty-state-a11y**: The dirty indicator MUST be communicated to assistive technologies — e.g., the header's accessibility label SHOULD include "edited" or "modified" when `isModified` is true.
- **placeholder-a11y**: Empty state and error placeholders MUST follow empty-state accessibility requirements (heading announced first, icon decorative).
- **save-menu-discoverable**: The Cmd+S save shortcut MUST be discoverable via the app's menu bar (File > Save) on macOS.
- **decorative-line-numbers**: Line numbers in the gutter MUST be decorative and not announced individually by screen readers.

