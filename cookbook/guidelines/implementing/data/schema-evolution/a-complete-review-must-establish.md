
- Migration tracking mechanism established: `PRAGMA user_version` incremented or migration table records applied migrations
- No unsupported ALTER TABLE operations used (SQLite doesn't support: DROP COLUMN, MODIFY COLUMN type, RENAME COLUMN in older versions)
- Backwards-compatible migrations: ADD COLUMN with NOT NULL requires DEFAULT, DROP COLUMN requires table recreation, RENAME uses compatibility layer
- Sync-compatible migrations are add-only: new columns have defaults, no deletions until sync strategy allows, no renames without compatibility mapping
- Migrations wrapped in transactions (`BEGIN` / `COMMIT`) with rollback strategy documented
- Column drops use `CREATE TABLE new AS SELECT * FROM old` pattern with constraint reconstruction
- Default values provided for new NOT NULL columns (schema will be readable by old code during upgrade)
- Migration scripts are idempotent: re-running migration is safe even if table already modified
- Major version changes tracked separately; deployment strategy ensures coordinated migration between client and server
- Every rule is kept, or the change says why not: `must-track-schema-version-with-user-version`, `must-end-migration-file-with-user-version`, `must-wrap-each-migration-in-transaction`, `must-make-migrations-idempotent`, `must-add-columns-nullable-or-defaulted`, `must-not-rename-column-below-3-25-0`, `must-not-drop-column-below-3-35-0`, `must-not-use-alter-table-for-unsupported-changes`, `must-disable-foreign-keys-during-recreate`, `must-run-foreign-key-check-before-commit`, `must-recreate-dependent-objects`, `must-keep-migrations-compatible-across-participants`, `must-only-add-columns-in-sync-schemas`, `must-default-new-columns-in-sync-schemas`, `must-test-migrations-from-every-version`, `must-back-up-before-server-migration`, `should-flag-type-changes-for-manual-sql`


A review passes when it establishes every item above.
