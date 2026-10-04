
| Term | Definition |
|------|-----------|
| Package document | A directory bundle that macOS presents as a single file in Finder, identified by a custom UTType conforming to `com.apple.package` |
| UTType | A Uniform Type Identifier declared in Info.plist that maps a file extension to a content type and conformance hierarchy |
| ReferenceFileDocument | A SwiftUI protocol for reference-type documents that triggers auto-save when the document's `objectWillChange` publisher fires |
| FileWrapper | An Apple framework class representing a file, directory, or symbolic link in memory; used to read from and write to package directories |
| Schema version | An integer stored in SQLite's `PRAGMA user_version` that identifies the database schema revision |
| Format migration | The process of reading a legacy format (e.g., JSON) and converting it to the current SQLite-based format on first save |
| Atomic write | Writing all data to a temporary SQLite file, reading it back as bytes, and wrapping it in a FileWrapper so the system can perform an atomic directory replacement |
| Key-value settings | A table of string key-value pairs used to store typed settings (booleans as `"true"`/`"false"`, numbers as string representations) |
| Document scene | A SwiftUI `DocumentGroup` scene that manages the open/save/close lifecycle for a document type |

