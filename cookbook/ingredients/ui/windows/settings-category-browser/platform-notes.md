
- **SwiftUI (macOS)**: Use `NavigationSplitView` with `.navigationSplitViewStyle(.balanced)`. Use `@AppStorage` with centralized `SettingsKeys` constants for binding settings. Use `Form { Section("Header") { ... } }` for content panel layout.
- **Compose (Windows)**: Use a `Row` with a `LazyColumn` sidebar and content panel. Store settings in a preferences file.
- **React/Web**: Use CSS Grid or Flexbox for the split layout. Persist settings in `electron-store` or `localStorage`.

