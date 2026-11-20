
- **must-not-edit-component-code-to-add-a-theme**: Adding a theme MUST NOT require editing component code — you never edit component code to add a theme.
- **should-keep-three-token-tiers**: SHOULD keep three tiers (primitive, semantic, component) so themes only rebind the middle one.
- **must-consume-only-semantic-tokens**: Components **MUST** consume only semantic (or component) tokens, never primitives or hard-coded literals. This is what makes theming automatic.
- **should-author-themes-as-value-sets**: Each theme **SHOULD** be authored as a value set that rebinds every semantic token — same keys, different primitive references. Light, dark, and high-contrast are sibling sets, not branches in code.
- **should-resolve-tokens-at-a-single-boundary**: SHOULD resolve tokens at a single boundary: a CSS custom-property scope (`:root[data-theme]`, `@media (prefers-color-scheme)`), a SwiftUI `Environment`/asset catalog, a Compose `MaterialTheme`/`CompositionLocal`, or a WinUI `ResourceDictionary` theme dictionary.
- **must-switch-theme-as-a-single-state-change**: Theme switching **MUST** be a single state change (swap the set), not per-component conditionals.
- **must-define-every-token-in-every-theme**: Every semantic token **MUST** be defined in every theme.
- **should-fail-fast-on-a-missing-token**: A missing key is a defect — SHOULD fail fast in a build/test check rather than falling back silently.
- **must-honor-os-theme-by-default**: The app **MUST** honor the OS theme by default (`prefers-color-scheme`,
  `UITraitCollection.userInterfaceStyle`, `isSystemInDarkTheme()`, `RequestedTheme`), and **SHOULD**
  offer an explicit override.
- **must-respond-to-system-contrast-signal**: SHOULD provide a **high-contrast / increase-contrast** theme and **MUST** respond to the system signal (`prefers-contrast: more`, `forced-colors`/Windows High Contrast, `UIAccessibility.isDarkerSystemColorsEnabled`, `accessibilityHighContrast`).
- **should-defer-to-system-colors-under-forced-colors**: Under forced-colors / Windows High Contrast, SHOULD defer to system colors and SHOULD NOT override them.
- **must-meet-wcag-aa-contrast-in-every-theme**: Every theme **MUST** satisfy WCAG 2.2 AA contrast: 4.5:1 normal text, 3:1 large text (18pt+ or 14pt+ bold) and non-text UI/graphical components.
- **must-check-contrast-per-theme**: Contrast **MUST** be checked for each theme independently — a token pair that passes in light can fail in dark or high-contrast.
- **should-automate-contrast-checks-in-ci**: SHOULD automate this (the per-theme contrast check) against the value sets in CI; SHOULD NOT eyeball it.
- **must-not-use-color-as-sole-state-signal**: Color **MUST NOT** be the sole signal for state (see [adc.guideline.implementing.ui.color](cookbook:e547d962-d561-4bd9-bb5a-50bdeec98335)).
- **should-align-tokens-to-dtcg-format**: SHOULD pin the token spec: align names/types to the W3C Design Tokens Community Group Format Module, whose first stable version is **2025.10** (designtokens.org).
- **should-pin-dated-spec-revision-and-isolate-parser**: The spec continues to evolve, so SHOULD pin to a dated revision and isolate the parser/build step so a spec update is a localized change.
- **should-adopt-token-pipeline-only-on-measured-need**: SHOULD adopt a token build pipeline (e.g., Style Dictionary) only when measured need justifies it.
- **may-hand-author-value-sets-in-small-apps**: A small app MAY hand-author per-platform value sets (per YAGNI).
