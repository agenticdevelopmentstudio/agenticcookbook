
Run `EXPLAIN QUERY PLAN` on any new query touching large tables. Flag these in review:

- `SCAN` — full table scan; needs an index
- `USE TEMP B-TREE FOR ORDER BY` — missing index on ORDER BY columns
- `AUTOMATIC INDEX` — SQLite created a temporary index; needs a permanent one
- `CORRELATED SCALAR SUBQUERY` — executes once per outer row; rewrite as JOIN
- `MATERIALIZE` — CTE materialized when a subquery would allow index use

