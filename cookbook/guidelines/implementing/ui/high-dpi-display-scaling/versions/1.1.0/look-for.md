
- `must-provide-bitmaps-at-multiple-scales`: a bitmap asset shipped at only one scale, or missing any of `.scale-100`, `.scale-125`, `.scale-150`, `.scale-200`, `.scale-400`
- `should-track-rasterization-scale-for-custom-rendering`: custom rendering (Win2D, Direct3D interop) that never reads `XamlRoot.RasterizationScale` or never handles `RasterizationScaleChanged`
- `must-not-hard-code-pixel-sizes`: a pixel size hard-coded in code-behind instead of left to XAML layout and the scaling system
