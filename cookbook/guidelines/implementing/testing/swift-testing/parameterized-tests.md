
- Pass `arguments:` to run one test body over many inputs: `@Test(arguments: [1, 2, 3])`. Each case is reported and rerun independently.
- Use `zip(...)` for paired inputs to avoid an unintended Cartesian product across two collections.
- You **SHOULD** prefer parameterization over hand-written loops so each case surfaces as a distinct result.

