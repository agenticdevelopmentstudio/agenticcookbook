
MUST use `PRAGMA user_version` to track schema version. It is a built-in 32-bit integer stored in the database file header — available immediately without querying any table.

```sql
-- Read current version
PRAGMA user_version;

-- Set version after applying a migration
PRAGMA user_version = 3;
```

Each migration file MUST end with the appropriate `PRAGMA user_version = N;` statement.

**Migration file structure:**

```
migrations/
  0001_initial_schema.sql
  0002_add_indexes.sql
  0003_add_fts.sql
```

**Python runner pattern:**

```python
current = db.execute('PRAGMA user_version').fetchone()[0]
for migration_file in sorted(migration_files):
    version = int(migration_file.split('_')[0])
    if version > current:
        db.executescript(open(migration_file).read())
```

Each migration MUST be wrapped in a transaction and MUST be idempotent (safe to run twice).

