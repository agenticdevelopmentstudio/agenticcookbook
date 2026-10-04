
MUST use `EXPLAIN QUERY PLAN` to validate index usage before deploying schema changes.

```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 42;
```

Key output terms:
- `SCAN table` — full table scan; check whether an index would help
- `SEARCH table USING INDEX` — index-assisted lookup
- `SEARCH table USING COVERING INDEX` — no table lookup needed (best)
- `USE TEMP B-TREE FOR ORDER BY` — a sort step is required; an index on the ORDER BY columns may eliminate it
- `AUTOMATIC INDEX` — SQLite created a temporary index; a permanent index would help
- `CORRELATED SCALAR SUBQUERY` — runs once per outer row; rewrite as a JOIN

Enable automatic query plan output in the SQLite CLI: `.eqp on`.

