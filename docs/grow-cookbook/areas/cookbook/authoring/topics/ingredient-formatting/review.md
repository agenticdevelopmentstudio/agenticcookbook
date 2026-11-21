# Review: ingredient-formatting

## Findings

none

## Checked

- `rules.md`: `accessibility-role`, `accessibility-label` and `accessibility-state-announcements` now each carry "**Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`." The new line sits inside `wcag-name-role-value`'s scope ("all user interface components"), and it no longer contradicts `accessibility-not-applicable-stated` or the "Saying a section has nothing to say" part. Each rule still ends with its citation, the same way `if-accessibility` does.
- `a-build-must-establish.md`: the build-bar lines for the three accessibility rules now say "a UI ingredient's `## Accessibility`", which matches the rules.
- `rules.md`, `short-required-core-labelled-optional-rest`: "carried by every ingredient" is gone. The new qualifier "(`## Appearance` and `## States` by UI ingredients only, per `if-appearance` and `if-states`)" agrees with those rules' "MAY be omitted for infrastructure ingredients". The rule is still SHOULD and its six citations are unchanged.
- `a-build-must-establish.md`: the `short-required-core-labelled-optional-rest` build-bar line names the same exception, so it matches the rule.
- `rationale.md`, `tmpl-states-table` / `states-include-hover-and-selected`: the bullet now says Fluent's list includes selected, with no hover. That matches `fluent-rest-selected-states` (rest and selected).
- `rationale.md`, `tmpl-logging-subsystem-category`: "so that each message carries the context of its functional area" follows from `apple-logger-optional` ("add context to all messages you log") and `apple-logger-subsystem-category` (functional areas). The filtering claim is gone.
- `rationale.md`, `section-structure-machine-checked`: the bullet now names only the wildcards `*`, `+` and `?` from `md043-wildcards-only`'s quote. It no longer makes the inference the second check refuted, that named optional sections need a custom rule.
- No other text changed in diff-3. `cookr roles check` reports `"ok": true`.

## Rulings

- R2.1: fixed — all three accessibility MUSTs and their build-bar lines are now scoped to UI ingredients, and infrastructure ingredients are sent to `accessibility-not-applicable-stated`. This resolves the contradiction and the overreach past `wcag-name-role-value`.
- R2.2: fixed — "carried by every ingredient" is removed, and the rule and its build-bar line now name the UI-only exception for `## Appearance` and `## States`, consistent with `if-appearance` and `if-states`.
- R2.3: fixed — all three Rationale bullets now use the requested wording, and each stays within its cited claims (`fluent-rest-selected-states`, `apple-logger-optional`/`apple-logger-subsystem-category`, `md043-wildcards-only`).

## Lint

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md
Artifact: cookbook/guidelines/cookbook/authoring/ingredient-formatting (rdid adc.guideline.cookbook.authoring.ingredient-formatting)

[PASS] FM-01: frontmatter present
[PASS] FM-02: id is a UUID (2c5ee8e0-9da5-4b44-9f87-51962abe76ab)
[PASS] FM-03: index.json entry matches folder and rdid (line 635); cookr validate passed
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: all required fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 "Ingredient Formatting" matches title
[PASS] FM-11a: links resolve (cookr validate passed)
[PASS] FM-12: Change History present with one row
[PASS] FM-13: no TODO/placeholder text
[PASS] gf-frontmatter-complete / gf-type-field / gf-title-heading
[PASS] GF-01 / gf-summary-statement: summary paragraph follows H1
[PASS] GF-02 / gf-structured-guidance: bullets, subsections and examples
[PASS] GF-03 / gf-rfc-keywords: 72 named rules, each with MUST, SHOULD or MAY
[PASS] gf-change-history: ends with the Version/Date/Author/Summary table
[PASS] gf-triggers-field: triggers: [recipe-authoring]
[PASS] gf-roled-parts: every part has a role. All of rules, review-focus, review-bar and build-bar are present. No routes or hosts.
[PASS] gf-named-rules: 72 kebab-named rules
[PASS] gf-research-folder: research.json and research.md present; cookr validate passed
[PASS] gf-rule-cites-research: every rule ends with (claim: ...) or (claims: ...)
[WARN] GF-04 / gf-compliance-section: no `## Compliance` section
       -> Optional here. It is recommended only if other compliance checks reference this guideline.

=== LINT SUMMARY ===
Artifact: ingredient-formatting
Type: guideline
Pass: 24 | Warn: 1 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

The one WARN (GF-04) is not an error.

lint: clean

verdict: pass
