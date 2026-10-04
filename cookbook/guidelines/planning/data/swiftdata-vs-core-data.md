---
id: 1138183b-296d-479b-9df7-7869a006c023
title: "Choose SwiftData vs Core Data"
domain: agenticdevelopercookbook://guidelines/planning/data/swiftdata-vs-core-data
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pick SwiftData or Core Data for Apple persistence by OS-version floor, model complexity, and migration needs — not by novelty."
platforms:
  - swift
  - ios
  - macos
tags:
  - apple
  - persistence
  - data
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/planning/data/datastore-selection
references:
  - https://developer.apple.com/documentation/swiftdata
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - data-modeling
  - schema-design
---

# Choose SwiftData vs Core Data

SwiftData and Core Data are both first-party Apple object-graph persistence frameworks backed by SQLite. SwiftData (`@Model`, Swift-native, built on top of the Core Data stack) is the modern default for new apps on recent OS versions; Core Data remains the right choice for fine-grained control, complex migrations, lower OS-version floors, or Objective-C interop. Make this a **deliberate decision**, not a reach for the newest API.

## Decision Rule

Apply these in order; the first matching row decides.

| If the project... | Choose |
|---|---|
| Must support iOS/iPadOS below 17 (or macOS below 14) | **Core Data** — SwiftData requires iOS 17 / macOS 14+ |
| Shares the store with an Objective-C target or extension | **Core Data** |
| Needs custom multi-stage migrations, model versioning UI, or a large/complex object graph at scale | **Core Data** |
| Needs CloudKit **public** database sync | **Core Data** — SwiftData supports private CloudKit only |
| Is a new app targeting iOS 17+ / macOS 14+ with a straightforward model | **SwiftData** |

When no row above forces Core Data, **SHOULD** default to SwiftData for new code.

## Rules

- The choice **MUST** be justified by OS-version floor, model complexity, and migration needs — never by framework novelty.
- New greenfield apps with an iOS 17+ / macOS 14+ floor **SHOULD** use SwiftData.
- Projects requiring deterministic, fully-controlled migrations or schema versioning **SHOULD** use Core Data, whose multi-stage migration tooling is more mature as of 2026.
- Code targeting OS versions below the SwiftData floor **MUST** use Core Data.
- A project **MUST NOT** rewrite a working Core Data stack into SwiftData purely to modernize; migrate only when a concrete need (new model work, concurrency cleanup) justifies the cost.

## SwiftData Notes (as of 2026)

- Define models with the `@Model` macro on a Swift class — no `.xcdatamodeld` file or `NSManagedObject` subclass required.
- Use `@ModelActor` for background work; it gives clearer actor-isolation boundaries under Swift 6 strict concurrency than Core Data's `perform` closures.
- **Maturing, not finished.** SwiftData has had reports of occasional silent save failures and behavior that shifted across iOS 17, 18, and 26. **MUST** verify writes persist (fetch-after-save in tests) rather than assuming success, and pin behavior expectations to a tested OS revision.
- iOS 26 / macOS 26 added **model (class) inheritance** and history fetch with a `sortBy` parameter; this is the only major SwiftData feature in that cycle. Commonly requested items (shared/public CloudKit sync, dynamic predicate adjustment) did **not** ship — treat them as unavailable, not roadmap guarantees.

## Core Data Notes (as of 2026)

- **Fully supported and not deprecated.** It remains the foundation SwiftData is built on and the recommended path for the cases in the decision rule.
- Preferred for fine-grained fetch tuning, batch operations at scale, and predictable performance on large datasets.
- Mature, well-documented migration story (lightweight + custom mapping models, staged migrations).

## Interoperability

- The two **can coexist in one app** over the same store, enabling incremental adoption.
- Teams **MAY** introduce SwiftData for new models in a Core Data app, or expose a Core Data stack to SwiftData, rather than performing a big-bang rewrite.
- When interoperating, the underlying schema **MUST** stay compatible across both layers; validate with migration tests before shipping.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
