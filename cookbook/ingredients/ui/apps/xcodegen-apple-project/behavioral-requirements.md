
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

