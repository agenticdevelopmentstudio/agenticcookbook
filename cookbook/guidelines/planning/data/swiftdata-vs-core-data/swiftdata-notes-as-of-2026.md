
- Define models with the `@Model` macro on a Swift class — no `.xcdatamodeld` file or `NSManagedObject` subclass required.
- Use `@ModelActor` for background work; it gives clearer actor-isolation boundaries under Swift 6 strict concurrency than Core Data's `perform` closures.
- **Maturing, not finished.** SwiftData has had reports of occasional silent save failures and behavior that shifted across iOS 17, 18, and 26. **MUST** verify writes persist (fetch-after-save in tests) rather than assuming success, and pin behavior expectations to a tested OS revision.
- iOS 26 / macOS 26 added **model (class) inheritance** and history fetch with a `sortBy` parameter; this is the only major SwiftData feature in that cycle. Commonly requested items (shared/public CloudKit sync, dynamic predicate adjustment) did **not** ship — treat them as unavailable, not roadmap guarantees.

