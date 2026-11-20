
A deletion that misses a copy is not a deletion.

- Deletions **SHOULD cascade** from the source of truth to every derived store: denormalized tables, read replicas, caches (Redis/CDN), search indexes (Elasticsearch/OpenSearch), data-warehouse/analytics copies, message-queue payloads, and object storage (S3/blob).
- Maintain an explicit inventory of where each category is copied; treat the inventory as the cascade checklist and keep it in version control.
- Prefer **event-driven** cascade (emit a `deletion-requested` event; each store subscribes) over a monolithic delete that must know every downstream — this keeps stores decoupled and the design open to new sinks (optimize for change).
- Make cascade steps **idempotent** and retryable; a partially failed cascade **MUST** be detectable and resumable, not silently abandoned.

