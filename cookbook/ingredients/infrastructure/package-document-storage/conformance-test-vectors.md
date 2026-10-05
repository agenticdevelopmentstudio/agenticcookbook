
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-store-001 | journal-mode-off | Open the SQLite database inside a saved package | `PRAGMA journal_mode` returns `off` |
| pd-store-002 | pragma-user-version, metadata-table | Open the SQLite database and query `PRAGMA user_version` and `SELECT * FROM metadata` | `user_version` matches expected schema version; metadata row contains name, version, created_date |
| pd-store-003 | settings-table, boolean-string-storage, numeric-string-storage | Insert boolean setting `autoSave = true` and numeric setting `fontSize = 14` | Settings table contains `("autoSave", "true")` and `("fontSize", "14")` |
| pd-store-004 | check-sqlite-first | Open a package containing `project.db` | Document reads from SQLite successfully |
| pd-store-005 | fallback-legacy-json, deserialize-legacy-json | Open a package containing `data.json` but no `project.db` | Document reads from JSON; model is populated correctly |
| pd-store-006 | deserialize-legacy-json | Open a legacy JSON package, modify model, trigger save | Saved package contains `project.db` (SQLite); legacy JSON format replaced |
| pd-store-007 | empty-package-defaults | Open an empty package directory (no `project.db`, no `data.json`) | Document initializes with default values |
| pd-store-008 | log-format-version | Open a SQLite document with schema version 3 | Log entry: `info` level, includes "schema version 3" |
| pd-store-009 | temp-sqlite-write, parameterized-queries, read-temp-bytes | Trigger a save on a document with model data | Temporary SQLite file is created, data is inserted with parameterized queries, bytes are read |
| pd-store-010 | wrap-database-filewrapper, directory-filewrapper | Inspect the FileWrapper returned from `fileWrapper(...)` | Directory FileWrapper with one child whose `preferredFilename` is `project.db` |
| pd-store-011 | cleanup-temp-database | Trigger a save and inspect the temporary directory afterward | No leftover temporary `.db` files remain |
| pd-store-012 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that is missing a field added in a newer schema version | Missing field falls back to its default value; no crash or error |
| pd-store-013 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that contains an unknown extra field | Extra field is ignored; known fields are populated correctly |
| pd-store-014 | model-version-field | Inspect the model after reading from either JSON or SQLite | Model's `version` field is populated and matches the source's schema version |
| pd-store-015 | domain-specific-tables | Save a project document with sessions | The database contains the project's domain-specific table alongside `metadata` and `settings` |

