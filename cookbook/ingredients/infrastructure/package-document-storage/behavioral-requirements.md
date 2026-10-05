
### SQLite database schema

- **journal-mode-off**: The SQLite database MUST use `PRAGMA journal_mode = OFF` since the database resides inside a package and is not a standalone file.
- **pragma-user-version**: The SQLite database MUST use `PRAGMA user_version = N` to track the schema version, where N is an integer incremented with each schema change.
- **metadata-table**: The database MUST contain a `metadata` table with columns for document name (`TEXT`), schema version (`INTEGER`), and created date (`TEXT` in ISO 8601 format).
- **settings-table**: The database MUST contain a `settings` table with columns `key` (`TEXT PRIMARY KEY`) and `value` (`TEXT`) for key-value pair storage.
- **boolean-string-storage**: Boolean settings MUST be stored as the string values `"true"` or `"false"`.
- **numeric-string-storage**: Numeric settings MUST be stored as their string representations (e.g., `"42"`, `"3.14"`).
- **domain-specific-tables**: Domain-specific data tables MUST be defined per document type (e.g., sessions table for projects, file references for workspaces).

### Read process

- **check-sqlite-first**: On read, the document MUST first check the package `FileWrapper` for the expected SQLite database file (e.g., `project.db`).
- **fallback-legacy-json**: If the SQLite database file is not found, the document MUST check for a legacy JSON file (e.g., `data.json`) for backward compatibility.
- **deserialize-legacy-json**: If a legacy JSON file is found, the document MUST deserialize it and populate the model from JSON data. The next save will write SQLite format.
- **empty-package-defaults**: If neither SQLite nor legacy JSON files are found in the package, the document MUST treat it as a new empty document with default values.
- **log-format-version**: On successful read, the document MUST log the format version (SQLite schema version or "legacy JSON") at `info` level.

### Write process

- **temp-sqlite-write**: On write, the document MUST create a temporary SQLite database file at a unique path (UUID-based filename in the temporary directory).
- **parameterized-queries**: The document MUST insert all model data into the temporary database using parameterized queries.
- **read-temp-bytes**: After writing all data, the document MUST read the temporary database file contents as raw bytes (`Data`).
- **wrap-database-filewrapper**: The document MUST wrap the database bytes in a `FileWrapper(regularFileWithContents:)` with the `preferredFilename` set to the database filename (e.g., `project.db`).
- **directory-filewrapper**: The document MUST return a `FileWrapper(directoryWithFileWrappers:)` containing the database file wrapper, forming the package directory.
- **cleanup-temp-database**: The temporary database file MUST be deleted after its bytes have been read (cleanup in a `defer` block or equivalent).

### Migration-safe Codable

- **migration-safe-codable**: Model types that are deserialized from legacy JSON MUST implement custom `init(from decoder: Decoder)` with per-field `try`/`catch`, falling back to default values for any field that fails to decode.
- **model-version-field**: Each model type MUST include a `version` field (integer or string) for schema identification in both JSON and SQLite representations.
- **backward-compatible-schema**: Adding new settings fields to the model MUST NOT break deserialization of documents created with older versions of the schema.

