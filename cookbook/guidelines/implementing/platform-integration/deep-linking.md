---
id: d27c35ab-84f6-4f40-8c29-91630fdc90e7
title: "Deep linking"
domain: agenticdevelopercookbook://guidelines/implementing/platform-integration/deep-linking
type: guideline
version: 1.1.3
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Make all significant feature points and views deep linkable using the platform's native URL or deep link mechanism, and define URL patterns in each spec."
platforms:
  - kotlin
  - swift
  - typescript
  - web
  - windows
tags:
  - deep-linking
  - platform
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - platform-integration
  - configuration
---

# Deep linking

All significant feature points and views MUST be deep linkable using the platform's native URL/deep link mechanism:

- **Apple**: Universal Links + custom URL schemes. `onOpenURL` in SwiftUI, `NavigationPath` for state restoration.
- **Android**: App Links + intent filters. Navigation component deep link support.
- **Web**: URL routing. Every view should have a unique, shareable URL.
- **Windows**: Protocol activation via `<uap:Protocol>` declaration in manifest. `AppInstance.GetActivatedEventArgs()` for rich activation handling.

Each spec SHOULD include a **Deep Linking** section defining URL patterns.

---

# Deep Linking

All significant feature points and views MUST be deep linkable using the platform's native URL/deep link mechanism. Each spec SHOULD include a **Deep Linking** section defining URL patterns.

## TypeScript

Every view MUST have a unique, shareable URL. Use framework routing (React Router, Next.js routing, etc.).

## Windows

Declare protocol handlers in `Package.appxmanifest` and handle activation through the Windows App SDK lifecycle APIs.

- Declare: `<uap:Protocol Name="myapp"/>` in manifest
- Handle via `AppInstance.GetActivatedEventArgs()` in `App.OnLaunched`
- Parse URI to determine target page/state, navigate accordingly
- Use `AppInstance.FindOrRegisterForKey()` for single-instancing (recommended for deep links)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.3 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.1.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.1.0 | 2026-04-02 | Mike Fullerton | Moved from ui/ to platform/ — system integration, not UI design |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
