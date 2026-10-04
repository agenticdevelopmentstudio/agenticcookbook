
- **SwiftUI**: Use `ContentUnavailableView(label:description:actions:)` on iOS 17+/macOS 14+. For older targets, use `VStack` with centered alignment in a `GeometryReader`.
- **Compose**: Use `Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally)` with `Icon`, `Text`, `Button` composables.
- **React/Web**: Centered `<div>` with flexbox `align-items: center; justify-content: center`. Use semantic heading tags (`<h3>`) and `<button>` elements.

