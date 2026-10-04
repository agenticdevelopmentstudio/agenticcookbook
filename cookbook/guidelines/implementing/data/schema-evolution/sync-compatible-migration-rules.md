
When SQLite databases sync with a server or between devices, schema migrations must be compatible across all participants — including devices that may be offline during rollout.

MUST follow these rules for any migration in a sync-capable schema:

1. **Only add columns — never remove or rename without a migration path.** A device on the old schema must be able to sync with the server on the new schema.
2. **New columns MUST have DEFAULT values.** CRDTs and merge logic require all columns to have a known value for all rows, including those written before the migration.
3. **Migrations MUST be idempotent.** A device may apply the same migration more than once if it reconnects after a partial sync.
4. **Wrap each migration in a transaction.** A failed migration must leave the database unchanged.
5. **Test migrations against databases at every previous version.** An offline device may skip multiple versions and apply them in sequence on reconnect.
6. **Always back up before migrating on the server side.**

**Migration tracking table (alternative to pragma for sync contexts):**

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    applied_date  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
```

Using a table instead of `PRAGMA user_version` allows the migration history to be synced to the server, giving visibility into which migrations each device has applied.

