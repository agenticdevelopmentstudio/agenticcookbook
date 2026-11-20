
- `should-encode-invariants-in-types`: whether invariants are encoded in the type system so invalid values cannot be constructed
- `should-parse-at-the-boundary`: whether untrusted input is converted into a domain type exactly once, at the boundary
- `should-not-revalidate-downstream`: whether raw strings and maps are threaded through the system and re-checked downstream
- `should-make-illegal-states-unconstructable`: whether each value is modelled with the narrowest type that fits, leaving no "this should never happen" branches
- `should-push-proof-upward-but-no-further`: whether each check happens as early as its information is available, without forcing callers to prove what they cannot yet know
