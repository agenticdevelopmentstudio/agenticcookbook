
- UUID PKs on all synced tables (not auto-incremented server IDs)
- Soft delete strategy chosen and documented (flag column vs tombstone table)
- Dirty tracking mechanism specified (dirty flag, change log, or operation queue)
- Version column present on all synced tables for optimistic concurrency
- Sync metadata tables defined (last_synced_at per table, change cursors, device state)

- `must-use-uuid-primary-keys`: A review passes when it establishes every item above.
