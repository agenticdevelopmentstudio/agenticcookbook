---
id: 1471cab8-cdd2-444d-84da-8e4e70eb2453
title: "Swift"
domain: agenticdevelopercookbook://guidelines/reviewing/language/swift
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review Swift for value types, optional handling, error handling and access control, then follow the links to the concurrency, testing and lint reviews."
platforms:
  - ios
  - macos
languages:
  - swift
tags:
  - language
  - swift
  - review
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/swift
  - agenticdevelopercookbook://guidelines/reviewing/platform-integration/prefer-explicit-apple-apis
  - agenticdevelopercookbook://guidelines/reviewing/language/objective-c
  - agenticdevelopercookbook://guidelines/reviewing/ui/appkit-and-uikit-patterns
references:
  - https://developer.apple.com/documentation/swift/choosing-between-structures-and-classes
  - https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/
  - https://docs.swift.org/swift-book/documentation/the-swift-programming-language/accesscontrol/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
---

# Swift

Review changed Swift against [Swift](agenticdevelopercookbook://guidelines/implementing/language/swift), then against the guidelines it links for concurrency, testing and lint.

## Types

- A new class has a stated reason: identity, Objective-C interoperability or required inheritance. Otherwise it should be a struct or enum.
- Classes are `final` unless subclassing is designed.
- Behavior is shared with protocols and extensions, not with a base class.

## Optionals

- No sentinel values where an optional fits.
- No new `!`, `try!` or `as!` without a comment that says why failure is a programmer error. No new implicitly unwrapped optional outside an injection point.
- `guard` is used for early exit.

## Errors

- Failing functions are `throws` and every call is marked `try`. Related failures are an enum that conforms to `Error`.
- `try?` is used only where the reason for failure is irrelevant, and a swallowed error is not hiding a real problem.
- Cleanup that must always run is in `defer`.
- Typed throws appear only where the closed error set is part of the design.

## Access control

- Each new declaration has the narrowest level that works.
- No declaration exposes a type with a lower access level.
- Every `public` or `open` member is part of an intended interface.

## Linked reviews

- Concurrency: isolation and `Sendable` follow the strict-concurrency guideline.
- UI framework: [Use AppKit and UIKit, not SwiftUI](agenticdevelopercookbook://guidelines/reviewing/platform-integration/prefer-explicit-apple-apis).
- Lint and tests pass under the repository's own configuration.

## Why this matters

Most Swift review comments repeat the same four themes. Naming them lets a reviewer check them quickly and spend attention on design.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
