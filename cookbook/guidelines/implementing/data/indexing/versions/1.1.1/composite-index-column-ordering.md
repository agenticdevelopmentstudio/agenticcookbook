
Column order in a multi-column index is not arbitrary. The query planner can only use a composite index from its left prefix — gaps break the chain.

```sql
-- Given: CREATE INDEX idx_a_b_c ON t(a, b, c);
WHERE a = 1 AND b = 2 AND c > 3   -- uses all 3 columns
WHERE a = 1 AND b > 2             -- uses a and b only
WHERE b = 2                        -- cannot use this index (no left prefix)
```

