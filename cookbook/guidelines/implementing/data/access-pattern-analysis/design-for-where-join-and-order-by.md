
A column belongs in an index if and only if queries will filter, join, or sort on it.

```sql
-- Before creating this index, confirm: which queries use status and created_date together?
CREATE INDEX idx_orders_status_date ON orders(status, created_date DESC);
```

**Column order in composite indexes follows query patterns:**
- Equality filters (`=`, `IN`) go first
- Range filters (`<`, `>`, `BETWEEN`) go last
- ORDER BY columns go last when the query has no range filter, enabling index-ordered scans that eliminate sort steps

