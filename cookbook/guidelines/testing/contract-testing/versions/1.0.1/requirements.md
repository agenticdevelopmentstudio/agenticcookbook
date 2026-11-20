
- Service-to-service integrations where you own both sides **SHOULD** be covered by consumer-driven contract tests, not by relying on end-to-end tests for boundary correctness.
- Contracts **MUST** assert the *shape* — required fields, types, and key status/error codes — and **MUST NOT** assert every field value or incidental detail. Loose contracts survive benign provider changes.
- Providers **MUST** verify outstanding consumer contracts in CI before deploy. A consumer-driven setup (e.g. Pact with a broker) **SHOULD** gate deployment with a `can-i-deploy` check that confirms every dependent consumer's contract still passes against the version being shipped.
- Contract tests **MUST** run as their own CI stage, separate from end-to-end tests, so a contract failure points directly at the broken boundary.
- Each contract **MUST** be versioned and tagged with the deployment environment (or pacticipant version) so the broker can answer "is this pair compatible in `production`?" rather than just "is the latest pair compatible?".
- For consumed third-party APIs, the pinned schema revision **MUST** be recorded (URL + version/date). When the provider publishes a new revision, re-pin deliberately — **MUST NOT** silently track a moving `latest`.
- Contract tests **MUST NOT** require the real provider to be running. The consumer side runs against a stub generated from the contract; the provider side replays recorded interactions against its real handler.

