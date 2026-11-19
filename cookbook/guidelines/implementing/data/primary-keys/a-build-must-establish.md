
- `should-default-to-integer-primary-key`: each table's primary key is `INTEGER PRIMARY KEY`, or the code says why another strategy was chosen
- `must-declare-rowid-alias-as-integer`: every key meant to alias the rowid is declared exactly `INTEGER PRIMARY KEY` (never `INT PRIMARY KEY` or `INTEGER UNIQUE`)
- `must-limit-autoincrement`: `AUTOINCREMENT` appears only on audit-log, financial-ledger or event-stream tables, where ID reuse is semantically wrong or a security concern
- `should-use-uuidv7-for-synced-tables`: every synced table's UUIDs are UUIDv7, or the code says why UUIDv4 was chosen
- `should-use-hybrid-ids`: every table with both internal and external IDs has an integer primary key and a separate unique UUID column, or the code says why not
- `must-not-autoincrement-synced-tables`: no synced table uses `INTEGER PRIMARY KEY AUTOINCREMENT`
- `should-use-without-rowid-when-it-fits`: every table with a non-integer or composite PK, small rows and no large strings or BLOBs is `WITHOUT ROWID`, or the code says why not
- `must-declare-primary-key-without-rowid`: every `WITHOUT ROWID` table declares an explicit PRIMARY KEY
- `must-not-autoincrement-without-rowid`: no `WITHOUT ROWID` table uses `AUTOINCREMENT`
- `must-use-client-uuids-for-multi-device-sync`: every row of a table synced across devices carries a client-generated UUID as its cross-device identifier (as its primary key, or as a unique UUID column beside an integer primary key), never a locally assigned integer
- `should-store-uuids-as-blob`: UUIDv7 values are stored as BLOB (16 bytes) or TEXT, the two forms the topic's decision table allows
- `must-not-rely-on-implicit-rowid`: no code stores or exchanges an implicit rowid as a persistent ID; every rowid that must persist is an `INTEGER PRIMARY KEY` alias
- `must-not-use-last-insert-rowid-without-rowid`: no code calls `sqlite3_last_insert_rowid()` after inserting into a `WITHOUT ROWID` table
- `must-not-use-without-rowid-below-3-8-2`: every `WITHOUT ROWID` table is in a database that only SQLite 3.8.2+ opens

