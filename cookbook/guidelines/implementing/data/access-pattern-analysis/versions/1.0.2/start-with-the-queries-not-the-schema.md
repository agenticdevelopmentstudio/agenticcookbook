
MUST answer these questions before finalizing any schema:

1. What are the most frequent queries? What columns appear in WHERE, JOIN, and ORDER BY?
2. What are the most expensive queries? (Use `EXPLAIN QUERY PLAN` and `ANALYZE`.)
3. Is this table read-heavy or write-heavy? What is the read-to-write ratio?
4. Are reads latency-sensitive (user-facing) or throughput-sensitive (background batch)?
5. What is the expected row count — today and at 10x scale?

The answers drive every subsequent decision: index selection, composite key ordering, WAL vs rollback journal, batch size, and connection count.

