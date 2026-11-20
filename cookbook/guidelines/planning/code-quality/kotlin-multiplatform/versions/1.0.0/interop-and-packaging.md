
- Android consumes the shared module directly as a Gradle dependency. iOS consumes it as an Apple framework (XCFramework / CocoaPods / SPM) — design the public API to be Swift-friendly: avoid Kotlin-only constructs (sealed-class exhaustiveness, default args) at the boundary.
- Expose `suspend` functions and `Flow` through a documented bridge (e.g., a `Skie`-style or hand-written wrapper) so Swift callers get idiomatic async; do not leak raw coroutines across the boundary.

