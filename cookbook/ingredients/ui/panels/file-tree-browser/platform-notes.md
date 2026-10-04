
- **SwiftUI**: Use `List` with `OutlineGroup` and `.listStyle(.sidebar)`. Model `FileTreeNode` as an `ObservableObject` with `@Published children: [FileTreeNode]?` (nil = not yet loaded, empty = loaded but empty). Load children on `OutlineGroup`'s `children` keypath access. Git status fetched via a separate provider running on a background `DispatchQueue`. Parallel scanning via `OperationQueue` with `maxConcurrentOperationCount` set to `maxScanWorkers`. Ignore patterns evaluated using `fnmatch()` from Darwin. Icons via `Image(systemName:)` with `.foregroundStyle()` for theming. Tooltips via `.help()` modifier (macOS).
- **visionOS**: Same SwiftUI implementation as macOS. List renders in a volume or window with standard sidebar appearance. No platform-specific adjustments beyond standard visionOS adaptations.
- **iOS**: Same SwiftUI implementation. Sidebar presented in `NavigationSplitView` sidebar column. Disclosure indicators use standard iOS chevron style.

