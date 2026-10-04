
MUST enable WAL mode on every SQLite database that participates in sync:

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;  -- safe for app crashes; use FULL only for power-loss safety
PRAGMA busy_timeout = 5000;   -- wait up to 5s instead of returning SQLITE_BUSY immediately
```

WAL mode enables concurrent readers and writers: readers never block writers, writers never block readers. This is essential for offline-first apps where the sync worker writes in the background while the UI reads. With the default rollback journal, a background write locks the entire database and freezes the UI.

SHOULD use one writer connection (writes serialized via an application-level queue) and multiple reader connections. Never hold a write transaction open while waiting on network I/O.

