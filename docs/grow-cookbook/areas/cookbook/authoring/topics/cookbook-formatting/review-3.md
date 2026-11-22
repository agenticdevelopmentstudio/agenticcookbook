# Review: cookbook-formatting

## Findings

none

## Checked

- `rules.md` line 46, `schema-structure-kind-enum`: the source folder now carries the lead-in "The schema MUST type `structure.kind` as written here:", exactly as owner-list.md lists it under the owner ruling of 2026-11-22. The prior text after it is word for word, and the rule still ends with `(claim: schema-structure-kind-enum-prior)`, which exists in research.json.
- Strength: `schema-structure-kind-enum-prior` is not among the second check's refutations (it appears nowhere in second-check.md; its `trust.basis` is "no research source supports it"), so MUST is allowed under criterion 3. The MUST comes from the owner's lead-in, which criterion 5 accepts. It matches how `schema-depends-on-dot-paths` and `schema-version-pattern` carry theirs.
- `a-complete-review-must-establish.md`: `schema-structure-kind-enum` has moved from the MAY list to the MUST list, matching its new MUST strength. Each rule appears in exactly one list.
- `a-build-must-establish.md` line 46: the `schema-structure-kind-enum` line now names `structure.kind`, which matches the rule's lead-in.
- The verdict for `schema-structure-kind-enum` (`unsupported`) still has a rule, and no `supported` or `new` verdict lost one: the round changes no citation.
- diff-3.md changes nothing else, so no other text is open to review this round.
- `cookr roles check` on the folder compiles every role, including the reviewer (88 lines) and the review-verifier (33 lines).

## Rulings

none (no findings were open)

## Lint

/lint-artifact (v2.0.1) on `cookbook/guidelines/cookbook/authoring/cookbook-formatting`, with this checkout's cookr run as instructed:

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: frontmatter present in the compiled doc
[PASS] FM-02: id is the UUID 4c7be774-12c6-4bf0-a9ee-82e8633610dc
[PASS] FM-03: index.json entry matches the folder (rdid adc.guideline.cookbook.authoring.cookbook-formatting; no domain field)
[PASS] FM-04: type is guideline
[PASS] FM-05: version is 1.0.0
[PASS] FM-06: all 17 required fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright is 2026 Mike Fullerton
[PASS] FM-09: created and modified are valid dates
[PASS] FM-10: summary is a full sentence
[PASS] FM-11: H1 "Cookbook Formatting" matches title
[PASS] FM-11a: cookr validate passed; related 2c5ee8e0-9da5-4b44-9f87-51962abe76ab resolves, depends-on empty
[PASS] FM-12: Change History has one row (1.0.0)
[PASS] FM-13: no TODO/TBD/FIXME/placeholder text
[PASS] GF-01 / gf-summary-statement: summary paragraph follows the H1
[PASS] GF-02 / gf-structured-guidance: rule bullets, tables and subsections
[PASS] GF-03 / gf-rfc-keywords: all 50 named rules carry MUST, SHOULD or MAY
[PASS] GF-04 / gf-compliance-section: optional and absent; no compliance check references this guideline
[PASS] gf-type-field, gf-title-heading: covered by FM-04 and FM-11
[PASS] gf-change-history: final section, Version/Date/Author/Summary table
[PASS] gf-triggers-field: triggers [recipe-authoring, configuration]
[PASS] gf-roled-parts: every part but intro and history has a role; rules, review-focus, review-bar and build-bar present
[PASS] gf-named-rules: 50 named, unique rules, each with an RFC keyword
[PASS] build-bar: 50 lines matching the 50 rule names exactly
[PASS] gf-research-folder: research.json and research.md present; not in research-exempt.json
[PASS] gf-rule-cites-research: all 50 rules end in a citation and every cited id is a claim in research.json

=== LINT SUMMARY ===
Artifact: cookbook-formatting (guideline)
Pass: 33 | Warn: 0 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

The round-2 `gf-named-rules` failure on `schema-structure-kind-enum` is resolved by the owner's lead-in.

lint: clean

verdict: pass
