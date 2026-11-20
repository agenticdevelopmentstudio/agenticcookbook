
- Lint with a spec linter (e.g. **Spectral**) using a checked-in `.spectral.yaml` ruleset; extend the built-in OpenAPI ruleset and add house rules (naming, required `operationId`, error-schema presence).
- Consider adding security-focused rules (e.g. an OWASP API Security ruleset) to catch missing auth and unconstrained inputs at design time.
- The CI job **MUST** run the linter on every change touching the spec and **MUST** treat errors as failures; warnings **MAY** be allowed but **SHOULD** trend to zero.
- Add a breaking-change diff check (e.g. `oasdiff`) so backward-incompatible edits are caught before merge.

