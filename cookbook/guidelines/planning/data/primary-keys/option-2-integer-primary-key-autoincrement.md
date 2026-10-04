
```sql
CREATE TABLE audit_entries (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action   TEXT NOT NULL
);
```

AUTOINCREMENT guarantees IDs are strictly monotonically increasing and never reused, even after row deletion. It maintains a counter in the internal `sqlite_sequence` table, which requires an extra read/write on every INSERT.

The official SQLite docs warn: *"AUTOINCREMENT imposes extra CPU, memory, disk space, and disk I/O overhead and should be avoided if not strictly needed."*

**Use AUTOINCREMENT only for:** audit logs, financial ledgers, event streams — where ID reuse is semantically wrong or a security concern. If the counter reaches `2^63 - 1`, further inserts fail with `SQLITE_FULL`.

