
- UUID PKs on all synced tables (not auto-incremented server IDs)
- Soft delete strategy chosen and documented (flag column vs tombstone table)
- Dirty tracking mechanism specified (dirty flag, change log, or operation queue)
- Version column present on all synced tables for optimistic concurrency
- Sync metadata tables defined (last_synced_at per table, change cursors, device state)
- Every MUST rule is kept, with no exception: `must-use-uuid-primary-keys`, `must-have-three-timestamp-columns`, `must-not-update-created-at`, `must-update-updated-at-on-every-change`, `must-not-mix-timestamp-formats`, `must-add-version-column`, `must-increment-version-on-update`, `must-check-changes-after-versioned-update`, `must-not-hard-delete`, `must-filter-deleted-in-normal-queries`, `must-include-deleted-in-sync-queries`, `must-set-dirty-on-every-local-write`
- Every SHOULD rule is kept, or the change says why not: `should-use-uuidv7`, `should-store-timestamps-as-iso-8601-utc`, `should-maintain-updated-at-by-trigger`, `should-use-is-deleted-column`, `should-add-dirty-tracking`, `should-clear-dirty-after-server-accepts`, `should-use-change-log-for-operation-awareness`, `should-add-sync-state-table`, `should-store-sync-version-checkpoint`, `should-map-types-cleanly-across-databases`, `should-convert-to-local-time-only-for-display`


A review passes when it establishes every item above.
