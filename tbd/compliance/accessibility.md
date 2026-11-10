---
id: 27846525-7E10-49F1-B1ED-06840FAF6120
title: "Accessibility"
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
  - tbd/compliance/platform-compliance.md
  - tbd/compliance/internationalization.md
  - tbd/compliance/performance.md
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
- [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)

---

### keyboard-navigable

All functionality MUST be operable via keyboard or equivalent non-pointer input.

**Applies when:** a component provides interactive functionality.

**Guidelines:**
- [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)

---

### dynamic-type-support

Text MUST scale with system font size settings on all platforms.

**Applies when:** a component displays text content.

**Guidelines:**
- [adc.guideline.implementing.accessibility.dynamic-type](cookbook:9dae85c5-85ff-4dd1-9bc4-5e923452dba8)
- [adc.guideline.implementing.accessibility.font-scaling](cookbook:01fffa23-5b96-491f-9199-8878cf676683)

---

### contrast-ratio

Text and interactive elements MUST meet WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text).

**Applies when:** a component renders text or interactive elements with foreground/background color combinations.

**Guidelines:**
- [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)

---

### touch-target-size

Touch and click targets MUST be at least 44x44pt (Apple) or 48x48dp (Android).

**Applies when:** a component renders tappable or clickable elements.

**Guidelines:**
- [adc.guideline.implementing.ui.touch-click-targets](cookbook:73b254b4-c611-434a-a9f4-67c8a7155576)

---

### reduced-motion

Animations MUST respect the system reduced-motion preference.

**Applies when:** a component uses animation or motion effects.

**Guidelines:**
- [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)
- [adc.guideline.implementing.ui.animation-motion](cookbook:9f13dbec-cecb-482b-824b-f7d3e341878a)

---

### focus-management

Focus MUST be managed logically; modal content MUST trap focus appropriately.

**Applies when:** a component manages focus order, presents modal dialogs, or uses overlays.

**Guidelines:**
- [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)

---

### semantic-markup

Web components MUST use correct ARIA roles, states, and properties.

**Applies when:** a component renders web-based UI using HTML/ARIA.

**Guidelines:**
- [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
