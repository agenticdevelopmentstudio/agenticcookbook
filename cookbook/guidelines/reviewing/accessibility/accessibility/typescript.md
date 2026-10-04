
### Standards

1. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — minimum AA conformance for all components. WCAG 2.2 is the current W3C Recommendation and supersedes 2.1; honor its new AA criteria: focus not obscured, focus appearance, a single-pointer alternative to dragging movements, **target size minimum 24×24 CSS px** (reconcile with the 44pt target in [touch-click-targets](agenticdevelopercookbook://guidelines/reviewing/ui/touch-click-targets) — 44pt is the stricter Apple guidance), consistent help, redundant entry, and accessible authentication (no cognitive-function test). Treat WCAG 3.0 as a horizon Working Draft, not yet actionable.
2. [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) — correct ARIA roles, states, and properties.

### CSS Media Queries

Components MUST respond to these user preferences:

| Setting | Media Query | Action |
|---------|-------------|--------|
| Reduced Motion | `prefers-reduced-motion: reduce` | Disable/simplify CSS animations and JS transitions |
| High Contrast | `prefers-contrast: more` | Increase border widths, use higher-contrast colors |
| Forced Colors | `forced-colors: active` | Respect system color palette (Windows High Contrast) |
| Dark Mode | `prefers-color-scheme: dark` | Full dark theme support |
| Reduced Transparency | `prefers-reduced-transparency: reduce` | Use opaque backgrounds |
| Reduced Data | `prefers-reduced-data: reduce` | Lazy-load images, reduce asset sizes |

Screen reader support: use ARIA roles, `aria-live` for dynamic content, proper landmark regions.

