
- Full-stack previews SHOULD include the real backend, not just a static frontend against shared staging — interaction bugs between front and back surface only when both run the PR's code.
- Run E2E/smoke suites and contract tests (see `agenticdevelopercookbook://guidelines/testing/contract-testing`) against the live URL, and post the preview link plus check results back as a PR comment for human review.
- For changes too large to stand up a full stack per PR, a request-routing / intercept approach (e.g. Telepresence-style local interception into a shared cluster) MAY substitute — treat that as a deliberate decision, not the default.

