<!-- leaf: implement-testing/swift-testing · source: guidelines/implementing/testing/swift-testing.md -->

**Rules** (cite as `implement-testing/swift-testing#<slug>`):

- `swift-unit-tests-use-runs-alongside-xctest` SHOULD — Swift Testing is the open-source test framework bundled with the Swift 6 toolchain and Xcode 16+; it requires no …
- `unit-tests-you-author-swift-testing-rather` SHOULD — For new Swift unit tests, you SHOULD author with Swift Testing rather than XCTest.
- `you-not-rewrite-passing-xctest-suites` MUST — You MUST NOT rewrite passing XCTest suites solely to switch frameworks; migrate opportunistically when a test changes.
- `test` SHOULD — marks a function as a test. The function MAY be a global function or a method, and MAY be async, throws, or isolated to …
- `expect` SHOULD — records a failure but continues; use it for ordinary assertions. It captures sub-expression values, so a single …
- `implicitly-but-you-annotate-set-name-traits` SHOULD — Group related tests with @Suite on a type (often a struct). A type containing @Test methods is treated as a suite …
- `deinit-teardown-you-prefer-over-shared-mutable` SHOULD — Per-test state lives in stored properties; fresh suite instances are created per test, so init is the setup and deinit …
- `you-prefer-parameterization-over-hand` SHOULD — You SHOULD prefer parameterization over hand-written loops so each case surfaces as a distinct result.
- `tags-network-you-keep-small-shared-tag` SHOULD — Define tags with @Tag and apply them to filter/organize runs (e.g. .tags(.network)). You SHOULD keep a small, shared …

# Swift Testing

Swift Testing is the open-source test framework bundled with the Swift 6 toolchain and Xcode 16+; it requires no package dependency. New Swift unit tests **SHOULD** use it. It runs alongside XCTest in the same target, so migration can proceed incrementally.

## When to use it

- For new Swift **unit tests**, you **SHOULD** author with Swift Testing rather than XCTest.
- You **MUST NOT** rewrite passing XCTest suites solely to switch frameworks; migrate opportunistically when a test changes.
- XCTest is **still required** for UI tests (`XCUIApplication`) and for XCTest-based performance measurement (`measure {}`); Swift Testing does not replace these as of Xcode 16. Keep those in XCTest.

## Core API

- **`@Test`** marks a function as a test. The function **MAY** be a global function or a method, and **MAY** be `async`, `throws`, or isolated to a global actor (e.g. `@MainActor`). A descriptive display name **SHOULD** be passed: `@Test("Parses ISO-8601 dates")`.
- **`#expect(expr)`** records a failure but continues; use it for ordinary assertions. It captures sub-expression values, so a single `#expect(a == b)` reports both operands on failure — you **SHOULD NOT** add a custom message that restates the expression.
- **`#require(expr)`** throws and halts the test when the expectation fails; use it for preconditions whose failure makes the rest of the test meaningless. `try #require(optional)` unwraps an optional and aborts on `nil`, replacing force-unwraps.
- Use **`#expect(throws:)`** / `#require(throws:)` to assert error behavior instead of `do/catch`.

## Suites and organization

- Group related tests with **`@Suite`** on a type (often a `struct`). A type containing `@Test` methods is treated as a suite implicitly, but you **SHOULD** annotate it to set a name or traits.
- Per-test state lives in stored properties; fresh suite instances are created per test, so `init` is the setup and `deinit` is the teardown. You **SHOULD** prefer this over shared mutable static state to keep tests independent (see `agenticdevelopercookbook://guidelines/implementing/testing/unit-test-patterns`).

## Parameterized tests

- Pass `arguments:` to run one test body over many inputs: `@Test(arguments: [1, 2, 3])`. Each case is reported and rerun independently.
- Use `zip(...)` for paired inputs to avoid an unintended Cartesian product across two collections.
- You **SHOULD** prefer parameterization over hand-written loops so each case surfaces as a distinct result.

## Traits and tags

- Attach **traits** for behavior and metadata: `.disabled("reason")`, `.bug("url")`, `.timeLimit(.minutes(1))`, `.enabled(if:)`, and serialization via `.serialized`.
- Define **tags** with `@Tag` and apply them to filter/organize runs (e.g. `.tags(.network)`). You **SHOULD** keep a small, shared tag vocabulary rather than ad-hoc per-file tags.

## Conventions for this codebase

- Target the latest Swift 6.2.x toolchain and write tests that are clean under strict concurrency; annotate `@MainActor` on `@Test` functions that touch main-actor state rather than dispatching manually.
- Follow one-entity-per-file: one suite `struct` per file, with nested helpers in an `extension`.
- Run with `swift test` (SwiftPM) or the Xcode test action; both discover Swift Testing and XCTest in the same target.
