
- **never-hardcode-colors**: Colors **MUST** come from `ThemeResource` brushes (e.g. `SolidBackgroundFillColorBase`), never hardcoded hex values, so light/dark theme switches and High Contrast work automatically. (native-controls, explicit-over-implicit.)
- **honor-system-fallback**: Code **MUST NOT** force material when the system disables it. Materials fall back to a solid color when the user turns off transparency (Settings > Personalization > Color), Battery/Energy Saver is active, on low-end hardware, or below Windows 11 22000. The platform handles this; do not override it.
- **high-contrast**: In High Contrast mode the user's chosen background color **MUST** replace the material; rely on theme resources rather than custom drawing to get this for free.
- **title-bar-continuity**: For a seamless window, the material **SHOULD** be visible in the title bar by extending into the non-client area with a transparent custom title bar.

