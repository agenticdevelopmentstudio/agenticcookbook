
```sql
CREATE TABLE findings (
    finding_id INTEGER PRIMARY KEY,
    content    TEXT NOT NULL
);
```

`INTEGER PRIMARY KEY` makes the column an alias for the rowid. There is no separate storage and no separate index — it is the fastest possible PK in SQLite.

On INSERT without a value, SQLite assigns `max(finding_id) + 1`. If the maximum row is deleted, that ID can be reused.

**Critical:** Only `INTEGER PRIMARY KEY` aliases rowid. `INT PRIMARY KEY` does NOT — it creates a regular column with a separate unique index, doubling storage overhead.

```sql
-- These alias rowid:
id INTEGER PRIMARY KEY
id INTEGER PRIMARY KEY NOT NULL  -- NOT NULL is redundant but harmless

-- These do NOT alias rowid:
id INT PRIMARY KEY         -- INT != INTEGER for this purpose
id INTEGER UNIQUE          -- UNIQUE != PRIMARY KEY for this purpose
```

