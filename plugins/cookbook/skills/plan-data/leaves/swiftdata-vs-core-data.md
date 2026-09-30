<!-- leaf: plan-data/swiftdata-vs-core-data · source: guidelines/planning/data/swiftdata-vs-core-data.md -->

**Rules** (cite as `plan-data/swiftdata-vs-core-data#<slug>`):

- `forces-core-data-default-swiftdata-new-code` SHOULD — When no row above forces Core Data, SHOULD default to SwiftData for new code.
- `choice-justified-os-version-floor` MUST — The choice MUST be justified by OS-version floor, model complexity, and migration needs — never by framework novelty.
- `macos-14-floor-use-swiftdata` SHOULD — New greenfield apps with an iOS 17+ / macOS 14+ floor SHOULD use SwiftData.
- `migrations-schema-versioning-use-core-data-whose` SHOULD — Projects requiring deterministic, fully-controlled migrations or schema versioning SHOULD use Core Data, whose …
- `below-swiftdata-floor-use-core-data` MUST — Code targeting OS versions below the SwiftData floor MUST use Core Data.
- `project-not-rewrite-working-core-data` MUST — A project MUST NOT rewrite a working Core Data stack into SwiftData purely to modernize; migrate only when a concrete …
- `maturing-not-finished` MUST — SwiftData has had reports of occasional silent save failures and behavior that shifted across iOS 17, 18, and 26. MUST …
- `teams-introduce-swiftdata-new-models` MAY — Teams MAY introduce SwiftData for new models in a Core Data app, or expose a Core Data stack to SwiftData, rather than …
- `interoperating-underlying-schema-stay-compatible-across-both` MUST — When interoperating, the underlying schema MUST stay compatible across both layers; validate with migration tests …

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
