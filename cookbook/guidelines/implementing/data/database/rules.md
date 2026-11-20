
- **must-use-sqlite-wal-for-concurrent-reads**: SQLite with WAL mode MUST be used for concurrent read access.
- **must-not-use-orm**: An ORM MUST NOT be used — use direct SQL via the `sqlite3` standard library module.
