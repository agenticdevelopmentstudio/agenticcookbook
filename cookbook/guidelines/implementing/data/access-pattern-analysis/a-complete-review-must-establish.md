
- All hot-path queries identified and mapped to available indexes
- Every WHERE, JOIN, and ORDER BY column has index coverage or explicitly chosen denormalization justifies lack of index
- Read/write ratio documented; schema normalized for high-write or denormalized for high-read as appropriate
- Batch sizes specified for sync operations (e.g., pull 1000 rows per batch, push 500 rows per transaction)
- Access patterns documented in code comments or design documentation for future maintainers
- Every MUST rule is kept, with no exception: `must-base-schema-on-query-patterns`, `must-answer-access-questions-before-schema`, `must-not-add-speculative-indexes`, `must-index-unsynced-record-query`, `must-wrap-sync-batch-in-one-transaction`, `must-begin-immediate-for-sync-writes`, `must-not-hold-write-lock-during-network-io`
- Every SHOULD rule is kept, or the change says why not: `should-maintain-query-inventory`, `should-verify-indexes-against-query-inventory`, `should-order-composite-columns-by-query-pattern`, `should-add-covering-indexes-on-read-heavy-tables`, `should-keep-read-heavy-working-set-in-memory`, `should-select-specific-columns`, `should-run-analyze-regularly`, `should-minimize-indexes-on-write-heavy-tables`, `should-use-partial-indexes-on-write-heavy-tables`, `should-batch-writes-in-transactions`, `should-profile-before-indexing-mixed-tables`, `should-act-on-missing-index-signals`, `should-restructure-correlated-subqueries-as-joins`, `should-monitor-sqlite-stat1`, `should-design-for-sync-query-shapes`, `should-verify-unsynced-query-uses-index`, `should-partial-index-outbox-and-change-log-tables`, `should-account-for-soft-delete-in-indexes`, `should-size-sync-batches-by-context`, `should-use-json-bulk-operations-for-bulk-ingestion`, `should-separate-sync-write-and-ui-read-connections`, `should-set-busy-timeout-on-all-connections`


A review passes when it establishes every item above.
