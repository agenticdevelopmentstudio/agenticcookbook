
Always check the query plan before shipping a new query that touches large tables.

```sql
EXPLAIN QUERY PLAN
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'active'
ORDER BY o.created_date DESC;
```

What each term means:
- `SCAN` — full table scan; investigate whether an index applies
- `SEARCH USING INDEX` — index-assisted lookup
- `SEARCH USING COVERING INDEX` — no table lookup needed (best outcome)
- `USE TEMP B-TREE FOR ORDER BY` — a sort step runs after the query; an index on the ORDER BY columns may eliminate it
- `AUTOMATIC INDEX` — SQLite built a temporary index at runtime; a permanent index would help
- `CORRELATED SCALAR SUBQUERY` — the subquery executes once per outer row; rewrite as a JOIN
- `MATERIALIZE` — subquery result stored in a temp table; may be avoidable
- `CO-ROUTINE` — subquery yields rows on demand; generally fine

Run `ANALYZE` (or `PRAGMA optimize`) before evaluating plans on tables with real data. Without statistics, the planner uses heuristics that may not reflect actual row counts.

