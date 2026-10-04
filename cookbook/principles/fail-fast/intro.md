
# Fail fast

Invalid state should be detected and surfaced immediately at the point of origin, not propagated silently:

- Use assertions and preconditions in debug builds
- Validate inputs at system boundaries
- Return typed errors rather than swallowing exceptions
- Never use empty catch blocks
- In production, fail gracefully with clear messages; in debug, fail loudly

