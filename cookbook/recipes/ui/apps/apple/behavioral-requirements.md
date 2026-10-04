
### Project structure

- **xcodegen-project**: The project MUST be generated using XcodeGen from a `project.yml` file.
- **output-directory**: The generated project MUST be output to `Tests/Projects/Apple/`.
- **five-platform-targets**: The project MUST contain five app targets, one per Apple platform:

  | Target | Platform | Deployment Target | Bundle ID |
  |--------|----------|-------------------|-----------|
  | LitterboxTestiOS | iOS | 17.0 | com.litterbox.test.ios |
  | LitterboxTestMac | macOS | 14.0 | com.litterbox.test.mac |
  | LitterboxTestWatch | watchOS | 10.0 | com.litterbox.test.watch |
  | LitterboxTestTV | tvOS | 17.0 | com.litterbox.test.tv |
  | LitterboxTestVision | visionOS | 1.0 | com.litterbox.test.vision |

- **standalone-swiftui-apps**: Each target MUST be a standalone SwiftUI app. watchOS MUST use independent app mode (no WatchKit companion).
- **test-shared-kit-package**: A local Swift package `TestSharedKit` MUST exist at `Tests/Projects/Apple/TestSharedKit/` and MUST target all five platforms at the deployment versions in five-platform-targets.
- **depend-on-shared-kit**: All five app targets MUST depend on `TestSharedKit`.

### Source layout

- **per-platform-source-dir**: Each target MUST have its own source directory under `Sources/{platform}/` containing the app entry point.
- **shared-source-directory**: A `Shared/` directory MUST be added as a source directory to all targets. It contains:
  - `Shared/Components/` — component implementations from `ui/` specs
  - `Shared/Catalog/` — catalog views showing all states per component
- **os-compilation-conditions**: Platform-specific adaptations within shared code MUST use `#if os(...)` compilation conditions.

### Catalog behavior

- **catalog-root-view**: Each app's entry point MUST display a `ComponentCatalogView` as its root view.
- **adaptive-navigation**: `ComponentCatalogView` MUST use `NavigationSplitView` on macOS, iPadOS, and visionOS, and `NavigationStack` on iPhone, watchOS, and tvOS.
- **navigable-component-list**: The catalog MUST list all implemented components by name. Selecting a component MUST navigate to its catalog entry view.
- **all-states-per-component**: Each catalog entry view MUST display the component in every state defined in its spec (default, pressed, disabled, focused, loading, etc.), each in its own labeled section.
- **preview-per-entry**: Each catalog entry view MUST include a `#Preview` block.

### Adding a component

- **adding-component-steps**: When adding a new component, the implementer MUST:
  1. Read the component spec from `ui/`
  2. Implement the component in `Shared/Components/`
  3. Create a catalog entry view in `Shared/Catalog/` showing all states
  4. Register the entry in `ComponentCatalogView`
  5. Build all five targets to verify cross-platform compatibility

