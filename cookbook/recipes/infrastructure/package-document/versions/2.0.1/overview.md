
A pattern for macOS document-based apps that use directory bundle packages (rendered as single files in Finder) containing SQLite databases. The document is a folder with a custom UTType conforming to `com.apple.package`, registered with a file extension (e.g., `.catnip-proj`, `.catnip-workspace`). Inside the package, one or more SQLite database files store all persistent state. The pattern supports schema versioning via `PRAGMA user_version`, format migration from legacy JSON files to SQLite, atomic writes through temporary database creation and `FileWrapper` packaging, and auto-save via SwiftUI's `ReferenceFileDocument` protocol. Each document type (project, workspace) follows the same structural pattern with its own UTType, file extension, database filename, and schema.

The recipe composes three ingredients. The package document type registers the UTType and owns the document protocol conformance, scenes, and lifecycle. The package document storage owns what is inside the package and the read, write, and migration process. The SQLite helpers are the safe database layer the storage format uses.

### Terminology

The terms Package document, UTType, ReferenceFileDocument, FileWrapper, and Document scene are defined in the package document type ingredient. The terms Schema version, Format migration, Atomic write, and Key-value settings are defined in the package document storage ingredient.

### Architecture

The architecture diagram of the document, auto-save path, and package on disk is in the package document storage ingredient. In this recipe the same flow is split across the three ingredients as shown in [Layout](#layout).

### Logging

Logging is specified per ingredient under subsystem `{{bundle_id}}` and category `PackageDocument`. Document created and session restoration events are in the package document type ingredient; open, write, migration, corruption, disk-full, date-parsing, and temp-file events are in the package document storage ingredient; SQLite open and exec failures are in the SQLite helpers ingredient.

