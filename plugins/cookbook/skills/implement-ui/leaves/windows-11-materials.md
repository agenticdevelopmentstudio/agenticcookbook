<!-- leaf: implement-ui/windows-11-materials · source: guidelines/implementing/ui/windows-11-materials.md -->

**Rules** (cite as `implement-ui/windows-11-materials#<slug>`):

- `mica-for-long-lived-windows` SHOULD
- `mica-alt-for-tabbed-titlebars` SHOULD
- `acrylic-for-transient-surfaces` SHOULD
- `one-backdrop-per-window` MUST
- `use-systembackdrop` SHOULD
- `transparent-layers` MUST
- `never-hardcode-colors` MUST
- `honor-system-fallback` MUST
- `high-contrast` MUST
- `title-bar-continuity` SHOULD

# Windows 11 materials (Mica and Acrylic)

Windows 11 Fluent materials add depth by sampling the desktop wallpaper and the user theme. Pick the material by surface lifetime: Mica for long-lived window backdrops, Acrylic for transient in-app surfaces. This pins to Microsoft Learn guidance dated 2024-11-21.

## Choosing the material

- **mica-for-long-lived-windows**: Long-lived top-level windows (main app, Settings) **SHOULD** use Mica as the base backdrop. Mica samples the wallpaper once, so it is the performant default and aids focus by falling back to a neutral tint when the window deactivates.
- **mica-alt-for-tabbed-titlebars**: Apps with a tabbed title bar or strong title-bar/commanding contrast **SHOULD** use Mica Alt (stronger wallpaper tint). Mica Alt requires Windows App SDK 1.1+ on Windows 11 build 22000+.
- **acrylic-for-transient-surfaces**: Transient/in-app surfaces — flyouts, context menus, tooltips, command bars, light-dismiss panes — **SHOULD** use Acrylic, not Mica. Acrylic blurs what is behind it in real time, which suits momentary surfaces but is heavier than Mica.
- **one-backdrop-per-window**: An app **MUST NOT** apply a backdrop material more than once per window, and **MUST NOT** apply backdrop material to an individual UI element (it only shows through transparent layers).

## Applying in WinUI 3

- **use-systembackdrop**: Set the material declaratively via the window/page `SystemBackdrop` property — `MicaBackdrop` (set `Kind="BaseAlt"` for Mica Alt) or `DesktopAcrylicBackdrop`. Agents **SHOULD** prefer `SystemBackdrop` over the lower-level `MicaController`/`DesktopAcrylicController` unless controller-level customization is required.
- **transparent-layers**: To let the backdrop show through, intervening layer backgrounds **MUST** be transparent; apply content-layer fills with `LayerFillColorDefaultBrush` (and `LayerOnMicaBaseAltFillColorDefaultBrush` for the Mica Alt commanding layer).
- **win32-and-wpf**: For Win32/WPF hosts, follow the platform-specific "Apply Mica in Win32 desktop apps" path rather than assuming the WinUI API surface.

## Respecting the user and system

- **never-hardcode-colors**: Colors **MUST** come from `ThemeResource` brushes (e.g. `SolidBackgroundFillColorBase`), never hardcoded hex values, so light/dark theme switches and High Contrast work automatically. (native-controls, explicit-over-implicit.)
- **honor-system-fallback**: Code **MUST NOT** force material when the system disables it. Materials fall back to a solid color when the user turns off transparency (Settings > Personalization > Color), Battery/Energy Saver is active, on low-end hardware, or below Windows 11 22000. The platform handles this; do not override it.
- **high-contrast**: In High Contrast mode the user's chosen background color **MUST** replace the material; rely on theme resources rather than custom drawing to get this for free.
- **title-bar-continuity**: For a seamless window, the material **SHOULD** be visible in the title bar by extending into the non-client area with a transparent custom title bar.

## Anti-patterns

- Using Acrylic as a full-window backdrop for a long-lived window (use Mica — Acrylic's real-time blur wastes power).
- Re-enabling transparency or material after the system fell back to solid color.
- Layering material on a single control instead of the window backdrop.
