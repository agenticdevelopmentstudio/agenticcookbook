
Review changed Swift against the rules above, then against the guidelines it links for concurrency, testing and lint.

- `should-start-with-value-types`, `should-use-classes-only-for-class-features`: A new class has a stated reason: identity, Objective-C interoperability or required inheritance. Otherwise it should be a struct or enum.
- `should-mark-classes-final`: Classes are `final` unless subclassing is designed.
- `should-share-behavior-with-protocols`: Behavior is shared with protocols and extensions, not with a base class.
- `must-model-absence-with-optional`: No sentinel values where an optional fits.
- `must-not-force-unwrap`, `must-not-declare-implicitly-unwrapped-optionals`, `should-keep-injected-values-private-and-documented`: No new `!`, `try!` or `as!` without a comment that says why failure is a programmer error. No new implicitly unwrapped optional outside an injection point.
- `should-guard-for-early-exit`: `guard` is used for early exit.
- `must-mark-throws-and-try`, `should-model-related-failures-as-an-enum`: Failing functions are `throws` and every call is marked `try`. Related failures are an enum that conforms to `Error`.
- `should-pick-catch-try-or-propagate`: `try?` is used only where the reason for failure is irrelevant, and a swallowed error is not hiding a real problem.
- `should-defer-cleanup`: Cleanup that must always run is in `defer`.
- `should-limit-typed-throws`, `should-throw-plain-error`: Typed throws appear only where the closed error set is part of the design.
- `should-state-narrowest-access-level`: Each new declaration has the narrowest level that works.
- `must-not-expose-more-restricted-types`: No declaration exposes a type with a lower access level.
- `must-mark-only-interface-members-public`: Every `public` or `open` member is part of an intended interface.
- `should-follow-strict-concurrency-guideline`: Concurrency: isolation and `Sendable` follow the strict-concurrency guideline.
- `should-use-appkit-and-uikit`: UI framework: Use AppKit and UIKit, not SwiftUI ([adc.guideline.implementing.platform-integration.prefer-explicit-apple-apis](cookbook:095b33a1-2835-4ed5-bf01-f1e492148819)).
- `should-pass-repository-lint-and-tests`: Lint and tests pass under the repository's own configuration.
- `should-prefer-let`: a `var` where nothing mutates it, or a mutable property that could be `let`.
- `should-unwrap-safely`: optionals unwrapped with `if let`, `guard let`, chaining or `??` rather than by force.
- `must-make-do-catch-exhaustive`, `should-prefer-exhaustive-enum-catches`: a `do`/`catch` that is neither exhaustive nor in a throwing function, or a catch-all where a switch over the error enum would catch new cases.
