
Soft-delete tombstones and sync outbox entries accumulate without a purge strategy. Define retention windows from the start.

```sql
-- Purge synced tombstones older than 90 days
DELETE FROM tasks_tombstones
WHERE synced = 1
  AND deleted_at < strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '-90 days');

-- Purge completed outbox entries older than 7 days
DELETE FROM outbox
WHERE status = 'done'
  AND created_at < strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '-7 days');
```

Only purge tombstones after confirming all sync targets have consumed them. Purging too early causes deleted records to reappear on devices that haven't synced yet.

After large purges, run `PRAGMA incremental_vacuum` to reclaim the freed pages.

