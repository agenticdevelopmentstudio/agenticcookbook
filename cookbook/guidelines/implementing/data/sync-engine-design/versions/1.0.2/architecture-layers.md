
Separate concerns into four layers:

```
┌──────────────────────────────────┐
│           Application            │
│  (reads local DB, writes through │
│   sync-aware mutations)          │
├──────────────────────────────────┤
│         Sync Orchestrator        │
│  (coordinates push/pull cycles,  │
│   manages sync state/versions)   │
├──────────────────────────────────┤
│       Content Type Handlers      │
│  (per-entity sync logic: what    │
│   to collect, how to upsert)     │
├──────────────────────────────────┤
│          Sync Transport          │
│  (HTTP client, WebSocket, SSE)   │
├──────────────────────────────────┤
│         Local Database           │
│  (SQLite with WAL mode)          │
└──────────────────────────────────┘
```

The **Application** layer reads from local SQLite exclusively. It never fetches from the network directly.

The **Orchestrator** coordinates the sync cycle, manages the checkpoint (last sync version), and dispatches to registered content type handlers.

The **Content Type Handlers** implement entity-specific logic: what queries collect dirty records, how to serialize for the API, and how to apply server responses.

The **Transport** layer handles HTTP/WebSocket communication, authentication, and raw retry mechanics.

