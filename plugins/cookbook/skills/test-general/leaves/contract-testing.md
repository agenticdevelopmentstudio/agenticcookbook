<!-- leaf: test-general/contract-testing · source: guidelines/testing/contract-testing.md -->

**Rules** (cite as `test-general/contract-testing#<slug>`):

- `own-both-sides-covered-consumer-driven-contract` SHOULD — Service-to-service integrations where you own both sides SHOULD be covered by consumer-driven contract tests, not by …
- `contracts-assert-shape-fields-types` MUST — Contracts MUST assert the *shape* — required fields, types, and key status/error codes — and MUST NOT assert every …
- `providers-verify-outstanding-consumer-contracts` MUST — Providers MUST verify outstanding consumer contracts in CI before deploy. A consumer-driven setup (e.g. Pact with a …
- `contract-tests-run-their-own-ci` MUST — Contract tests MUST run as their own CI stage, separate from end-to-end tests, so a contract failure points directly at …
- `contract-versioned-tagged-deployment-environment` MUST — Each contract MUST be versioned and tagged with the deployment environment (or pacticipant version) so the broker can …
- `pinned-schema-revision-recorded-url-version-date` MUST — For consumed third-party APIs, the pinned schema revision MUST be recorded (URL + version/date). When the provider …
- `contract-tests-not-require-real-provider-running` MUST — Contract tests MUST NOT require the real provider to be running. The consumer side runs against a stub generated from …
- `tool-what-matters-applied-whatever-framework-fits` SHOULD — This lets consumer and provider deploy independently while keeping the boundary honest. Pact is a common toolchain for …
- `must-not` MUST — treat end-to-end tests as a substitute for contract tests — they are slower, flakier, and fail far from the cause.
- `must-not-2` MUST — write a "contract" test against a third-party API you own neither side of and expect it to gate *their* deploys; you …
- `should-not` SHOULD — duplicate full business-logic assertions inside contracts — that belongs in unit/integration tests for each service.

# Contract testing for services

A contract test verifies that two independently deployed services agree on the shape of the messages they exchange — without standing up the whole system. It catches the integration breakage that unit tests miss and end-to-end tests catch too late and too expensively.

When an AI codegen system emits several interoperating services (microservices, a web backend, mobile/web clients), each side evolves on its own schedule. The blind spot is structural: each service's own tests pass, yet a renamed field or a changed status code silently breaks the boundary. Contract tests close that gap.

## When to use which style

- **Consumer-driven contracts** — use when you own *both* sides of the interaction (your own services calling each other). The consumer's expectations define the contract; the provider verifies it.
- **Provider / schema contracts** — use for third-party or upstream APIs you consume but do **not** control. Pin to the provider's published schema (e.g. an OpenAPI document at a dated revision) and test that your client tolerates it; you cannot make them run your contract.

## Requirements

- Service-to-service integrations where you own both sides **SHOULD** be covered by consumer-driven contract tests, not by relying on end-to-end tests for boundary correctness.
- Contracts **MUST** assert the *shape* — required fields, types, and key status/error codes — and **MUST NOT** assert every field value or incidental detail. Loose contracts survive benign provider changes.
- Providers **MUST** verify outstanding consumer contracts in CI before deploy. A consumer-driven setup (e.g. Pact with a broker) **SHOULD** gate deployment with a `can-i-deploy` check that confirms every dependent consumer's contract still passes against the version being shipped.
- Contract tests **MUST** run as their own CI stage, separate from end-to-end tests, so a contract failure points directly at the broken boundary.
- Each contract **MUST** be versioned and tagged with the deployment environment (or pacticipant version) so the broker can answer "is this pair compatible in `production`?" rather than just "is the latest pair compatible?".
- For consumed third-party APIs, the pinned schema revision **MUST** be recorded (URL + version/date). When the provider publishes a new revision, re-pin deliberately — **MUST NOT** silently track a moving `latest`.
- Contract tests **MUST NOT** require the real provider to be running. The consumer side runs against a stub generated from the contract; the provider side replays recorded interactions against its real handler.

## Consumer-driven flow (own-both-sides)

1. **Consumer** writes a test describing the requests it makes and the response shape it depends on; this produces a contract artifact.
2. The contract is published to a shared **broker** (or committed/exchanged) and tagged with the consumer's version + environment.
3. **Provider** pulls outstanding contracts and verifies them against its real implementation in CI.
4. Either side runs **`can-i-deploy`** before release: the broker confirms the to-be-deployed version is compatible with every counterpart already in the target environment. A failure blocks the deploy.

This lets consumer and provider deploy independently while keeping the boundary honest. Pact is a common toolchain for this pattern (see references); the practice — not the tool — is what matters and **SHOULD** be applied with whatever framework fits the stack.

## Keep contracts loose

- Match on field presence and type, and on matcher-based values (e.g. "an ISO-8601 string", "a positive integer"), not on exact literals that change per request.
- Assert the error/status codes the consumer branches on; ignore codes it never inspects.
- A contract that breaks on a *backward-compatible* provider change (a new optional field, a reordered list) is too strict — loosen it.

## Anti-patterns

- **MUST NOT** treat end-to-end tests as a substitute for contract tests — they are slower, flakier, and fail far from the cause.
- **MUST NOT** write a "contract" test against a third-party API you own neither side of and expect it to gate *their* deploys; you can only assert your tolerance of their pinned schema.
- **SHOULD NOT** duplicate full business-logic assertions inside contracts — that belongs in unit/integration tests for each service.
