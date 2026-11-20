
- `should-use-design-time-data-context`: every view sets `d:DataContext` with a `d:DesignInstance` that renders realistic content, or the work says why not
- `should-preview-all-significant-states`: each view's default, empty, error, loading and populated states can be previewed, or the work says why not
- `should-use-xaml-hot-reload`: the project supports XAML Hot Reload for iteration, or the work says why not
- `should-keep-design-time-data-lightweight-and-separate`: every design-time data class is lightweight and lives apart from production code, or the work says why not
- `must-not-put-production-logic-in-design-time-data`: no design-time data class holds production logic
