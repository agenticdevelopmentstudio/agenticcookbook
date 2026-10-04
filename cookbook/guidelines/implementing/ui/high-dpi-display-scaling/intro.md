
# High DPI / Display Scaling

XAML layout uses effective pixels (epx) — scaling is automatic for all XAML-rendered content.

- Bitmap assets MUST be provided at multiple scales: `.scale-100`, `.scale-125`, `.scale-150`, `.scale-200`, `.scale-400`
- For custom rendering (Win2D, Direct3D interop), query `XamlRoot.RasterizationScale` and listen for `RasterizationScaleChanged`
- Pixel sizes MUST NOT be hard-coded in code-behind — rely on XAML layout and the scaling system

