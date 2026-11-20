
- WAL mode enabled on local SQLite database for offline capability
- Local-first read/write with background sync to server
- Operation queue pattern implemented for mutations queued while offline
- Optimistic UI updates with rollback path when server rejects operation
- Schema migration strategy handles offline devices (deferred, conditional, or dual schema)
- Data expiry and cache invalidation strategy documented
- Connectivity detection implemented to trigger sync when connection restored

A review passes when it establishes every item above.
