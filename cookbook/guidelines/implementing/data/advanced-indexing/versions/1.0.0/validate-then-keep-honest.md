
- **explain-before-after**: Every new index **MUST** be justified by `EXPLAIN (ANALYZE, BUFFERS)` showing the planner uses it and the cost drops; a created-but-unused index is pure write overhead.
- **drop-unused**: Indexes with near-zero scans in `pg_stat_user_indexes.idx_scan` over a representative window **SHOULD** be dropped.
- **measured-need**: Specialized strategies — BRIN on huge append-only tables, table partitioning, custom operator classes — are adopt-only-when-a-concrete-measured-need-justifies-it, not defaults (YAGNI; make-it-work, make-it-right, make-it-fast).

