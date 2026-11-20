
- Target the latest Swift 6.2.x toolchain and write tests that are clean under strict concurrency; annotate `@MainActor` on `@Test` functions that touch main-actor state rather than dispatching manually.
- Follow one-entity-per-file: one suite `struct` per file, with nested helpers in an `extension`.
- Run with `swift test` (SwiftPM) or the Xcode test action; both discover Swift Testing and XCTest in the same target.

