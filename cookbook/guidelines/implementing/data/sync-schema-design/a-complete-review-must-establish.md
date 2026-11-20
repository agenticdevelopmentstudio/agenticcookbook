
- UUID PKs on all synced tables (not auto-incremented server IDs)
- Soft delete strategy chosen and documented (flag column vs tombstone table)
- Dirty tracking mechanism specified (dirty flag, change log, or operation queue)
- Version column present on all synced tables for optimistic concurrency
- Sync metadata tables defined (last_synced_at per table, change cursors, device state)
- Every rule is kept, or the change says why not: `must-use-uuid-primary-keys`, `should-use-uuidv7`, `must-have-three-timestamp-columns`, `must-not-update-created-at`, `must-update-updated-at-on-every-change`, `should-store-timestamps-as-iso-8601-utc`, `must-not-mix-timestamp-formats`, `should-maintain-updated-at-by-trigger`, `must-add-version-column`, `must-increment-version-on-update`, `must-check-changes-after-versioned-update`, `must-not-hard-delete`, `should-use-is-deleted-column`, `must-filter-deleted-in-normal-queries`, `must-include-deleted-in-sync-queries`, `should-add-dirty-tracking`, `must-set-dirty-on-every-local-write`, `should-clear-dirty-after-server-accepts`, `should-use-change-log-for-operation-awareness`, `should-add-sync-state-table`, `should-store-sync-version-checkpoint`, `should-map-types-cleanly-across-databases`, `should-convert-to-local-time-only-for-display`


A review passes when it establishes every item above.
