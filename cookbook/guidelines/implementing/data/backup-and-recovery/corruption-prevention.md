
SQLite is highly resistant to corruption. Crashed transactions are automatically rolled back on next access. Corruption almost always originates from one of these causes:

- **Network filesystems** — never run SQLite on NFS, CIFS, or any networked filesystem. File locking is unreliable.
- **Synchronous mode too low** — `PRAGMA synchronous = OFF` allows the OS to lie about writes completing. SHOULD use `NORMAL` (safe with WAL mode) or `FULL`.
- **Deleting journal files** — deleting `*-journal` or `*-wal` while the database is open prevents crash recovery.
- **Multiple processes writing directly** — only allow SQLite's own locking to coordinate access.
- **Moving a database without its journal** — the database and its journal/WAL are a unit.

These PRAGMAs MUST NOT be set in production:

```sql
PRAGMA synchronous = OFF;       -- risk of corruption on power loss
PRAGMA journal_mode = OFF;      -- disables crash recovery entirely
PRAGMA journal_mode = MEMORY;   -- same risk as OFF
```

