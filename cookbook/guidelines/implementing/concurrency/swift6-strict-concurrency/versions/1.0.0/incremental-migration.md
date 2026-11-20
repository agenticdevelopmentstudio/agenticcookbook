
- Strict concurrency **SHOULD** be adopted incrementally per module — a Swift 6 compiler still builds Swift 5 modules, so the strictness is opt-in per target.
- Recommended order (durable practice from the Swift migration guide):
  1. Enable checks as **warnings** first via the `StrictConcurrency` upcoming-feature flag (or the "Strict Concurrency Checking" build setting at `Targeted`, then `Complete`) while still in Swift 5 mode.
  2. Migrate **leaf modules first** (no dependents), then work upward; switch the **app target last**.
  3. Flip a module to the Swift 6 language mode only once its warnings are clear.
  4. Use `@preconcurrency` on imports/conformances to keep Swift-5 clients compiling against a not-yet-migrated dependency — treat it as a **temporary** shim, not a destination.
- Do not flip the whole workspace to Swift 6 mode at once; that produces an unactionable wall of errors.

