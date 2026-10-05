---
id: 97f55007-2eb6-4ffd-ab2c-c7247191627d
title: "References"
domain: agenticdevelopercookbook://reference/references
type: reference
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Platform-specific coding conventions, design guidelines, and best practices that all implementations should follow."
platforms: 
  - csharp
  - kotlin
  - swift
  - typescript
  - web
  - windows
tags: 
  - references
depends-on: []
related: []
references: 
  - https://developer.android.com/topic/architecture/recommendations
  - https://developer.apple.com/documentation/Xcode/understanding-and-improving-swiftui-performance
  - https://fluent2.microsoft.design/
  - https://github.com/dotnet/runtime/blob/main/docs/coding-guidelines/coding-style.md
  - https://github.com/microsoft/WinUI-Gallery
  - https://github.com/microsoft/WindowsAppSDK
  - https://kotlinlang.org/docs/coding-conventions.html
  - https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
  - https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/
  - https://learn.microsoft.com/en-us/windows/apps/design/
---

# References

Platform-specific coding conventions, design guidelines, and best practices that all implementations should follow.

## Swift

1. Follow the [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/) for all naming and API surface decisions.
2. Follow the [SwiftUI Performance guide](https://developer.apple.com/documentation/Xcode/understanding-and-improving-swiftui-performance) when building views.

## Kotlin

1. Follow the [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html) for all naming and style decisions.
2. Follow [Material Design 3](https://m3.material.io/) for UI components and theming.
3. Follow [Android Architecture Recommendations](https://developer.android.com/topic/architecture/recommendations) for app structure.

## C#

1. Follow the [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) for all naming and style decisions.
2. Follow the [.NET Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/) for public API surface design.
3. Follow the [.NET Runtime Coding Style](https://github.com/dotnet/runtime/blob/main/docs/coding-guidelines/coding-style.md) as the canonical style reference.

## Windows

1. [WinUI 3 / Windows App SDK](https://learn.microsoft.com/en-us/windows/apps/winui/winui3/) — the primary UI framework for Windows desktop apps.
2. [Fluent 2 Design System](https://fluent2.microsoft.design/) — Microsoft's cross-platform design system.
3. [Windows Design Guidelines](https://learn.microsoft.com/en-us/windows/apps/design/) — layout, navigation, typography, color, and motion.
4. [WinUI Gallery (GitHub)](https://github.com/microsoft/WinUI-Gallery) — interactive reference for all WinUI 3 controls.
5. [Windows App SDK (GitHub)](https://github.com/microsoft/WindowsAppSDK) — releases, issues, and roadmap.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
