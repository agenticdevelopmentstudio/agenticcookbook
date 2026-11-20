
- **must-provide-bitmaps-at-multiple-scales**: Bitmap assets MUST be provided at multiple scales: `.scale-100`, `.scale-125`, `.scale-150`, `.scale-200`, `.scale-400`.
- **should-track-rasterization-scale-for-custom-rendering**: For custom rendering (Win2D, Direct3D interop), SHOULD query `XamlRoot.RasterizationScale` and listen for `RasterizationScaleChanged`.
- **must-not-hard-code-pixel-sizes**: Pixel sizes MUST NOT be hard-coded in code-behind — rely on XAML layout and the scaling system.
