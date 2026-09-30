<!-- leaf: recipes-infrastructure/package-document--edge-cases · source: recipes/infrastructure/package-document.md -->

# Package Document

**Rules** (cite as `recipes-infrastructure/package-document--edge-cases#<slug>`):

- `corrupt-sqlite-database` MUST — If sqlite3_open succeeds but queries fail (e.g., malformed schema, incomplete write), the document MUST surface a …
- `disk-full-during-write` MUST — If the temporary SQLite file cannot be fully written due to insufficient disk space, the exec() call will fail. The …
- `very-large-documents` SHOULD — For documents with tens of thousands of rows, the write process creates the entire database in memory (temporary file). …
- `schema-downgrade-attempt` MUST — If a document's user_version is higher than the app's current schema version, the document MUST refuse to load and …
- `temporary-file-cleanup-failure` SHOULD — If the temporary database file cannot be deleted after reading its bytes, the operation SHOULD still succeed (the data …
- `empty-settings-table` MUST — If the settings table exists but contains no rows, all settings MUST fall back to their coded default values. This is …
- `date-parsing-failures` MUST — If a date string in the metadata table does not conform to ISO 8601, the invalidDate error MUST be thrown and surfaced, …
- `multiple-database-files-in-package` MUST — If future versions add additional database files to the package (e.g., cache.db), the read/write process MUST handle …

## Edge Cases

- **Corrupt SQLite database**: If `sqlite3_open` succeeds but queries fail (e.g., malformed schema, incomplete write), the document MUST surface a user-facing error describing the corruption and MUST NOT overwrite the corrupt file. The user should be offered the option to create a new document or attempt manual recovery.
- **Missing files in package**: If the package directory exists but contains neither the expected SQLite database nor a legacy JSON file, the document treats this as a new empty document (empty-package-defaults). If the package directory itself is missing or inaccessible, the system reports a file-not-found error.
- **Format migration (JSON to SQLite)**: When a legacy JSON document is opened, the model is populated from JSON. On the next save, the write process creates a SQLite database. The legacy JSON file is not explicitly deleted from the package — the new `FileWrapper(directoryWithFileWrappers:)` simply omits it, and the atomic directory replacement removes it.
- **Concurrent access**: If two processes or two app instances attempt to open the same package document simultaneously, behavior is undefined. The pattern relies on macOS file coordination (`NSFileCoordinator`) when available, but does not implement custom locking. Documents opened via `DocumentGroup` benefit from the system's built-in file coordination.
- **Disk full during write**: If the temporary SQLite file cannot be fully written due to insufficient disk space, the `exec()` call will fail. The document MUST catch this error and surface it to the user. The existing on-disk package MUST NOT be modified or corrupted.
- **Very large documents**: For documents with tens of thousands of rows, the write process creates the entire database in memory (temporary file). If memory pressure is a concern, the implementation SHOULD write incrementally and monitor for memory warnings on iOS.
- **Schema downgrade attempt**: If a document's `user_version` is higher than the app's current schema version, the document MUST refuse to load and present an error indicating that a newer version of the app is required (see States table).
- **Temporary file cleanup failure**: If the temporary database file cannot be deleted after reading its bytes, the operation SHOULD still succeed (the data was already captured). The leftover temp file will be cleaned up by the OS eventually.
- **Package opened by external tool**: If a user right-clicks "Show Package Contents" and modifies the SQLite database externally, the app has no mechanism to detect this. The next open will read whatever state the database is in. No integrity checking beyond schema version is performed.
- **Empty settings table**: If the settings table exists but contains no rows, all settings MUST fall back to their coded default values. This is not an error condition.
- **Date parsing failures**: If a date string in the metadata table does not conform to ISO 8601, the `invalidDate` error MUST be thrown and surfaced, rather than silently using a fallback date.
- **Multiple database files in package**: If future versions add additional database files to the package (e.g., `cache.db`), the read/write process MUST handle the presence of unknown files gracefully — they are preserved in the directory FileWrapper during write.
