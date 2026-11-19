
The worker evaluates the sync protocol design, ensuring it specifies sync direction (push/pull/bidirectional), uses version cursors for incremental sync, implements idempotent operations (UPSERT or idempotency keys), applies outbox pattern for transactional consistency, and defines batch sync with pagination and retry strategy with exponential backoff.

