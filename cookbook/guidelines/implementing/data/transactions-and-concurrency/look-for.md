
Evaluates transaction patterns and concurrency configuration for SQLite. Verifies WAL mode is enabled for concurrent access. Checks that write transactions use BEGIN IMMEDIATE to avoid serialization errors. Reviews connection pooling strategy (single writer + multiple readers). Validates busy_timeout configuration. Audits production PRAGMAs including synchronous level, cache_size, journal_size_limit, and foreign_keys enforcement.

