
A standard bidirectional sync cycle SHOULD complete in a single server round trip:

```
1. Collect    — Query all registered entities for dirty (isDirty = 1) records
2. Package    — Build request body: { lastSyncVersion, dirtyRecords[] }
3. Send       — POST /api/sync (one endpoint handles all entity types)
4. Receive    — Server returns: { currentSyncVersion, changedRecords[] }
5. Apply      — Upsert server records locally, clear dirty flags
6. Checkpoint — Store currentSyncVersion; use as since_version on next sync
```

Combining push and pull into one HTTP request halves network round trips compared to separate push and pull calls — significant on mobile networks with 200–800ms latency.

After step 5, rebuild any derived views or computed state that depends on the synced entities before notifying the UI of changes.

