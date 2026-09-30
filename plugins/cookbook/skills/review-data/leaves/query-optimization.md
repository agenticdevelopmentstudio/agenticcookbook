<!-- leaf: review-data/query-optimization · source: guidelines/reviewing/data/query-optimization.md -->

# Query Optimization

When reviewing database queries, check EXPLAIN QUERY PLAN output and flag these anti-patterns.

## EXPLAIN QUERY PLAN red flags

Run `EXPLAIN QUERY PLAN` on any new query touching large tables. Flag these in review:

- `SCAN` — full table scan; needs an index
- `USE TEMP B-TREE FOR ORDER BY` — missing index on ORDER BY columns
- `AUTOMATIC INDEX` — SQLite created a temporary index; needs a permanent one
- `CORRELATED SCALAR SUBQUERY` — executes once per outer row; rewrite as JOIN
- `MATERIALIZE` — CTE materialized when a subquery would allow index use

## Anti-patterns to flag

1. **Correlated subqueries in SELECT** — rewrite as JOINs
2. **Functions on indexed columns in WHERE** — `WHERE date(col) = '...'` prevents index use; use range comparison instead
3. **UNION when UNION ALL suffices** — 60%+ slower due to unnecessary deduplication sort
4. **SELECT \*** — prevents covering index optimization; select only needed columns
5. **NOT IN with subqueries** — if the subquery returns any NULL, the entire result is empty. Use `NOT EXISTS` instead.
6. **OR without indexes on both sides** — causes full scan unless both columns are indexed

See the implementing copy of this guideline for detailed examples and fix patterns.
