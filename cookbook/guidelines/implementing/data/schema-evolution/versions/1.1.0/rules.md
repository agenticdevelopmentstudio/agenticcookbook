
- **must-track-schema-version-with-user-version**: MUST use `PRAGMA user_version` to track schema version.
- **must-end-migration-file-with-user-version**: Each migration file MUST end with the appropriate `PRAGMA user_version = N;` statement.
- **must-wrap-each-migration-in-transaction**: Each migration MUST be wrapped in a transaction.
- **must-make-migrations-idempotent**: Each migration MUST be idempotent (safe to run twice).
- **must-add-columns-nullable-or-defaulted**: A column added with `ALTER TABLE x ADD COLUMN y` MUST allow NULL or have a DEFAULT.
- **must-not-rename-column-below-3-25-0**: `ALTER TABLE x RENAME COLUMN old TO new` MUST NOT be used where the database must be migrated by SQLite older than 3.25.0; it requires SQLite 3.25.0+.
- **must-not-drop-column-below-3-35-0**: `ALTER TABLE x DROP COLUMN y` MUST NOT be used where the database must be migrated by SQLite older than 3.35.0; it requires SQLite 3.35.0+.
- **must-not-use-alter-table-for-unsupported-changes**: A migration MUST NOT rely on ALTER TABLE for changing column types, adding/removing constraints, changing DEFAULT values, or reordering columns; SQLite's ALTER TABLE does NOT support them.
- **must-disable-foreign-keys-during-recreate**: A table recreate MUST disable foreign keys before the recreate and re-enable them after.
- **must-run-foreign-key-check-before-commit**: A table recreate MUST run `foreign_key_check` before committing to catch any broken references.
- **must-recreate-dependent-objects**: A table recreate MUST recreate indexes, triggers, and views that referenced the old table.
- **must-keep-migrations-compatible-across-participants**: When SQLite databases sync with a server or between devices, schema migrations MUST be compatible across all participants — including devices that may be offline during rollout.
- **must-only-add-columns-in-sync-schemas**: A migration in a sync-capable schema MUST only add columns — never remove or rename without a migration path.
- **must-default-new-columns-in-sync-schemas**: In a sync-capable schema, new columns MUST have DEFAULT values.
- **must-test-migrations-from-every-version**: Migrations in a sync-capable schema MUST be tested against databases at every previous version.
- **must-back-up-before-server-migration**: In a sync-capable schema, MUST always back up before migrating on the server side.
- **should-flag-type-changes-for-manual-sql**: A declarative migration SHOULD flag column type changes or removals for manual SQL.

