
- **SwiftUI (macOS)**: `HStack` with `Image(systemName: "chevron.right").rotationEffect(isExpanded ? .degrees(90) : .degrees(0))`. Use `.onTapGesture` on the entire `HStack`. Persist via `@AppStorage` or project settings binding. Animate with `.animation(.easeInOut(duration: 0.2), value: isExpanded)`.
- **SwiftUI (iOS/visionOS)**: Same pattern, useful in `HSplitView` or custom multi-pane layouts.
- **Compose**: `Row` with `Icon` (animated rotation via `animateFloatAsState`). Click on entire row. Persist via `rememberSaveable` or preferences.

