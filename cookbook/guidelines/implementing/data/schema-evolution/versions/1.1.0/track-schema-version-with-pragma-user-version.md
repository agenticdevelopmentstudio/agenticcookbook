
```sql
-- Read current version
PRAGMA user_version;

-- Set version after applying a migration
PRAGMA user_version = 3;
```

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

