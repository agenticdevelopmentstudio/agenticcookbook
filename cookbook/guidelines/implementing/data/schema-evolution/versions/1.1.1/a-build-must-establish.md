
- `must-track-schema-version-with-user-version`: the schema version is tracked with `PRAGMA user_version` or, in a sync context, a migration tracking table
- `must-end-migration-file-with-user-version`: every migration file ends with its `PRAGMA user_version = N;` statement
- `must-wrap-each-migration-in-transaction`: every migration runs inside a transaction
- `must-make-migrations-idempotent`: every migration is safe to run twice
- `must-add-columns-nullable-or-defaulted`: every `ADD COLUMN` adds a column that allows NULL or has a DEFAULT
- `must-not-rename-column-below-3-25-0`: no `RENAME COLUMN` runs against SQLite older than 3.25.0
- `must-not-drop-column-below-3-35-0`: no `DROP COLUMN` runs against SQLite older than 3.35.0
- `must-not-use-alter-table-for-unsupported-changes`: no migration uses ALTER TABLE to change a column type, add or remove a constraint, change a DEFAULT value or reorder columns
- `must-disable-foreign-keys-during-recreate`: every table recreate disables foreign keys before it and re-enables them after
- `must-run-foreign-key-check-before-commit`: every table recreate runs `PRAGMA foreign_key_check` before it commits
- `must-recreate-dependent-objects`: every table recreate recreates the indexes, triggers and views that referenced the old table
- `must-keep-migrations-compatible-across-participants`: in a synced schema, every migration stays compatible with every participant, including devices offline during rollout
- `must-only-add-columns-in-sync-schemas`: no migration in a sync-capable schema removes or renames a column without a migration path
- `must-default-new-columns-in-sync-schemas`: every column a migration adds to a sync-capable schema has a DEFAULT value
- `must-test-migrations-from-every-version`: sync-capable migrations are tested against databases at every previous version
- `must-back-up-before-server-migration`: in a sync-capable schema, every server-side migration runs after a backup
- `should-flag-type-changes-for-manual-sql`: a declarative migration leaves column type changes and removals to manual SQL, or the code says why not

