
**Fresh database per test.** Each test gets a blank database, applies the schema, and closes when done.

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

**Transaction rollback.**

```python
@pytest.fixture
def db(shared_db):
    shared_db.execute("BEGIN")
    yield shared_db
    shared_db.execute("ROLLBACK")
```

**Template + backup API.**

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

