
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mc-007 | open-panel-directory-mode | Trigger "New Project" | NSOpenPanel opens with directory selection enabled and file selection disabled |
| mc-008 | validate-git-directory | Select a directory without a .git subdirectory | Error alert appears: "The selected folder is not a Git repository." |
| mc-009 | validate-git-directory | Select a directory containing a .git subdirectory | Validation passes; flow proceeds to package creation or opening |
| mc-010 | open-existing-package, open-via-document-controller | Select a directory that already contains `dirname.catnip-proj` | Existing package is opened; no new package created |
| mc-011 | create-new-package, open-via-document-controller | Select a valid git directory with no existing package | New package created at `{dir}/{dirname}.{ext}`; document opens |
| mc-012 | show-creation-error-alert | Select a directory where package creation fails (e.g., read-only filesystem) | Error alert displayed with failure reason |
| mc-013 | workspace-save-panel, enforce-workspace-extension | Trigger "New Workspace" | NSSavePanel opens with workspace file extension enforced |
| mc-014 | create-workspace-package, open-workspace-document | Confirm save location in NSSavePanel | Workspace package created at chosen path; document opens |
| mc-015 | show-workspace-error-alert | Confirm save location on a read-only volume | Error alert displayed with failure reason |
| mc-020 | voiceover-error-announce | Trigger validation error with VoiceOver enabled | VoiceOver announces the error alert |

