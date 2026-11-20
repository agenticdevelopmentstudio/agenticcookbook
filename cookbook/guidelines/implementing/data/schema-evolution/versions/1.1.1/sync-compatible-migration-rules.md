
**Migration tracking table (alternative to pragma for sync contexts):**

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    applied_date  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
```

Using a table instead of `PRAGMA user_version` allows the migration history to be synced to the server, giving visibility into which migrations each device has applied.

