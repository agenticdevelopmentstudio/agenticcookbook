---
id: 9D54950C-FED8-40DA-8F68-B01508884D6C
title: "Platform Compliance"
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for platform-specific design, conventions, and store policies."
platforms: []
tags: [compliance, platform]
depends-on: []
related:
  - tbd/compliance/accessibility.md
  - tbd/compliance/performance.md
  - tbd/compliance/user-safety.md
references: []
---

# Platform Compliance

Compliance checks that ensure components respect platform-specific design languages, conventions, and distribution policies. These checks promote native-feeling experiences and smooth app store approval across Apple, Android, Windows, and web platforms.

## Applicability

All recipes targeting a specific platform. Guidelines covering platform-specific patterns or UI design.

## Checks

### platform-design-language

UI MUST follow the platform's native design language (HIG, Material, Fluent).

**Applies when:** a component renders user interface on a specific platform.

**Guidelines:**
- [adc.guideline.implementing.ui.platform-design-languages](cookbook:3741ed5e-0b67-48f2-b227-36ae152c0f4b)

---

### native-controls-preference

Standard UI patterns SHOULD use native platform controls before custom implementations.

**Applies when:** a component implements common UI patterns (lists, navigation, dialogs, pickers).

**Guidelines:**
- [adc.principle.native-controls](cookbook:dec7cf4a-449b-47fa-9d6e-f7e9376383a7)

---

### platform-touch-targets

Interactive elements MUST meet platform-specific minimum touch target sizes.

**Applies when:** a component renders tappable or clickable elements on mobile or touch-enabled platforms.

**Guidelines:**
- [adc.guideline.implementing.ui.touch-click-targets](cookbook:73b254b4-c611-434a-a9f4-67c8a7155576)

---

### deep-linking-support

Features with addressable content MUST support platform deep linking conventions.

**Applies when:** a component presents content that should be navigable via external links.

**Guidelines:**
- [adc.guideline.implementing.platform-integration.deep-linking](cookbook:d27c35ab-84f6-4f40-8c29-91630fdc90e7)

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
- [adc.guideline.implementing.ui.theming](cookbook:5cc9773e-78de-493e-891c-2a819baf9b60)
- [adc.guideline.implementing.ui.color](cookbook:e547d962-d561-4bd9-bb5a-50bdeec98335)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
