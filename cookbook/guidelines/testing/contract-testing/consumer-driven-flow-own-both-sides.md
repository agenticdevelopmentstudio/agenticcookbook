
1. **Consumer** writes a test describing the requests it makes and the response shape it depends on; this produces a contract artifact.
2. The contract is published to a shared **broker** (or committed/exchanged) and tagged with the consumer's version + environment.
3. **Provider** pulls outstanding contracts and verifies them against its real implementation in CI.
4. Either side runs **`can-i-deploy`** before release: the broker confirms the to-be-deployed version is compatible with every counterpart already in the target environment. A failure blocks the deploy.

This lets consumer and provider deploy independently while keeping the boundary honest. Pact is a common toolchain for this pattern (see references); the practice — not the tool — is what matters and **SHOULD** be applied with whatever framework fits the stack.

