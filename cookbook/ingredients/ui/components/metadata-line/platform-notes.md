
- **SwiftUI**: `Label("text", systemImage: "icon").labelStyle(.titleAndIcon)` or custom `HStack { Image(systemName:) Text() }` with `.lineLimit(1).truncationMode()`.
- **Compose**: `Row(verticalAlignment = Alignment.CenterVertically) { Icon(); Spacer(4.dp); Text(maxLines = 1, overflow = TextOverflow.Ellipsis) }`.
- **React/Web**: `<span>` with flexbox `display: inline-flex; align-items: center; gap: 4px`. CSS `text-overflow: ellipsis; white-space: nowrap; overflow: hidden`.

