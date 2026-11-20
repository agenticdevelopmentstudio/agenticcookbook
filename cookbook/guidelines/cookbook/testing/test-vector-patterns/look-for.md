
- `should-follow-arrange-act-assert`: a vector missing its preconditions and input state, the action under test, or the expected outcome
- `must-test-one-behavioral-concept`: a vector that bundles multiple unrelated assertions
- `must-not-depend-on-other-vectors`: a vector that needs another vector's result or setup
- `should-target-public-api`: a vector that reaches into implementation details instead of the public API in the artifact's requirements
- `should-use-descriptive-specification-names`: a vector name that does not read as a specification
- `must-make-names-clear-enough-to-document`: a name too vague to serve as test documentation once a code generator uses it verbatim
