
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-001 | package-uttype-declaration, unique-file-extension, swift-uttype-property | Register UTType for `.catnip-proj` conforming to `com.apple.package` | Finder displays the package directory as a single file icon with the correct extension |
| pd-002 | reference-file-document, published-model-property | Create a new `ProjectDocument` and modify the `model` property | `objectWillChange` fires; auto-save triggers |
| pd-003 | filewrapper-read-write | Call `fileWrapper(snapshot:configuration:)` on a document | Returns a `FileWrapper` of kind directory containing `project.db` |
| pd-004 | journal-mode-off | Open the SQLite database inside a saved package | `PRAGMA journal_mode` returns `off` |
| pd-005 | pragma-user-version, metadata-table | Open the SQLite database and query `PRAGMA user_version` and `SELECT * FROM metadata` | `user_version` matches expected schema version; metadata row contains name, version, created_date |
| pd-006 | settings-table, boolean-string-storage, numeric-string-storage | Insert boolean setting `autoSave = true` and numeric setting `fontSize = 14` | Settings table contains `("autoSave", "true")` and `("fontSize", "14")` |
| pd-007 | check-sqlite-first | Open a package containing `project.db` | Document reads from SQLite successfully |
| pd-008 | fallback-legacy-json, deserialize-legacy-json | Open a package containing `data.json` but no `project.db` | Document reads from JSON; model is populated correctly |
| pd-009 | deserialize-legacy-json | Open a legacy JSON package, modify model, trigger save | Saved package contains `project.db` (SQLite); legacy JSON format replaced |
| pd-010 | empty-package-defaults | Open an empty package directory (no `project.db`, no `data.json`) | Document initializes with default values |
| pd-011 | log-format-version | Open a SQLite document with schema version 3 | Log entry: `info` level, includes "schema version 3" |
| pd-012 | temp-sqlite-write, parameterized-queries, read-temp-bytes | Trigger a save on a document with model data | Temporary SQLite file is created, data is inserted with parameterized queries, bytes are read |
| pd-013 | wrap-database-filewrapper, directory-filewrapper | Inspect the FileWrapper returned from `fileWrapper(...)` | Directory FileWrapper with one child whose `preferredFilename` is `project.db` |
| pd-014 | cleanup-temp-database | Trigger a save and inspect the temporary directory afterward | No leftover temporary `.db` files remain |
| pd-015 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that is missing a field added in a newer schema version | Missing field falls back to its default value; no crash or error |
| pd-016 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that contains an unknown extra field | Extra field is ignored; known fields are populated correctly |
| pd-017 | model-version-field | Inspect the model after reading from either JSON or SQLite | Model's `version` field is populated and matches the source's schema version |
| pd-018 | temp-database-url-helper | Call `tempDatabaseURL()` twice | Both URLs are in the temp directory, have `.db` extension, and are unique (different UUIDs) |
| pd-019 | exec-with-bindings | Call `exec("INSERT INTO settings (key, value) VALUES (?, ?)", [.text("k"), .text("v")])` | Row is inserted; no SQL injection possible with parameterized bindings |
| pd-020 | query-functions | Call `queryRow("SELECT value FROM settings WHERE key = ?", [.text("k")])` | Returns single row with value `"v"` |
| pd-021 | last-insert-row-id | Insert a row and call `lastInsertRowID()` | Returns the integer row ID of the just-inserted row |
| pd-022 | sqlite-error-type | Attempt to open a non-existent database path | Throws error of type `.cannotOpen` |
| pd-023 | sqlite-error-type | Execute invalid SQL | Throws error of type `.execFailed` |
| pd-024 | document-group-scene | Launch the app | `DocumentGroup` scenes are registered for each document type; File > Open shows the correct file type filters |
| pd-025 | autosave-via-published | Modify the model's `@Published` property | Auto-save fires without any user action |
| pd-026 | save-open-urls-on-quit | Open two documents, quit the app | Both document URLs are saved for session restoration |
| pd-027 | restore-urls-on-launch | Launch the app after quitting with two documents open | Both documents reopen; if one URL is invalid, the valid one still opens and the failure is logged |

