
Index only the rows a query actually touches. A partial index is smaller, faster to write through, and can enforce conditional uniqueness.

```sql
-- Index only pending outbox rows (the ones that matter for queries)
CREATE INDEX idx_outbox_pending ON outbox(status, next_attempt_at)
  WHERE status = 'pending';

-- Conditional uniqueness: only one team leader per team
CREATE UNIQUE INDEX idx_team_leader ON person(team_id)
  WHERE is_team_leader;
```

Partial indexes require SQLite 3.8.0+. Databases with partial indexes cannot be read by older SQLite versions.

