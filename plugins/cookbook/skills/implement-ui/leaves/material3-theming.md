<!-- leaf: implement-ui/material3-theming · source: guidelines/implementing/ui/material3-theming.md -->

**Rules** (cite as `implement-ui/material3-theming#<slug>`):

- `components-consume-semantic-color-roles` MUST — Components MUST consume semantic color roles (primary, onPrimary, surface, onSurface, surfaceContainer, error, outline, …
- `theme-provide-both-lightcolorscheme-darkcolorscheme` MUST — The theme MUST provide both a lightColorScheme() and a darkColorScheme() and select between them based on …
- `materialtheme-colorscheme-role-not-read-hard-coded-color` MUST — Read colors at use sites via MaterialTheme.colorScheme.<role>. MUST NOT read a hard-coded color when a role exists.
- `should` SHOULD — guard the API level and fall back to your branded scheme:
- `materialtheme-typography-role-not-apply-ad-hoc-fontsize` MUST — Use the M3 type scale roles (displayLarge … labelSmall) via MaterialTheme.typography.<role>. MUST NOT apply ad-hoc …
- `component-corner-treatment-come-from-scale-per` SHOULD — Use the shape scale (extraSmall … extraLarge) via MaterialTheme.shapes. Component corner treatment SHOULD come from the …
- `dark-support-complete-screen-reads-onsurface` MUST — Dark support MUST be complete: every screen reads onSurface/onSurfaceVariant for text and the matching dark scheme, …
- `meet-contrast-targets-verify-contrast-against-wcag` SHOULD — Role pairs (primary/onPrimary, surface/onSurface) are designed to meet contrast targets; SHOULD verify contrast against …
- `must-not` MUST — blanket-adopt Expressive in production. Default to stable M3 color roles; adopt Expressive only behind a flag, on a …

# Material 3 theming on Android

Theme Jetpack Compose UIs through `MaterialTheme`, which exposes three subsystems — `colorScheme`, `typography`, and `shapes`. Drive components from semantic color roles, never raw hex values, so theming, dark mode, and dynamic color all flow automatically. Pin `androidx.compose.material3` to a dated stable version.

## Color roles and ColorScheme

- Components **MUST** consume semantic color roles (`primary`, `onPrimary`, `surface`, `onSurface`, `surfaceContainer`, `error`, `outline`, …), never raw `Color(0xFF…)` literals or app-defined palettes.
- The theme **MUST** provide both a `lightColorScheme()` and a `darkColorScheme()` and select between them based on `isSystemInDarkTheme()`.
- A `ColorScheme` is generated from five key colors (primary, secondary, tertiary, neutral, neutral-variant), each expanded into a 13-tone tonal palette. Generate schemes with the Material Theme Builder rather than hand-authoring every role.
- Read colors at use sites via `MaterialTheme.colorScheme.<role>`. **MUST NOT** read a hard-coded color when a role exists.

## Dynamic color (Material You)

- Dynamic color derives the scheme from the user's wallpaper on Android 12+ (`Build.VERSION_CODES.S`). Treat it as a deliberate decision, not a default — opt in when brand identity allows the OS to drive palette.
- **SHOULD** guard the API level and fall back to your branded scheme:
  ```kotlin
  val scheme = when {
      dynamicColorEnabled && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
          if (dark) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
      dark -> DarkColors
      else -> LightColors
  }
  ```
- When brand color fidelity is a hard requirement, prefer a fixed branded scheme over dynamic color.

## Typography and shape scales

- Use the M3 type scale roles (`displayLarge` … `labelSmall`) via `MaterialTheme.typography.<role>`. **MUST NOT** apply ad-hoc `fontSize`/`fontWeight` where a scale role fits.
- Use the shape scale (`extraSmall` … `extraLarge`) via `MaterialTheme.shapes`. Component corner treatment **SHOULD** come from the scale, not per-component magic numbers.

## Dark theme and accessibility

- Dark support **MUST** be complete: every screen reads `onSurface`/`onSurfaceVariant` for text and the matching dark scheme, with no hard-coded light-only colors.
- Role pairs (`primary`/`onPrimary`, `surface`/`onSurface`) are designed to meet contrast targets; **SHOULD** verify contrast against WCAG 2.1 AA when overriding any role.

## Versioning and Material 3 Expressive (FORECAST)

- Pin the dependency, e.g. `androidx.compose.material3:material3:1.4.x` (stable line as of mid-2026), via the Compose BOM where possible.
- **Material 3 Expressive is NOT stable** (FORECAST). Its APIs (`ExperimentalMaterial3ExpressiveApi`) were removed from the stable 1.4.x line; using Expressive components requires an alpha artifact (e.g. `1.5.0-alphaXX`), and mixing alpha and stable material3 artifacts breaks builds.
- **MUST NOT** blanket-adopt Expressive in production. Default to stable M3 color roles; adopt Expressive only behind a flag, on a pinned alpha, when a concrete UX need justifies the instability.
