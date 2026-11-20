
- Map the shared type scale onto each platform's native ramp (Apple Dynamic Type text styles, Material 3 type scale, web `clamp()`/`rem` steps) — **SHOULD** prefer the native scale over forcing one platform's sizes onto another.
- Color tokens **MUST** carry light/dark (and high-contrast where supported) variants; emit platform-native color resources (asset catalogs, Compose `ColorScheme`, CSS custom properties, WinUI `ThemeResource`).
- Wide-gamut color **SHOULD** be expressed in a device-independent space (e.g., Display P3 / OKLCH — both standardized in DTCG 2025.10's color type) and degraded to sRGB where the target lacks gamut support.
- Motion tokens (duration, easing) **SHOULD** map to each platform's standard curves and respect reduced-motion settings; do not hardcode one platform's spring or duration as universal.

