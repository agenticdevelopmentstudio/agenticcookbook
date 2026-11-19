
Choose one of three approaches based on complexity needs:

**Flag columns** — simplest. Add `is_dirty INTEGER NOT NULL DEFAULT 0` to each synced table. Set to `1` on every local write; clear to `0` after the server confirms the change.

**Change-log table with triggers** — more information. A central table records the entity, record ID, operation type (INSERT/UPDATE/DELETE), and timestamp. Triggers on each synced table populate it.

```sql
CREATE TABLE change_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name  TEXT NOT NULL,
    record_id   TEXT NOT NULL,
    operation   TEXT NOT NULL,  -- 'INSERT', 'UPDATE', 'DELETE'
    changed_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    synced      INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_changelog_unsynced ON change_log(synced, changed_at);
```

**SQLite Session Extension** — binary changesets. Records exact pre- and post-values for every row change, packaged as a binary blob for transport. Requires compile-time flags. Best when replaying changes to another SQLite database with the same schema.

