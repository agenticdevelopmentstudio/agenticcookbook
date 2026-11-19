
SHOULD start with `isDirty` flag columns — simple, low overhead, works everywhere:

```sql
-- Set on every local INSERT/UPDATE
UPDATE tasks SET is_dirty = 1, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
WHERE id = ?;

-- Clear after successful sync
UPDATE tasks SET is_dirty = 0, last_synced_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
WHERE id IN (...);
```

Upgrade to a **change-log table** (populated via triggers) only if you need operation-type awareness (INSERT vs UPDATE vs DELETE) or ordered change history for field-level merge.

Upgrade to an **edit operations table** (field-level deltas with timestamps and device IDs) only if the server needs to perform three-way field merges.

