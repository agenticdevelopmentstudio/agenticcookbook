
- **should-encode-invariants-in-types**: SHOULD encode invariants in the type system so invalid values cannot be constructed; a value that type-checks SHOULD already be known-good.
- **should-parse-at-the-boundary**: Parse at the boundary: SHOULD convert untrusted input into a domain type exactly once; the parsed value *is* the proof.
- **should-not-revalidate-downstream**: SHOULD NOT thread raw strings and maps through the system and re-check them downstream.
- **should-make-illegal-states-unconstructable**: Make illegal states unconstructable: SHOULD model with the narrowest type that fits — sum types/enums for "one of", non-empty collections, bounded ranges, opaque/branded types — so a whole class of "this should never happen" branches disappears.
- **should-push-proof-upward-but-no-further**: Push the burden of proof upward, but no further: SHOULD validate as early as the information is available, without forcing callers to prove things they cannot yet know.
