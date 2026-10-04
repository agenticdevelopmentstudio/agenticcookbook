
**Read-heavy tables** (lookups, reporting, list views):
- Add covering indexes for the hottest queries — eliminate table lookups entirely
- Use `mmap_size` and a larger `cache_size` to keep working set in memory
- Prefer `SELECT` with specific columns over `SELECT *` to maximize covering index usage
- Run `ANALYZE` regularly to keep query planner statistics current

**Write-heavy tables** (event logs, outboxes, audit trails, sync change logs):
- Minimize the number of indexes — each index adds overhead to every INSERT, UPDATE, and DELETE
- A heavily indexed table can sustain 5x slower inserts compared to the same table with no secondary indexes
- Use partial indexes to limit index size to the rows that matter
- Batch writes in explicit transactions (100–1,000 rows per transaction for general use)
- Append-only tables (insert but never update) may need no secondary indexes at all beyond the primary key

**Mixed workload tables** (the common case):
- Profile the actual read/write ratio before adding indexes
- One index on the most selective filter column often covers 80% of the read benefit
- Add additional indexes only when profiling confirms they are needed

