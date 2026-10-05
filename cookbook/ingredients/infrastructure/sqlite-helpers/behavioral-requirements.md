
- **temp-database-url-helper**: The codebase MUST provide a `tempDatabaseURL()` helper that returns a URL in the temporary directory with a UUID-based filename and `.db` extension.
- **exec-with-bindings**: The codebase MUST provide an `exec()` function that executes a SQL statement with parameterized bindings (supporting at minimum `.text(String)`, `.int(Int)`, and `.null` binding types).
- **query-functions**: The codebase MUST provide `queryRow()` and `queryAll()` functions for reading single and multiple rows from the database.
- **last-insert-row-id**: The codebase MUST provide a `lastInsertRowID()` function to retrieve the row ID of the last inserted row.
- **sqlite-error-type**: SQLite errors MUST be represented as a dedicated error type with cases for: `cannotOpen`, `execFailed`, `missingData`, and `invalidDate`.

