
```sql
CREATE TABLE word_counts (
    word  TEXT PRIMARY KEY,
    count INTEGER NOT NULL DEFAULT 0
) WITHOUT ROWID;
```

`WITHOUT ROWID` uses the declared PRIMARY KEY as the clustered index. The table is a single B-tree keyed on the PK columns — for the word_counts example, this means the word is stored once instead of twice (rowid B-tree + unique index), giving roughly 50% less disk space and 2x faster lookups.

**Restrictions:**
- `sqlite3_last_insert_rowid()` does not work
- Requires SQLite 3.8.2+

