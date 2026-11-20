
- `should-set-theme-at-app-and-element-level`: whether the app theme is set via `Application.RequestedTheme` and per-element overrides via `FrameworkElement.RequestedTheme`
- `must-use-theme-resource`: whether every color and brush uses `ThemeResource`, not `StaticResource`
- `should-use-semantic-color-resources`: whether semantic color resources are used instead of hex values
- `should-define-theme-dictionaries`: whether custom theme-aware colors are defined in a `ResourceDictionary` with `Default`/`Light`/`Dark` theme dictionaries
- `must-use-theme-resource`: `ThemeResource` used exclusively for colors and brushes;
- `should-render-in-light-dark-and-high-contrast`: app renders correctly in Light, Dark, and High Contrast modes;
- `should-define-theme-dictionaries`: custom colors defined with theme dictionary variants
