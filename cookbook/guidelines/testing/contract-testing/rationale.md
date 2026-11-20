
- `should-cover-owned-integrations-with-consumer-driven-contracts`, `should-gate-deploy-with-can-i-deploy`: This lets consumer and provider deploy independently while keeping the boundary honest.
- `should-use-schema-contracts-for-uncontrolled-apis`, `must-not-expect-third-party-contracts-to-gate-their-deploys`: For an API you do not control, you cannot make them run your contract.
- `must-assert-contract-shape`, `must-not-assert-incidental-detail`, `should-loosen-over-strict-contracts`: Loose contracts survive benign provider changes.
