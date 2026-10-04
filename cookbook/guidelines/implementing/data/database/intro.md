
# Database

SQLite with WAL mode MUST be used for concurrent read access. An ORM MUST NOT be used — use direct SQL via the `sqlite3` standard library module.

```python
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL")
```

