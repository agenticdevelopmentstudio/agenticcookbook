
- The app **MUST** honor the OS theme by default (`prefers-color-scheme`,
  `UITraitCollection.userInterfaceStyle`, `isSystemInDarkTheme()`, `RequestedTheme`), and **SHOULD**
  offer an explicit override.
- Provide a **high-contrast / increase-contrast** theme and **MUST** respond to the system signal
  (`prefers-contrast: more`, `forced-colors`/Windows High Contrast,
  `UIAccessibility.isDarkerSystemColorsEnabled`, `accessibilityHighContrast`).
- Under forced-colors / Windows High Contrast, defer to system colors; do not override them.

