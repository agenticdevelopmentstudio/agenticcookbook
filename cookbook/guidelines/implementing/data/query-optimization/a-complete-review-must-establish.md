
- `EXPLAIN QUERY PLAN` was run on every new query touching large tables; no `SCAN` (full table scan) left unaddressed by an index
- No `USE TEMP B-TREE FOR ORDER BY` in the plan — ORDER BY columns are indexed
- No `AUTOMATIC INDEX` in the plan — a permanent index is added where SQLite would otherwise build a temporary one
- No `CORRELATED SCALAR SUBQUERY` in the plan — such subqueries are rewritten as JOINs
- No `MATERIALIZE` where a subquery would permit index use instead of materializing a CTE
- No correlated subqueries in SELECT where a JOIN would serve
- No functions applied to indexed columns in WHERE (e.g., `WHERE date(col) = '...'`); range comparisons are used instead
- `UNION ALL` is used in place of `UNION` wherever deduplication is not required
- No `SELECT *`; queries select only the needed columns so covering indexes can apply
- No `NOT IN` with a subquery that may return NULL; `NOT EXISTS` is used instead
- No `OR` across columns unless both sides are indexed

