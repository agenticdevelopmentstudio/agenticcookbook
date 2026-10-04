
- Every theme **MUST** satisfy WCAG 2.2 AA contrast: 4.5:1 normal text, 3:1 large text (18pt+ or 14pt+
  bold) and non-text UI/graphical components.
- Contrast **MUST** be checked for each theme independently — a token pair that passes in light can
  fail in dark or high-contrast. Automate this against the value sets in CI; do not eyeball it.
- Color **MUST NOT** be the sole signal for state (see
  agenticdevelopercookbook://guidelines/implementing/ui/color).

