
For structural changes (changing column types, adding constraints, removing columns on old SQLite, reordering):

```sql
BEGIN TRANSACTION;
PRAGMA foreign_keys = OFF;

-- 1. Create the new table with the desired schema
CREATE TABLE tasks_new (
    task_id  INTEGER PRIMARY KEY,
    title    TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'medium'  -- was nullable, now required
);

-- 2. Copy data, transforming as needed
INSERT INTO tasks_new (task_id, title, priority)
SELECT task_id, title, COALESCE(priority, 'medium') FROM tasks;

-- 3. Drop the old table
DROP TABLE tasks;

-- 4. Rename the new table
ALTER TABLE tasks_new RENAME TO tasks;

-- 5. Recreate indexes, triggers, and views that referenced the old table
CREATE INDEX ix_tasks_priority ON tasks(priority);

-- 6. Verify referential integrity
PRAGMA foreign_key_check;

PRAGMA foreign_keys = ON;
COMMIT;
```

**Critical:** Disable foreign keys before the recreate and re-enable after. Run `foreign_key_check` before committing to catch any broken references.

