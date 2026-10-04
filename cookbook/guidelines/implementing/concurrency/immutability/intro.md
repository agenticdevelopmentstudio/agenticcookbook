
# Immutability

Mutable shared state is the root cause of most concurrency bugs. Immutable values MUST be the default; introduce mutability only where necessary. Value types SHOULD be preferred over reference types. Mutation MUST be contained behind clear boundaries.

