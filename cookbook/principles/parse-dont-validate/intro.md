
# Make illegal states unrepresentable

Encode invariants in the type system so invalid values cannot be constructed, and *parse* untrusted input once at the boundary into a type that carries proof of its own validity — rather than passing raw primitives inward and re-validating them at every use. A value that type-checks should already be known-good. This is the structural form of fail-fast: the compiler rejects the bad case before it can run.

- Parse at the boundary: convert untrusted input into a domain type exactly once; the parsed value *is* the proof. Don't thread raw strings and maps through the system and re-check them downstream.
- Make illegal states unconstructable: model with the narrowest type that fits — sum types/enums for "one of", non-empty collections, bounded ranges, opaque/branded types — so a whole class of "this should never happen" branches disappears.
- Push the burden of proof upward, but no further: validate as early as the information is available, without forcing callers to prove things they cannot yet know.
- Per language: Rust enums and newtypes, TypeScript discriminated unions and branded types, Kotlin sealed classes, Swift enums with associated values, Python typed/Pydantic models.
- Complements input-validation as a security control: validation rejects bad input; this principle ensures that what survives validation cannot later be misused.

