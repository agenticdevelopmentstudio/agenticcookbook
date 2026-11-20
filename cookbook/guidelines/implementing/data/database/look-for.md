
- `must-use-sqlite-wal-for-concurrent-reads`: a SQLite connection read concurrently without `PRAGMA journal_mode=WAL` set
- `must-not-use-orm`: an ORM import or model layer instead of direct SQL through `sqlite3`
