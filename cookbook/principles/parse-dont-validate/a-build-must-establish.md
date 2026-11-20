
- `should-encode-invariants-in-types`: invariants are encoded in the type system so invalid values cannot be constructed, or the work says why not
- `should-parse-at-the-boundary`: every untrusted input is converted into a domain type exactly once at the boundary, or the work says why not
- `should-not-revalidate-downstream`: no raw strings or maps are threaded through the system and re-checked downstream, or the work says why
- `should-make-illegal-states-unconstructable`: each value is modelled with the narrowest type that fits and no "this should never happen" branch remains, or the work says why not
- `should-push-proof-upward-but-no-further`: each check happens as early as its information is available and no caller is forced to prove what it cannot yet know, or the work says why not
