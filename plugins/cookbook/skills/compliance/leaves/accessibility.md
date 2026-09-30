<!-- leaf: compliance/accessibility · source: compliance/accessibility.md -->

**Rules** (cite as `compliance/accessibility#<slug>`):

- `interactive-elements-accessible-screen-readers-meaningful` MUST — All interactive elements MUST be accessible to screen readers with meaningful labels.
- `functionality-operable-via-keyboard-equivalent` MUST — All functionality MUST be operable via keyboard or equivalent non-pointer input.
- `text-scale-system-font-size` MUST — Text MUST scale with system font size settings on all platforms.
- `text-interactive-elements-meet-wcag-aa-contrast` MUST — Text and interactive elements MUST meet WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text).
- `touch-click-targets-least-44x44pt-apple-48x48dp` MUST — Touch and click targets MUST be at least 44x44pt (Apple) or 48x48dp (Android).
- `animations-respect-system-reduced-motion` MUST — Animations MUST respect the system reduced-motion preference.
- `focus-managed-logically-modal-content` MUST — Focus MUST be managed logically; modal content MUST trap focus appropriately.
- `web-components-use-correct-aria-roles` MUST — Web components MUST use correct ARIA roles, states, and properties.

# Accessibility

Compliance checks that ensure user interfaces are perceivable, operable, understandable, and robust for all users, including those who rely on assistive technologies. These checks align with WCAG guidelines and platform-specific accessibility standards.

## Applicability

All recipes with a user interface. Guidelines covering UI patterns, interaction design, or visual presentation.

## Checks

### screen-reader-support

All interactive elements MUST be accessible to screen readers with meaningful labels.

**Applies when:** a component renders interactive UI elements (buttons, links, form controls, custom widgets).

**Guidelines:**
- Accessibility

---

### keyboard-navigable

All functionality MUST be operable via keyboard or equivalent non-pointer input.

**Applies when:** a component provides interactive functionality.

**Guidelines:**
- Accessibility

---

### dynamic-type-support

Text MUST scale with system font size settings on all platforms.

**Applies when:** a component displays text content.

**Guidelines:**
- Dynamic Type
- Font Scaling

---

### contrast-ratio

Text and interactive elements MUST meet WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text).

**Applies when:** a component renders text or interactive elements with foreground/background color combinations.

**Guidelines:**
- Accessibility

---

### touch-target-size

Touch and click targets MUST be at least 44x44pt (Apple) or 48x48dp (Android).

**Applies when:** a component renders tappable or clickable elements.

**Guidelines:**
- Touch and Click Targets

---

### reduced-motion

Animations MUST respect the system reduced-motion preference.

**Applies when:** a component uses animation or motion effects.

**Guidelines:**
- Accessibility
- Animation and Motion

---

### focus-management

Focus MUST be managed logically; modal content MUST trap focus appropriately.

**Applies when:** a component manages focus order, presents modal dialogs, or uses overlays.

**Guidelines:**
- Accessibility

---

### semantic-markup

Web components MUST use correct ARIA roles, states, and properties.

**Applies when:** a component renders web-based UI using HTML/ARIA.

**Guidelines:**
- Accessibility
