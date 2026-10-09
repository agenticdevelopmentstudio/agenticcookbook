---
id: 65367d27-1d4e-41e5-9e8c-e9adb08ddc90
title: "Objective-C"
domain: agenticdevelopercookbook://guidelines/reviewing/language/objective-c
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review Objective-C for ARC ownership, retain cycles, Core Foundation bridging, nullability on public headers and clean Swift import."
platforms:
  - ios
  - macos
languages:
  - objective-c
tags:
  - language
  - objective-c
  - arc
  - nullability
  - review
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/objective-c
  - agenticdevelopercookbook://guidelines/reviewing/language/swift
references:
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
  - https://developer.apple.com/documentation/swift/designating-nullability-in-objective-c-apis
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
---

# Objective-C

Review changed Objective-C against [Objective-C](agenticdevelopercookbook://guidelines/implementing/language/objective-c). Read the header and the implementation together.

## Ownership

- Every object property has an explicit `strong`, `weak` or `copy` attribute. Flag `assign` on an object property.
- `NSString`, collection and block properties that a caller could hand a mutable value to are `copy`.
- Delegates and back-references are `weak`.
- No manual `retain`, `release` or `autorelease` in an ARC file, and no per-file `-fno-objc-arc` without a written reason.
- A name starting with `alloc`, `new`, `copy` or `mutableCopy` is only used for methods that return an owned object.

## Retain cycles

- A block stored on `self` that mentions `self` (directly, or through an ivar) captures a weak reference, and uses a strong local inside.
- Timers, notification observers and KVO registrations are removed in `dealloc` or an earlier teardown, and do not keep their target alive.

## Core Foundation bridging

- Every Objective-C and Core Foundation cast says who owns the result: `__bridge`, `__bridge_retained` or `__bridge_transfer`. Check that every `__bridge_retained` has a matching `CFRelease`, and that no object is released twice.

## Nullability

- Each public header has `NS_ASSUME_NONNULL_BEGIN` and `NS_ASSUME_NONNULL_END`.
- Anything that can be `nil` is marked `nullable`, and the implementation actually returns `nil` there.
- Typedef'd pointers inside the audited region carry their own annotation.
- No new unannotated public declaration, which Swift would import as an implicitly unwrapped optional.

## Swift import

- Collections carry generics. A refined API uses `NS_REFINED_FOR_SWIFT` and the Swift-side wrapper calls the original instead of copying its logic.
- Designated initializers are marked, and unusable inherited ones are `NS_UNAVAILABLE`.

## Errors and naming

- Recoverable failure uses `NSError **`, not an exception. Public symbols carry the project prefix.

## Why this matters

Ownership and null mistakes in Objective-C compile cleanly and fail later, far from the cause. A checklist that targets exactly those two classes finds them while the context is still on screen.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
