
### Info.plist exported type declaration

Each document type requires an exported UTType entry in Info.plist:

```
UTExportedTypeDeclarations:
  - UTTypeIdentifier: com.example.catnip-project
    UTTypeDescription: Catnip Project
    UTTypeConformsTo: [com.apple.package]
    UTTypeTagSpecification:
      public.filename-extension: [catnip-proj]
```

### Swift UTType extension

```swift
extension UTType {
    static let catnipProject = UTType(exportedAs: "com.example.catnip-project")
    static let catnipWorkspace = UTType(exportedAs: "com.example.catnip-workspace")
}
```

