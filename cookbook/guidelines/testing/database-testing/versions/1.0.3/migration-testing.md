
Every migration file MUST be tested for forward application. Run all migrations in order on a blank database and assert the resulting schema matches expectations.

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

Migrations SHOULD be idempotent where possible. Test idempotency by applying the migration set twice:

```python
def test_migration_idempotency():
    conn = sqlite3.connect(':memory:')
    for _ in range(2):
        for f in sorted(glob.glob('migrations/*.sql')):
            conn.executescript(open(f).read())
    # should not raise
```

Test backward migration (rollback) when rollback scripts exist. Apply forward, then backward, then verify the schema matches the pre-migration state.

Always test migrations against a database seeded with production-representative data to catch data conversion errors — type coercions, NOT NULL violations, and constraint failures that only appear with real values.

