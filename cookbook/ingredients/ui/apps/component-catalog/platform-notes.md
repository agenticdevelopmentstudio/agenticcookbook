
- **SwiftUI**: All catalog views are SwiftUI. Use `NavigationSplitView` or `NavigationStack` per adaptive-navigation, and gate platform-specific entries with `#if os(...)`.
- **Compose and React/Web**: Not applicable — the catalog targets Apple platforms only.

### Catalog entry pattern

```swift
struct PrimaryButtonCatalog: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                Text("PrimaryButton").font(.title)

                Section("Default") {
                    PrimaryButton("Label", action: {})
                }
                Section("Disabled") {
                    PrimaryButton("Label", action: {}).disabled(true)
                }
                Section("Loading") {
                    PrimaryButton("Label", isLoading: true, action: {})
                }
            }
            .padding()
        }
    }
}

#Preview {
    PrimaryButtonCatalog()
}
```

