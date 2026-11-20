
### All platforms

- **must-integrate-accessibility-apis-from-day-one**: All components MUST integrate with platform accessibility APIs from initial implementation; the requirements of that integration are the rules that follow.
- **must-give-interactive-elements-semantic-roles-and-labels**: Semantic roles and labels MUST be on all interactive elements.
- **must-fully-support-screen-readers**: Components MUST give full screen reader support: VoiceOver (Apple), TalkBack (Android), Narrator (Windows) and screen readers via ARIA (Web).
- **must-support-keyboard-and-switch-control**: Components MUST support keyboard and switch control navigation.
- **must-not-break-at-larger-text-sizes**: Dynamic Type / font scaling — layouts MUST NOT break at larger text sizes
- **must-meet-wcag-aa-contrast**: Components MUST meet WCAG AA minimum contrast (4.5:1 for text, 3:1 for large text).
- **must-follow-visual-layout-focus-order**: Components MUST have a meaningful focus order following visual layout.
- **must-respond-to-display-settings**: Components MUST respond to platform accessibility and display settings including reduced motion, high contrast, color inversion, bold text, and grayscale — they respect accessibility display options.
  - See platform-specific files for the full list of settings and environment keys.

### Swift

- **must-respond-to-swiftui-environment-values**: Components MUST respond to these SwiftUI environment values, taking the action the Swift table gives for each: Reduce Motion, Reduce Transparency, Differentiate Without Color, Increase Contrast, Invert Colors, Cross-Fade Transitions.

### Kotlin

- **must-respond-to-android-accessibility-settings**: Components MUST respond to these Android accessibility settings, taking the action the Kotlin table gives for each: Remove Animations, Font Scale, High Contrast Text, Color Inversion, TalkBack, Switch Access, Dark Theme, Display Size.

### Standards

- **should-meet-wcag-2-2-aa**: Web (TypeScript) components SHOULD meet WCAG 2.2 minimum AA conformance — all components. WCAG 2.2 is the current W3C Recommendation and supersedes 2.1.
- **should-honor-wcag-2-2-new-aa-criteria**: Components SHOULD honor WCAG 2.2's new AA criteria: focus not obscured, focus appearance, a single-pointer alternative to dragging movements, **target size minimum 24×24 CSS px** (reconcile with the 44pt target in [adc.guideline.implementing.ui.touch-click-targets](cookbook:73b254b4-c611-434a-a9f4-67c8a7155576) — 44pt is the stricter Apple guidance), consistent help, redundant entry, and accessible authentication (no cognitive-function test).
- **should-treat-wcag-3-as-not-yet-actionable**: Authors SHOULD treat WCAG 3.0 as a horizon Working Draft, not yet actionable.
- **should-follow-wai-aria-authoring-practices**: Components SHOULD follow the WAI-ARIA Authoring Practices: correct ARIA roles, states, and properties.
### CSS Media Queries

- **must-respond-to-css-user-preferences**: Web (TypeScript) components MUST respond to these user preferences, taking the action the TypeScript table gives for each CSS media query: Reduced Motion, High Contrast, Forced Colors, Dark Mode, Reduced Transparency, Reduced Data.
- **should-support-screen-readers-with-aria**: Web screen reader support SHOULD use ARIA roles, `aria-live` for dynamic content, and proper landmark regions.

### Windows

- **should-set-automation-name-on-unlabeled-elements**: Components SHOULD set `AutomationProperties.Name` on interactive elements that lack visible text labels.
- **should-use-labeled-by-for-form-fields**: Form fields SHOULD use `AutomationProperties.LabeledBy`.
- **should-use-live-setting-for-dynamic-regions**: Dynamic content regions SHOULD use `AutomationProperties.LiveSetting`.
- **must-not-hard-code-colors**: High contrast support is automatic when using `ThemeResource` — components MUST NOT hard-code colors.
- **should-test-with-accessibility-insights**: Components SHOULD be tested with [Accessibility Insights for Windows](https://accessibilityinsights.io/).
- **must-make-elements-keyboard-reachable**: Keyboard navigation: all interactive elements MUST be reachable via Tab, actionable via Enter/Space.
- **should-use-40-epx-touch-targets**: Windows touch targets SHOULD be a minimum of 40x40 epx, as recommended.
- **must-respond-to-windows-accessibility-settings**: Components MUST respond to these Windows accessibility settings, taking the action the Windows table gives for each: High Contrast, Animations Disabled, Text Scaling, Color Filters, Narrator, Keyboard Navigation, Dark Theme, Caret Browsing.
