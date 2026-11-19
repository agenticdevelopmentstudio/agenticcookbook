
- **must-base-schema-on-query-patterns**: Schema and index decisions MUST follow from actual query patterns, not from assumptions about what might be queried. Before adding a column, index, or table, identify the queries that will use it and verify the design supports them efficiently.
- **must-answer-access-questions-before-schema**: MUST answer these questions before finalizing any schema:
  1. What are the most frequent queries? What columns appear in WHERE, JOIN, and ORDER BY?
  2. What are the most expensive queries? (Use `EXPLAIN QUERY PLAN` and `ANALYZE`.)
  3. Is this table read-heavy or write-heavy? What is the read-to-write ratio?
  4. Are reads latency-sensitive (user-facing) or throughput-sensitive (background batch)?
  5. What is the expected row count — today and at 10x scale?
- **must-not-add-speculative-indexes**: MUST NOT add an index speculatively.
- **should-maintain-query-inventory**: SHOULD maintain a query inventory: a list of the significant queries for each table, their frequency, and which columns they filter on.
- **should-verify-indexes-against-query-inventory**: SHOULD use the query inventory to verify that every index earns its place, and that every frequent query has index support.
- **should-order-composite-columns-by-query-pattern**: Column order in composite indexes SHOULD follow query patterns: equality filters (`=`, `IN`) first; range filters (`<`, `>`, `BETWEEN`) last; ORDER BY columns last when the query has no range filter.
- **should-add-covering-indexes-on-read-heavy-tables**: On read-heavy tables, SHOULD add covering indexes for the hottest queries — eliminate table lookups entirely.
- **should-keep-read-heavy-working-set-in-memory**: On read-heavy tables, SHOULD use `mmap_size` and a larger `cache_size` to keep working set in memory.
- **should-select-specific-columns**: On read-heavy tables, SHOULD prefer `SELECT` with specific columns over `SELECT *` to maximize covering index usage.
- **should-run-analyze-regularly**: On read-heavy tables, SHOULD run `ANALYZE` regularly to keep query planner statistics current.
- **should-minimize-indexes-on-write-heavy-tables**: On write-heavy tables, SHOULD minimize the number of indexes — each index adds overhead to every INSERT, UPDATE, and DELETE.
- **should-use-partial-indexes-on-write-heavy-tables**: On write-heavy tables, SHOULD use partial indexes to limit index size to the rows that matter.
- **should-batch-writes-in-transactions**: On write-heavy tables, SHOULD batch writes in explicit transactions (100–1,000 rows per transaction for general use).
- **should-profile-before-indexing-mixed-tables**: On mixed workload tables, SHOULD profile the actual read/write ratio before adding indexes, and add additional indexes only when profiling confirms they are needed.
- **should-act-on-missing-index-signals**: When `EXPLAIN QUERY PLAN` shows `SCAN` (full table scan), `AUTOMATIC INDEX` (a temporary index built at query time) or `USE TEMP B-TREE FOR ORDER BY` (an in-memory sort), SHOULD act on the signal: a permanent index on the filtered or ORDER BY columns may help.
- **should-restructure-correlated-subqueries-as-joins**: When `EXPLAIN QUERY PLAN` shows `CORRELATED SCALAR SUBQUERY` (runs per outer row), SHOULD restructure it as a JOIN.
- **should-monitor-sqlite-stat1**: SHOULD monitor `sqlite_stat1` after running `ANALYZE` to see actual row counts per index.
- **should-design-for-sync-query-shapes**: Sync workloads have predictable query shapes; SHOULD design for them explicitly.
- **must-index-unsynced-record-query**: The unsynced-record query ("what changed since the last sync?", run on every sync cycle) MUST have an index that covers it.
- **should-verify-unsynced-query-uses-index**: SHOULD verify with `EXPLAIN QUERY PLAN` that the unsynced-record query shows `SEARCH ... USING INDEX`, not `SCAN`.
- **should-partial-index-outbox-and-change-log-tables**: Outbox and change-log tables SHOULD have partial indexes on the filter condition.
- **should-account-for-soft-delete-in-indexes**: Index design SHOULD account for the soft-delete filter: if most queries filter `WHERE is_deleted = 0`, include `is_deleted` in composite indexes or use a partial index on the active subset.
- **should-size-sync-batches-by-context**: Sync batch sizes SHOULD follow the recommended size for their context: mobile (unstable network) 50–100 records, desktop (stable network) 500–1,000, initial bootstrap 1,000–5,000, background sync 100–500.
- **must-wrap-sync-batch-in-one-transaction**: MUST wrap each sync batch in a single transaction.
- **should-use-json-bulk-operations-for-bulk-ingestion**: For bulk ingestion (initial sync or large imports), SHOULD use JSON bulk operations to avoid SQLite's per-statement parameter limit and reduce round-trips.
- **must-begin-immediate-for-sync-writes**: MUST use `BEGIN IMMEDIATE` for sync write transactions (not `BEGIN DEFERRED`).
- **must-not-hold-write-lock-during-network-io**: MUST NOT hold the write lock open while waiting for network responses.
- **should-separate-sync-write-and-ui-read-connections**: Sync SHOULD use one dedicated write connection for sync writes and separate read connections for UI queries that run during sync.
- **should-set-busy-timeout-on-all-connections**: SHOULD set `busy_timeout = 5000` on all connections to absorb brief contention without returning errors.

