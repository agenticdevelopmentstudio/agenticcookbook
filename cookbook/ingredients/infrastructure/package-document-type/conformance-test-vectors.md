
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-type-001 | package-uttype-declaration, unique-file-extension, swift-uttype-property | Register UTType for `.catnip-proj` conforming to `com.apple.package` | Finder displays the package directory as a single file icon with the correct extension |
| pd-type-002 | reference-file-document, published-model-property | Create a new `ProjectDocument` and modify the `model` property | `objectWillChange` fires; auto-save triggers |
| pd-type-003 | filewrapper-read-write | Call `fileWrapper(snapshot:configuration:)` on a document | Returns a `FileWrapper` of kind directory containing the document's database file |
| pd-type-004 | document-group-scene | Launch the app | `DocumentGroup` scenes are registered for each document type; File > Open shows the correct file type filters |
| pd-type-005 | autosave-via-published | Modify the model's `@Published` property | Auto-save fires without any user action |
| pd-type-006 | save-open-urls-on-quit | Open two documents, quit the app | Both document URLs are saved for session restoration |
| pd-type-007 | restore-urls-on-launch | Launch the app after quitting with two documents open | Both documents reopen; if one URL is invalid, the valid one still opens and the failure is logged |
| pd-type-008 | non-document-window-group | Inspect the scenes for the settings and welcome windows | They are `WindowGroup` scenes, not `DocumentGroup` |

