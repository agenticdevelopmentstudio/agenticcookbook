
This is a non-UI recipe, so the layout is the layering of the components and the direction of the data flow. Calls go downward; nothing below imports from above.

```
 Finder / File > Open / session restoration
            │
 ┌──────────▼──────────────────────────────────────────┐
 │ Package document type                                │
 │  UTType (com.apple.package) · DocumentGroup scenes   │
 │  ReferenceFileDocument · @Published model → autosave │
 └──────────┬──────────────────────────────────────────┘
            │ init(configuration:)  /  fileWrapper(snapshot:configuration:)
 ┌──────────▼──────────────────────────────────────────┐
 │ Package document storage                             │
 │  read: project.db → legacy JSON → empty defaults     │
 │  write: temp SQLite → bytes → FileWrapper(directory) │
 └──────────┬──────────────────────────────────────────┘
            │ exec / queryRow / queryAll / lastInsertRowID
 ┌──────────▼──────────────────────────────────────────┐
 │ SQLite helpers  (bindings only · SQLiteError)        │
 └─────────────────────────────────────────────────────┘

 Package on disk:   MyDocument.catnip-proj/   project.db   (legacy: data.json)
```

