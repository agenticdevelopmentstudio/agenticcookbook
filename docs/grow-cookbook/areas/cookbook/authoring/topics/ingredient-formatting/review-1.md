# Review: ingredient-formatting

## Findings

- `rules.md` (source fidelity, strength rule): four rules that are not on the owner list carry MUST, but the weakest claim each one cites is only a recommendation or advice. Every instance:
  - `if-overview` cites `govuk-when-to-use`. That claim is an unmarked template prompt ("Briefly describe the situation(s) when to use this component"). The same template marks only the description as required (`govuk-description-required`: "It is required to display the description"), and `govuk-template-empty-fields-hidden` shows its other fields are optional. So "when to use it" is at MUST without support.
  - `if-behavioral-requirements` cites `oasis-ta-identifier` (an OASIS Committee Note; "It is recommended that the identifier be made universally unique") and `respec-conformance-lint` (a tool that only "will warn you").
  - `if-accessibility` cites `apple-strive-min-control-size` ("Strive to meet …") and `android-touch-target-48dp` ("we recommend …"). These two are the only claims behind its "minimum tap target size" item. `apg-button-role` is descriptive.
  - `if-test-vectors` cites `w3c-qa-test-assertions` (good practice GP12, "not a requirement"), `w3c-qa-template-test-assertion-section` ("advisory") and `oasis-ta-normative-source` (Committee Note).
  - Fix: in each rule, keep MUST only on the part a MUST-strength claim carries, and move the rest to SHOULD:
    - `if-overview`: MUST for what the component is (`govuk-description-required`); "when to use it" becomes SHOULD, in this rule or in `overview-states-when-not-to-use`.
    - `if-accessibility`: MUST for role, label and announced state changes (`wcag-name-role-value`); the tap-target item becomes SHOULD (`per-platform-target-sizes` already holds it at SHOULD).
    - `if-behavioral-requirements` and `if-test-vectors`: lower to SHOULD, or cite only their MUST-strength claims (`w3c-qa-conformance-clause`, `w3c-qa-consistent-requirement-style`, `w3c-qa-indicate-levels`, `act-examples-pass-fail-inapplicable`) for the MUST part and give the rest SHOULD.
  - I checked the other non-owner MUST rules and they hold: `accessibility-options-include-text-size` (WCAG AA), `analytics-event-names-fit-platform-limits` (Firebase's hard limits), `released-version-immutable` (SemVer MUST).
- `rules.md`, `tmpl-feature-flags-table` (source fidelity): the MUST covers the table layout `| Flag Key | Default | Description |`. `openfeature-flag-key-and-default` supports only that a flag has a key and a default value, and it says that about the client evaluation API, not about a documentation table. The build-bar line already leaves the table out ("every flag … has its key and its default value"). Fix: keep the MUST on "give each flag its key and its default value". Put the table at SHOULD, or drop it.
- `rules.md` (source fidelity: every rule follows from the claims it cites): three rules cite a claim their text does not use, or say more than the claim supports. Every instance:
  - `tmpl-appearance-properties` cites `fluent-contrast-in-all-states` but says nothing about contrast. Contrast is `appearance-contrast-in-all-states`'s subject.
  - `tmpl-states-table` cites `wcag-name-role-value`. That claim is about states being programmatically determinable and announced, not about a visual table of appearance changes.
  - `tmpl-design-decisions-approved`: its first SHOULD ("Each decision … SHOULD be recorded in `## Design Decisions`") has no supporting claim, because `nygard-adr-status` covers only a decision's status. Its second SHOULD says "approved by the user", but the claim says "project stakeholders".
  - Fix:
    - Drop `fluent-contrast-in-all-states` from `tmpl-appearance-properties`. `appearance-contrast-in-all-states` still cites it.
    - Drop `wcag-name-role-value` from `tmpl-states-table` (`if-accessibility` still cites it), or add the programmatic-state point the claim actually makes.
    - Reduce `tmpl-design-decisions-approved` to the status the claim supports, for example "Each decision in `## Design Decisions` SHOULD carry its status: pending (proposed) until its stakeholders agree, then yes (accepted)." Change its build-bar line to match.
- `rules.md`, `accessibility-options-include-text-size` (internal consistency): the rule says an ingredient that shows text MUST give its text-resize behaviour "in `## Accessibility Options`". `if-section-order` marks that section "(MAY omit)", and nothing tells the author that such an ingredient must therefore carry it. Its build-bar line also leaves out where the statement goes. Fix: say so in the rule, for example "… MUST carry `## Accessibility Options` and say there how its text resizes …". Alternatively, put the statement in `## Accessibility`, which is always present. Make the build-bar line name the section either way.
- `a-build-must-establish.md` (the build bar must match the rule it checks): four lines for owner-list rules leave out values that the kept rule text requires. Each omission quietly leans toward an open question that belongs to the owner. Every instance:
  - `tmpl-accessibility-min-tap-target` drops "44×44pt" (open question 4).
  - `tmpl-deep-linking-patterns` drops the three URL patterns, among them `{{app_scheme}}://component-name` (open question 6).
  - `tmpl-analytics-events` drops the two template rows and their dotted names (open question 5).
  - `if-compliance` drops the status values `passed`, `failed`, `partial` (open question 7).
  - Fix: restore each value as the rule states it, for example "`## Accessibility` holds the template's items: …, and a minimum tap target of 44×44pt" and "… Status values `passed`, `failed`, `partial`, each check linked to its definition".
- `rules.md` (behavioral-requirements `must-not-bundle-behaviors-into-one-requirement`): rules that are not on the owner list bundle separately testable behaviours into one bullet. Every instance:
  - `short-required-core-labelled-optional-rest`: core and optional labels; the specified heading and level.
  - `overview-states-when-not-to-use`: when not to use; why to use.
  - `if-overview`: what it is; when to use it.
  - `if-behavioral-requirements`: the section is present; RFC 2119 keywords; bold kebab-case names.
  - `if-accessibility`: four separate items, plus the infrastructure "not applicable" case.
  - `if-test-vectors`: the four-column table; each vector mapped to a named requirement.
  - `tmpl-test-vector-id-format`: unique ID form; requirements named; table form.
  - `assumptions-and-limitations-stated`: assumptions, limitations and exceptions; out of scope and why.
  - `tmpl-privacy-fields`: the four fields; an ingredient that collects nothing says so.
  - `tmpl-logging-subsystem-category`: Apple's meaning for subsystem and category; the events table.
  - `tmpl-platform-notes-platforms`: an entry per targeted platform; the "nothing to add" line.
  - `tmpl-design-decisions-approved`: recorded; approved.
  - `tmpl-feature-flags-table`: key and default; table.
  - Fix: split each into one named rule per behaviour. The verdict name stays on one part, and new names are free. Each part cites the subset of the original claims it rests on, at that subset's weakest strength. Each new rule gets its own `a-build-must-establish.md` line, and every `supported` and `new` claim stays cited.
- `rationale.md` (behavioral-requirements `must-explain-rationale-for-should-requirements`): the Rationale covers 11 of 53 rules. These SHOULD rules give no reason, either inline or in the Rationale: `tmpl-approval-fields`, `overview-states-when-not-to-use`, `appearance-contrast-in-all-states`, `tmpl-states-table`, `states-include-hover-and-selected`, `accessibility-keyboard-interaction`, `tmpl-test-vector-id-format`, `assumptions-and-limitations-stated`, `tmpl-deep-linking-patterns`, `tmpl-accessibility-options`, `tmpl-analytics-events`, `tmpl-privacy-fields`, `privacy-states-encryption-in-transit`, `tmpl-logging-subsystem-category`, `tmpl-design-decisions-approved`, `tmpl-compliance-link-form`, `change-history-iso-dates`. The ones that do give a reason are `tmpl-localization-table` ("for the translator"), `tmpl-platform-notes-platforms` ("since each platform's own guidelines differ") and those in `rationale.md`. Fix: add one Rationale bullet per rule, or an inline "so that …" clause, drawn from the cited claim. Examples:
  - `change-history-iso-dates`: an ISO standard date format, per Keep a Changelog.
  - `tmpl-compliance-link-form`: a UUID is unique across space and time, so the link survives renames.
  - `accessibility-keyboard-interaction`: APG documents keyboard interaction beside roles, states and properties.
- `rules.md` `short-required-core-labelled-optional-rest` and `intro.md` (behavioral-requirements `should-not-use-unanchored-relative-terms`): "a short core of sections" gives no threshold and names no core, so a build cannot test "short". Fix: define the core as the sections `if-section-order` does not mark "(MAY omit)", or drop "short" in both places.

## Checked

- All 53 verdicts have a rule of the same name in `rules.md`, and no rule lacks a verdict.
- Every rule ends with exactly one `(claim: …)`/`(claims: …)` citation with nothing after it. Every cited id exists in research.json and is named by some verdict.
- Every claim of every `supported` and `new` verdict is cited by at least one rule. Some rules dropped a verdict claim (`if-overview` dropped `patternfly-usage-when-to-use`; `accessibility-options-include-text-size` dropped `apple-dynamic-type`), and another rule cites each of those claims (`overview-states-when-not-to-use`, `tmpl-accessibility-options`).
- Strength rule for refuted claims: no MUST rule cites any of the seven refuted claims (`rfc-no-actions-statement`, `md043-wildcards-only`, `rfc-security-considerations-required`, `patternfly-usage-when-to-use`, `apple-dynamic-type`, `material-states-list`, `apg-keyboard-interaction-section`). The rules that cite them are all SHOULD or MAY. No claim is listed under "citation dropped".
- Every SHOULD/MAY rule not named in the findings reads at or below its weakest claim, and its content follows from that claim. That includes the per-platform figures in `per-platform-target-sizes` and `tmpl-platform-notes-platforms`, and Dynamic Type limited to "Apple platforms that offer it", which matches the second check.
- Owner list: all 16 MUST-text rules match their prior text word for word (whitespace aside) and cite only `<rule>-prior`. The four keyword-less rules (`tmpl-approval-fields`, `tmpl-accessibility-min-tap-target`, `tmpl-deep-linking-patterns`, `tmpl-analytics-events`) carry exactly the lead-in owner-list.md lists, followed by the prior text word for word. `component-recipe-sections-in-order` keeps its nested prior bullet as-is.
- No rule settles an owner open question. Where kept owner text and new rules point different ways (dotted vs Firebase-valid event names, custom scheme vs universal links, `partial` vs `inapplicable`, 44×44pt vs per-platform), both stand and the choice stays the owner's. The build-bar omissions above are the exception.
- Structure follows guideline-formatting `gf-roled-parts`/`gf-named-rules`: intro, Rules, two how-to parts, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References, Change History. Every part except intro and history carries a valid role.
- `a-build-must-establish.md` has exactly 53 lines, one per named rule, in rule order. `cookr roles check` is ok (53 rules, no findings, four skills compile).
- `a-complete-review-must-establish.md` lists every MUST, SHOULD and MAY rule under the right keyword.
- References: `references.md`, `meta.references` and research.json `sources` hold the same 44 URLs.
- Frontmatter: `summary` is 151 characters and describes the new text. `tags` fit the topic. `platforms` is `[]`, the same as every authoring sibling. Both `related` UUIDs resolve, to template-conformance and behavioral-requirements, and both are relevant. Version, modified and history are left for stage 5.
- Examples conform to the rules: the toggle States table has Hover and Selected rows, the test vectors cover passed, failed and inapplicable with `component-001`-form IDs, the Privacy section states "none" in every field including encryption, and the event names are Firebase-valid.
- The how-to tool table matches the claims: MD043 wildcards only, JSON Schema objects unordered and `prefixItems` positional, MD025 treating front-matter `title` as the H1, MD041 not comparing the H1 with the title.
- Sibling topics, for routing only: whole-cookbook `cookr validate` reports Neutrality `unlisted` host names in `guidelines/cookbook/authoring/activity-triggers` and `guidelines/cookbook/authoring/principle-formatting`, not in this artifact.

## Lint

/lint-artifact v2.0.1 on `cookbook/guidelines/cookbook/authoring/ingredient-formatting` (type guideline, compliance `tbd/compliance/artifact-formatting/guideline-formatting.md`), cookr run from this checkout: Pass 17, Warn 2, Fail 0. RESULT: CLEAN.

- [PASS] FM-01 to FM-13 (frontmatter, UUID id, semver, required fields, MIT, dates, summary, FM-03 index entry and rdid, FM-11 H1 equals title, FM-11a `cookr validate` frontmatter and links, no placeholders), GF-01, GF-02, GF-03, gf-type-field, gf-title-heading, gf-change-history, gf-triggers-field (`recipe-authoring`), gf-roled-parts and gf-named-rules (roles check clean), gf-research-folder, gf-rule-cites-research.
- [WARN] GF-04 / gf-compliance-section: no `## Compliance` section (recommended because `tbd/compliance/artifact-formatting/ingredient-formatting.md` references this subject).
- [WARN] research owner-decides: the rules citing `*-prior` claims ruled unsupported or contradicted are the owner's to keep, reword or drop.
- Whole-cookbook `cookr validate` ends "Validation failed" because of the sibling Neutrality findings noted under Checked, not because of this artifact.

lint: clean

verdict: fail
