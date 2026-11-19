
- `must-join-correlated-subqueries`: no correlated scalar subquery in a SELECT list is the bottleneck; each such subquery is a JOIN (no `CORRELATED SCALAR SUBQUERY` on a slow path in `EXPLAIN QUERY PLAN`)
- `must-not-wrap-indexed-filter-columns`: no WHERE clause applies a function to an indexed column unless an expression index matching that call exists
- `should-select-only-needed-columns`: each query selects only the columns its caller uses, or says why it does not
- `must-use-not-exists-over-not-in`: no `NOT IN` takes a subquery; each is `NOT EXISTS`
- `should-use-ctes-for-clarity`: queries that a CTE makes clearer use one, or say why they do not
- `should-replace-materialized-ctes`: no CTE shows as `MATERIALIZE` in `EXPLAIN QUERY PLAN` while causing a performance problem, unless the code says why it stays
- `should-optimize-on-connection-open`: each long-lived connection runs `PRAGMA optimize` when it opens, or the code says why not
- `should-analyze-after-bulk-changes`: `ANALYZE` runs after each bulk insert or major schema change, or the code says why not
- `must-check-query-plan-before-shipping`: every new query that touches a large table had its `EXPLAIN QUERY PLAN` checked before it shipped
- `should-analyze-before-evaluating-plans`: every query plan used to judge a query was taken after `ANALYZE` (or `PRAGMA optimize`) on real data, or the code says why not
- `should-investigate-scans`: every `SCAN` in a plan for a non-trivial table was checked for an applicable index, or the code says why not
- `should-check-for-materialize`: where a FROM-clause subquery is expected to be flattened, its `EXPLAIN QUERY PLAN` output was checked for `MATERIALIZE`, or the code says why not
- `should-use-union-all`: every `UNION` combines result sets that may overlap and must be deduplicated; otherwise it is `UNION ALL`, or the code says why not
- `should-index-both-sides-of-or`: every OR across columns has an index on each column (`MULTI-INDEX OR`) or is a `UNION ALL`, or the code says why not

