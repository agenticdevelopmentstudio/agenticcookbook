
### Correlated subqueries instead of JOINs

```sql
-- BAD: subquery runs once per order row
SELECT o.id,
  (SELECT name FROM customers WHERE id = o.customer_id) AS customer_name
FROM orders o;

-- GOOD: single join
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id;
```

MUST rewrite correlated scalar subqueries in SELECT lists as JOINs when the subquery is the bottleneck. The planner labels these `CORRELATED SCALAR SUBQUERY` in EXPLAIN output.

### Functions on indexed columns in WHERE

Wrapping an indexed column in a function prevents index use.

```sql
-- BAD: index on created_date is not used
WHERE date(created_date) = '2024-01-15'

-- GOOD: index is used
WHERE created_date >= '2024-01-15' AND created_date < '2024-01-16'

-- ALTERNATIVE: create an expression index to match the function call
CREATE INDEX idx_date ON orders(date(created_date));
```

MUST NOT apply functions to indexed filter columns unless a matching expression index exists.

### UNION when UNION ALL suffices

```sql
-- BAD: sorts all rows to deduplicate (often unnecessary)
SELECT id FROM active_users
UNION
SELECT id FROM archived_users;

-- GOOD: appends results directly
SELECT id FROM active_users
UNION ALL
SELECT id FROM archived_users;
```

Use `UNION ALL` when the result sets are known to be disjoint, or when duplicates are acceptable. `UNION` can be 60%+ slower on large datasets due to the sort and deduplication pass.

### SELECT * when specific columns suffice

```sql
-- BAD: fetches all columns, prevents covering index optimization
SELECT * FROM orders WHERE status = 'active';

-- GOOD: may use a covering index
SELECT id, customer_id FROM orders WHERE status = 'active';
```

SHOULD select only the columns the caller needs. This enables covering index optimization and reduces data transfer.

### NOT IN with subqueries (NULL hazard)

```sql
-- DANGEROUS: if the subquery returns any NULL, NOT IN evaluates to NULL,
-- returning zero rows regardless of other values
SELECT * FROM orders WHERE customer_id NOT IN (SELECT id FROM inactive_customers);

-- SAFE: NOT EXISTS handles NULLs correctly
SELECT * FROM orders o
WHERE NOT EXISTS (
  SELECT 1 FROM inactive_customers ic WHERE ic.id = o.customer_id
);
```

MUST use `NOT EXISTS` instead of `NOT IN` with subqueries. The NULL behavior of `NOT IN` causes silent data loss.

### OR conditions without indexes on both sides

```sql
-- Potentially slow without indexes on both columns
WHERE status = 'active' OR priority > 5
```

SQLite uses `MULTI-INDEX OR` if both columns are indexed independently. Without indexes on both columns, it falls back to a full scan. Either index both columns or restructure as a `UNION ALL`.

