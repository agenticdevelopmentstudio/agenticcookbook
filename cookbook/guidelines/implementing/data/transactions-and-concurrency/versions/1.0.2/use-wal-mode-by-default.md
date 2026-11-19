
MUST enable WAL mode for any application with concurrent reads, or where write latency matters.

```sql
PRAGMA journal_mode = WAL;
```

WAL (Write-Ahead Log) changes the write mechanism: instead of modifying the database file directly, SQLite appends changes to a separate `-wal` file. The original database stays intact until a checkpoint transfers changes back.

**Concurrency model:**
- Unlimited simultaneous readers
- One writer at a time
- Readers do not block writers; writers do not block readers
- Each reader sees a consistent snapshot from transaction start

**Performance advantages over rollback journal modes:**
- Writes are sequential (append-only), not random I/O
- Fewer `fsync()` calls — a COMMIT appends a commit record, no database-file fsync required
- With `synchronous = NORMAL`, per-transaction overhead drops from 30ms+ to under 1ms

**Limitations:**
- All processes must share the same physical machine (shared memory requirement)
- Cannot change `page_size` after enabling WAL
- Adds `-wal` and `-shm` files alongside the database
- Cannot use on network file systems

WAL mode persists in the database header — it survives reconnects. Set it once per database, but re-setting it on connection open is safe and recommended.

