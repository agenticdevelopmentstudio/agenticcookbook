---
id: 3f442861-abec-4dfc-a2e2-a3761904d16d
title: "Kotlin Multiplatform"
domain: agenticdevelopercookbook://guidelines/planning/code-quality/kotlin-multiplatform
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Share domain and data logic broadly across platforms with KMP; choose shared vs native UI per platform maturity."
platforms:
  - kotlin
tags:
  - kotlin
  - kmp
  - architecture
depends-on: []
related:
  - agenticdevelopercookbook://principles/manage-complexity-through-boundaries
references:
  - https://www.jetbrains.com/kotlin-multiplatform/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - new-module
---

# Kotlin Multiplatform

Kotlin Multiplatform (KMP) shares non-UI logic — domain, data, networking — across Android, iOS, desktop, and web from a single `commonMain` source set, using `expect`/`actual` for the few platform-specific seams. The default share boundary is business logic; UI is a per-platform decision, not an automatic share.

## Layering and the share boundary

- Teams **SHOULD** share the domain and data layers (use cases, repositories, models, networking, serialization) in `commonMain`. KMP has been Stable since November 2023, so this is durable, low-risk reuse.
- The shared module **MUST NOT** depend on platform UI toolkits. Keep platform-idiomatic UI (SwiftUI, Jetpack Compose, web framework) on the consuming side unless a shared-UI decision is made deliberately.
- A shared ViewModel/presentation layer **MAY** be shared when the team accepts coupling presentation state to KMP; treat it as a deliberate scope expansion, not a default.
- Apply boundaries per `agenticdevelopercookbook://principles/manage-complexity-through-boundaries`: expose narrow interfaces from the shared module so platforms stay swappable.

## expect / actual discipline

- `expect`/`actual` **SHOULD** be reserved for thin platform shims (e.g., logging sink, secure storage, file paths, UUID/clock). Most common code needs none.
- Every `expect` declaration **MUST** have a matching `actual` in the same package for every target; the compiler enforces this. Prefer interfaces plus dependency injection over `expect`/`actual` when the seam is non-trivial — it is easier to test and delete.
- Use the hierarchical source-set structure (e.g., an intermediate `appleMain` shared by `iosMain`/`macosMain`) so common-but-not-universal code is not duplicated.

## Shared UI: Compose Multiplatform (CMP)

- Compose Multiplatform reached **Stable for iOS in CMP 1.8.0 (May 2025)**; current line is **CMP 1.11.0 (May 2026)**. Pin the CMP version explicitly in the build and re-check the release notes before relying on a specific UI feature.
- iOS UI parity (text selection, native scrolling, accessibility/VoiceOver, gestures) is improving release-over-release but **still evolving** — FORECAST any unreleased item against the version you pin, and validate accessibility on-device.
- Choose shared CMP UI **only** when the team accepts current iOS maturity and values UI reuse over fully native look-and-feel; otherwise keep SwiftUI on iOS and Compose on Android while still sharing all non-UI logic. Present this as a deliberate decision per app, not a mandate.

## Interop and packaging

- Android consumes the shared module directly as a Gradle dependency. iOS consumes it as an Apple framework (XCFramework / CocoaPods / SPM) — design the public API to be Swift-friendly: avoid Kotlin-only constructs (sealed-class exhaustiveness, default args) at the boundary.
- Expose `suspend` functions and `Flow` through a documented bridge (e.g., a `Skie`-style or hand-written wrapper) so Swift callers get idiomatic async; do not leak raw coroutines across the boundary.

## Build and verification

- The shared module **SHOULD** have its own `commonTest` suite covering domain/data logic once, plus minimal per-target tests for `actual` implementations.
- Run platform builds in CI for every target the project ships; a green Android build does not prove the iOS framework links.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
