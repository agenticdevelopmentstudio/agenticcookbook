
- `should-encode-invariants-in-types`: an invariant kept only by convention or runtime checks where the type system could hold it
- `should-parse-at-the-boundary`: untrusted input carried past the boundary without being converted into a domain type
- `should-not-revalidate-downstream`: raw strings or maps threaded inward and re-checked downstream
- `should-make-illegal-states-unconstructable`: a wide type (string, int, nullable bag of fields) where a narrower one (enum, non-empty collection, bounded range, branded type) fits, or a "this should never happen" branch
- `should-push-proof-upward-but-no-further`: validation done later than the information allowed, or callers forced to prove things they cannot yet know
