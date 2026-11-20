
- **use-systembackdrop**: Set the material declaratively via the window/page `SystemBackdrop` property — `MicaBackdrop` (set `Kind="BaseAlt"` for Mica Alt) or `DesktopAcrylicBackdrop`. Agents **SHOULD** prefer `SystemBackdrop` over the lower-level `MicaController`/`DesktopAcrylicController` unless controller-level customization is required.
- **transparent-layers**: To let the backdrop show through, intervening layer backgrounds **MUST** be transparent; apply content-layer fills with `LayerFillColorDefaultBrush` (and `LayerOnMicaBaseAltFillColorDefaultBrush` for the Mica Alt commanding layer).
- **win32-and-wpf**: For Win32/WPF hosts, follow the platform-specific "Apply Mica in Win32 desktop apps" path rather than assuming the WinUI API surface.

