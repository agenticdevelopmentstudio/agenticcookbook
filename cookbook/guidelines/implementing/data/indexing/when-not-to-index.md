
Every index is maintained on every INSERT, UPDATE, and DELETE. The number of indexes on a table is the dominant factor for insert performance — heavily indexed tables can see 5x slower inserts.

**SHOULD NOT index:**
- Columns that are never in a WHERE, JOIN, or ORDER BY clause.
- Low-cardinality columns (e.g., a boolean `is_active` on a table where 99% of rows are active) — a full table scan is often faster.
- Tables that are write-only or insert-heavy with infrequent reads.

Run `PRAGMA optimize` periodically to keep query planner statistics current. Monitor with `SELECT * FROM sqlite_stat1;` (populated by `ANALYZE`) to see which indexes the planner is actually using.

