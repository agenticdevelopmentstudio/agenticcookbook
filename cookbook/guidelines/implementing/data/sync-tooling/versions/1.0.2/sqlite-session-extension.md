
Built into SQLite (compile with `-DSQLITE_ENABLE_SESSION -DSQLITE_ENABLE_PREUPDATE_HOOK`). Records changes to attached tables and packages them as binary changesets.

**Capabilities:**
- Captures INSERT, UPDATE, DELETE as binary blobs with full before/after values
- Changesets can be applied to any other SQLite database with the same schema
- Built-in conflict handler callback with four conflict types (DATA, NOTFOUND, CONFLICT, CONSTRAINT)
- Supports changeset inversion (undo) and concatenation (batch multiple sessions)

**Limitations:** Tables must have a declared PRIMARY KEY. Virtual tables not supported. NULL values in PK columns are ignored. Requires C API — no official higher-level language bindings.

**Use when:** Syncing SQLite to SQLite (e.g., device-to-device or device-to-server SQLite), when you need full control over conflict handling, or when you're building a custom sync protocol on top of raw changesets.

