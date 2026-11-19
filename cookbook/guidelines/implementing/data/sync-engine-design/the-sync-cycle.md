
```
1. Collect    — Query all registered entities for dirty (isDirty = 1) records
2. Package    — Build request body: { lastSyncVersion, dirtyRecords[] }
3. Send       — POST /api/sync (one endpoint handles all entity types)
4. Receive    — Server returns: { currentSyncVersion, changedRecords[] }
5. Apply      — Upsert server records locally, clear dirty flags
6. Checkpoint — Store currentSyncVersion; use as since_version on next sync
```

