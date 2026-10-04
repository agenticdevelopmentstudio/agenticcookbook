
# Typography

The platform's system font MUST be used. Establish a type scale with clear roles — don't invent
sizes ad-hoc.

Platform system fonts:
- **Apple**: SF Pro (iOS/macOS), New York (serif alternative)
- **Android**: Roboto, or system default via Material type system
- **Windows**: Segoe UI Variable
- **Web**: System font stack (`system-ui, -apple-system, sans-serif`)

Defaults when no design system exists:
- **Body text**: 14-17pt (16px is the safest cross-platform default)
- **Minimum readable size**: 11-12pt for captions/labels, text MUST NOT be smaller
- **Line height**: 1.4x-1.5x font size for body text
- **Heading scale**: Use the platform's built-in type scale (Dynamic Type, Material type
  tokens, Fluent type ramp) rather than inventing sizes

General principles:
- Limit to 2-3 font weights per screen (regular, medium/semibold, bold)
- All-caps SHOULD be avoided for more than a few words — harms readability and screen reader experience
- Paragraph width: 45-75 characters for comfortable reading
- See agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility for Dynamic Type / font scaling requirements

References:
- [Apple HIG: Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- [Material Design: Type Scale](https://m3.material.io/styles/typography/type-scale-tokens)
- [Fluent Design: Typography](https://learn.microsoft.com/en-us/windows/apps/design/style/typography)
- [WCAG 1.4.12: Text Spacing](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)

