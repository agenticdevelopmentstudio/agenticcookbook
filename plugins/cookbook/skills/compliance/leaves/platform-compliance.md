<!-- leaf: compliance/platform-compliance · source: compliance/platform-compliance.md -->

**Rules** (cite as `compliance/platform-compliance#<slug>`):

- `ui-follow-platform-native-design` MUST — UI MUST follow the platform's native design language (HIG, Material, Fluent).
- `standard-ui-patterns-use-native-platform-controls` SHOULD — Standard UI patterns SHOULD use native platform controls before custom implementations.
- `interactive-elements-meet-platform-specific-minimum` MUST — Interactive elements MUST meet platform-specific minimum touch target sizes.
- `features-addressable-content-support-platform-deep-linking` MUST — Features with addressable content MUST support platform deep linking conventions.
- `features-request-only-minimum-platform` MUST — Features MUST request only the minimum platform permissions required.
- `ios-macos-recipes-comply-apple-app-store` MUST — iOS/macOS recipes MUST comply with Apple App Store Review Guidelines.
- `android-recipes-comply-google-play-developer` MUST — Android recipes MUST comply with Google Play Developer Program Policies.
- `components-support-platform-theming-dark` MUST — Components MUST support platform theming (dark mode, high contrast, accent colors).

# Platform Compliance

Compliance checks that ensure components respect platform-specific design languages, conventions, and distribution policies. These checks promote native-feeling experiences and smooth app store approval across Apple, Android, Windows, and web platforms.

## Applicability

All recipes targeting a specific platform. Guidelines covering platform-specific patterns or UI design.

## Checks

### platform-design-language

UI MUST follow the platform's native design language (HIG, Material, Fluent).

**Applies when:** a component renders user interface on a specific platform.

**Guidelines:**
- Platform Design Languages

---

### native-controls-preference

Standard UI patterns SHOULD use native platform controls before custom implementations.

**Applies when:** a component implements common UI patterns (lists, navigation, dialogs, pickers).

**Guidelines:**
- Native Controls

---

### platform-touch-targets

Interactive elements MUST meet platform-specific minimum touch target sizes.

**Applies when:** a component renders tappable or clickable elements on mobile or touch-enabled platforms.

**Guidelines:**
- Touch and Click Targets

---

### deep-linking-support

Features with addressable content MUST support platform deep linking conventions.

**Applies when:** a component presents content that should be navigable via external links.

**Guidelines:**
- Deep Linking

---

### platform-permissions

Features MUST request only the minimum platform permissions required.

**Applies when:** a recipe requires system capabilities (camera, location, contacts, etc.).

---

### app-store-guidelines

iOS/macOS recipes MUST comply with Apple App Store Review Guidelines.

**Applies when:** a recipe targets Apple platforms.

---

### play-store-policies

Android recipes MUST comply with Google Play Developer Program Policies.

**Applies when:** a recipe targets Android/Google Play.

---

### platform-theming

Components MUST support platform theming (dark mode, high contrast, accent colors).

**Applies when:** a component renders UI that should adapt to system appearance settings.

**Guidelines:**
- Theming
- Color
