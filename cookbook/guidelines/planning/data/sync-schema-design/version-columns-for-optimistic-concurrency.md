
MUST add a `version INTEGER NOT NULL DEFAULT 1` column to every synced table. The version column is the authoritative signal for conflict detection.

On update: increment the version. On sync, the server applies the write only if the client's base version matches the server's current version. A mismatch signals a conflict.

```sql
UPDATE tasks
SET title = ?, version = version + 1, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
WHERE id = ? AND version = ?;
-- Check sqlite3_changes() == 1. If 0, conflict occurred.
```

