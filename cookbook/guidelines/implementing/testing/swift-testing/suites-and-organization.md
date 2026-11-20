
- A type containing `@Test` methods is treated as a suite implicitly.
- Per-test state lives in stored properties; fresh suite instances are created per test, so `init` is the setup and `deinit` is the teardown.

