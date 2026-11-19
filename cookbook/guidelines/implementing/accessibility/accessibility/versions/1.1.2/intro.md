
# Accessibility from day one

All components MUST integrate with platform accessibility APIs from initial implementation:

1. Semantic roles and labels on all interactive elements
2. VoiceOver (Apple) / TalkBack (Android) / screen reader (Web) full support
3. Keyboard and switch control navigation
4. Dynamic Type / font scaling — layouts MUST NOT break at larger text sizes
5. WCAG AA minimum contrast (4.5:1 for text, 3:1 for large text)
6. Meaningful focus order following visual layout

Platform-specific tooling:
- **Windows**: UI Automation patterns, Narrator testing, [Accessibility Insights](https://accessibilityinsights.io/), minimum 40x40 epx recommended touch targets

# Respect accessibility display options

Components MUST respond to platform accessibility and display settings including reduced motion, high contrast, color inversion, bold text, and grayscale. See platform-specific files for the full list of settings and environment keys.

---

# Accessibility

All components MUST integrate with platform accessibility APIs from initial implementation. Requirements:

1. Semantic roles and labels on all interactive elements
2. Screen reader full support (VoiceOver, TalkBack, Narrator, ARIA)
3. Keyboard and switch control navigation
4. Dynamic Type / font scaling — layouts MUST NOT break at larger text sizes
5. WCAG AA minimum contrast (4.5:1 for text, 3:1 for large text)
6. Meaningful focus order following visual layout
7. Components MUST respond to platform accessibility and display settings including reduced motion, high contrast, color inversion, bold text, and grayscale

