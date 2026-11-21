# Research agent run: ingredient-formatting

The research team could not run (`team_probe.py researchteam`: "missing
distributions: PyYAML, aiohttp, mcp, websockets"), so one fresh Opus Agent ran
the `research` prompt, as `write_brief.py prompt research` printed it, on
2026-11-21. Its reply, verbatim:

---

I wrote both research files and the validator prints `✓ Research passed.` I did not commit them, because the brief said to write exactly two files and edit nothing else. The topic folder `cookbook/guidelines/cookbook/authoring/ingredient-formatting/` is untracked. The brief's own folder `docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/` is untracked too, but it was already there.

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting/research/research.md`

**Claims per question** (114 in total: 94 research claims plus 20 prior claims)
- best-practices: 35 (24 research, 11 prior)
- known-solutions: 33 (29 research, 4 prior)
- platform-guidelines: 40 (35 research, 5 prior)
- experts-view: 6 (all research)

Every research claim is `single`, because no quote was found word for word at two independent publishers. Every prior claim is `uncorroborated` with a trust score of 0. The four rule-checks about frontmatter, type, title and applicability are filed under known-solutions, because their sources are tools and schemas.

**How the files were built**
- I wrote both files with inline `python3 -c` commands; no script file was saved anywhere. The commands wrote `research.json` in place and appended the four question sections to `research.md`.
- Each new-practice verdict carries an extra `strength` field. The validator ignores extra keys.

**Verdicts**
- if-applicability: unsupported — if-applicability-prior, json-schema-const, json-schema-if-then
- if-section-order: unsupported — if-section-order-prior, rfc-order-strongly-recommended-in-body, patternfly-template-omit-but-fixed-headings, md043-enforces-heading-structure, ubl-template-clarity, ubl-form-fits-project
- if-frontmatter-complete: unsupported — if-frontmatter-complete-prior, jekyll-front-matter-first, json-schema-required-properties
- if-type-field: unsupported — if-type-field-prior, json-schema-const
- if-title-heading: unsupported — if-title-heading-prior, md041-first-line-h1, md025-front-matter-title-is-h1, markdownlint-custom-rules
- if-overview: supported — govuk-description-required, govuk-when-to-use, patternfly-usage-when-to-use
- if-behavioral-requirements: supported — w3c-qa-conformance-clause, w3c-qa-consistent-requirement-style, w3c-qa-indicate-levels, oasis-ta-identifier, respec-conformance-lint
- if-appearance: unsupported — if-appearance-prior, material-attribute-table
- if-states: unsupported — if-states-prior, apple-press-state, material-states-list, flutter-interactive-states
- if-accessibility: supported — wcag-name-role-value, apg-button-role, wcag-target-size-minimum-24, apple-strive-min-control-size, android-touch-target-48dp
- if-test-vectors: supported — act-examples-pass-fail-inapplicable, oasis-ta-normative-source, oasis-ta-identifier, w3c-qa-test-assertions, w3c-qa-template-test-assertion-section
- if-edge-cases: unsupported — if-edge-cases-prior, act-assumptions-listed, rfc3552-out-of-scope-stated
- if-configuration: unsupported — if-configuration-prior, rfc-empty-iana-section-kept, w3c-qa-label-optional-features, material-attribute-table
- if-logging: unsupported — if-logging-prior, apple-logger-optional, apple-logger-subsystem-category
- if-platform-notes: unsupported — if-platform-notes-prior, apple-platform-considerations-none, apple-min-control-size-per-platform
- if-reference-implementations: unsupported — if-reference-implementations-prior, act-optional-items
- if-design-decisions: unsupported — if-design-decisions-prior, nygard-adr-status, nygard-consequences-listed
- if-compliance: contradicted — if-compliance-prior, earl-outcome-values, act-outcome-types
- if-change-history: unsupported — if-change-history-prior, kac-guiding-principles, semver-released-immutable
- tmpl-approval-fields: unsupported — tmpl-approval-fields-prior, nygard-adr-status
- tmpl-appearance-properties: supported — material-attribute-table, fluent-contrast-in-all-states
- tmpl-states-table: supported — material-states-list, apple-press-state, flutter-interactive-states, wcag-name-role-value
- tmpl-accessibility-min-tap-target: contradicted — tmpl-accessibility-min-tap-target-prior, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40, wcag-target-size-minimum-24
- tmpl-test-vector-id-format: supported — oasis-ta-identifier, w3c-qa-test-assertions
- tmpl-deep-linking-patterns: contradicted — tmpl-deep-linking-patterns-prior, apple-universal-links-recommended, apple-url-scheme-attack-vector
- tmpl-localization-table: supported — android-string-context
- tmpl-accessibility-options: supported — apple-reduce-motion, apple-increase-contrast, apple-more-than-color, mq5-prefers-reduced-motion, mq5-prefers-contrast, wcag-use-of-color, wcag-animation-from-interactions
- tmpl-feature-flags-table: supported — openfeature-flag-key-and-default
- tmpl-analytics-events: contradicted — tmpl-analytics-events-prior, firebase-event-name-charset
- tmpl-privacy-fields: supported — apple-collect-definition, play-ephemeral-processing, play-form-even-if-no-data
- tmpl-logging-subsystem-category: supported — apple-logger-subsystem-category
- tmpl-platform-notes-platforms: supported — apple-strive-min-control-size, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40
- tmpl-design-decisions-approved: supported — nygard-adr-status
- tmpl-compliance-link-form: supported — oasis-ta-normative-source, uuid-unique-identifier
- component-recipe-sections-in-order: unsupported — component-recipe-sections-in-order-prior, rfc-order-strongly-recommended-in-body, rfc-some-sections-required, patternfly-template-omit-but-fixed-headings, json-schema-if-then
- inapplicable-section-stated-not-omitted: new (recommended) — rfc-empty-iana-section-kept, rfc-no-actions-statement, w3c-qa-label-optional-features, apple-platform-considerations-none, play-form-even-if-no-data, rfc-editor-removes-empty-iana, govuk-template-empty-fields-hidden
- section-structure-machine-checked: new (optional) — md043-enforces-heading-structure, md043-wildcards-only, markdownlint-custom-rules, vale-occurrence-min-flags-absence, vale-script-arbitrary-rules, json-schema-required-properties, json-schema-prefixitems-positional, json-schema-objects-unordered, respec-privsec-lint, respec-headingless-lint
- short-required-core-labelled-optional-rest: new (recommended) — rfc-some-sections-required, rfc-security-considerations-required, rfc3552-security-section-required, act-required-items, act-optional-items, w3c-qa-label-optional-features, patternfly-template-omit-but-fixed-headings
- compliance-status-includes-inapplicable: new (recommended) — earl-outcome-values, act-outcome-types
- test-vectors-cover-pass-fail-inapplicable: new (recommended; ACT requires it for its own rules) — act-examples-pass-fail-inapplicable, act-outcome-types
- overview-states-when-not-to-use: new (recommended) — govuk-when-not-to-use, patternfly-usage-when-to-use
- per-platform-target-sizes: new (recommended) — apple-min-control-size-per-platform, apple-strive-min-control-size, apple-button-hit-region-44, android-touch-target-48dp, android-touch-target-spacing, windows-touch-target-40, wcag-target-size-minimum-24, wcag-target-size-enhanced-44
- accessibility-options-include-text-size: new (required at WCAG 2.2 AA) — wcag-resize-text, apple-dynamic-type
- states-include-hover-and-selected: new (recommended) — flutter-hover-state, flutter-selected-state, material-states-list, fluent-rest-selected-states
- appearance-contrast-in-all-states: new (recommended) — fluent-contrast-in-all-states
- accessibility-keyboard-interaction: new (recommended) — apg-keyboard-interaction-section
- deep-links-use-verified-https-links: new (recommended) — apple-universal-links-recommended, android-app-links-recommended, apple-url-scheme-attack-vector
- analytics-event-names-fit-platform-limits: new (required where Firebase is used) — firebase-event-name-charset
- privacy-states-encryption-in-transit: new (recommended) — play-encryption-in-transit
- assumptions-and-limitations-stated: new (required in ACT and RFC; recommended here) — act-assumptions-listed, rfc3552-out-of-scope-stated
- informative-sections-labelled: new (optional) — respec-informative-marking
- released-version-immutable: new (required by SemVer) — semver-released-immutable
- change-history-iso-dates: new (recommended) — kac-iso-dates
