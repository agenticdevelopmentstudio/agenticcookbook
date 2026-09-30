<!-- leaf: implement-ui/iconography · source: guidelines/implementing/ui/iconography.md -->

**Rules** (cite as `implement-ui/iconography#<slug>`):

- `native-icon-set-used-first-sf-symbols` SHOULD — The platform's native icon set SHOULD be used first (SF Symbols, Material Symbols, Segoe Fluent Icons)
- `icons-accompanying-actions-have-text-label-accessible` MUST — All icons accompanying actions MUST have a text label or accessible name
- `error-success-warning-paired-color-shape-see` MUST — Icons conveying state (error, success, warning) MUST be paired with color AND shape — see Color section

# Iconography

Icons supplement text — they do not replace it (except for universally understood symbols
like play, pause, close, and search).

- The platform's native icon set SHOULD be used first (SF Symbols, Material Symbols, Segoe Fluent Icons)
- All icons accompanying actions MUST have a text label or accessible name
- Maintain consistent size and weight across the UI — don't mix outlined and filled styles
  without intention (e.g., filled = selected, outlined = unselected)
- Minimum icon size: 16x16pt for decorative, 24x24pt for interactive (see Touch & Click Targets
  for the full hit area)
- Icons conveying state (error, success, warning) MUST be paired with color AND shape —
  see Color section

References:
- [Apple HIG: SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)
- [Material Design: Icons](https://m3.material.io/styles/icons/overview)
- [Fluent Design: Icons](https://learn.microsoft.com/en-us/windows/apps/design/style/icons)
