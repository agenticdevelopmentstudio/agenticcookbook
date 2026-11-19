
The query planner signals missing index opportunities in `EXPLAIN QUERY PLAN` output:

```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 42;
```

Signals to act on:
- `SCAN orders` — full table scan; an index on `customer_id` would help
- `AUTOMATIC INDEX` — SQLite built a temporary index at query time; a permanent index would be faster
- `USE TEMP B-TREE FOR ORDER BY` — the sort is happening in memory; an index on the ORDER BY columns may eliminate it
- `CORRELATED SCALAR SUBQUERY` — runs per outer row; restructure as a JOIN

```sql
-- Enable automatic query plan output in the CLI during development
.eqp on
```

Also monitor `sqlite_stat1` after running `ANALYZE` to see actual row counts per index. If an index covers a column with very low cardinality on a large table, it may not help — the planner may prefer a full scan.

