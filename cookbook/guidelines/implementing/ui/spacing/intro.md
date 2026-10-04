
# Spacing

Use a consistent spatial scale based on a **4px base unit** (8px primary grid). All spacing,
padding, and margin values MUST be multiples of 4. This aligns with Apple HIG, Material
Design, and Fluent Design.

Default spacing scale: **4, 8, 12, 16, 24, 32, 48, 64**

- **4px** — tight spacing within compact elements (icon-to-label, badge padding)
- **8px** — default inner padding, spacing between related items
- **12px** — padding within cards or list items
- **16px** — standard content padding from screen/container edges
- **24px** — separation between content groups
- **32-64px** — major section separation

Arbitrary values (5px, 13px, 37px) SHOULD be avoided. If a value isn't on the scale, reconsider.

References:
- [Apple HIG: Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Material Design: Layout](https://m3.material.io/foundations/layout/overview)
- [Fluent Design: Layout](https://learn.microsoft.com/en-us/windows/apps/design/layout/)

