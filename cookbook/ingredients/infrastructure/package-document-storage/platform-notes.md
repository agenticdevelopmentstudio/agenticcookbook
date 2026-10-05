
- **macOS (SwiftUI)**: Use `FileWrapper(directoryWithFileWrappers:)` for the package and `FileWrapper(regularFileWithContents:)` for each file inside it. For atomic writes, the temporary database lives in the temporary directory and its bytes are handed to the `FileWrapper`; the system performs the atomic replacement.
- **macOS (AppKit)**: Override `read(from:ofType:)` and `fileWrapper(ofType:)` on `NSDocument` with the same SQLite read/write logic.
- **iOS / visionOS**: The same SQLite read/write logic applies. No platform-specific changes to the storage layer.
- **Windows**: The pattern is an ordinary directory containing a SQLite file; the same schema, versioning, and temp-file-then-replace write apply, using the platform's atomic rename.
- **Compose / React/Web**: Not applicable — the package and `FileWrapper` model are Apple-specific.

