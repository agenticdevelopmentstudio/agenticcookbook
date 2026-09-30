<!-- leaf: implement-ui/theming-with-tokens · source: guidelines/implementing/ui/theming-with-tokens.md -->

**Rules** (cite as `implement-ui/theming-with-tokens#<slug>`):

- `components-consume-only-semantic-component` MUST — Components MUST consume only semantic (or component) tokens, never primitives or hard-coded literals. This is what …
- `theme-authored-value-set-rebinds` SHOULD — Each theme SHOULD be authored as a value set that rebinds every semantic token — same keys, different primitive …
- `theme-switching-single-state-change-swap` MUST — Theme switching MUST be a single state change (swap the set), not per-component conditionals.
- `semantic-token-defined-theme-missing-key` MUST — Every semantic token MUST be defined in every theme. A missing key is a defect — fail fast in a build/test check rather …
- `app-honor-os-theme-default` MUST — The app MUST honor the OS theme by default (prefers-color-scheme, UITraitCollection.userInterfaceStyle, …
- `increase-contrast-theme-respond-system-signal-prefers` MUST — Provide a high-contrast / increase-contrast theme and MUST respond to the system signal (prefers-contrast: more, …
- `theme-satisfy-wcag-aa-contrast` MUST — Every theme MUST satisfy WCAG 2.2 AA contrast: 4.5:1 normal text, 3:1 large text (18pt+ or 14pt+ bold) and non-text …
- `contrast-checked-theme-independently-token` MUST — Contrast MUST be checked for each theme independently — a token pair that passes in light can fail in dark or …
- `color-not-sole-signal-state-see` MUST — Color MUST NOT be the sole signal for state (see agenticdevelopercookbook://guidelines/implementing/ui/color).

# Theming with tokens

A theme is just an alternate set of values for the same semantic tokens. Components read semantic
tokens, so switching the active value set re-themes the whole UI automatically — you never edit
component code to add a theme.

## The token layering model

Keep three tiers so themes only rebind the middle one:

| Tier | Example | Themed? |
|------|---------|---------|
| **Primitive** (raw scale) | `blue-600 = #2563EB` | No — a fixed palette |
| **Semantic** (role) | `color.text.primary`, `color.surface.raised` | Yes — each theme maps it to a primitive |
| **Component** (optional) | `button.primary.background` | Aliases a semantic token |

- Components **MUST** consume only semantic (or component) tokens, never primitives or hard-coded
  literals. This is what makes theming automatic.
- Each theme **SHOULD** be authored as a value set that rebinds every semantic token — same keys,
  different primitive references. Light, dark, and high-contrast are sibling sets, not branches in code.

## Switching the active set

- Resolve tokens at a single boundary: a CSS custom-property scope (`:root[data-theme]`,
  `@media (prefers-color-scheme)`), a SwiftUI `Environment`/asset catalog, a Compose
  `MaterialTheme`/`CompositionLocal`, or a WinUI `ResourceDictionary` theme dictionary.
- Theme switching **MUST** be a single state change (swap the set), not per-component conditionals.
- Every semantic token **MUST** be defined in every theme. A missing key is a defect — fail fast in a
  build/test check rather than falling back silently.

## Respect the system and accessibility settings

- The app **MUST** honor the OS theme by default (`prefers-color-scheme`,
  `UITraitCollection.userInterfaceStyle`, `isSystemInDarkTheme()`, `RequestedTheme`), and **SHOULD**
  offer an explicit override.
- Provide a **high-contrast / increase-contrast** theme and **MUST** respond to the system signal
  (`prefers-contrast: more`, `forced-colors`/Windows High Contrast,
  `UIAccessibility.isDarkerSystemColorsEnabled`, `accessibilityHighContrast`).
- Under forced-colors / Windows High Contrast, defer to system colors; do not override them.

## Verify contrast per theme

- Every theme **MUST** satisfy WCAG 2.2 AA contrast: 4.5:1 normal text, 3:1 large text (18pt+ or 14pt+
  bold) and non-text UI/graphical components.
- Contrast **MUST** be checked for each theme independently — a token pair that passes in light can
  fail in dark or high-contrast. Automate this against the value sets in CI; do not eyeball it.
- Color **MUST NOT** be the sole signal for state (see
  agenticdevelopercookbook://guidelines/implementing/ui/color).

## Notes

- Pin the token spec: align names/types to the W3C Design Tokens Community Group Format Module,
  whose first stable version is **2025.10** (designtokens.org). It continues to evolve, so pin to a
  dated revision and isolate the parser/build step so a spec update is a localized change.
- Adopt a token build pipeline (e.g., Style Dictionary) only when measured need justifies it — a small
  app may hand-author per-platform value sets (per YAGNI).

References:
- [Design Tokens Community Group](https://www.designtokens.org/)
- [Design Tokens spec — first stable version (2025.10)](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [WCAG 2.2 — 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [WCAG 2.2 — 1.4.11: Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
