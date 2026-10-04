---
id: 73b87332-8024-4a21-95ab-1e08f1cbd1a1
title: "Design-Time Data"
domain: agenticdevelopercookbook://guidelines/testing/design-time-data
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Use design-time data contexts for visual preview testing — verify UI renders correctly without running the app."
platforms:
  - csharp
  - windows
tags:
  - design-time-data
  - platform
  - windows
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - ui-implementation
---

# Design-Time Data

Design-time data enables visual preview testing in the XAML designer without running the application — the Windows equivalent of SwiftUI `#Preview` and Compose `@Preview`.

## What to verify

- Views SHOULD use `d:DataContext` and `d:DesignInstance` so the designer renders realistic content, not empty surfaces
- Verify all significant view states are previewable: default, empty, error, loading, populated
- Use XAML Hot Reload for rapid visual iteration during testing

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for testing use case — reframe as visual preview testing |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
