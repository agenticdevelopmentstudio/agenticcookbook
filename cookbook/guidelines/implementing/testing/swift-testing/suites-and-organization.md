
- Group related tests with **`@Suite`** on a type (often a `struct`). A type containing `@Test` methods is treated as a suite implicitly, but you **SHOULD** annotate it to set a name or traits.
- Per-test state lives in stored properties; fresh suite instances are created per test, so `init` is the setup and `deinit` is the teardown. You **SHOULD** prefer this over shared mutable static state to keep tests independent (see `agenticdevelopercookbook://guidelines/implementing/testing/unit-test-patterns`).

