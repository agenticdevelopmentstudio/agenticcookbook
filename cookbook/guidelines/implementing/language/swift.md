---
id: e0fa9d85-2143-4869-bea9-e085bc4c2f9d
title: "Swift"
domain: agenticdevelopercookbook://guidelines/implementing/language/swift
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "The Swift language rules this cookbook expects (value types, optionals, error handling, access control) and an index of the Swift concurrency, testing, lint and preview guidelines."
platforms:
  - ios
  - macos
languages:
  - swift
tags:
  - language
  - swift
  - value-types
  - optionals
  - errors
  - access-control
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/concurrency/swift6-strict-concurrency
  - agenticdevelopercookbook://guidelines/implementing/testing/swift-testing
  - agenticdevelopercookbook://guidelines/implementing/code-quality/linting
  - agenticdevelopercookbook://guidelines/implementing/ui/previews
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/prefer-explicit-apple-apis
  - agenticdevelopercookbook://guidelines/implementing/language/objective-c
  - agenticdevelopercookbook://guidelines/implementing/ui/appkit-and-uikit-patterns
  - agenticdevelopercookbook://guidelines/reviewing/language/swift
  - agenticdevelopercookbook://principles/immutability-by-default
  - agenticdevelopercookbook://principles/errors-as-values
references:
  - https://developer.apple.com/documentation/swift/choosing-between-structures-and-classes
  - https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/
  - https://docs.swift.org/swift-book/documentation/the-swift-programming-language/accesscontrol/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - refactor
  - error-handling
---

# Swift

This is the entry point for Swift work. It states the language rules that apply to all Swift code and links the guidelines that cover the rest.

## Related Swift guidelines

- [Adopt Swift 6 strict concurrency incrementally](agenticdevelopercookbook://guidelines/implementing/concurrency/swift6-strict-concurrency) for actors, `Sendable` and isolation.
- [Swift Testing](agenticdevelopercookbook://guidelines/implementing/testing/swift-testing) for writing tests.
- [Linting](agenticdevelopercookbook://guidelines/implementing/code-quality/linting) for the lint configuration.
- [Previews](agenticdevelopercookbook://guidelines/implementing/ui/previews) for UI previews.
- [Use AppKit and UIKit, not SwiftUI](agenticdevelopercookbook://guidelines/implementing/platform-integration/prefer-explicit-apple-apis) for the choice of UI framework, and [AppKit and UIKit patterns](agenticdevelopercookbook://guidelines/implementing/ui/appkit-and-uikit-patterns) for using them.
- [Objective-C](agenticdevelopercookbook://guidelines/implementing/language/objective-c) when Swift and Objective-C share a target.
- [Xcode project hygiene](agenticdevelopercookbook://guidelines/implementing/code-quality/xcode-project-hygiene) for project settings.

## Value types first

- Start with a `struct` (or `enum`) and move to a `class` only when you need a class feature. Apple's guidance is to choose structures by default.
- Use a class for identity (compare with `===`, one shared mutable instance such as a file handle, a connection or a hardware intermediary), for Objective-C interoperability, or for inheritance from a framework class you are expected to subclass.
- Value semantics keep a change local: a copy changed in one place is not visible elsewhere unless the code passes it back. Prefer `let` and immutable properties, and add `var` where mutation is the point.
- Share behavior across structures with protocols and protocol extensions, not with class inheritance.
- Mark classes `final` unless a subclass is part of the design.

## Optionals

- Model absence with `Optional`, not with sentinel values such as `-1`, `""` or `NSNotFound`.
- Unwrap with `if let`, `guard let`, optional chaining or `??`. Use `guard` for early exit so the main path is not indented.
- Do not force-unwrap (`!`) or use `try!` or `as!` except where failure is a programmer error that should crash, and then prefer `preconditionFailure` with a message.
- Do not declare implicitly unwrapped optionals (`Type!`) in new Swift code. The legitimate case is a value injected before first use, such as an outlet; keep it `private` and document the injection point.

## Error handling

- Mark a function that can fail `throws`, and mark each call site `try`. Errors are values of a type that conforms to `Error`; model related failures as an `enum`.
- Handle an error with `do`/`catch`, convert it to an optional with `try?` only when the reason does not matter, and let it propagate when the caller is better placed to decide.
- A `do`/`catch` must be exhaustive or sit in a throwing function. A `catch` that matches every case of an enum by switch gets a compile error if a case is added later; prefer that to a catch-all that hides new cases.
- Use `defer` for cleanup that must run on every exit, such as closing a file. Deferred blocks run in reverse order of appearance and cannot exit their scope.
- Most functions should throw plain `Error`. Use typed throws (`throws(MyError)`) only where the error type is a stable, closed set: embedded code that avoids boxing, an error that is an internal detail of a library, or code that forwards the errors of a generic closure parameter.

## Access control

- The default is `internal`. State the narrowest level that works: `private` for the enclosing declaration and its same-file extensions, `fileprivate` for the file, `internal` for the module, `package` for the Swift package, `public` for use outside the module, and `open` only for classes designed for outside subclassing and overriding.
- No declaration may expose a type with a more restrictive level than its own.
- The members of a `public` type are `internal` unless marked. Mark each member that belongs to the interface and nothing else, because the public surface of a framework is an API you must keep.

## Why this matters

Value types, honest optionals, typed failure and narrow access are what let the compiler find bugs that other languages find in production. Keeping them in one index guideline gives a reader (human or agent) a single place to start and the links to everything else Swift-specific.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
