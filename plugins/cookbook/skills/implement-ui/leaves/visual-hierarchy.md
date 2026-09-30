<!-- leaf: implement-ui/visual-hierarchy · source: guidelines/implementing/ui/visual-hierarchy.md -->

**Rules** (cite as `implement-ui/visual-hierarchy#<slug>`):

- `one-primary-action-per-screen` MUST — there MUST be a single focal point; if everything is bold, nothing is bold
- `interactive-elements-visually-distinguishable-from-static` MUST — Interactive elements MUST be visually distinguishable from static content
- `disabled-elements-visually-muted-but-still` SHOULD — Disabled elements SHOULD be visually muted but still discoverable

# Visual Hierarchy

Establish clear importance through size, weight, color, and spacing. Every screen should
have one obvious focal point — the primary action or content the user came for.

- **One primary action per screen** — there MUST be a single focal point; if everything is bold, nothing is bold
- Use size and weight (not just color) to distinguish heading levels
- Group related content with proximity; separate unrelated content with whitespace
- Interactive elements MUST be visually distinguishable from static content
- Disabled elements SHOULD be visually muted but still discoverable

See agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility for accessibility requirements (contrast, labels, focus order).

References:
- [NNGroup: Visual Hierarchy](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)
- [Apple HIG: Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Material Design: Applying Layout](https://m3.material.io/foundations/layout/applying-layout/overview)
- [Fluent Design: Layout](https://learn.microsoft.com/en-us/windows/apps/design/layout/)
