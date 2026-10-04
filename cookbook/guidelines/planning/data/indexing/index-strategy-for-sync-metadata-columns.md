
Sync queries follow predictable patterns. Index for them explicitly.

```sql
-- Find unsynced records (the most important sync query)
CREATE INDEX idx_tasks_sync_status ON tasks(last_synced_at, updated_at)
  WHERE last_synced_at IS NULL OR updated_at > last_synced_at;

-- Change log: unsynced changes only
CREATE INDEX idx_changelog_unsynced ON change_log(synced, changed_at)
  WHERE synced = 0;

-- Soft-delete filter (nearly every query excludes deleted rows)
CREATE INDEX idx_tasks_active ON tasks(updated_at)
  WHERE is_deleted = 0;
```

Always verify with `EXPLAIN QUERY PLAN` that sync queries show `SEARCH ... USING INDEX`, not `SCAN`.

