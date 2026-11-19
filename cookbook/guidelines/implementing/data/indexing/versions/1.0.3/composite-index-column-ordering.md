
Column order in a multi-column index is not arbitrary. The query planner can only use a composite index from its left prefix — gaps break the chain.

**MUST follow:**
- Equality columns (`=`, `IN`, `IS`) go first.
- Inequality columns (`<`, `>`, `<=`, `>=`, `BETWEEN`) go last — only the rightmost used column can use a range constraint.
- Columns to the right of an inequality are not used for filtering.

```sql
-- Given: CREATE INDEX idx_a_b_c ON t(a, b, c);
WHERE a = 1 AND b = 2 AND c > 3   -- uses all 3 columns
WHERE a = 1 AND b > 2             -- uses a and b only
WHERE b = 2                        -- cannot use this index (no left prefix)
```

**MUST NOT** create an index that is a prefix of an existing index. If you have `(a, b, c)`, you do not need separate indexes on `(a)` or `(a, b)`. Redundant indexes waste write budget with no read benefit.

