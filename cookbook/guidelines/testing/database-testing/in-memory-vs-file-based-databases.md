
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

