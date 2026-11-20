
- `must-include-preview-declarations`: every UI component has a preview declaration
- `should-cover-significant-states`: previews cover default, loading, error, empty and populated states, or the code says why not
- `must-include-swiftui-preview-blocks`: every SwiftUI view has a `#Preview` block
- `should-verify-swiftui-previews-render`: every SwiftUI preview renders without crashing, or the build says why it was not checked
- `must-include-compose-preview-functions`: every Compose component has an `@Preview` function
- `should-verify-compose-previews-compile`: every Compose preview function compiles, or the build says why it was not checked
