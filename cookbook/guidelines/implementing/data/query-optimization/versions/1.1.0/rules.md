
- **must-join-correlated-subqueries**: MUST rewrite correlated scalar subqueries in SELECT lists as JOINs when the subquery is the bottleneck. The planner labels these `CORRELATED SCALAR SUBQUERY` in EXPLAIN output.
- **must-not-wrap-indexed-filter-columns**: MUST NOT apply functions to indexed filter columns unless a matching expression index exists.
- **should-select-only-needed-columns**: SHOULD select only the columns the caller needs.
- **must-use-not-exists-over-not-in**: MUST use `NOT EXISTS` instead of `NOT IN` with subqueries.
- **should-use-ctes-for-clarity**: SHOULD use CTEs for clarity.
- **should-replace-materialized-ctes**: SHOULD switch to subqueries if `EXPLAIN QUERY PLAN` shows the CTE is being materialized and causing a performance problem.
- **should-optimize-on-connection-open**: SHOULD run `PRAGMA optimize` on connection open for long-lived connections.
- **should-analyze-after-bulk-changes**: SHOULD run `ANALYZE` after bulk inserts or major schema changes.
- **must-check-query-plan-before-shipping**: MUST always check the query plan before shipping a new query that touches large tables.
- **should-analyze-before-evaluating-plans**: SHOULD run `ANALYZE` (or `PRAGMA optimize`) before evaluating plans on tables with real data.
- **should-investigate-scans**: When the plan shows `SCAN` (a full table scan), SHOULD investigate whether an index applies.
- **should-check-for-materialize**: SHOULD check `MATERIALIZE` in EXPLAIN output to see when subquery flattening does not apply.
- **should-use-union-all**: SHOULD use `UNION ALL` when the result sets are known to be disjoint, or when duplicates are acceptable.
- **should-index-both-sides-of-or**: For OR conditions across columns, SHOULD either index both columns or restructure as a `UNION ALL`.

