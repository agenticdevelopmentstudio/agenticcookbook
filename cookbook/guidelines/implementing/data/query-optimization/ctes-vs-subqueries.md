
CTEs (`WITH` clauses) improve readability but have a performance tradeoff in SQLite.

- SQLite materializes CTEs referenced more than once (stores the result in a temp table). This prevents the planner from pushing WHERE predicates into the CTE.
- A subquery in a FROM clause may be flattened into the outer query, preserving index use on the underlying table.

```sql
-- CTE: readable but materialized; WHERE on the outer query does not push into it
WITH recent_orders AS (
  SELECT * FROM orders WHERE created_date > '2026-01-01'
)
SELECT * FROM recent_orders WHERE customer_id = 42;

-- Subquery: may be flattened; planner can use index on both conditions
SELECT * FROM (
  SELECT * FROM orders WHERE created_date > '2026-01-01'
) WHERE customer_id = 42;
```

SHOULD use CTEs for clarity. SHOULD switch to subqueries if `EXPLAIN QUERY PLAN` shows the CTE is being materialized and causing a performance problem.

