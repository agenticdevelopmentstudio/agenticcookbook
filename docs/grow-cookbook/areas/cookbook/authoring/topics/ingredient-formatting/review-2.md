# Review: ingredient-formatting

## Findings

- `rules.md`, `accessibility-role`, `accessibility-label`, `accessibility-state-announcements` (source fidelity, internal consistency). These rules are new this round. Each is a MUST with no "Applies when", so it binds every ingredient. `if-accessibility` says "Applies when: always". `wcag-name-role-value` covers only "user interface components". `accessibility-not-applicable-stated` and the new "Saying a section has nothing to say" bullet tell an infrastructure ingredient to say accessibility is out of scope. Under the three MUSTs, that same ingredient must also give a role, a label and its state announcements. The two sets of rules contradict each other, and the MUSTs reach past the claim's scope. The build-bar lines for all three repeat the gap. Fix: scope each of the three rules, and its build-bar line, to an ingredient with a user interface, for example "**Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`."
- `rules.md`, `short-required-core-labelled-optional-rest` (internal consistency). This text changed this round. It defines the required sections as "carried by every ingredient" and as those `if-section-order` leaves unmarked. `## Appearance` and `## States` are unmarked there, but `if-appearance` and `if-states` say they "MAY be omitted for infrastructure ingredients". So the rule calls two sections required by every ingredient when another rule lets some ingredients omit them. Fix: drop "carried by every ingredient", or qualify it, for example "(`## Appearance` and `## States` by UI ingredients only, per `if-appearance` and `if-states`)". If the build-bar line names the exception, make it match.
- `rationale.md` (factual error against cited claims; every Rationale bullet is new this round). Three bullets say more than the claims they draw on. Every instance:
    - `tmpl-states-table`, `states-include-hover-and-selected`: the bullet says "Flutter's, Material's and Fluent's state lists include hover and selected". `fluent-rest-selected-states` names only rest and selected, and has no hover. Fix: "Flutter's and Material's state lists include hover and selected, and Fluent's includes selected."
    - `tmpl-logging-subsystem-category`: the bullet says "so that log messages can be filtered by functional area". Neither `apple-logger-subsystem-category` nor `apple-logger-optional` mentions filtering. The second claim says only that the two strings "add context to all messages you log". Fix: "so that each message carries the context of its functional area".
    - `section-structure-machine-checked`: the bullet says "MD043's wildcards stand only for unspecified headings, so named optional sections take a custom rule". `md043-wildcards-only`'s second check refuted exactly that inference: the doc also lists `%` regex headings and `^` loops, and never says a named heading cannot be optional or that a custom rule is needed. Fix: "MD043's wildcards `*`, `+` and `?` stand for unspecified headings; a custom rule can name an optional section".

## Checked

- Every one of the 72 rules ends with a citation, and every cited claim exists in research.json (scripted check; `cookr roles check` ok, 72 rules, no findings).
- Every claim named by a `supported` or `new` verdict is still cited after the splits (none uncited).
- Every rule has exactly one `a-build-must-establish.md` line, and every rule appears in `a-complete-review-must-establish.md` under its keyword.
- Every SHOULD rule now has a Rationale bullet (only MUST and MAY rules are absent from `rationale.md`).
- The new MUSTs cite only MUST-strength claims: `if-overview` (`govuk-description-required`), `if-behavioral-requirements` (`w3c-qa-conformance-clause`), `behavioral-requirements-keyword-levels` (`w3c-qa-indicate-levels`), `behavioral-requirements-one-style` (`w3c-qa-consistent-requirement-style`), the accessibility MUSTs (`wcag-name-role-value`, Level A), `if-test-vectors` (`act-examples-pass-fail-inapplicable`) and `tmpl-feature-flags-table` (`openfeature-flag-key-and-default`).
- Each split-off SHOULD sits at the strength of its weakest claim: `behavioral-requirements-named`, `test-vectors-table`, `test-vectors-map-to-requirements`, `template-carries-test-vectors`, `accessibility-min-target-size`, `accessibility-role-from-apg`, `overview-states-*`.
- The new `requirement-keywords-without-section-flagged` is MAY, matching `respec-conformance-lint` (a tool's warning).
- `present-section-uses-specified-heading` follows `patternfly-template-omit-but-fixed-headings`, at SHOULD.
- `accessibility-options-include-text-size` now names `## Accessibility Options` as present for a text-showing ingredient, and so does its build-bar line.
- The owner-list rules keep their prior text. The four restored build-bar lines (`tmpl-accessibility-min-tap-target`, `tmpl-deep-linking-patterns`, `tmpl-analytics-events`, `if-compliance`) carry the kept values word for word, and `tmpl-approval-fields` now has its `""` values.
- `tmpl-design-decisions-approved` now matches `nygard-adr-status` ("its stakeholders"), with the new example in Examples.
- The new table row and the rule text for MD043's wildcards match `md043-wildcards-only`'s quote (`*` zero or more, `+` one or more, `?` exactly one).
- The new Feature Flags example and the infrastructure "not applicable" line in "Saying a section has nothing to say" are consistent with their rules.
- The summary is 157 characters and describes the new text. The intro no longer says "short".

## Rulings

- R1.1: fixed — `if-overview`, `if-behavioral-requirements`, `if-accessibility` and `if-test-vectors` now keep MUST only on what a MUST-strength claim carries. The rest is split into SHOULD rules (`overview-states-when-to-use`, `accessibility-min-target-size`, `behavioral-requirements-named`, `test-vectors-table`, `test-vectors-map-to-requirements`, `template-carries-test-vectors`).
- R1.2: fixed — `tmpl-feature-flags-table` is now only "give each flag its key and its default value", and the table moved to Examples.
- R1.3: fixed — `fluent-contrast-in-all-states` was dropped from `tmpl-appearance-properties` and `wcag-name-role-value` from `tmpl-states-table`. `tmpl-design-decisions-approved` was reduced to the status per stakeholders, with a matching build-bar line.
- R1.4: fixed — the rule and its build-bar line now require `## Accessibility Options` for an ingredient that shows text.
- R1.5: fixed — the four build-bar lines carry 44×44pt, the three URL patterns, the two dotted analytics rows, and `passed`/`failed`/`partial`.
- R1.6: fixed — each bundled rule is split into one named rule per behaviour, each with its own claims and build-bar line. The logging events table and the feature-flags table are left to `if-logging` and to Examples.
- R1.7: fixed — every SHOULD rule now has a Rationale bullet. Three of them overstate their claims, which is raised above as a new finding.
- R1.8: fixed — "short" was dropped from the rule and the intro, and the required sections are defined as the unmarked ones in `if-section-order`. The conflict with `if-appearance` and `if-states` that this definition creates is raised above as a new finding.

## Lint

lint-artifact v2.0.1 on `cookbook/guidelines/cookbook/authoring/ingredient-formatting` (guideline; compliance `tbd/compliance/artifact-formatting/guideline-formatting.md`):

- Shared checks FM-01 to FM-13: all PASS. `cookr validate` passed, with no unresolved links and no index drift.
- Guideline checks: all PASS. This covers type field, title heading, summary statement, structured guidance, RFC keywords (72 rules), change history, triggers, compliance section, roled parts (one build-bar line per rule), named rules, research folder and rule-cites-research.
- WARN gf-named-rules (form): `component-recipe-sections-in-order` embeds a second bullet in its text. This is owner-list prior text, kept word for word.
- WARN gf-named-rules (form): `tmpl-accessibility-min-tap-target` and the `if-*` rules quote the template's items inside the rule. This is a style note.
- Summary: Pass 27, Warn 2, Fail 0. RESULT: CLEAN.

lint: clean

verdict: fail
