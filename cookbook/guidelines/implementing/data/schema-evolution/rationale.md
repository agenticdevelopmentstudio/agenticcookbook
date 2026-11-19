
- `must-track-schema-version-with-user-version`: It is a built-in 32-bit integer stored in the database file header — available immediately without querying any table.
- `must-only-add-columns-in-sync-schemas`: A device on the old schema must be able to sync with the server on the new schema.
- `must-default-new-columns-in-sync-schemas`: CRDTs and merge logic require all columns to have a known value for all rows, including those written before the migration.
- `must-make-migrations-idempotent`: A device may apply the same migration more than once if it reconnects after a partial sync.
- `must-wrap-each-migration-in-transaction`: A failed migration must leave the database unchanged.
- `must-test-migrations-from-every-version`: An offline device may skip multiple versions and apply them in sequence on reconnect.

