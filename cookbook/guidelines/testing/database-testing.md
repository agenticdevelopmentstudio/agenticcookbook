---
id: 183D07F2-ECFC-4DA3-9A21-96953EFEFA91
title: "Database testing"
domain: agenticdevelopercookbook://guidelines/testing/database-testing
type: guideline
version: 1.0.2
status: accepted
language: en
created: 2026-04-06
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Prescriptive rules for testing SQLite-backed code: in-memory vs file-based databases, test isolation strategies, migration testing, sync logic testing, and conflict resolution testing."
platforms:
  - sqlite
  - postgresql
tags:
  - database
  - testing
  - migrations
  - sync
  - fixtures
depends-on: []
related:
  - guidelines/data/sqlite-best-practices.md
references:
  - https://sqlite.org/testing.html
  - https://oneuptime.com/blog/post/2026-02-02-sqlite-testing/view
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-06"
triggers:
  - writing-tests
  - database-operations
---

# Database testing

## In-memory vs file-based databases

Use `:memory:` databases for unit tests. They are faster (no disk I/O), perfectly isolated (each connection is independent), and require no cleanup.

```python
import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript(open('schema.sql').read())
# ... run tests ...
conn.close()  # database destroyed automatically
```

Use file-based databases only for integration tests that must verify WAL behavior, file locking, concurrent connections, or platform-specific I/O. In those cases, write the database to a temp directory and delete it in teardown.

MUST NOT share a single in-memory database across unrelated test modules. The `:memory:` URL creates a new database per connection; use named in-memory databases (`file:name?mode=memory&cache=shared`) only when multiple connections to the same in-memory database are intentionally required.

## Test isolation strategies

**Fresh database per test** (SHOULD be the default) gives perfect isolation. Each test gets a blank database, applies the schema, and closes when done. Schema setup cost is negligible for most schemas.

```python
import pytest, sqlite3

@pytest.fixture
def db():
    conn = sqlite3.connect(':memory:')
    conn.executescript(open('schema.sql').read())
    yield conn
    conn.close()

def test_insert(db):
    db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    assert db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1

def test_empty(db):
    # guaranteed empty — no cross-test contamination
    assert db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0
```

**Transaction rollback** (MAY use for large schemas) creates the schema once and wraps each test in a transaction that is rolled back after the test. Tests MUST NOT commit; nested operations need SAVEPOINTs.

```python
@pytest.fixture
def db(shared_db):
    shared_db.execute("BEGIN")
    yield shared_db
    shared_db.execute("ROLLBACK")
```

**Template + backup API** (MAY use when tests need pre-populated data and isolated writes) creates a seeded template once per session and copies it per test.

```python
@pytest.fixture(scope='session')
def template_db():
    conn = sqlite3.connect(':memory:')
    conn.executescript(open('schema.sql').read())
    conn.executescript(open('test_seeds.sql').read())
    return conn

@pytest.fixture
def db(template_db):
    conn = sqlite3.connect(':memory:')
    template_db.backup(conn)
    return conn
```

## Test fixtures and seed data

SHOULD maintain a `test_seeds.sql` file with representative fixture data. Seed data SHOULD cover:

- Typical records (normal state)
- Edge cases (nulls, empty strings, boundary values)
- Records in each relevant status (e.g., pending, active, deleted)

MUST NOT build fixture data record-by-record inside individual tests when the same data is needed across multiple tests. Shared seed files are easier to maintain and faster to apply.

Use function-scoped fixtures for tests that write. Use session-scoped fixtures for read-only tests.

## Performance settings for test databases

Test databases SHOULD use relaxed durability settings. Test data is disposable — crash safety is irrelevant.

```python
conn = sqlite3.connect(':memory:')
conn.execute("PRAGMA journal_mode = OFF")
conn.execute("PRAGMA synchronous = OFF")
```

These settings are UNSAFE for production but maximize test throughput. Apply them only in test fixtures.

## Migration testing

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

## Testing sync logic

Sync logic requires testing at the unit level (change detection, serialization) and integration level (round-trip apply).

**Change detection**: verify that the unsynced-records query returns the correct rows.

```python
def test_detects_unsynced_records(db):
    # insert a record but do not mark it synced
    db.execute("INSERT INTO tasks (id, title, updated_at) VALUES (?, ?, ?)",
               ('t1', 'Task', '2026-04-06T00:00:00Z'))
    rows = db.execute(
        "SELECT id FROM tasks WHERE last_synced_at IS NULL OR updated_at > last_synced_at"
    ).fetchall()
    assert ('t1',) in rows
```

**Sync apply**: verify that applying a changeset from the server updates the local database correctly, including soft-delete propagation.

**Outbox round-trip**: write a record locally, confirm it appears in the outbox, simulate a sync cycle, confirm the record is marked synced and the outbox entry is consumed.

**Tombstone propagation**: delete a record on one simulated peer, apply the tombstone to a second peer, confirm the record is absent on the second peer and not resurrected by a subsequent sync.

## Testing conflict resolution

Conflict tests require two databases representing two peers. Apply divergent changes to each, then merge and assert the outcome matches the defined resolution strategy.

```python
def test_last_write_wins(peer_a, peer_b):
    # Both peers start from the same record
    peer_a.execute("UPDATE tasks SET title = 'A title', updated_at = '2026-04-06T10:00:00Z' WHERE id = 't1'")
    peer_b.execute("UPDATE tasks SET title = 'B title', updated_at = '2026-04-06T11:00:00Z' WHERE id = 't1'")

    # Apply peer_a's changes to peer_b (B's timestamp is later)
    changes_a = export_changes(peer_a)
    apply_changes(peer_b, changes_a)

    result = peer_b.execute("SELECT title FROM tasks WHERE id = 't1'").fetchone()
    assert result[0] == 'B title'  # last-write-wins: B's later timestamp survives
```

Test all defined conflict cases:
- Update vs update (same field, different values)
- Update vs delete (one peer deletes while another updates)
- Insert vs insert (duplicate IDs from offline creation)

## Cross-database compatibility

SQLite in tests does not behave identically to PostgreSQL or MySQL in production. Key differences that affect test validity:

| Behavior | SQLite | PostgreSQL |
|----------|--------|------------|
| Type enforcement | Permissive | Strict |
| Boolean | `INTEGER 0/1` | Native `BOOLEAN` |
| LIKE case sensitivity | Case-sensitive (ASCII) | Case-insensitive (`ILIKE`) |
| NULL in PK | Allowed | Not allowed |

Use SQLite for unit tests where dialect differences do not affect the logic under test. MUST use the production database for integration tests that cover type enforcement, constraint behavior, or database-specific SQL features.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-04-06 | Mike Fullerton | Initial version |
