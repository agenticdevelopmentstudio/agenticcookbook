# Review: cookbook-formatting

## Findings

none

## Checked

- `rules.md`, `version-is-semver`: "as Android's guidance points to" and `android-semver-good-basis` are gone. The rule is SHOULD and cites `semver-normal-version-form`, `semver-no-leading-zeroes`, `semver-suggested-regex`, `swiftpm-version-semver`, `npm-version-node-semver` and `cargo-version-three-numeric-parts`. None of these is permissive or refuted. `android-semver-good-basis` is still named by the verdict that keeps `version-is-semver` as its rule, so no `supported` or `new` verdict is left without a rule.
- `references.md` and the `references` frontmatter still list the Android versioning page. That is still correct, because `cf-format-is-integer` and `schema-format-const-2` cite `android-versioncode-integer` from the same page.
- `rationale.md`, paragraph 2: "Cargo's packaging step checks a package by building it, beyond parsing its manifest" matches `cargo-package-verify-build` ("beyond parsing it").
- `rationale.md`, paragraph 3: "JSON Schema 2020-12 says unknown keywords should be treated as annotations" matches the SHOULD in the quote of `jsonschema-unknown-keywords-annotations`, and so keeps the second check's correction. "Unless the schema is compiled strictly" stays consistent with `validate-the-schema-strictly`.
- `rationale.md`, last paragraph: "npm, for one, requires only `name` and `version`, and only of a package it publishes" matches `npm-name-version-required-to-publish`. It no longer contradicts the "against" source that owner-list.md records for `cf-required-project-fields`.
- `a-build-must-establish.md`, `closed-objects-keep-an-extension-point`: the build-bar line is now conditional ("when added", "when closed with `unevaluatedProperties`"), which matches the rule's two MAY halves.
- `what-a-reviewer-looks-for.md`: the `allOf` bullet is now conditional ("if closed, ... or the change says why"), which matches the MAY strength and the form of the other MAY bullets.
- `artifact.json` `related` now holds `2c5ee8e0-9da5-4b44-9f87-51962abe76ab` (ingredient-formatting), the sibling that `cf-source-domains`, `cf-code-root-coverage` and `cf-library-tree-mirrors-code` rest on.
- diff-2.md changes nothing beyond these four fixes, so no other text is open to review this round.
- `cookr lint` Phase A: all 389 artifacts passed the deterministic checks. Phase B, the LLM pass, cannot run from this checkout's cookr because `skills/cookr/cli/references/prompts/lint.md` is missing, so the /lint-artifact skill below supplies the quality pass. `cookr roles check` compiles every role for this guideline, including the reviewer and review-verifier.

## Rulings

- R1.1: fixed — `version-is-semver` no longer cites `android-semver-good-basis` or invokes Android's guidance. It rests on claims that support SHOULD.
- R1.2: fixed — all three rationale sentences now read as the research words them: SHOULD for unknown keywords, "beyond parsing" for Cargo, and npm's name and version for publishing.
- R1.3: fixed — the build-bar line and the review-focus bullet for `closed-objects-keep-an-extension-point` are both conditional, matching the rule's MAY.
- R1.4: fixed — `related` now names ingredient-formatting (`2c5ee8e0-9da5-4b44-9f87-51962abe76ab`).

## Lint

/lint-artifact on `cookbook/guidelines/cookbook/authoring/cookbook-formatting`, with cookr run as instructed:

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: YAML frontmatter block present
[PASS] FM-02: id is a valid UUID (4c7be774-12c6-4bf0-a9ee-82e8633610dc)
[PASS] FM-03: index.json entry matches folder (rdid adc.guideline.cookbook.authoring.cookbook-formatting; no domain field)
[PASS] FM-04: type is guideline
[PASS] FM-05: version is valid semver (1.0.0)
[PASS] FM-06: all required fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright has year and name
[PASS] FM-09: created and modified are valid dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 matches title
[PASS] FM-11a: links resolve (cookr validate passed)
[PASS] FM-12: Change History present with one row
[PASS] FM-13: no TODO/TBD/FIXME/placeholder text
[PASS] GF-01 / gf-summary-statement: summary follows the H1
[PASS] GF-02 / gf-structured-guidance: rules, a numbered procedure, subsections
[WARN] GF-03 / gf-rfc-keywords: schema-structure-kind-enum
       -> The rule is only a quoted JSON fragment. Its only keyword, "MAY be omitted", sits inside the
          quoted description string. The rule states no obligation of its own. Every other rule is fine.
[PASS] gf-frontmatter-complete
[PASS] gf-type-field
[PASS] gf-title-heading
[PASS] gf-change-history
[PASS] gf-triggers-field: triggers [recipe-authoring, configuration]
[PASS] gf-roled-parts: every part has a role, and rules, review-focus, review-bar and build-bar are all present
[FAIL] gf-named-rules: schema-structure-kind-enum
       -> The obligation must be an RFC 2119 keyword in the rule's own text. It currently reads
          `- **schema-structure-kind-enum**: "kind": { ... }`.
          Reword it as "The schema MUST type `structure.kind` as written here: ...", the way
          schema-version-pattern does.
          The other 49 rules have unique names and a keyword.
[PASS] gf-research-folder: research.json and research.md present, with the four headings in order
[PASS] gf-rule-cites-research: all 50 rules end in a citation and every cited id is a claim
[PASS] build-bar: 50 lines, one per rule, none extra
[WARN] GF-04 / gf-compliance-section: no `## Compliance` section
       -> Optional unless a compliance check references this guideline.
[WARN] style: cf-type-field
       -> The rule text reads `MUST be \"cookbook\"`, with a stray backslash-escaped quote in the markdown.
          Write the value as `` `cookbook` `` or `"cookbook"`.

=== LINT SUMMARY ===
Artifact: cookbook-formatting
Type: guideline
Pass: 28 | Warn: 3 | Fail: 1
RESULT: NOT CLEAN — 1 failing check.
```

The one FAIL, `gf-named-rules` on `schema-structure-kind-enum`, hits text that this round did not change. That text is the owner-list prior text, kept word for word. Round 1's lint passed the same text. owner-list.md gives this rule no lead-in, so under criterion 5 the author cannot add the suggested "The schema MUST type `structure.kind` as written here:". Only a lead-in listed in owner-list.md is accepted. The fix therefore belongs to the owner: add a lead-in for `schema-structure-kind-enum` to owner-list.md, and the author then applies it. Until that happens the lint error stands, so it is counted below.

lint: fail 1

verdict: fail
