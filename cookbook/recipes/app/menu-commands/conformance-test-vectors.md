
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-001 | replace-default-new-item, creation-command-order | Open the File menu | Default "New" item is replaced with "New Project", "New Session", "New Workspace" in that order |
| mc-002 | unique-keyboard-shortcuts | Press Cmd-N | "New Project" flow initiates (NSOpenPanel appears) |
| mc-003 | unique-keyboard-shortcuts | Press Cmd-Shift-N with a project window focused | "New Session" creates a session in the focused project |
| mc-004 | unique-keyboard-shortcuts | Press Cmd-Option-N | "New Workspace" flow initiates (NSSavePanel appears) |
| mc-005 | sf-symbol-icons | Open the File menu on macOS | Each creation command displays its SF Symbol icon |
| mc-006 | disable-without-focus, disable-without-project, graceful-nil-focused-object | Press Cmd-Shift-N with no window focused | Menu item is disabled; nothing happens |
| mc-007 | open-panel-directory-mode | Trigger "New Project" | NSOpenPanel opens with directory selection enabled and file selection disabled |
| mc-008 | validate-git-directory | Select a directory without a .git subdirectory | Error alert appears: "The selected folder is not a Git repository." |
| mc-009 | validate-git-directory | Select a directory containing a .git subdirectory | Validation passes; flow proceeds to package creation or opening |
| mc-010 | open-existing-package, open-via-document-controller | Select a directory that already contains `dirname.catnip-proj` | Existing package is opened; no new package created |
| mc-011 | create-new-package, open-via-document-controller | Select a valid git directory with no existing package | New package created at `{dir}/{dirname}.{ext}`; document opens |
| mc-012 | show-creation-error-alert | Select a directory where package creation fails (e.g., read-only filesystem) | Error alert displayed with failure reason |
| mc-013 | workspace-save-panel, enforce-workspace-extension | Trigger "New Workspace" | NSSavePanel opens with workspace file extension enforced |
| mc-014 | create-workspace-package, open-workspace-document | Confirm save location in NSSavePanel | Workspace package created at chosen path; document opens |
| mc-015 | show-workspace-error-alert | Confirm save location on a read-only volume | Error alert displayed with failure reason |
| mc-016 | create-session-in-window, focused-object-project-state | Press Cmd-Shift-N with project window focused | New session created in the focused project |
| mc-017 | focused-object-dispatch, provide-focused-object | Focus Window A, press Cmd-Shift-N, then focus Window B, press Cmd-Shift-N | Session created in Window A's project first, then in Window B's project |
| mc-018 | graceful-nil-focused-object | Focus a non-project window (e.g., settings), press Cmd-Shift-N | Menu item is disabled; no action taken |
| mc-019 | voiceover-menu-access | Enable VoiceOver, navigate to File menu | VoiceOver announces each menu item with title and shortcut |
| mc-020 | voiceover-error-announce | Trigger validation error with VoiceOver enabled | VoiceOver announces the error alert |

