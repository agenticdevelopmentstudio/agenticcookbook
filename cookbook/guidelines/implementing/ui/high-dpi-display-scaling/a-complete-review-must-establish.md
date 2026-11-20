
- `must-provide-bitmaps-at-multiple-scales`: whether every bitmap asset is provided at `.scale-100`, `.scale-125`, `.scale-150`, `.scale-200` and `.scale-400`
- `should-track-rasterization-scale-for-custom-rendering`: whether every custom renderer (Win2D, Direct3D interop) queries `XamlRoot.RasterizationScale` and listens for `RasterizationScaleChanged`
- `must-not-hard-code-pixel-sizes`: whether any pixel size is hard-coded in code-behind
