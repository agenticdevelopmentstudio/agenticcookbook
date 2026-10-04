---
id: f26a9468-a15c-4cd2-b944-d39221e7eee2
title: "Platform Design Languages"
domain: agenticdevelopercookbook://guidelines/cookbook/ui/platform-design-languages
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Canonical platform design sources that cookbook artifacts MUST reference when specifying UI behavior, spacing, and appearance."
platforms:
  - kotlin
  - web
  - windows
tags:
  - platform-design-languages
  - ui
depends-on: []
related: []
references:
  - https://developer.apple.com/design/human-interface-guidelines/
  - https://fluent2.microsoft.design/
  - https://m3.material.io/
  - https://www.w3.org/TR/WCAG21/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - ui-implementation
  - platform-integration
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for cookbook use case — reframe for cookbook artifact authoring |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
