
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-001 | replace-default-new-item, creation-command-order | Open the File menu | Default "New" item is replaced with "New Project", "New Session", "New Workspace" in that order |
| mc-003 | unique-keyboard-shortcuts | Press Cmd-Shift-N with a project window focused | "New Session" creates a session in the focused project |
| mc-005 | sf-symbol-icons | Open the File menu on macOS | Each creation command displays its SF Symbol icon |
| mc-006 | disable-without-focus, disable-without-project, graceful-nil-focused-object | Press Cmd-Shift-N with no window focused | Menu item is disabled; nothing happens |
| mc-016 | create-session-in-window, focused-object-project-state | Press Cmd-Shift-N with project window focused | New session created in the focused project |
| mc-017 | focused-object-dispatch, provide-focused-object | Focus Window A, press Cmd-Shift-N, then focus Window B, press Cmd-Shift-N | Session created in Window A's project first, then in Window B's project |
| mc-018 | graceful-nil-focused-object | Focus a non-project window (e.g., settings), press Cmd-Shift-N | Menu item is disabled; no action taken |
| mc-019 | voiceover-menu-access | Enable VoiceOver, navigate to File menu | VoiceOver announces each menu item with title and shortcut |

