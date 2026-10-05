
The flows that create and open documents from the "New Project" and "New Workspace" menu commands. New Project opens a directory picker, validates the selection is a Git repository, then opens an existing project package or creates a new one; New Workspace opens a save panel with the workspace extension enforced and creates a workspace package. Both flows open the result through the document controller and show an error alert on failure. Package contents follow the package-document recipe.

### Terminology

| Term | Definition |
|------|-----------|
| NSOpenPanel | A macOS panel for selecting existing files or directories |
| NSSavePanel | A macOS panel for choosing a save location and filename for a new file |
| NSDocumentController | The macOS singleton that manages the app's open documents and coordinates document lifecycle |
| Package document | A directory bundle presented as a single file in Finder, as defined in package-document.md |

