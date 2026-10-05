
Package document storage defines what is inside a document package and how it is read and written: one or more SQLite database files holding all persistent state, versioned by `PRAGMA user_version`, with a fallback that reads legacy JSON files and migrates them to SQLite on the next save. Writes are atomic by construction — all data goes into a temporary SQLite file, its bytes are wrapped in a `FileWrapper`, and the system replaces the package directory in one step. Use it for each document type (project, workspace) that follows the structural pattern with its own database filename and schema.

### Terminology

| Term | Definition |
|------|-----------|
| Schema version | An integer stored in SQLite's `PRAGMA user_version` that identifies the database schema revision |
| Format migration | The process of reading a legacy format (e.g., JSON) and converting it to the current SQLite-based format on first save |
| Atomic write | Writing all data to a temporary SQLite file, reading it back as bytes, and wrapping it in a `FileWrapper` so the system can perform an atomic directory replacement |
| Key-value settings | A table of string key-value pairs used to store typed settings (booleans as `"true"`/`"false"`, numbers as string representations) |

### Architecture

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

