
- `should-choose-tool-by-requirements`: the chosen sync tool fits the write path requirements, server database, conflict resolution needs, and maturity tolerance, or the code says why not
- `must-evaluate-maturity-before-beta-in-production`: a Beta tool in production has an evaluation of its maturity and support model
- `should-avoid-beta-tools-in-production-critical-systems`: no production-critical system uses cr-sqlite, sqlite-sync, or Turso offline writes, or the code says why not
- `should-prefer-session-or-powersync-for-production`: a production system where stability and custom logic are priorities uses the Session Extension or PowerSync, or the code says why not
- `must-build-sqlite-with-session-flags`: wherever the SQLite Session Extension is used, SQLite is compiled with `-DSQLITE_ENABLE_SESSION` and `-DSQLITE_ENABLE_PREUPDATE_HOOK`
- `must-declare-primary-key-for-session-tables`: every table the Session Extension tracks declares a PRIMARY KEY
- `must-not-track-virtual-tables-with-session`: no virtual table depends on the Session Extension for change tracking
- `must-not-store-null-in-session-pk-columns`: no table the Session Extension tracks holds NULL in a PK column
- `must-wrap-cr-sqlite-schema-changes`: every cr-sqlite schema change sits between `crsql_begin_alter` and `crsql_commit_alter`
- `must-not-use-litestream-for-sync`: Litestream serves no device-to-server sync or multi-writer scenario
- `must-validate-electricsql-writes-in-postgres`: with ElectricSQL, write validation lives in Postgres constraints and DDLX rules
- `must-use-turso-cloud-as-turso-server`: a Turso client syncs with Turso Cloud
- `must-default-not-null-columns-for-sqlite-sync`: with sqlite-sync, every NOT NULL column has a DEFAULT
- `must-use-text-uuidv7-pks-for-sqlite-sync`: with sqlite-sync, every primary key is TEXT holding a UUIDv7
- `must-wrap-sqlite-sync-schema-changes`: with sqlite-sync, every ALTER TABLE sits between `cloudsync_begin_alter` and `cloudsync_commit_alter`

