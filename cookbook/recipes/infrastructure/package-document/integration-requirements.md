
- **document-delegates-to-storage**: The document class declared by the package document type MUST implement `init(configuration:)` by running the storage read process and `fileWrapper(snapshot:configuration:)` by running the storage write process. The document class MUST NOT contain its own SQLite or JSON handling.
- **storage-uses-sqlite-helpers**: The storage read and write processes MUST access SQLite only through the SQLite helpers, passing every value as a binding. The storage MUST NOT call the `sqlite3` API directly or build SQL by string interpolation.
- **autosave-ends-in-atomic-replacement**: An auto-save triggered by the `@Published` model MUST result in a temporary database write, a byte read, and a directory `FileWrapper` handed back to the document system, so the package on disk is replaced as a whole and never partially written.
- **restoration-uses-storage-read**: Documents reopened during session restoration MUST be read through the same storage read process, including the legacy JSON fallback and schema version check, as documents opened by the user.
- **errors-surface-through-document**: A `SQLiteError` raised by the helpers, a corrupt database, or a schema version newer than the app supports MUST surface to the user through the document open or save error path, and MUST leave the existing package on disk unmodified.
- **shared-log-category**: All three ingredients MUST log under the single `PackageDocument` category so one filter shows a document's complete lifecycle.
- **unique-database-name-per-kind**: Each document kind MUST use its own UTType, file extension, and database filename; two kinds MUST NOT share an extension.

