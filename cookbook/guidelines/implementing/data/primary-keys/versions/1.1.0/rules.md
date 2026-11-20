
- **should-default-to-integer-primary-key**: Tables SHOULD default to `INTEGER PRIMARY KEY`, which makes the column an alias for the rowid.
- **must-declare-rowid-alias-as-integer**: Only `INTEGER PRIMARY KEY` aliases rowid, so a rowid-aliased key MUST be declared `INTEGER PRIMARY KEY`. `INT PRIMARY KEY` does NOT alias it — it creates a regular column with a separate unique index, doubling storage overhead.
- **must-limit-autoincrement**: AUTOINCREMENT MUST be used only for audit logs, financial ledgers, event streams — where ID reuse is semantically wrong or a security concern.
- **should-use-uuidv7-for-synced-tables**: Synced tables SHOULD use UUIDv7 rather than UUIDv4.
- **should-use-hybrid-ids**: For internal + external IDs, a table SHOULD use a hybrid approach: an integer primary key internally and a separate unique UUID column for the API and sync.
- **must-not-autoincrement-synced-tables**: Synced tables MUST NOT use `INTEGER PRIMARY KEY AUTOINCREMENT`.
- **should-use-without-rowid-when-it-fits**: A table SHOULD use WITHOUT ROWID when:
  - The PK is non-integer or composite
  - Rows are small (roughly < 50–200 bytes)
  - The table does not store large strings or BLOBs
- **must-declare-primary-key-without-rowid**: A `WITHOUT ROWID` table MUST have an explicit PRIMARY KEY.
- **must-not-autoincrement-without-rowid**: A `WITHOUT ROWID` table MUST NOT use AUTOINCREMENT.
- **must-use-client-uuids-for-multi-device-sync**: Rows of a multi-device synced table MUST carry a client-generated UUID as their cross-device identifier, never a locally assigned integer.
- **should-store-uuids-as-blob**: SHOULD store UUIDv7 as BLOB for maximum efficiency (16 bytes vs 36 for TEXT).
- **must-not-rely-on-implicit-rowid**: A table MUST NOT use its implicit rowid as a persistent identifier; a rowid that must persist MUST be aliased by `INTEGER PRIMARY KEY`.
- **must-not-use-last-insert-rowid-without-rowid**: Code MUST NOT rely on `sqlite3_last_insert_rowid()` for a `WITHOUT ROWID` table; it does not work there.
- **must-not-use-without-rowid-below-3-8-2**: A `WITHOUT ROWID` table MUST NOT be used where the database must be opened by SQLite older than 3.8.2.

