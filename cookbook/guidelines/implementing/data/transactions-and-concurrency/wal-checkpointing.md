
WAL content must be periodically transferred back to the main database file. By default, SQLite checkpoints automatically when the WAL reaches 1,000 pages.

```sql
PRAGMA wal_checkpoint(PASSIVE);   -- non-blocking; checkpoints what it can
PRAGMA wal_checkpoint(FULL);      -- blocks new writers until complete
PRAGMA wal_checkpoint(TRUNCATE);  -- blocks briefly; resets WAL to zero bytes
```

SHOULD run `PRAGMA wal_checkpoint(PASSIVE)` periodically during normal operation. After large sync batches, use `TRUNCATE` to reclaim WAL disk space.

SHOULD cap WAL file size to prevent unbounded growth:

```sql
PRAGMA journal_size_limit = 6144000;  -- limit WAL to ~6MB
```

Three causes of WAL growth to avoid:
1. Auto-checkpointing disabled without a manual replacement
2. Long-running read transactions that prevent checkpoint completion
3. Very large write transactions that block the checkpoint

Run checkpoints in a separate thread or connection so they do not block foreground reads.

