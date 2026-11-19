
MUST NOT hard-delete records from synced tables. Hard deletes cannot be propagated — there is nothing left to sync.

Use `is_deleted INTEGER NOT NULL DEFAULT 0` (SQLite) / `is_deleted BOOLEAN NOT NULL DEFAULT FALSE` (PostgreSQL). All normal queries filter on `is_deleted = 0`; sync queries include deleted records.

```sql
-- Deletion
UPDATE tasks SET is_deleted = 1, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
WHERE id = ?;

-- Normal query
SELECT * FROM tasks WHERE is_deleted = 0;

-- Index to keep filtering fast
CREATE INDEX idx_tasks_is_deleted ON tasks(is_deleted);
```

For high-volume tables, a separate tombstone table keeps the live table lean:

```sql
CREATE TABLE tasks_tombstones (
    id          TEXT NOT NULL PRIMARY KEY,
    deleted_at  TEXT NOT NULL,
    synced      INTEGER NOT NULL DEFAULT 0
);

-- Purge tombstones confirmed synced to all devices
DELETE FROM tasks_tombstones
WHERE synced = 1
  AND deleted_at < strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '-90 days');
```

