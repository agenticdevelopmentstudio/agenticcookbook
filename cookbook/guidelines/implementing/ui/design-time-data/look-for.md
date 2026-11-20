
- `should-use-design-time-data-context`: XAML views with no `d:DataContext` / `d:DesignInstance`, so the designer shows empty surfaces
- `should-preview-all-significant-states`: a view whose default, empty, error, loading or populated state has no design-time preview
- `should-use-xaml-hot-reload`: a workflow that rebuilds and relaunches for visual changes instead of using XAML Hot Reload
- `should-keep-design-time-data-lightweight-and-separate`: keep design-time data classes lightweight and separate from production code
- `must-not-put-production-logic-in-design-time-data`: a design-time data class that holds production logic
