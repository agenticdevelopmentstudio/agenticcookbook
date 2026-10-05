
The four phases are a pipeline around one owner. This is a non-UI recipe, so the layout is the logical arrangement of the components and the order of the data flow.

```
 launch
   │
   ▼
 ┌──────────────────────┐   cached tree   ┌──────────────────────────┐
 │ Directory tree cache │ ───────────────▶│                          │──▶ published tree (UI)
 └──────────────────────┘                  │ Directory watch          │──▶ isSyncing (UI)
 ┌──────────────────────┐   scanned tree  │ coordinator              │
 │ Directory tree       │ ───────────────▶│  (one per directory;     │
 │ scanner              │ ◀───────────────│   workspace manager      │
 └──────────────────────┘  changed paths  │   pools one per entry)   │
 ┌──────────────────────┐ ───────────────▶│                          │
 │ Filesystem watcher   │                 └─────────────┬────────────┘
 └──────────────────────┘                               │ save after sync / update
                                                        ▼
                                              Directory tree cache (atomic write)
```

