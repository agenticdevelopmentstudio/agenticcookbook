---
id: 27846525-7E10-49F1-B1ED-06840FAF6120
title: "Accessibility"
domain: agenticdevelopercookbook://compliance/accessibility
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for accessibility, assistive technology support, and inclusive design."
platforms: []
tags: [compliance, accessibility]
depends-on: []
related:
  - agenticdevelopercookbook://compliance/platform-compliance
  - agenticdevelopercookbook://compliance/internationalization
  - agenticdevelopercookbook://compliance/performance
references: []
---

# Accessibility

Compliance checks that ensure user interfaces are perceivable, operable, understandable, and robust for all users, including those who rely on assistive technologies. These checks align with WCAG guidelines and platform-specific accessibility standards.

## Applicability

All recipes with a user interface. Guidelines covering UI patterns, interaction design, or visual presentation.

## Checks

### screen-reader-support

All interactive elements MUST be accessible to screen readers with meaningful labels.

**Applies when:** a component renders interactive UI elements (buttons, links, form controls, custom widgets).

**Guidelines:**
- [Accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility)

---

### keyboard-navigable

All functionality MUST be operable via keyboard or equivalent non-pointer input.

**Applies when:** a component provides interactive functionality.

**Guidelines:**
- [Accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility)

---

### dynamic-type-support

Text MUST scale with system font size settings on all platforms.

**Applies when:** a component displays text content.

**Guidelines:**
- [Dynamic Type](agenticdevelopercookbook://guidelines/implementing/accessibility/dynamic-type)
- [Font Scaling](agenticdevelopercookbook://guidelines/implementing/accessibility/font-scaling)

---

### contrast-ratio

Text and interactive elements MUST meet WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text).

**Applies when:** a component renders text or interactive elements with foreground/background color combinations.

**Guidelines:**
- [Accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility)

---

### touch-target-size

Touch and click targets MUST be at least 44x44pt (Apple) or 48x48dp (Android).

**Applies when:** a component renders tappable or clickable elements.

**Guidelines:**
- [Touch and Click Targets](agenticdevelopercookbook://guidelines/implementing/ui/touch-click-targets)

---

### reduced-motion

Animations MUST respect the system reduced-motion preference.

**Applies when:** a component uses animation or motion effects.

**Guidelines:**
- [Accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility)
- [Animation and Motion](agenticdevelopercookbook://guidelines/implementing/ui/animation-motion)

---

### focus-management

Focus MUST be managed logically; modal content MUST trap focus appropriately.

**Applies when:** a component manages focus order, presents modal dialogs, or uses overlays.

**Guidelines:**
- [Accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility)

---

### semantic-markup

Web components MUST use correct ARIA roles, states, and properties.

**Applies when:** a component renders web-based UI using HTML/ARIA.

**Guidelines:**
- [Accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
