
- `should-use-memory-databases-for-unit-tests`: They are faster (no disk I/O), perfectly isolated (each connection is independent), and require no cleanup.
- `should-default-to-fresh-database-per-test`: Schema setup cost is negligible for most schemas.
- `must-not-build-shared-fixtures-per-test`: Shared seed files are easier to maintain and faster to apply.
- `should-relax-test-durability`: Test data is disposable — crash safety is irrelevant.
- `should-apply-relaxed-settings-only-in-tests`: These settings are UNSAFE for production but maximize test throughput.
- `should-use-sqlite-where-dialect-is-irrelevant`, `must-use-production-database-for-dialect-tests`: see *Cross-database compatibility* for the differences that affect test validity.
