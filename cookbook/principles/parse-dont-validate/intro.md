
# Make illegal states unrepresentable

Encode invariants in the type system so invalid values cannot be constructed, and *parse* untrusted input once at the boundary into a type that carries proof of its own validity — rather than passing raw primitives inward and re-validating them at every use. A value that type-checks should already be known-good. This is the structural form of fail-fast: the compiler rejects the bad case before it can run.
