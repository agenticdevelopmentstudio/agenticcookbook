
CRDTs are data structures that converge automatically across replicas with no coordination required.

CRDT types for sync:

| Type | Behavior | Use Case |
|------|----------|----------|
| LWW-Register | Last write wins per field | Individual record fields |
| G-Counter | Grow-only counter | Page views, like counts |
| PN-Counter | Increment and decrement | Inventory, resource pools |
| OR-Set | Add/remove with add-wins | Shopping carts, tag sets |
| RGA | Replicated Growable Array | Collaborative text, ordered lists |

With cr-sqlite, mark a table as a conflict-free replicated relation (CRR) and normal SQL operations sync automatically:

```sql
.load crsqlite
CREATE TABLE tasks (id TEXT PRIMARY KEY NOT NULL, title TEXT, status TEXT);
SELECT crsql_as_crr('tasks');

-- Export changes for sync
SELECT * FROM crsql_changes WHERE db_version > ?;

-- Import changes from another device
INSERT INTO crsql_changes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
```

