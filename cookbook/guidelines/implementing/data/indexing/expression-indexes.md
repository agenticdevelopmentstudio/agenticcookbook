
Index the result of a deterministic expression rather than a raw column.

```sql
CREATE INDEX idx_upper_last ON employees(UPPER(last_name));
CREATE INDEX idx_event_date ON events(date(created_at));
```

**MUST:** The expression in the query must match the index definition exactly — the planner does no algebra.

```sql
-- Given: CREATE INDEX idx_xy ON t(x + y);
WHERE x + y > 10   -- uses the index
WHERE y + x > 10   -- does NOT use the index (operand order differs)
```

**Restrictions:** Only deterministic functions, no subqueries, only columns from the indexed table. Expression indexes require SQLite 3.9.0+.

