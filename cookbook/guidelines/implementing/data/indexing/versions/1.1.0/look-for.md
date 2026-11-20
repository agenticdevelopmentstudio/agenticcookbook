
Evaluates index design choices including B-tree fundamentals, partial indexes for filtered queries, expression indexes for computed columns, composite index column ordering (equality-first), and covering indexes. Analyzes EXPLAIN QUERY PLAN output to verify index usage and identifies when indexes should NOT be created (low-selectivity columns, small tables). Ensures sync metadata columns (isDirty, sync_version) are properly indexed.

