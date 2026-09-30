<!-- leaf: implement-ui/color · source: guidelines/implementing/ui/color.md -->

**Rules** (cite as `implement-ui/color#<slug>`):

- `semantic-color-tokens` SHOULD — platforms' semantic colors SHOULD be used (e.g., TextFillColorPrimary, label, onSurface) rather than hard-coded hex …
- `not-color-alone` MUST — color MUST be paired with a secondary indicator (icon, shape, text, pattern) for state changes, errors, and status.
- `dark-mode` MUST — every color MUST work in both light and dark themes. Test both.

# Color

Use color with intention — never as the sole means of conveying information.

- **Semantic color tokens** — platforms' semantic colors SHOULD be used (e.g., `TextFillColorPrimary`,
  `label`, `onSurface`) rather than hard-coded hex values. They adapt to theme and accessibility
  settings automatically.
- **Limit the palette** — 1 primary/accent color, 1-2 neutral tones, plus semantic colors for
  success/warning/error. Avoid rainbow UIs.
- **Not color alone** — color MUST be paired with a secondary indicator (icon, shape, text, pattern)
  for state changes, errors, and status.
- **Contrast minimums** (WCAG AA, per agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility):

| Element | AA Minimum | AAA Enhanced |
|---------|-----------|-------------|
| Normal text (<18pt / <14pt bold) | 4.5:1 | 7:1 |
| Large text (18pt+ or 14pt+ bold) | 3:1 | 4.5:1 |
| Non-text UI components | 3:1 | — |

- **Dark mode** — every color MUST work in both light and dark themes. Test both.

References:
- [WCAG 1.4.3: Contrast Minimum](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [WCAG 1.4.11: Non-text Contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html)
- [Apple HIG: Color](https://developer.apple.com/design/human-interface-guidelines/color)
- [Material Design: Color System](https://m3.material.io/styles/color/system/how-the-system-works)
- [Fluent Design: Color](https://learn.microsoft.com/en-us/windows/apps/design/style/color)
