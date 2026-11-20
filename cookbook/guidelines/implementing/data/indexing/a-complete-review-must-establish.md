
- Composite indexes ordered with equality columns first, range/inequality columns second
- Partial indexes used for filtered queries (e.g., WHERE deleted = 0)
- No indexes on low-selectivity columns (booleans, status fields with few values) or tables under 10K rows
- Sync metadata columns (isDirty, sync_version) indexed for hot-path queries
- EXPLAIN QUERY PLAN shows index usage for all hot-path queries; no full table scans on large tables
- Covering indexes reduce disk seeks for queries selecting multiple columns


A review passes when it establishes every item above.
