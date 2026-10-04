
# Touch & Click Targets

Interactive elements MUST be large enough to tap or click accurately. Defer to the platform
HIG first — each prescribes its own minimum:

| Platform | Minimum Target | Recommended |
|----------|---------------|-------------|
| Apple (iOS) | 44x44 pt | 44x44 pt |
| Android (Material) | 48x48 dp | 48x48 dp |
| Windows (Fluent) | 32x32 epx | 40x40 epx |
| Web (WCAG AA) | 24x24 CSS px | 44x44 CSS px |

**Cross-platform default: 44x44** when no platform HIG applies.

- The visual element (icon, text) can be smaller than the touch target — pad the hit area
- There MUST be minimum **8px spacing** between adjacent targets to prevent mis-taps
- Inline text links in paragraphs are exempt from size minimums but should have sufficient
  line height for comfortable tapping

See agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility for full accessibility requirements.

References:
- [Apple HIG: Accessibility — User Interaction](https://developer.apple.com/design/human-interface-guidelines/accessibility#User-interaction)
- [Material Design: Accessibility Basics](https://m3.material.io/foundations/accessible-design/accessibility-basics)
- [Fluent Design: Targeting Guidelines](https://learn.microsoft.com/en-us/windows/apps/design/input/guidelines-for-targeting)
- [WCAG 2.5.8: Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

