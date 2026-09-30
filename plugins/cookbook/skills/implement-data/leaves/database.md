<!-- leaf: implement-data/database · source: guidelines/implementing/data/database.md -->

**Rules** (cite as `implement-data/database#<slug>`):

- `sqlite-wal-mode-used-concurrent-read-access` MUST — SQLite with WAL mode MUST be used for concurrent read access. An ORM MUST NOT be used — use direct SQL via the sqlite3 …

# Database

SQLite with WAL mode MUST be used for concurrent read access. An ORM MUST NOT be used — use direct SQL via the `sqlite3` standard library module.

```python
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL")
```
