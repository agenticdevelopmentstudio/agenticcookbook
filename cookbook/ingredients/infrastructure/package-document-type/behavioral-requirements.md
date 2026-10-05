
### UTType registration

- **package-uttype-declaration**: Each document type MUST declare a custom UTType conforming to `com.apple.package` in the app's Info.plist as an exported type.
- **unique-file-extension**: Each UTType MUST specify a unique file extension in `UTTypeTagSpecification` under `public.filename-extension`.
- **swift-uttype-property**: The UTType MUST be declared as a Swift `UTType` static property via `UTType(exportedAs:)` for use in document and file panel APIs.

### Document protocol conformance

- **reference-file-document**: Each document class MUST conform to `ReferenceFileDocument` (SwiftUI) and declare its `readableContentTypes` and `writableContentTypes` as the corresponding custom UTType.
- **published-model-property**: The document MUST expose a `@Published var model` property whose changes trigger `objectWillChange`, enabling SwiftUI auto-save.
- **filewrapper-read-write**: The document MUST implement `init(configuration:)` to read from a `FileWrapper` and `fileWrapper(snapshot:configuration:)` to write to a `FileWrapper`.

### Document scenes

- **document-group-scene**: The app MUST declare a `DocumentGroup(newDocument:)` scene for each document type, associating it with the correct `ReferenceFileDocument` subclass.
- **non-document-window-group**: Non-document windows (e.g., settings, welcome screen) MUST use `WindowGroup` scenes, not `DocumentGroup`.
- **custom-menu-save-panel**: Custom menu commands for creating new documents MUST use `NSSavePanel` to select the save location and then programmatically create the document.

### Lifecycle

- **autosave-via-published**: Auto-save MUST be triggered automatically by the `@Published` model property's `objectWillChange` publisher. No manual save action is required from the user.
- **save-open-urls-on-quit**: On application quit, the document system MUST save the URLs of all currently open documents for session restoration.
- **restore-urls-on-launch**: On application launch, the document system MUST attempt to reopen previously saved document URLs, logging any that fail to open.

