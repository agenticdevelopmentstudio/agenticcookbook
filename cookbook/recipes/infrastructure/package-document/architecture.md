
```
┌─────────────────────────────────────────────────┐
│  DocumentGroup(newDocument:)                     │
│  ┌─────────────────────────────────────────────┐ │
│  │  ReferenceFileDocument                      │ │
│  │  ┌───────────────────────┐                  │ │
│  │  │  @Published var model │──objectWillChange│ │
│  │  └───────────┬───────────┘    → auto-save   │ │
│  │              │                              │ │
│  │  ┌───────────▼───────────┐                  │ │
│  │  │  fileWrapper(...)     │                  │ │
│  │  │  ┌─────────────────┐  │                  │ │
│  │  │  │ Temp SQLite DB  │  │                  │ │
│  │  │  │ → Insert data   │  │                  │ │
│  │  │  │ → Read bytes    │  │                  │ │
│  │  │  │ → FileWrapper   │  │                  │ │
│  │  │  └─────────────────┘  │                  │ │
│  │  └───────────────────────┘                  │ │
│  └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘

Package on disk:
┌──────────────────────────┐
│  MyDocument.catnip-proj/ │  ← Finder shows as single file
│  ├── project.db          │  ← SQLite database
│  └── (legacy: data.json) │  ← Removed after migration
└──────────────────────────┘
```

