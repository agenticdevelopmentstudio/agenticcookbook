<!-- leaf: cookbook-ui/platform-design-languages · source: guidelines/cookbook/ui/platform-design-languages.md -->

**Rules** (cite as `cookbook-ui/platform-design-languages#<slug>`):

- `sources-cookbook-artifacts-not-specify-values-contradict-platform` MUST — When writing UI ingredients or recipes, refer to these canonical platform design sources. Cookbook artifacts MUST NOT …

# Platform Design Languages

When writing UI ingredients or recipes, refer to these canonical platform design sources. Cookbook artifacts MUST NOT specify values that contradict the platform HIG.

## Canonical sources

- **Apple**: [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- **Android**: [Material Design 3](https://m3.material.io/)
- **Windows**: [Fluent 2 Design System](https://fluent2.microsoft.design/)
- **Web**: [WCAG 2.1](https://www.w3.org/TR/WCAG21/) + platform-appropriate system

## How this applies to cookbook authoring

- When specifying spacing, type sizes, or target sizes in an ingredient's Appearance section, defer to the platform HIG. If the platform prescribes a value, use it.
- When the HIG has no opinion, specify a cross-platform default and note it as such.
- In the Platform Notes section of an ingredient, list any platform-specific overrides with links to the relevant HIG section.
