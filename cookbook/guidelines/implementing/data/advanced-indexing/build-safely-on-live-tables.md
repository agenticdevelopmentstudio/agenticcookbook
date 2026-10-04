
- **concurrent-build**: Indexes on large live tables **MUST** be created with `CREATE INDEX CONCURRENTLY` so writes are not blocked by a long `ACCESS EXCLUSIVE` lock. It runs slower and cannot run inside a transaction block.
- **failed-index-cleanup**: A `CONCURRENTLY` build that fails leaves an `INVALID` index. The author **MUST** detect it (`pg_index.indisvalid = false`) and `DROP INDEX CONCURRENTLY` before retrying.
- **rebuild-without-lock**: To rebuild a bloated index, you **SHOULD** use `REINDEX INDEX CONCURRENTLY` rather than drop-and-recreate, preserving query coverage throughout.

