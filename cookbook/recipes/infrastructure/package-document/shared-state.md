
| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Document model | Package document storage (on read) and the UI (edits) | Package document type, the UI | two-way | `@Published var model` on the document; each change fires `objectWillChange` |
| Model snapshot | Package document type | Package document storage write process | one-way | The snapshot passed to `fileWrapper(snapshot:configuration:)` |
| Package `FileWrapper` | Package document storage | Document system | one-way | Directory `FileWrapper` containing the database file wrapper, replaced atomically |
| Schema version | `PRAGMA user_version` in the database | Package document storage | one-way | Read on open and compared with the app's current version |
| Open document URLs | Package document type | Session restoration on next launch | one-way | Saved on quit, reopened on launch, failures logged and skipped |
| Temporary database path | SQLite helpers (`tempDatabaseURL()`) | Package document storage write process | one-way | UUID-named file in the temporary directory, deleted after its bytes are read |

