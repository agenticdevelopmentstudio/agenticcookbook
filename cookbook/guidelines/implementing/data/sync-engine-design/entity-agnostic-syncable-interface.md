
```
interface Syncable<T> {
    collectDirty(): List<T>           // query local records where isDirty = true
    buildPayload(items: List<T>)      // serialize for sync request body
    applyResponse(items: List<T>)     // upsert server records locally
    markSynced(items: List<T>)        // clear dirty flags, update last_synced_at
}
```

The orchestrator iterates over all registered content types without knowing their entity-specific details.

