
- `must-provide-bitmaps-at-multiple-scales`: every bitmap asset exists at `.scale-100`, `.scale-125`, `.scale-150`, `.scale-200` and `.scale-400`
- `should-track-rasterization-scale-for-custom-rendering`: every custom renderer (Win2D, Direct3D interop) queries `XamlRoot.RasterizationScale` and handles `RasterizationScaleChanged`, or the code says why not
- `must-not-hard-code-pixel-sizes`: no pixel size is hard-coded in code-behind
