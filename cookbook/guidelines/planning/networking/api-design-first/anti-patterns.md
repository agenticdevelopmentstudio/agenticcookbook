
- **MUST NOT** generate the spec from running code as the primary workflow (code-first) for a new API — that inverts the source of truth and lets undocumented behavior leak in.
- **MUST NOT** keep multiple divergent copies of the spec; one canonical document, referenced by all tooling.
- **MUST NOT** merge an implementation whose behavior the spec does not describe.

