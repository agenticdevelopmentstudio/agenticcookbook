
An XcodeGen-generated Xcode project with one standalone SwiftUI app target per Apple platform (iOS, macOS, watchOS, tvOS, visionOS) and a local Swift package, TestSharedKit, shared by all five. A single `project.yml` is the source of truth; the generated project is output to `Tests/Projects/Apple/`. This ingredient owns project structure, targets, and source layout; what the apps display is the Component Catalog ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| TestSharedKit | Local SPM package containing code shared across all five platform targets |

