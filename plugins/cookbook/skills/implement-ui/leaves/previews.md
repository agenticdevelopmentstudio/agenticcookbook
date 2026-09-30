<!-- leaf: implement-ui/previews · source: guidelines/implementing/ui/previews.md -->

**Rules** (cite as `implement-ui/previews#<slug>`):

- `ui-components-include-preview-declarations-rapid` MUST — All UI components MUST include preview declarations for rapid visual verification during development. Previews should …
- `swiftui-views-include-preview-blocks-verification` MUST — All SwiftUI views MUST include #Preview blocks. Verification includes confirming previews render without crashes.
- `compose-components-include-preview-functions-verification` MUST — All Compose components MUST include @Preview functions. Verification includes confirming preview functions compile.

# Previews

All UI components MUST include preview declarations for rapid visual verification during development. Previews should cover all significant states (default, loading, error, empty, populated).

## Swift

All SwiftUI views MUST include `#Preview` blocks. Verification includes confirming previews render without crashes.

## Kotlin

All Compose components MUST include `@Preview` functions. Verification includes confirming preview functions compile.
