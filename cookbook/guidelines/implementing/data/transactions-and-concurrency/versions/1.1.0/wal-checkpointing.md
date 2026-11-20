
WAL content must be periodically transferred back to the main database file. By default, SQLite checkpoints automatically when the WAL reaches 1,000 pages.

```sql
PRAGMA wal_checkpoint(PASSIVE);   -- non-blocking; checkpoints what it can
PRAGMA wal_checkpoint(FULL);      -- blocks new writers until complete
PRAGMA wal_checkpoint(TRUNCATE);  -- blocks briefly; resets WAL to zero bytes
```

Capping WAL file size prevents unbounded growth:

```sql
PRAGMA journal_size_limit = 6144000;  -- limit WAL to ~6MB
```

