
After applying sync changes, some entities require derived state to be rebuilt before the UI can display accurate data:

```
1. Receive server changes for entity X
2. Upsert raw records into local DB (inside a transaction)
3. Rebuild computed views, aggregates, or snapshots that depend on entity X
4. Notify the UI layer of changes (e.g., via reactive query, live query, or notification)
```

This matters especially for entities with edit history: the current visible state may be a function of applying all edits in sequence, not just the latest record. MUST rebuild snapshots in the correct dependency order when multiple entity types are synced in the same cycle.

