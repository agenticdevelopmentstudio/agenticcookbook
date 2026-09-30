<!-- leaf: plan-networking/api-design-first · source: guidelines/planning/networking/api-design-first.md -->

**Rules** (cite as `plan-networking/api-design-first#<slug>`):

- `trivial-http-apis-defined-contract-first-write` SHOULD — Non-trivial HTTP APIs SHOULD be defined contract-first: write the OpenAPI document, agree on it, then implement.
- `openapi-document-source-truth-code-spec` MUST — The OpenAPI document MUST be the source of truth. When code and spec disagree, the spec wins and the code is the defect.
- `new-changed-apis-ship-spec-change-same` MUST — New or changed APIs MUST ship the spec change in the same change set as the implementation, never after the fact.
- `spec-linted-ci-lint-step` MUST — The spec MUST be linted in CI, and the lint step MUST fail the build on errors.
- `version-explicitly-document-not-leave-implicit-mixed-across` MUST — Always state the openapi: version explicitly in the document; MUST NOT leave it implicit or mixed across files.
- `agent-derive-from-spec-rather` SHOULD — The agent SHOULD derive these from the spec rather than author them by hand:
- `generated-code-not-edited-hand-regenerate-from` MUST — Generated code MUST NOT be edited by hand; regenerate from the spec instead.
- `ci-job-run-linter-change-touching` MUST — The CI job MUST run the linter on every change touching the spec and MUST treat errors as failures; warnings MAY be …
- `provider-tests-assert-responses-conform-spec` SHOULD — Provider tests SHOULD assert that responses conform to the spec schemas.
- `consumers-validate-against-same-spec` SHOULD — Consumers SHOULD validate against the same spec (generated client + schema validation) so a contract drift fails a …
- `must-not` MUST — generate the spec from running code as the primary workflow (code-first) for a new API — that inverts the source of …
- `must-not-2` MUST — keep multiple divergent copies of the spec; one canonical document, referenced by all tooling.
- `must-not-3` MUST — merge an implementation whose behavior the spec does not describe.

# Design-first API development with OpenAPI

Write the OpenAPI specification before implementing any endpoint, and treat that document as the single source of truth. For an AI agent, the spec is the machine-readable contract you generate code *from* and validate code *against* — design-first turns API work into a deterministic, checkable pipeline instead of guesswork.

## When this applies

- Any non-trivial HTTP/REST API you author or extend (more than one or two trivial endpoints).
- Designing a new module that exposes or consumes an HTTP surface.
- Skip the full ceremony only for throwaway prototypes you will delete.

## Core requirements

- Non-trivial HTTP APIs **SHOULD** be defined contract-first: write the OpenAPI document, agree on it, then implement.
- The OpenAPI document **MUST** be the source of truth. When code and spec disagree, the spec wins and the code is the defect.
- New or changed APIs **MUST** ship the spec change in the same change set as the implementation, never after the fact.
- The spec **MUST** be linted in CI, and the lint step **MUST** fail the build on errors.

## Pin the version

- Use **OpenAPI 3.1.x** as the baseline (full JSON Schema 2020-12 alignment). See https://spec.openapis.org/oas/v3.1.0.
- OpenAPI **3.2.0** was published in September 2025 (adds streaming media types, the `query` HTTP method, `additionalOperations`, and a richer Tag Object). Adopt it **only** when your toolchain — generators, linters, mock servers — fully supports it; otherwise stay on 3.1.x. Verify tool support before relying on 3.2-only features.
- Always state the `openapi:` version explicitly in the document; **MUST NOT** leave it implicit or mixed across files.

## Generate, don't hand-write, the derivatives

The agent **SHOULD** derive these from the spec rather than author them by hand:

| Artifact | Generated from spec | Why |
|----------|--------------------|-----|
| Typed client | `openapi-generator`, `openapi-typescript`, etc. | Callers stay in sync with the contract |
| Server stubs / route validation | server generators or request-validation middleware | Implementation cannot drift silently |
| Mock server | Prism, or generator mocks | Consumers integrate before the backend exists |
| Docs | Redoc, Scalar, Swagger UI | Human + agent reference, always current |

- Generated code **MUST NOT** be edited by hand; regenerate from the spec instead.

## Lint in CI

- Lint with a spec linter (e.g. **Spectral**) using a checked-in `.spectral.yaml` ruleset; extend the built-in OpenAPI ruleset and add house rules (naming, required `operationId`, error-schema presence).
- Consider adding security-focused rules (e.g. an OWASP API Security ruleset) to catch missing auth and unconstrained inputs at design time.
- The CI job **MUST** run the linter on every change touching the spec and **MUST** treat errors as failures; warnings **MAY** be allowed but **SHOULD** trend to zero.
- Add a breaking-change diff check (e.g. `oasdiff`) so backward-incompatible edits are caught before merge.

## Contract checks both ways

- Provider tests **SHOULD** assert that responses conform to the spec schemas.
- Consumers **SHOULD** validate against the same spec (generated client + schema validation) so a contract drift fails a test, not production.

## Anti-patterns

- **MUST NOT** generate the spec from running code as the primary workflow (code-first) for a new API — that inverts the source of truth and lets undocumented behavior leak in.
- **MUST NOT** keep multiple divergent copies of the spec; one canonical document, referenced by all tooling.
- **MUST NOT** merge an implementation whose behavior the spec does not describe.
