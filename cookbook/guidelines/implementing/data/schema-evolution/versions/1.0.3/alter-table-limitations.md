
SQLite's ALTER TABLE is severely limited. It supports:

- `ALTER TABLE x RENAME TO y`
- `ALTER TABLE x ADD COLUMN y` — column must allow NULL or have a DEFAULT
- `ALTER TABLE x RENAME COLUMN old TO new` (SQLite 3.25.0+)
- `ALTER TABLE x DROP COLUMN y` (SQLite 3.35.0+)

It does NOT support: changing column types, adding/removing constraints, changing DEFAULT values, or reordering columns.

**Backwards-compatible changes (safe to do directly):**

```sql
-- Add a nullable column
ALTER TABLE tasks ADD COLUMN priority TEXT;

-- Add a column with a default
ALTER TABLE tasks ADD COLUMN is_flagged INTEGER NOT NULL DEFAULT 0;

-- Create a new index
CREATE INDEX ix_tasks_priority ON tasks(priority);

-- Rename a column (SQLite 3.25.0+)
ALTER TABLE tasks RENAME COLUMN content TO description;
```

