
- Tool evaluation performed against explicit requirements (offline support, conflict model, server type, maturity level)
- Selection criteria documented for comparison (e.g., CRDT vs LWW, built-in conflict UI, schema migration support)
- Chosen tool justified with acknowledged tradeoffs (what it solves, what it requires, what it doesn't handle)
- Server requirements documented (PostgreSQL, custom backend, cloud-hosted, self-hosted options)
- License compatibility verified
- Migration path or escape hatch documented if tool becomes unsuitable
- Every rule is kept, or the change says why not: `should-choose-tool-by-requirements`, `must-evaluate-maturity-before-beta-in-production`, `should-avoid-beta-tools-in-production-critical-systems`, `should-prefer-session-or-powersync-for-production`, `must-build-sqlite-with-session-flags`, `must-declare-primary-key-for-session-tables`, `must-not-track-virtual-tables-with-session`, `must-not-store-null-in-session-pk-columns`, `must-wrap-cr-sqlite-schema-changes`, `must-not-use-litestream-for-sync`, `must-validate-electricsql-writes-in-postgres`, `must-use-turso-cloud-as-turso-server`, `must-default-not-null-columns-for-sqlite-sync`, `must-use-text-uuidv7-pks-for-sqlite-sync`, `must-wrap-sqlite-sync-schema-changes`


A review passes when it establishes every item above.
