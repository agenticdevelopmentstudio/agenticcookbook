
```sql
BEGIN;              -- same as BEGIN DEFERRED
BEGIN DEFERRED;     -- default: acquire locks lazily
BEGIN IMMEDIATE;    -- acquire write lock at BEGIN time
BEGIN EXCLUSIVE;    -- exclusive lock (equivalent to IMMEDIATE in WAL mode)
```

**DEFERRED** acquires no lock until first access. The first write statement then attempts to upgrade from a read lock to a write lock. If another writer is active, this upgrade fails immediately — `busy_timeout` does NOT apply to lock upgrades in DEFERRED mode. Work done before the failed upgrade is lost and must be retried.

**IMMEDIATE** acquires the write lock at `BEGIN` time. If another writer is active, SQLite waits up to `busy_timeout` milliseconds before returning `SQLITE_BUSY`. Benchmarks show approximately 2x better throughput than DEFERRED for write-heavy workloads.

MUST use `BEGIN IMMEDIATE` for any transaction that will write. It fails fast at `BEGIN` time rather than mid-transaction after work has been done.

```sql
-- Correct pattern for write transactions
BEGIN IMMEDIATE;
INSERT INTO tasks ...;
UPDATE tasks SET ...;
COMMIT;
```

