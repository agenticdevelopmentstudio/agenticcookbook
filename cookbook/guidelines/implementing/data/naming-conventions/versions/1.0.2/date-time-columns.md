
MUST use descriptive event names. Avoid vague suffixes like `_at`:

```sql
-- Correct
creation_date     TEXT NOT NULL DEFAULT (datetime('now')),
modification_date TEXT,
completion_date   TEXT

-- Wrong
created_at TEXT,
updated_at TEXT
```

