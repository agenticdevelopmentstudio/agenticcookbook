
### New Project flow

- **open-panel-directory-mode**: "New Project" MUST open an `NSOpenPanel` configured for directory selection (`canChooseDirectories = true`, `canChooseFiles = false`).
- **validate-git-directory**: The selected directory MUST be validated to contain a `.git` directory. If the `.git` directory is not present, the command MUST show an error alert with a clear message (e.g., "The selected folder is not a Git repository. Please select a folder that contains a .git directory.").
- **open-existing-package**: If a project package already exists at the expected path (`{selected_dir}/{dir_name}.{extension}`), the command MUST open the existing package instead of creating a duplicate.
- **create-new-package**: If no existing package is found, the command MUST create a new project package at `{selected_dir}/{dir_name}.{extension}` following the package-document spec (see dependency `package-document.md@1.0.0`).
- **open-via-document-controller**: After creation or discovery of an existing package, the command MUST open the document via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **show-creation-error-alert**: If document creation or opening fails, the command MUST show an error alert with the failure reason.

### New Workspace flow

- **workspace-save-panel**: "New Workspace" MUST open an `NSSavePanel` for file creation.
- **enforce-workspace-extension**: The save panel MUST enforce the workspace file extension (e.g., `.catnip-workspace`) via `allowedContentTypes` set to the workspace UTType.
- **create-workspace-package**: After the user confirms the save location, the command MUST create a new workspace package at the chosen path following the package-document spec.
- **open-workspace-document**: After creation, the command MUST open the new document via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **show-workspace-error-alert**: If document creation or opening fails, the command MUST show an error alert with the failure reason.

