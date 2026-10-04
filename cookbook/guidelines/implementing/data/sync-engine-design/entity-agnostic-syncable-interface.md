
SHOULD design the engine so every synced entity implements a common interface:

```
interface Syncable<T> {
    collectDirty(): List<T>           // query local records where isDirty = true
    buildPayload(items: List<T>)      // serialize for sync request body
    applyResponse(items: List<T>)     // upsert server records locally
    markSynced(items: List<T>)        // clear dirty flags, update last_synced_at
}
```

The orchestrator iterates over all registered content types without knowing their entity-specific details. Conflict handling MAY be customized per content type while sharing a common transport and scheduling layer.

Benefits: sync logic is tested once in the orchestrator; adding a new entity is a single interface implementation; entity-specific quirks are contained.

