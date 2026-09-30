<!-- leaf: implement-ui/cross-platform-token-adaptation · source: guidelines/implementing/ui/cross-platform-token-adaptation.md -->

**Rules** (cite as `implement-ui/cross-platform-token-adaptation#<slug>`):

- `md-font-body-platform-neutral-shared-typically` MUST — The semantic token source (e.g., color.surface.primary, space.md, font.body) MUST be platform-neutral and shared — …
- `tokens-carry-semantic-names-tied` MUST — Tokens MUST carry semantic names tied to intent, not raw values; map base → semantic → component layers so a single …
- `platform-specific-overrides-live-transforms-aliases-over` SHOULD — Platform-specific overrides SHOULD live as transforms or aliases over the shared source, never as a forked copy of it.
- `dimension-tokens-emitted-target-density-independent` MUST — Dimension tokens MUST be emitted in the target's density-independent unit; numeric values usually stay equal (8 → 8pt / …
- `type-sizes-map-sp-android-rem` MUST — Type sizes SHOULD map to sp on Android and rem on the web so they grow with user accessibility settings; pixel-locking …
- `hairline-borders-resolve-smallest-crisp-value` SHOULD — Hairline borders SHOULD resolve to the smallest crisp value per device scale rather than a fixed 1px.
- `clamp-rem-steps-prefer-native-scale-over` SHOULD — Map the shared type scale onto each platform's native ramp (Apple Dynamic Type text styles, Material 3 type scale, web …
- `color-tokens-carry-light-dark-high` MUST — Color tokens MUST carry light/dark (and high-contrast where supported) variants; emit platform-native color resources …
- `wide-gamut-color-expressed-device-independent-space` SHOULD — Wide-gamut color SHOULD be expressed in a device-independent space (e.g., Display P3 / OKLCH — both standardized in …
- `tokens-duration-easing-map-platform-standard-curves` SHOULD — Motion tokens (duration, easing) SHOULD map to each platform's standard curves and respect reduced-motion settings; do …
- `component-level-tokens-diverge-per-platform-corner` MAY — Component-level tokens MAY diverge per platform (e.g., corner radius, elevation vs. shadow) while sharing the same …

# Cross-platform token adaptation

Keep the semantic token source shared across every target, then adapt its values to each platform's native unit system, typography scale, and motion conventions. Share intent; render with native units and idioms rather than copying one platform's values verbatim.

## Source of truth

- The semantic token source (e.g., `color.surface.primary`, `space.md`, `font.body`) **MUST** be platform-neutral and shared — typically a single JSON/DTCG file that platform builds transform.
- Use the W3C Design Tokens Community Group format (DTCG), which reached its first stable version, [2025.10](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/), in October 2025; pin to a dated revision so one source feeds Style Dictionary or an equivalent transform per platform. See <https://www.designtokens.org/>.
- Tokens **MUST** carry semantic names tied to intent, not raw values; map base → semantic → component layers so a single base change cascades.
- Platform-specific overrides **SHOULD** live as transforms or aliases over the shared source, never as a forked copy of it.

## Unit adaptation

Adapt the same numeric intent to each platform's density-independent unit. Do not ship raw `px` everywhere.

| Platform | Length unit | Type unit | Notes |
|----------|-------------|-----------|-------|
| Apple (Swift/SwiftUI) | points (pt) | pt | Points scale by `@1x/2x/3x`; honor Dynamic Type |
| Android (Kotlin/Compose) | `dp` | `sp` | `sp` respects the user font-size setting |
| Web (TypeScript) | `rem` for type/space, `px` for hairlines | `rem` | `rem` honors the user's root font size |
| Windows (C#/WinUI) | effective pixels (epx) | epx | epx is already density-scaled |

- Dimension tokens **MUST** be emitted in the target's density-independent unit; numeric values usually stay equal (8 → 8pt / 8dp / 0.5rem) but the unit and scaling semantics differ.
- Type sizes **SHOULD** map to `sp` on Android and `rem` on the web so they grow with user accessibility settings; pixel-locking text **MUST NOT** be the default.
- Hairline borders **SHOULD** resolve to the smallest crisp value per device scale rather than a fixed `1px`.

## Typography, color, and motion

- Map the shared type scale onto each platform's native ramp (Apple Dynamic Type text styles, Material 3 type scale, web `clamp()`/`rem` steps) — **SHOULD** prefer the native scale over forcing one platform's sizes onto another.
- Color tokens **MUST** carry light/dark (and high-contrast where supported) variants; emit platform-native color resources (asset catalogs, Compose `ColorScheme`, CSS custom properties, WinUI `ThemeResource`).
- Wide-gamut color **SHOULD** be expressed in a device-independent space (e.g., Display P3 / OKLCH — both standardized in DTCG 2025.10's color type) and degraded to sRGB where the target lacks gamut support.
- Motion tokens (duration, easing) **SHOULD** map to each platform's standard curves and respect reduced-motion settings; do not hardcode one platform's spring or duration as universal.

## Respect the platform design language

- Adapt to the host idiom — navigation patterns, control shapes, default density, and haptics — rather than forcing one platform's look onto another. See `agenticdevelopercookbook://guidelines/planning/ui/platform-design-languages`.
- Component-level tokens **MAY** diverge per platform (e.g., corner radius, elevation vs. shadow) while sharing the same semantic ancestor.
- Centralized design-system tooling (token build pipelines, multi-target generators) is an adopt-when-measured-need-justifies investment (per YAGNI): start with a single shared file and per-platform transforms; add heavier infrastructure only when token volume or platform count makes it pay off.
