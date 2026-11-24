# Owner list: e2e-test-authoring

For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **rationale-names-what-makes-assertion-correct** — verdict `unsupported` (claims: rationale-names-what-makes-assertion-correct-prior, bp-istqb-traceability). Prior text, kept word for word: "The rationale names the feature doc, plan, or commit the new assertion derives from. A rationale that argues the assertion is sensible, without citing what makes it correct, is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "A spec's rationale MUST keep this true:" (the one change the reviewer accepts)
  - against: Test cases are traced to the test-basis elements (requirements, plans) they derive from.

## Open questions

- Whether a rationale that does not cite its feature doc, plan or commit is a fail (MUST, as rationale-names-what-makes-assertion-correct states) or a SHOULD, which is what the ISTQB traceability text supports.
- Whether a test id may be a first-choice locator: Playwright calls test ids the most resilient way of testing, while Testing Library recommends them only when no role or text match fits; the owner decides which order the cookbook adopts.
- Whether hermetic is the default for every spec, and how many live or preview specs a suite keeps (Cypress suggests one true end-to-end test per feature with the rest stubbed); the count itself belongs to the test-pyramid topic.
- How live specs are selected and gated: by tag and grep, by a separate project or directory, or by an environment variable; the sources show all three and prefer none.
- Whether CI retries are allowed for E2E specs and how many; Playwright and Android both offer retries and both say a test that passes on retry is flaky and must be fixed.
- Whether the rule against real user data in a patch is kept at MUST strength: its credentials half rests on OWASP ASVS, its personal-data half on the data-minimisation principle and a Thoughtworks Hold rather than a test-specific requirement.
- Whether page objects are recommended, allowed or left to the team, given that Cypress lists sharing page objects as an anti-pattern while Selenium and Playwright's fixture guide build on them.
