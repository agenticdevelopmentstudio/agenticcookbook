
- `should-set-theme-at-app-and-element-level`: the app theme is set via `Application.RequestedTheme` and overrides via `FrameworkElement.RequestedTheme`, or the code says why not
- `must-use-theme-resource`: every color and brush uses `ThemeResource`, none `StaticResource`
- `should-use-semantic-color-resources`: no hex value stands where a semantic color resource fits, or the code says why
- `should-define-theme-dictionaries`: every custom theme-aware color is defined in `Default`/`Light`/`Dark` theme dictionaries of a `ResourceDictionary`, or the code says why not
