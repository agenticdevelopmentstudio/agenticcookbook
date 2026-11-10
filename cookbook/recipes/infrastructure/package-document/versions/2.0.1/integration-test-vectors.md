
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-028 | document-delegates-to-storage, autosave-ends-in-atomic-replacement | Modify the `@Published` model of an open document | Auto-save runs the storage write process; the document returns a directory `FileWrapper` with one child `project.db`; no temporary `.db` file remains |
| pd-029 | storage-uses-sqlite-helpers | Save a document whose model contains a string with an SQL metacharacter such as `'; DROP TABLE settings; --` | The value is stored verbatim through a binding; the settings table still exists |
| pd-030 | document-delegates-to-storage, restoration-uses-storage-read | Quit with a legacy-JSON document open (no `project.db`), relaunch | The document reopens through the storage read process with the model populated from JSON; the next save writes SQLite |
| pd-031 | errors-surface-through-document | Open a package whose `project.db` is corrupt | The user sees an error; the file on disk is not modified; other restored documents still open |
| pd-032 | errors-surface-through-document | Open a package whose `user_version` is higher than the app's schema version | The document refuses to load and reports that a newer app version is required |
| pd-033 | unique-database-name-per-kind | Register a project kind and a workspace kind | Each has its own UTType, extension, and database filename |

Vectors pd-001 to pd-027 are single-ingredient vectors and appear in the ingredients under new IDs: the package document type holds pd-001, pd-002, pd-003, pd-024, pd-025, pd-026, and pd-027 (as pd-type-001 to pd-type-008, which add a non-document-window-group vector); the package document storage holds pd-004 to pd-017 (as pd-store-001 to pd-store-015, which add a domain-specific-tables vector); and the SQLite helpers hold pd-018 to pd-023 (as sqlite-helpers-001 to sqlite-helpers-007, which add a `queryAll` vector).

