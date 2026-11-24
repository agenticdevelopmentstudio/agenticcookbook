# Review: e2e-test-authoring

## Findings

none

## Checked

- `writing-a-spec.md`, the Selenium bullet now reads "It ranks unique IDs, then a well-written CSS selector, above XPath; this guideline applies that order to the structural locator a spec falls back to." That matches ks-se-locator-preference ("If unique IDs are unavailable, a well-written CSS selector is the preferred method of locating an element"). It also says that limiting the order to the structural fallback is this guideline's choice, not Selenium's.
- `writing-a-spec.md`, the Windows UI Automation bullet now reads "which typically needs container and scope information to be useful". That matches pg-ms-automationid-scope's quote and the Rationale's wording.
- The diff-3.md changes are these two bullets only. No other text changed, so there is nothing new to review.
- The new Selenium wording agrees with `e2e-prefer-unique-id-to-css-to-xpath` in `rules.md` ("Where a spec falls back to a structural locator, it SHOULD prefer a unique ID, then a well-written CSS selector, to XPath") and with the Rationale ("kept for the structural locator a spec falls back to").
- `cookr roles check` passes: `ok: true`, 47 rules, no findings, and the builder, reviewer and review-verifier skills compile.

## Rulings

- R2.1: fixed — (1) the Selenium bullet now gives Selenium's order as unique IDs, then a well-written CSS selector, above XPath, and says this guideline applies that order to the structural fallback; (2) the Windows UI Automation bullet restores "typically", as pg-ms-automationid-scope's quote has it.

## Lint

/lint-artifact on `guidelines/testing/quality-assurance/e2e-test-authoring` (guideline): CLEAN. Pass 22 | Warn 1 | Fail 0.
- WARN gf-research-folder (owner-decides): `rationale-names-what-makes-assertion-correct` cites a claim the research marks `unsupported`. `cookr validate` passes it with the owner-decides warning. This rule is on the owner list.
- PASS: FM-01 to FM-13, GF-01 to GF-03, gf-roled-parts, gf-named-rules, build-bar parity (47 lines, one per rule), gf-research-folder, gf-rule-cites-research, gf-triggers-field.
- N/A: GF-04 (the optional `## Compliance` section).
- Outside this artifact: repo-wide `cookr validate` reports 3 issues, all missing frontmatter in the `research.md` files of exploratory-testing-charters, test-failure-triage and test-impact-analysis. None of them is in this artifact.
lint: clean

verdict: pass
