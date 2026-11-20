
- **should-follow-arrange-act-assert**: Each test vector in a cookbook artifact SHOULD follow the Arrange-Act-Assert pattern:
  - **Arrange** — describe the preconditions and input state
  - **Act** — describe the action or method call being tested
  - **Assert** — describe the expected outcome
- **must-test-one-behavioral-concept**: Each vector MUST test one behavioral concept — not multiple unrelated assertions
- **must-not-depend-on-other-vectors**: Vectors MUST NOT depend on each other — each is self-contained
- **should-target-public-api**: Vectors SHOULD target the public API described in the artifact's requirements, not implementation details
- **should-use-descriptive-specification-names**: Test vectors SHOULD use descriptive names that read as specifications.
- **must-make-names-clear-enough-to-document**: These names will be used verbatim by code generators, so they MUST be clear enough to serve as test documentation.
