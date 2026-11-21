# Review: cookbook-formatting

## Findings

- `rules.md`, `version-is-semver` (strength rule, criterion 3): the rule is SHOULD, but it cites `android-semver-good-basis`. That claim says Android's guidance points at Semantic Versioning "without mandating it" ("many developers consider Semantic Versioning a good basis"), and the second check notes "the guidance does not mandate SemVer". So the weakest cited claim is below SHOULD. I checked all 50 rules for a SHOULD or MUST that cites a claim whose own wording is permissive or non-mandating. This is the only instance. Definitional and factual claims, such as `jsonschema-required-keyword`, `jsonschema-const-keyword` and `topological-order-needs-dag`, do not weaken a rule. Fix: drop "as Android's guidance points to" and `android-semver-good-basis` from the citation. The rule still rests on `semver-normal-version-form`, `semver-no-leading-zeroes`, `swiftpm-version-semver`, `npm-version-node-semver` and `cargo-version-three-numeric-parts`, and the `version-is-full-semver` verdict keeps its rule. Leave the Android point to `rationale.md` if it is wanted.
- `rationale.md` (source fidelity, criterion 2): three sentences say more than, or the opposite of, the research. (1) Paragraph 3: "Unknown keywords are treated as annotations too". This flat statement is the overstatement the second check refuted for `jsonschema-unknown-keywords-annotations`: Core 2020-12 says they "SHOULD be treated as annotations", and Ajv's strict mode rejects them. `validate-the-schema-strictly` already words it correctly. Fix: "JSON Schema 2020-12 says unknown keywords should be treated as annotations, so a misspelt keyword in the schema constrains nothing unless the schema is compiled strictly." (2) Paragraph 2: "as Cargo checks a package by building it rather than by parsing its manifest". `cargo-package-verify-build` says Cargo's packaging step checks the package "beyond parsing it", not instead of parsing it. Fix: "as Cargo's packaging step checks a package by building it, beyond parsing its manifest". (3) Last paragraph: "no outside source requires them or argues against them". The research has a source against one of them: the `cf-required-project-fields` verdict cites `npm-name-version-required-to-publish` (npm requires only name and version, and only for a package that will be published), and owner-list.md lists it as "against". Fix: "…are this cookbook's own design; no outside source requires them, and npm, for one, requires only `name` and `version`, and only of a package it publishes."
- `a-build-must-establish.md` and `what-a-reviewer-looks-for.md`, `closed-objects-keep-an-extension-point` (the bars must match the rule's strength, cross-recipe-consistency within the guideline): both halves of the rule are MAY, including "a closed object meant to be extended through `allOf` MAY be closed with `unevaluatedProperties`". Both parts turn the second half into an unconditional requirement. Build bar: "closed objects extended through `allOf` use `unevaluatedProperties`". Review focus: "an object meant to be extended through `allOf` uses `unevaluatedProperties`". I checked every other MAY rule's build-bar line and review-focus bullet, and each is conditional ("when marked", "when present", "when generated", "when added"). Fix: build bar "an extension point, when added, is open for other tools, and a closed object extended through `allOf`, when closed with `unevaluatedProperties`, sees its subschemas' properties". Review focus: "an object meant to be extended through `allOf`, if closed, is closed with `unevaluatedProperties` rather than `additionalProperties`, or the change says why".
- `artifact.json` `related` (frontmatter, criterion 6): `related` is `[]`, though the new text rests on a sibling guideline. `cf-source-domains` needs every `source.id` to be "the UUID of an ingredient or recipe" that resolves in `index.json`. `cf-code-root-coverage` and `cf-library-tree-mirrors-code` depend on "artifact's implementations" recorded in `index.json`. `ingredient-formatting` (`2c5ee8e0-9da5-4b44-9f87-51962abe76ab`) defines that identity and the `index.json` implementations (`if-reference-implementations`). Its siblings `guideline-formatting`, `ingredient-formatting` and `principle-formatting` all fill `related`. Fix: add `2c5ee8e0-9da5-4b44-9f87-51962abe76ab` to `related`.

## Checked

- Every one of the 50 verdicts has a rule. Two `new` verdicts were renamed, which criterion 4 allows: `report-every-error-with-its-location` became `report-every-error`, and `version-is-full-semver` became `version-is-semver`. No other rule name changed.
- Every claim named by a `supported` or `new` verdict is cited by some rule, including `jsonschema-defined-over-json`, `cargo-version-three-numeric-parts`, `rfc9562-mixed-case` and `jsonschema-unknown-keywords-annotations` (checked by script).
- Every rule ends with exactly one citation, every cited id exists in research.json, and every cited id is named by some verdict. `jsonschema-uuid-format-rfc4122`, the one claim no verdict names, is not cited.
- Refuted claims: none carries a MUST. `rfc9562-treat-uuids-opaquely` is cited only by `uuid-compared-not-parsed` (SHOULD), and `cf-uuid-format` cites only its prior. `jsonschema-defined-over-json` is cited by `semantic-checks-in-code` (SHOULD), and `cf-valid-json` dropped it to keep its MUST on `rfc8259-parser-accepts-grammar`. `schemastore-version-suffixed-schemas` is cited by `schema-has-stable-absolute-id` (SHOULD), `jsonschema-unknown-keywords-annotations` by `validate-the-schema-strictly` (SHOULD), and `cargo-metadata-ignored` by `closed-objects-keep-an-extension-point` (MAY). The second check listed no dropped citations.
- MUST rules on cited claims rest on claims that say must, or on definitions and facts: `cf-valid-json`, `manifest-is-utf8-without-bom`, `cf-schema-valid`, `cf-required-identity-fields`, `cf-format-is-integer`, `cf-rdid-format`, `released-version-is-immutable`, `cf-spec-paths-valid`, `cf-no-circular-deps`, `schema-required-identity`, `schema-format-const-2` and `schema-rdid-pattern`. SHOULD rules on SHOULD claims (`no-duplicate-member-names`, `schema-dialect-2020-12`, `schema-has-stable-absolute-id`, `schema-license-spdx`) are at strength.
- Owner list: all 17 prior rules match their prior text word for word (checked by script), and each cites only `<rule>-prior`. The four lead-ins (`cf-dependencies-in-cookr-config`, `cf-library-tree-is-arrangement`, `schema-version-pattern`, `schema-depends-on-dot-paths`) are exactly the ones owner-list.md gives. `schema-structure-kind-enum` has no lead-in because the owner list gives none. Its only keyword is the MAY inside the quoted description, so the review bar's MAY classification follows the text.
- Open questions are left open. `version-is-semver` asks for no leading zeroes ("either way", as the open question says) and does not rule on pre-release or build suffixes. `enable-format-assertion` and the how-to offer both format assertion and a `pattern`. `schema-closed-objects` and the MAY extension point leave the closure question open. `uuid-compared-not-parsed` rules only on comparison, not on written case or normalisation. `schema-rdid-pattern` keeps the existing pattern without tightening it. `schema-license-spdx` does not choose between a single identifier and an expression. `schema-association-declared` is only a MAY.
- `## A build must establish` has exactly one line per rule (50) and no stray names. `cookr roles check` reports ok with 50 rules and no findings.
- `## A complete review must establish` sorts every rule by its keyword: 27 MUST, 18 SHOULD and 5 MAY, 50 in all.
- The how-to's order (bytes, parse, schema, semantic checks) matches the rules. The Python sketch's `TopologicalSorter` mapping (node to its depends-on list) is correct, and the cycle example's output `['app.ui', 'app.store', 'app.ui']` matches what `graphlib` prints when run.
- The examples' version table matches `version-is-semver` and `cf-semver-fields`: `01.2.3` is accepted by the pattern but is not SemVer.
- Frontmatter: `summary` is 145 characters and describes the new text. `tags` (`cookbook`, `manifest`, `json-schema`, `validation`) fit, `platforms` is `[]`, and `triggers` are set. `references` matches references.md and the research's 29 sources. `version`, `modified` and the history are left to stage 5.
- recipe-quality guidelines: there are no invented requirements beyond the cited research or the owner's prior text (source-fidelity), the roled parts are all present (template-conformance), and there are no TODOs or placeholders (completeness).

## Lint

/lint-artifact on `cookbook/guidelines/cookbook/authoring/cookbook-formatting` (cookr run as instructed):

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: frontmatter present
[PASS] FM-02: id is a valid UUID (4c7be774-12c6-4bf0-a9ee-82e8633610dc)
[PASS] FM-03: cookbook/index.json has the entry at guidelines/cookbook/authoring/cookbook-formatting, rdid adc.guideline.cookbook.authoring.cookbook-formatting, no domain field
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: all required fields present, plus triggers
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright is "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 "Cookbook Formatting" matches title
[PASS] FM-11a: links resolve (cookr validate: all 389 artifacts passed deterministic checks)
[PASS] FM-12: Change History has a row
[PASS] FM-13: no TODO, TBD, FIXME, placeholder or fill-in text
[PASS] GF-01 / gf-summary-statement: a summary follows the H1
[PASS] GF-02 / gf-structured-guidance: 50 named rules plus subsections
[PASS] GF-03 / gf-rfc-keywords: rules use MUST, SHOULD and MAY
[PASS] gf-roled-parts: rules, review-focus, review-bar and build-bar parts are present
[PASS] gf-named-rules: 50 rules, all named
[PASS] build-bar: 50 lines, one per rule
[PASS] gf-research-folder: research/research.json and research/research.md are present
[PASS] gf-rule-cites-research: 50 rules, each ending in a (claim: ...) citation, and cookr validate passes the research citation checks
[PASS] gf-triggers-field: triggers are present
[WARN] GF-04 / gf-compliance-section: no ## Compliance section
       -> This is optional (MAY). Add one only if other compliance checks reference this guideline.

=== LINT SUMMARY ===
Artifact: cookbook-formatting (guideline)
Type: guideline
Pass: 23 | Warn: 1 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

The repo-wide `cookr validate` printed "Validation failed", but only for `owner-decides` research rows on other artifacts. No line names this artifact.

lint: clean

verdict: fail
