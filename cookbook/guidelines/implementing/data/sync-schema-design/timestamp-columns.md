
Every synced table MUST have three timestamp columns:

| Column | Purpose |
|--------|---------|
| `created_at` | Record creation time (set once, never updated) |
| `updated_at` | Last modification time (updated on every change) |
| `last_synced_at` | Last successful server sync (NULL until first sync) |

Store all timestamps as **ISO-8601 UTC strings** in SQLite (`TEXT`), and as `TIMESTAMPTZ` in PostgreSQL. Never mix formats within a column.

Use a trigger to keep `updated_at` current automatically:

```sql
CREATE TRIGGER tasks_update_timestamp
AFTER UPDATE ON tasks
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE tasks SET updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
    WHERE id = NEW.id;
END;
```

Detect unsynced records with:

```sql
SELECT * FROM tasks
WHERE last_synced_at IS NULL
   OR updated_at > last_synced_at;
```

