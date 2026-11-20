
- **should-choose-tool-by-requirements**: SHOULD choose a sync tool based on the write path requirements, server database, conflict resolution needs, and maturity tolerance.
- **must-evaluate-maturity-before-beta-in-production**: MUST evaluate maturity and support model before committing to a Beta tool in production.
- **should-avoid-beta-tools-in-production-critical-systems**: SHOULD NOT use cr-sqlite, sqlite-sync, or Turso offline writes in production-critical systems.
- **should-prefer-session-or-powersync-for-production**: SHOULD prefer the Session Extension or PowerSync for production systems where stability and custom logic are priorities.
- **must-build-sqlite-with-session-flags**: Wherever the SQLite Session Extension is used, SQLite MUST be compiled with `-DSQLITE_ENABLE_SESSION` and `-DSQLITE_ENABLE_PREUPDATE_HOOK`.
- **must-declare-primary-key-for-session-tables**: Every table the Session Extension tracks MUST have a declared PRIMARY KEY.
- **must-not-track-virtual-tables-with-session**: MUST NOT rely on the Session Extension to track virtual tables.
- **must-not-store-null-in-session-pk-columns**: Tables the Session Extension tracks MUST NOT hold NULL values in PK columns; such rows are ignored.
- **must-wrap-cr-sqlite-schema-changes**: cr-sqlite schema changes MUST be wrapped in `crsql_begin_alter` / `crsql_commit_alter`.
- **must-not-use-litestream-for-sync**: MUST NOT use Litestream for device-to-server sync or multi-writer scenarios.
- **must-validate-electricsql-writes-in-postgres**: With ElectricSQL, write validation MUST live in Postgres constraints and DDLX rules, because writes bypass the application backend.
- **must-use-turso-cloud-as-turso-server**: Turso MUST be used with Turso Cloud as the server; it is not compatible with arbitrary Postgres backends.
- **must-default-not-null-columns-for-sqlite-sync**: With sqlite-sync, all NOT NULL columns MUST have DEFAULT values.
- **must-use-text-uuidv7-pks-for-sqlite-sync**: With sqlite-sync, primary keys MUST be TEXT holding UUIDv7.
- **must-wrap-sqlite-sync-schema-changes**: With sqlite-sync, ALTER TABLE MUST be wrapped with `cloudsync_begin_alter` / `cloudsync_commit_alter`.

