
```sql
-- Set on every local INSERT/UPDATE
UPDATE tasks SET is_dirty = 1, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
WHERE id = ?;

-- Clear after successful sync
UPDATE tasks SET is_dirty = 0, last_synced_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
WHERE id IN (...);
```

