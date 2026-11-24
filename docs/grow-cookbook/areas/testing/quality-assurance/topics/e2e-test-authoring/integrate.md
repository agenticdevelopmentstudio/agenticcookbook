# Integrate: e2e-test-authoring

Lossless: a new topic, with no base text in the cookbook (`roles lossless` reports the artifact is not in the base 77a898dbc718928bbd96ef617723c83ec69cd549); nothing to account for.

## For the owner

`cookr validate` owner-decides warning for this topic:

- `rationale-names-what-makes-assertion-correct` cites `rationale-names-what-makes-assertion-correct-prior`, which the research rules unsupported. The owner decides the rule: keep it as it is, reword it, or drop it. It stands, word for word under the lead-in "A spec's rationale MUST keep this true:", until the owner decides.

Open questions from owner-list.md:

- Whether a rationale that does not cite its feature doc, plan or commit is a fail (MUST, as rationale-names-what-makes-assertion-correct states) or a SHOULD, which is what the ISTQB traceability text supports.
- Whether a test id may be a first-choice locator: Playwright calls test ids the most resilient way of testing, while Testing Library recommends them only when no role or text match fits; the owner decides which order the cookbook adopts.
- Whether hermetic is the default for every spec, and how many live or preview specs a suite keeps (Cypress suggests one true end-to-end test per feature with the rest stubbed); the count itself belongs to the test-pyramid topic.
- How live specs are selected and gated: by tag and grep, by a separate project or directory, or by an environment variable; the sources show all three and prefer none.
- Whether CI retries are allowed for E2E specs and how many; Playwright and Android both offer retries and both say a test that passes on retry is flaky and must be fixed.
- Whether the rule against real user data in a patch is kept at MUST strength: its credentials half rests on OWASP ASVS, its personal-data half on the data-minimisation principle and a Thoughtworks Hold rather than a test-specific requirement.
- Whether page objects are recommended, allowed or left to the team, given that Cypress lists sharing page objects as an anti-pattern while Selenium and Playwright's fixture guide build on them.

Routed by review R1.7. The two guidelines are outside this area, so the question stays here:

- `testing/properties-of-good-tests` (`must-be-isolated`, `must-be-deterministic`) and `testing/flaky-test-prevention` (`must-not-share-mutable-state`, `must-not-depend-on-execution-order`, `must-not-ignore-flaky-tests`) state at MUST what this guideline's research supports only at SHOULD (`write-deterministic-specs`, `e2e-isolate-test-state`, `e2e-no-shared-test-data`, `e2e-fix-flaky-tests`). The owner decides whether those guidelines keep MUST or are re-researched.

- from the phase 3 code review (claude-code-review/f6): `rationale-names-what-makes-assertion-correct` (MUST) restates the SHOULD `rationale-cites-assertion-source`, so the SHOULD's stated-departure escape does nothing. The review suggests merging the pair into one rule at one strength.
- from the phase 3 code review (claude-code-review/f8): the name `no-credentials-or-real-user-data` promises a ban on real user data, but the rule covers credentials only, so a reviewer checking by name may enforce more than the text. It is a prior rule, whose name stays fixed, so the rename is the owner's; the review suggests renaming it to match its text.

integrated: 2026-11-24
