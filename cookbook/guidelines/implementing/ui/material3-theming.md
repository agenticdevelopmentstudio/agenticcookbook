---
id: 1e7f8c3d-ece9-4c5c-b7ca-7703391995dd
title: "Material 3 theming on Android"
domain: agenticdevelopercookbook://guidelines/implementing/ui/material3-theming
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Theme Compose UIs with Material 3 color roles, ColorScheme, type and shape scales, and full dark support."
platforms:
  - kotlin
tags:
  - android
  - material
  - theming
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/ui/theming
  - agenticdevelopercookbook://guidelines/implementing/ui/color
references:
  - https://m3.material.io/
  - https://blog.google/products-and-platforms/platforms/android/material-3-expressive-android-wearos-launch/
  - https://developer.android.com/jetpack/androidx/releases/compose-material3
  - https://developer.android.com/develop/ui/compose/designsystems/material3
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - ui-implementation
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
