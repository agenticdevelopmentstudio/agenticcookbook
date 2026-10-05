
A package document type declares a directory bundle — shown by Finder as a single file — as a first-class document: a custom UTType conforming to `com.apple.package`, a unique file extension (e.g., `.catnip-proj`, `.catnip-workspace`), a `ReferenceFileDocument` class that reads and writes a `FileWrapper`, and a `DocumentGroup` scene that gives the type open, save, and close behavior. Auto-save follows automatically from the document's `@Published` model, and the app restores the set of open documents across launches. Use it for each document kind (project, workspace) an app persists as a package.

### Terminology

| Term | Definition |
|------|-----------|
| Package document | A directory bundle that macOS presents as a single file in Finder, identified by a custom UTType conforming to `com.apple.package` |
| UTType | A Uniform Type Identifier declared in Info.plist that maps a file extension to a content type and conformance hierarchy |
| ReferenceFileDocument | A SwiftUI protocol for reference-type documents that triggers auto-save when the document's `objectWillChange` publisher fires |
| FileWrapper | An Apple framework class representing a file, directory, or symbolic link in memory; used to read from and write to package directories |
| Document scene | A SwiftUI `DocumentGroup` scene that manages the open/save/close lifecycle for a document type |

### UTType Registration

Each document type requires an exported UTType entry in Info.plist:

```
UTExportedTypeDeclarations:
  - UTTypeIdentifier: com.example.catnip-project
    UTTypeDescription: Catnip Project
    UTTypeConformsTo: [com.apple.package]
    UTTypeTagSpecification:
      public.filename-extension: [catnip-proj]
```

And a matching Swift `UTType` extension:

```swift
extension UTType {
    static let catnipProject = UTType(exportedAs: "com.example.catnip-project")
    static let catnipWorkspace = UTType(exportedAs: "com.example.catnip-workspace")
}
```

