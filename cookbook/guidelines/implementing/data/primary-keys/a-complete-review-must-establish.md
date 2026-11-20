
- Primary key strategy documented and justified (INTEGER PRIMARY KEY vs UUID vs composite)
- INTEGER PRIMARY KEY correctly aliases rowid; AUTOINCREMENT only used where gap-free sequence is required
- UUID format consistent across local and server databases if table is synced
- UUID storage method chosen (TEXT base64/hex vs BLOB) with rationale
- UUID generation strategy documented (v4 for randomness, v7 for sortability, application-generated or database-generated)
- WITHOUT ROWID tables only for non-integer primary keys with clustered access patterns
- Without ROWID tables use composite PK or TEXT/BLOB PK, never INTEGER
- Cross-database PK mapping documented for synced tables (e.g., SQLite UUID ↔ PostgreSQL uuid type)
- Every MUST rule is kept, with no exception: `must-declare-rowid-alias-as-integer`, `must-limit-autoincrement`, `must-not-autoincrement-synced-tables`, `must-declare-primary-key-without-rowid`, `must-not-autoincrement-without-rowid`, `must-use-client-uuids-for-multi-device-sync`, `must-not-rely-on-implicit-rowid`, `must-not-use-last-insert-rowid-without-rowid`, `must-not-use-without-rowid-below-3-8-2`
- Every SHOULD rule is kept, or the change says why not: `should-default-to-integer-primary-key`, `should-use-uuidv7-for-synced-tables`, `should-use-hybrid-ids`, `should-use-without-rowid-when-it-fits`, `should-store-uuids-as-blob`


A review passes when it establishes every item above.
