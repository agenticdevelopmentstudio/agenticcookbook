
Forward application:

```python
import glob, sqlite3

def test_migrations_apply_cleanly():
    conn = sqlite3.connect(':memory:')
    for migration_file in sorted(glob.glob('migrations/*.sql')):
        conn.executescript(open(migration_file).read())
    tables = {row[0] for row in
              conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert 'users' in tables
    assert 'sessions' in tables
```

Idempotency, by applying the migration set twice:

```python
def test_migration_idempotency():
    conn = sqlite3.connect(':memory:')
    for _ in range(2):
        for f in sorted(glob.glob('migrations/*.sql')):
            conn.executescript(open(f).read())
    # should not raise
```

