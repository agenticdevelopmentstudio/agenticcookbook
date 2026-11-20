
```sql
CREATE TABLE findings (
    finding_id INTEGER PRIMARY KEY,
    content    TEXT NOT NULL
);
```

On INSERT without a value, SQLite assigns `max(finding_id) + 1`. If the maximum row is deleted, that ID can be reused.

```sql
-- These alias rowid:
id INTEGER PRIMARY KEY
id INTEGER PRIMARY KEY NOT NULL  -- NOT NULL is redundant but harmless

-- These do NOT alias rowid:
id INT PRIMARY KEY         -- INT != INTEGER for this purpose
id INTEGER UNIQUE          -- UNIQUE != PRIMARY KEY for this purpose
```

