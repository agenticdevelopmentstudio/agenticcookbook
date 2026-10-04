
A loadable extension that adds multi-master replication via column-level CRDTs. Any table can become a conflict-free replicated relation (CRR) with one SQL call.

```sql
.load crsqlite
CREATE TABLE tasks (id TEXT PRIMARY KEY NOT NULL, title TEXT, status TEXT);
SELECT crsql_as_crr('tasks');

-- Export changes for sync
SELECT * FROM crsql_changes WHERE db_version > ?;

-- Import changes from another device
INSERT INTO crsql_changes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
```

**Conflict resolution:** Automatic LWW per column. Concurrent edits to different columns on the same row merge automatically. Only same-column conflicts require LWW fallback.

**Performance:** Writes approximately 2.5x slower than standard SQLite. Reads are identical.

**Limitations:** Beta maturity. No custom write-path business logic — CRDTs converge automatically, which means the server cannot reject writes. Schema changes require `crsql_begin_alter` / `crsql_commit_alter` wrappers.

**Use when:** Peer-to-peer sync, collaborative editing without a central server, or when you want automatic conflict resolution without custom code.

