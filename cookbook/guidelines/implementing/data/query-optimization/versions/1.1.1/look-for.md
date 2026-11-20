
Run `EXPLAIN QUERY PLAN` on any new query touching large tables and flag the planner red flags: `SCAN` (full table scan that needs an index); `USE TEMP B-TREE FOR ORDER BY` (missing index on the ORDER BY columns); `AUTOMATIC INDEX` (SQLite built a throwaway index, so a permanent one is needed); `CORRELATED SCALAR SUBQUERY` (re-executes once per outer row — rewrite as a JOIN); and `MATERIALIZE` (a CTE got materialized where a subquery would have allowed index use). Beyond the plan, flag these query anti-patterns: correlated subqueries in SELECT (rewrite as JOINs); functions applied to indexed columns in WHERE such as `WHERE date(col) = '...'`, which defeats the index — use a range comparison instead; `UNION` where `UNION ALL` would suffice, since the unneeded deduplication sort runs 60%+ slower; `SELECT *`, which blocks covering-index optimization — select only the needed columns; `NOT IN` against a subquery, which returns an empty result if the subquery yields any NULL — use `NOT EXISTS` instead; and `OR` across columns that aren't both indexed, which forces a full scan unless an index exists on each side.

When reviewing database queries, check EXPLAIN QUERY PLAN output and flag these anti-patterns.

### EXPLAIN QUERY PLAN red flags

Run `EXPLAIN QUERY PLAN` on any new query touching large tables. Flag these in review:

- `SCAN` — full table scan; needs an index
- `USE TEMP B-TREE FOR ORDER BY` — missing index on ORDER BY columns
- `AUTOMATIC INDEX` — SQLite created a temporary index; needs a permanent one
- `CORRELATED SCALAR SUBQUERY` — executes once per outer row; rewrite as JOIN
- `MATERIALIZE` — CTE materialized when a subquery would allow index use

### Anti-patterns to flag

1. **Correlated subqueries in SELECT** — rewrite as JOINs
2. **Functions on indexed columns in WHERE** — `WHERE date(col) = '...'` prevents index use; use range comparison instead
3. **UNION when UNION ALL suffices** — 60%+ slower due to unnecessary deduplication sort
4. **SELECT \*** — prevents covering index optimization; select only needed columns
5. **NOT IN with subqueries** — if the subquery returns any NULL, the entire result is empty. Use `NOT EXISTS` instead.
6. **OR without indexes on both sides** — causes full scan unless both columns are indexed

