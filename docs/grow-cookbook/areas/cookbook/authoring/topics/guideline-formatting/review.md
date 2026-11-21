# Review: guideline-formatting

## Findings

none

## Checked

- `cookr roles check` on the folder: ok, 59 rules, no findings; it compiles to the four skills (builder, build-verifier, reviewer, review-verifier).
- The build bar has exactly one line per named rule, in the rules' order (59 and 59, no extra or missing name).
- The review bar names all 59 rules exactly once, sorted by keyword: every MUST rule (including the owner-list rules whose lead-in carries MUST), every SHOULD rule (gf-triggers-field, whose presence is SHOULD, among them), and gf-compliance-section as the one MAY rule.
- Every rule ends with its citation, and every cited id is a claim in `research/research.json` that some verdict names (the only non-matching ids, `fk-index-postgres` and `fk-index-sqlite`, sit in gf-rule-cites-research's example code block, which is owner-list prior text).
- Every `supported` and `new` verdict's rule is present, and every claim those verdicts name is cited by some rule.
- No MUST or MUST NOT rule cites a claim the second check refuted. The MUST rules changed this round cite confirmed claims: gf-structured-guidance (`w3c-qa-consistent-requirement-style`), no-domain-field (`json-schema-no-additional-properties`), released-versions-immutable (`semver-released-immutable`), keywords-impose-no-method (`rfc2119-no-method-imposition`).
- The new SHOULD rules split out this round each cite claims at or above SHOULD strength, refuted claims among them only at SHOULD: guidance-in-discrete-components, list-items-share-one-structure, summary-leads-with-most-important, guideline-defines-scope, scope-holds-no-requirements, rule-specific-and-unambiguous, rule-in-standardized-form, no-positional-rule-identifiers, informative-part-says-so, informative-text-not-normative-sounding, references-marked-normative-or-informative, link-instead-of-repeating, change-history-explains-changes, change-history-dates-each-version, change-history-not-commit-log.
- Owner-list rules keep their prior text word for word, with only the listed lead-ins (conv-legacy-keeps-working, conv-role-values, conv-no-roles-under-reviewing, conv-four-skills, conv-skill-names).
- No rule changed this round carries its reason in its bullet; the reasons sit in the matching `rationale.md` bullets.
- The rationale's source statements match the second check: OWASP ASVS's identifiers "may change between versions" and the problem is a reference without its version (`asvs-positional-ids-problematic`, `asvs-versioned-identifiers`); NASA's checklist "flags" a paragraph mixing requirements and rationale, without calling it common (`nasa-requirements-and-rationale-mixed`); NASA's checklist "asks whether" each requirement can be verified (`nasa-requirements-verifiable`).
- The intro states its conditions (a roled guideline; not listed in `cookbook/research-exempt.json`), carries no RFC keyword, adds a conformance statement, and a scope statement that holds no requirement; it links requirement-keywords, activity-triggers and research-results-document rather than repeating them.
- Each informative part (`how-to-keep-the-rules.md`, `examples.md`, `rationale.md`, `references.md`) says it is informative in its first sentence, and the informative text changed this round states no RFC keyword.
- `references.md` marks RFC 2119 normative and every other source informative, under H3 headings below the part's H2, so no heading level is skipped.
- The how-to's "Choose the keyword from the evidence" bullet is advice with no keyword, and the weakest-claim question is listed in the rationale's "Questions left to the owner".
- `what-a-reviewer-looks-for.md` covers each rule added this round, and its line "does not say when it applies" is held by rule-states-when-it-applies.
- Frontmatter: `summary` is 143 characters and describes the new text; `related` holds research-results-document, template-conformance, requirement-keywords and activity-triggers; `tags` and `platforms: []` fit the guideline.
- `disputes.md` holds one dispute, on a sibling's finding (requirement-keywords R1.8), not on an open finding of this topic, so it needs no ruling here.

## Rulings

- R1.1: fixed — gf-structured-guidance is MUST for one consistent, distinguishable requirement style, citing only `w3c-qa-consistent-requirement-style`; guidance-in-discrete-components and list-items-share-one-structure are new SHOULD rules with their own build-bar lines.
- R1.2: fixed — rule-states-when-it-applies now states the circumstances requirement at SHOULD (claim: iom-standardized-form-and-circumstances), and the action half is the new rule-in-standardized-form, so the reviewer, review-bar, how-to and rationale wording is backed by a rule.
- R1.3: fixed — the "keyword stronger than its claims" review line and review-bar line are gone, the remaining review line ties to normative-keywords-only-where-required and keywords-impose-no-method, the how-to bullet is recast as keyword-free advice, and the question is in the rationale's "Questions left to the owner".
- R1.4: fixed — the intro carries no MUST and states both conditions: roles only for a roled guideline, research unless listed in `cookbook/research-exempt.json`.
- R1.5: fixed — the rationale now says ASVS identifiers may change between versions and a reference without its version becomes a problem, NASA's checklist flags the mixed paragraph, and NASA's checklist asks whether each requirement can be verified; the "since…" clause is gone from stable-rule-identifiers.
- R1.6: fixed — change-history-newest-first, stable-rule-identifiers, conv-research-cited and conv-rationale-to-references each end at their requirement.
- R1.7: fixed — every listed compound rule is split into separately named, separately cited rules (no-domain-field, guidance-in-discrete-components, list-items-share-one-structure, summary-leads-with-most-important, change-history-explains-changes, change-history-dates-each-version, change-history-not-commit-log, informative-part-says-so, informative-text-not-normative-sounding, references-marked-normative-or-informative, guideline-defines-scope, scope-holds-no-requirements, no-positional-rule-identifiers, link-instead-of-repeating), examples-are-non-normative is one clause, and each has its own build-bar line.
- R1.8: fixed — references are marked normative (RFC 2119) or informative, the intro holds a conformance statement and a requirement-free scope statement, and each informative part says so at its start.
- R1.9: fixed — the review bar follows the indexing form and names all 59 rules under MUST, SHOULD and MAY.
- R1.10: fixed — `related` now holds requirement-keywords (`456f23bd-4523-47e8-9541-073ac046f2ad`) and activity-triggers (`1b7b83f9-3b8a-46f7-81b7-9a55291a23a2`).

## Lint

/lint-artifact on `cookbook/guidelines/cookbook/authoring/guideline-formatting` (type guideline, compliance file `tbd/compliance/artifact-formatting/guideline-formatting.md`, compiled doc linted):

```
[PASS] FM-01: YAML frontmatter block present
[PASS] FM-02: id is a valid UUID
[PASS] FM-03: Index entry matches folder (cookbook/index.json path and rdid adc.guideline.cookbook.authoring.guideline-formatting; no domain field)
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: All required fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright is "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates (2026-11-21)
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 "Guideline Formatting" matches title
[PASS] FM-11a: Links resolve (cookr validate passed)
[PASS] FM-12: Change History present with one row
[PASS] FM-13: No TODO or placeholder text
[PASS] GF-01: Summary statement follows the H1
[PASS] GF-02: Structured guidance (59 named rules, bullets, subsections)
[PASS] GF-03: RFC 2119 keywords present in every rule
[PASS] GF-04: Compliance section — not required here. No compliance check references this guideline.
[PASS] gf-type-field
[PASS] gf-title-heading
[PASS] gf-triggers-field: `triggers: []`
[PASS] gf-roled-parts: every part has a role. rules, review-focus, review-bar and build-bar are all present, with no routes or hosts.
[PASS] gf-named-rules: 59 unique kebab-named rules, each with an RFC keyword
[PASS] gf-research-folder: research.json and research.md present, with the four question headings in order. cookr validate passed.
[PASS] gf-rule-cites-research: every rule ends with a (claim: …) citation and every cited id exists in research.json
[PASS] gf-roled-parts (build-bar): exactly one line per named rule, 59 for 59, with no extras

=== LINT SUMMARY ===
Artifact: guideline-formatting
Type: guideline
Pass: 26 | Warn: 0 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

`cookr validate` for the whole cookbook passed; its `owner-decides` warnings were on other artifacts.

lint: clean

verdict: pass
