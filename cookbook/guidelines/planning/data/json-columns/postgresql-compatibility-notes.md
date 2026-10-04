
- SQLite's `->` and `->>` operators are designed to be syntactically compatible with PostgreSQL
- SQLite JSONB is NOT binary-compatible with PostgreSQL JSONB — they are different on-disk formats
- SQLite's `json1` returns NULL for invalid JSON; PostgreSQL raises an error — validate on both sides
- PostgreSQL JSONB supports GIN indexes; SQLite uses B-tree indexes on generated columns or expressions

