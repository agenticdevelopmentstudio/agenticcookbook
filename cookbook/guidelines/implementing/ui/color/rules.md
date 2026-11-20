
- **should-use-semantic-color-tokens**: **Semantic color tokens** — platforms' semantic colors SHOULD be used (e.g., `TextFillColorPrimary`,
  `label`, `onSurface`) rather than hard-coded hex values. They adapt to theme and accessibility
  settings automatically.
- **should-limit-the-palette**: **Limit the palette** — the palette SHOULD be limited to 1 primary/accent color, 1-2 neutral tones, plus semantic colors for
  success/warning/error. Rainbow UIs SHOULD be avoided.
- **must-not-rely-on-color-alone**: **Not color alone** — color MUST be paired with a secondary indicator (icon, shape, text, pattern)
  for state changes, errors, and status.
- **must-meet-contrast-minimums**: **Contrast minimums** — text and non-text UI components MUST meet the WCAG AA contrast minimums (per [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)) in *Contrast minimums*.
- **must-work-in-light-and-dark**: **Dark mode** — every color MUST work in both light and dark themes.
- **should-test-light-and-dark**: Both light and dark themes SHOULD be tested.
