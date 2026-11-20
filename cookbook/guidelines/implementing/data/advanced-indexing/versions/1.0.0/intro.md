
# Advanced database indexing

An index is a deliberate trade: faster reads for slower writes and more storage. Add one only when a measured query needs it, pick the type that matches the access pattern, and prove the gain with `EXPLAIN (ANALYZE, BUFFERS)`. Examples below assume PostgreSQL 16/17; pin behavior to your server's version.

