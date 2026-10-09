---
id: 7c8d5c06-af21-41f1-86db-ed5809c2d38d
title: "Objective-C"
domain: agenticdevelopercookbook://guidelines/implementing/language/objective-c
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Write Objective-C under ARC with nullability annotations on every public header, so the code is safe on its own and imports into Swift without implicitly unwrapped optionals."
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
  - swift-interop
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/swift
  - agenticdevelopercookbook://guidelines/implementing/ui/appkit-and-uikit-patterns
  - agenticdevelopercookbook://guidelines/reviewing/language/objective-c
  - agenticdevelopercookbook://principles/explicit-over-implicit
references:
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
  - https://developer.apple.com/documentation/swift/designating-nullability-in-objective-c-apis
  - https://developer.apple.com/documentation/swift/improving-objective-c-api-declarations-for-swift
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - refactor
  - platform-integration
---

# Objective-C

Objective-C code in a mixed or legacy Apple codebase MUST compile with ARC, MUST declare nullability in every public header, and MUST be shaped so Swift imports it as idiomatic Swift. Do not write new Objective-C where Swift will do; when the code must stay Objective-C (an existing module, a C++ interop shim, a framework with an Objective-C public surface), the rules below apply.

## ARC ownership

- Build with ARC (`-fobjc-arc`). Do not call `retain`, `release` or `autorelease` by hand in an ARC file, and do not mix manual reference counting into a target by file-level flags without a written reason.
- Declare object properties with an explicit ownership attribute: `strong` for owned objects, `weak` for back-references and delegates, `copy` for `NSString`, `NSArray`, `NSDictionary` and block properties whose mutable subclasses a caller could pass in.
- Ownership qualifiers on variables are `__strong` (the default), `__weak`, `__unsafe_unretained` and `__autoreleasing`. Reach for `__unsafe_unretained` only where the compiler cannot express the lifetime, and say why in a comment.
- Method families decide ownership of a returned object. A method whose name begins with `alloc`, `new`, `copy` or `mutableCopy` returns a retained object that the caller owns; any other name returns an object the caller does not own. Name your own methods with that rule in mind, because ARC applies it to them too.
- Break retain cycles in blocks. A block that captures `self` and is stored on `self` MUST capture a `__weak` reference and, inside the block, take a `__strong` local before use.
- Wrap long-running loops that create many temporary objects in `@autoreleasepool { }` so memory does not grow until the loop ends.

## Bridging Core Foundation

- Casting between an Objective-C object pointer and a Core Foundation pointer MUST state who owns the result. Use `__bridge` when ownership does not change, `__bridge_retained` to hand an object to Core Foundation (you now `CFRelease` it), and `__bridge_transfer` to take a Core Foundation object into ARC (ARC now releases it).
- Never use a bare C cast between the two worlds in ARC code. The compiler rejects it for good reason.

## Nullability

- Every public header MUST wrap its declarations in `NS_ASSUME_NONNULL_BEGIN` and `NS_ASSUME_NONNULL_END`, and mark only the exceptions `nullable`. Unannotated declarations inside the region are treated as non-null.
- Use `nullable`, `nonnull` and `null_resettable` on properties, parameters and return types; use `_Nullable` and `_Nonnull` where the simple forms do not fit, such as `_Nullable id * _Nonnull`.
- Without any annotation Swift imports a type as an implicitly unwrapped optional, which hides crashes. `typedef` types are not assumed non-null even inside an audited region, so annotate each use.
- A method documented to return `nil` on failure MUST be declared `nullable`, and a method that must never receive `nil` MUST say so in its signature, not only in a comment.

## Bridging to Swift

- Design the Objective-C API so it needs no Swift-side fix-ups: declare generics on collections (`NSArray<MyListItem *> *`) so Swift sees `[MyListItem]`, and use designated nullability.
- When the Swift form should differ from the Objective-C form (a tuple instead of out-parameters, reordered or renamed arguments), mark the Objective-C declaration `NS_REFINED_FOR_SWIFT` and write the Swift-facing API in a Swift extension. The original is imported with a double underscore prefix (`__getRed(red:green:blue:alpha:)`), which keeps it out of ordinary autocompletion.
- Keep the Objective-C implementation as the single source of behavior. The refined Swift API calls it; it does not reimplement it.

## API design

- Name methods so a call site reads as a phrase, with a label for every argument after the first. Follow the conventions of the framework you extend rather than inventing new vocabulary.
- Prefix every public class, protocol, enum and constant with a project prefix, because Objective-C has no namespaces.
- Mark designated initializers (`NS_DESIGNATED_INITIALIZER`) and forbid inherited ones that cannot work (`NS_UNAVAILABLE`), so a half-initialized object cannot be built.
- Report recoverable failure with a `BOOL` or object return plus an `NSError **` out-parameter, not with exceptions. Exceptions are for programmer errors.

## Why this matters

Objective-C gives no compile-time help with ownership or null unless you ask for it. ARC and nullability annotations turn the two largest sources of crashes into compiler diagnostics, and annotated headers are what let Swift callers use the code without force-unwraps. The rules cost little to follow when the header is first written and a great deal to retrofit.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
