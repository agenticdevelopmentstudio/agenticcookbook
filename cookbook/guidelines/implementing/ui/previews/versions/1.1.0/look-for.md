
- `must-include-preview-declarations`: a UI component with no preview declaration
- `should-cover-significant-states`: previews that leave out a significant state (default, loading, error, empty, populated)
- `must-include-swiftui-preview-blocks`: a SwiftUI view with no `#Preview` block
- `should-verify-swiftui-previews-render`: verification that never renders the SwiftUI previews, or previews that crash
- `must-include-compose-preview-functions`: a Compose component with no `@Preview` function
- `should-verify-compose-previews-compile`: verification that never compiles the Compose preview functions, or previews that fail to compile
