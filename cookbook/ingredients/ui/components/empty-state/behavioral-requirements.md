
- **centered-layout**: The empty state MUST be centered both horizontally and vertically within its container.
- **icon-and-heading**: The empty state MUST display at minimum an icon and a heading.
- **optional-description**: The empty state MAY display a description below the heading for additional context.
- **optional-action-buttons**: The empty state MAY display one or more action buttons below the description.
- **prominent-primary-action**: If action buttons are present, the primary action SHOULD be visually prominent (filled/borderedProminent style).
- **adaptive-container-fit**: The empty state MUST adapt to the container's available space — it MUST NOT overflow or require scrolling in typical container sizes.
- **native-unavailable-view**: On Apple platforms (iOS 17+, macOS 14+), implementations SHOULD use the native `ContentUnavailableView` as the base control.
- **platform-native-icon**: The icon MUST use a platform-native symbol (SF Symbol on Apple, Material Icon on Android, inline SVG on Web).

