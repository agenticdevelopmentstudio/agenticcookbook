
- **macOS (SwiftUI)**: `NSOpenPanel` and `NSSavePanel` are called from the button action via `await panel.begin()` (or `panel.runModal()` on the main actor). After directory selection, validate by checking `FileManager.default.fileExists(atPath: selectedURL.appendingPathComponent(".git").path)`. Create the package document per `package-document.md` and open it via `NSDocumentController.shared.openDocument(withContentsOf: url, display: true)`.
- **macOS (AppKit)**: Present the panels with `begin(completionHandler:)` on the key window; the document controller call is identical to the SwiftUI path.
- **Windows**: File/directory pickers use `IFileOpenDialog` (directory mode) and `IFileSaveDialog` respectively. Validation logic (checking for `.git` directory) uses standard filesystem APIs.
- **Compose and React/Web**: Not applicable — the flows use native OS pickers and the macOS document controller; Compose Desktop and Electron use their platform file dialogs with the same validation steps.

