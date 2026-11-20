
- Composite indexes ordered with equality columns first, range/inequality columns second
- Partial indexes used for filtered queries (e.g., WHERE deleted = 0)
- No indexes on low-selectivity columns (booleans, status fields with few values) or tables under 10K rows
- Sync metadata columns (isDirty, sync_version) indexed for hot-path queries
- EXPLAIN QUERY PLAN shows index usage for all hot-path queries; no full table scans on large tables
- Covering indexes reduce disk seeks for queries selecting multiple columns
- Every rule is kept, or the change says why not: `must-put-equality-columns-first`, `must-put-inequality-columns-last`, `must-not-duplicate-index-prefix`, `must-match-partial-index-predicate`, `must-match-index-expression-exactly`, `must-explain-before-schema-deploy`, `should-not-index-unqueried-columns`, `should-not-index-low-cardinality-columns`, `should-not-index-write-heavy-tables`, `should-use-covering-indexes-on-hot-paths`, `must-not-use-partial-indexes-below-3-8-0`, `must-keep-index-expressions-deterministic`, `must-not-use-expression-indexes-below-3-9-0`, `should-index-json-via-generated-columns`, `should-use-virtual-generated-columns`, `should-index-sync-queries`, `must-verify-sync-queries-use-indexes`, `should-check-index-for-scans`, `should-rewrite-correlated-subqueries-as-joins`, `should-run-pragma-optimize-periodically`, `should-monitor-index-usage`


A review passes when it establishes every item above.
