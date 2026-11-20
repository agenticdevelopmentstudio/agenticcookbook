
- Primary key strategy documented and justified (INTEGER PRIMARY KEY vs UUID vs composite)
- INTEGER PRIMARY KEY correctly aliases rowid; AUTOINCREMENT only used where gap-free sequence is required
- UUID format consistent across local and server databases if table is synced
- UUID storage method chosen (TEXT base64/hex vs BLOB) with rationale
- UUID generation strategy documented (v4 for randomness, v7 for sortability, application-generated or database-generated)
- WITHOUT ROWID tables only for non-integer primary keys with clustered access patterns
- Without ROWID tables use composite PK or TEXT/BLOB PK, never INTEGER
- Cross-database PK mapping documented for synced tables (e.g., SQLite UUID ↔ PostgreSQL uuid type)

A review passes when it establishes every item above.
