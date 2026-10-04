
MUST use incremental sync in production. Full sync (transfer everything every time) is only acceptable for initial bootstrap or recovery after database corruption.

Incremental sync using a version number (preferred over timestamp-based):

```sql
-- Client pulls: "give me everything after version 42"
SELECT id, title, status, updated_at, version, is_deleted, sync_version
FROM tasks
WHERE sync_version > 42
ORDER BY sync_version ASC
LIMIT 100;
-- Response includes the max sync_version in the batch
-- Client stores that as the checkpoint for the next pull
```

Timestamp-based delta sync is simpler but vulnerable to clock skew. If using timestamps, use Hybrid Logical Clocks (HLC) rather than wall-clock time.

