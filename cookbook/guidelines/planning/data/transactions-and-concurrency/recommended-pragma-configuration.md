
Set these on every new connection:

```sql
PRAGMA journal_mode = WAL;       -- concurrent reads + fast sequential writes
PRAGMA synchronous = NORMAL;     -- safe in WAL mode; only checkpoints fsync
PRAGMA cache_size = -64000;      -- 64MB page cache (negative value = KB)
PRAGMA mmap_size = 268435456;    -- 256MB memory-mapped I/O
PRAGMA temp_store = MEMORY;      -- temp tables and indexes in RAM
PRAGMA busy_timeout = 5000;      -- wait 5s on lock contention
PRAGMA foreign_keys = ON;        -- enforce referential integrity
PRAGMA optimize = 0x10002;       -- update query planner stats (long-lived connections)
```

**synchronous = NORMAL** in WAL mode: checkpoints fsync to disk, but individual commits do not. This is safe against application crashes. The only risk is a committed transaction rolling back on sudden power loss — acceptable for most use cases.

**cache_size** is session-only; it resets on each connection. 64MB is a good starting point for applications with larger working sets.

**mmap_size** enables memory-mapped I/O, reducing syscall overhead on read-heavy workloads. On 64-bit systems, setting this to the expected database size reserves virtual address space without consuming physical RAM.

