
- `should-set-theme-at-app-and-element-level`: a theme set other than through `Application.RequestedTheme` at app level and `FrameworkElement.RequestedTheme` per element
- `must-use-theme-resource`: a color or brush bound with `StaticResource` instead of `ThemeResource`
- `should-use-semantic-color-resources`: a hex value where a semantic color resource (`TextFillColorPrimary`, `CardBackgroundFillColorDefault`) fits
- `should-define-theme-dictionaries`: a custom color with no `Default`/`Light`/`Dark` theme dictionaries in a `ResourceDictionary`
- `must-use-theme-resource`: always use `ThemeResource` (not `StaticResource`) for colors and brushes to enable runtime switching;
- `should-render-in-light-dark-and-high-contrast`: an app that does not render correctly in Light, Dark or High Contrast mode.
