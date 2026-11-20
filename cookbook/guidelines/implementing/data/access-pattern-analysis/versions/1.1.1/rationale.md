
- `must-answer-access-questions-before-schema`: The answers drive every subsequent decision: index selection, composite key ordering, WAL vs rollback journal, batch size, and connection count.
- `must-not-add-speculative-indexes`: An index that no query uses costs write performance with no read benefit.
- `must-wrap-sync-batch-in-one-transaction`: Applying changes row-by-row in autocommit mode pays an fsync per row — at 30ms+ per fsync, a 500-record batch would take 15 seconds.
- `must-begin-immediate-for-sync-writes`: `IMMEDIATE` acquires the write lock at transaction start, preventing mid-batch lock failures that would require rolling back the entire batch.

