
- **should-set-theme-at-app-and-element-level**: SHOULD set app-level theme via `Application.RequestedTheme`, override per-element with `FrameworkElement.RequestedTheme`
- **must-use-theme-resource**: Colors and brushes MUST use `ThemeResource` (not `StaticResource`) — enables runtime theme switching
- **should-use-semantic-color-resources**: Semantic color resources (`TextFillColorPrimary`, `CardBackgroundFillColorDefault`) SHOULD be used instead of hex values
- **should-define-theme-dictionaries**: SHOULD define custom theme-aware colors in a `ResourceDictionary` with `Default`/`Light`/`Dark` theme dictionaries
