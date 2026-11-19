
Local SQLite databases grow unbounded without maintenance. Sync metadata — outbox entries, change logs, tombstones — accumulates fastest.

Prune on a schedule (e.g., on app launch or after sync completes):

```sql
-- Purge completed outbox entries older than 7 days
DELETE FROM outbox
WHERE status = 'done'
  AND created_at < strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '-7 days');

-- Purge synced change log entries older than 30 days
DELETE FROM change_log
WHERE synced = 1
  AND changed_at < strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '-30 days');

-- Hard-delete confirmed tombstones older than 90 days
DELETE FROM tasks
WHERE is_deleted = 1
  AND last_synced_at IS NOT NULL
  AND updated_at < strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '-90 days');
```

After significant deletions, reclaim disk space with incremental vacuum (less disruptive than full VACUUM):

```sql
-- Check space before deciding
SELECT page_count * page_size AS total_bytes,
       freelist_count * page_size AS free_bytes
FROM pragma_page_count(), pragma_page_size(), pragma_freelist_count();

-- Gradual reclamation (does not lock the database for long)
PRAGMA incremental_vacuum(500);  -- free up to 500 pages
```

SHOULD trigger a full sync (not delta) if `last_full_sync` is older than a threshold (e.g., 7 days), to catch any gaps from previous sync failures.

