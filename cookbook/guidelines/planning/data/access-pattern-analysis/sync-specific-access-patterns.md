
Sync workloads have predictable query shapes. Design for them explicitly.

### Unsynced record queries

The most critical sync query: "what changed since the last sync?"

```sql
SELECT * FROM tasks
WHERE last_synced_at IS NULL
   OR updated_at > last_synced_at;
```

This query runs on every sync cycle. MUST have an index that covers it:

```sql
CREATE INDEX idx_tasks_sync_status ON tasks(last_synced_at, updated_at)
  WHERE last_synced_at IS NULL OR updated_at > last_synced_at;
```

Verify with `EXPLAIN QUERY PLAN` that this shows `SEARCH ... USING INDEX`, not `SCAN`.

### Outbox and change log queries

```sql
-- Outbox: pending entries to upload
SELECT * FROM outbox WHERE status = 'pending' ORDER BY next_attempt_at;

-- Change log: unsynced entries
SELECT * FROM change_log WHERE synced = 0 ORDER BY changed_at;
```

Both benefit from partial indexes on the filter condition:

```sql
CREATE INDEX idx_outbox_pending ON outbox(status, next_attempt_at)
  WHERE status = 'pending';

CREATE INDEX idx_changelog_unsynced ON change_log(synced, changed_at)
  WHERE synced = 0;
```

Partial indexes remain small even as the underlying table grows, because they only index the rows still in the active state.

### Soft-delete filter

Nearly every application query excludes deleted rows. Account for this in index design:

```sql
-- If most queries filter WHERE is_deleted = 0, include is_deleted in composite indexes
-- OR use a partial index on the active subset
CREATE INDEX idx_tasks_active_status ON tasks(status, created_date)
  WHERE is_deleted = 0;
```

