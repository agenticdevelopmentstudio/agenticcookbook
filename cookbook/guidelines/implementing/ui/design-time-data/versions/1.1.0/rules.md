
- **should-use-design-time-data-context**: Views SHOULD use `d:DataContext` and `d:DesignInstance` so the designer renders realistic content, not empty surfaces — they are the XAML designer's preview data.
- **should-preview-all-significant-states**: Work SHOULD verify all significant view states are previewable: default, empty, error, loading, populated.
- **should-use-xaml-hot-reload**: XAML Hot Reload SHOULD be used for live iteration during development, and for rapid visual iteration during testing.
