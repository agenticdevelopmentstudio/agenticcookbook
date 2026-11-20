
- `must-use-sqlite-wal-for-concurrent-reads`: every SQLite connection used for concurrent reads sets `PRAGMA journal_mode=WAL`
- `must-not-use-orm`: no ORM is a dependency; all database access is direct SQL via the `sqlite3` standard library module
