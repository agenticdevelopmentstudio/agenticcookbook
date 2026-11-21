# Write brief: ingredient-formatting

Today is 2026-11-21.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/tbd/compliance/artifact-formatting/guideline-formatting.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- if-applicability: unsupported (claims: if-applicability-prior, json-schema-const, json-schema-if-then)
- if-section-order: unsupported (claims: if-section-order-prior, rfc-order-strongly-recommended-in-body, patternfly-template-omit-but-fixed-headings, md043-enforces-heading-structure, ubl-template-clarity, ubl-form-fits-project)
- if-frontmatter-complete: unsupported (claims: if-frontmatter-complete-prior, jekyll-front-matter-first, json-schema-required-properties)
- if-type-field: unsupported (claims: if-type-field-prior, json-schema-const)
- if-title-heading: unsupported (claims: if-title-heading-prior, md041-first-line-h1, md025-front-matter-title-is-h1, markdownlint-custom-rules)
- if-overview: supported (claims: govuk-description-required, govuk-when-to-use, patternfly-usage-when-to-use)
- if-behavioral-requirements: supported (claims: w3c-qa-conformance-clause, w3c-qa-consistent-requirement-style, w3c-qa-indicate-levels, oasis-ta-identifier, respec-conformance-lint)
- if-appearance: unsupported (claims: if-appearance-prior, material-attribute-table)
- if-states: unsupported (claims: if-states-prior, apple-press-state, material-states-list, flutter-interactive-states)
- if-accessibility: supported (claims: wcag-name-role-value, apg-button-role, wcag-target-size-minimum-24, apple-strive-min-control-size, android-touch-target-48dp)
- if-test-vectors: supported (claims: act-examples-pass-fail-inapplicable, oasis-ta-normative-source, oasis-ta-identifier, w3c-qa-test-assertions, w3c-qa-template-test-assertion-section)
- if-edge-cases: unsupported (claims: if-edge-cases-prior, act-assumptions-listed, rfc3552-out-of-scope-stated)
- if-configuration: unsupported (claims: if-configuration-prior, rfc-empty-iana-section-kept, w3c-qa-label-optional-features, material-attribute-table)
- if-logging: unsupported (claims: if-logging-prior, apple-logger-optional, apple-logger-subsystem-category)
- if-platform-notes: unsupported (claims: if-platform-notes-prior, apple-platform-considerations-none, apple-min-control-size-per-platform)
- if-reference-implementations: unsupported (claims: if-reference-implementations-prior, act-optional-items)
- if-design-decisions: unsupported (claims: if-design-decisions-prior, nygard-adr-status, nygard-consequences-listed)
- if-compliance: contradicted (claims: if-compliance-prior, earl-outcome-values, act-outcome-types)
- if-change-history: unsupported (claims: if-change-history-prior, kac-guiding-principles, semver-released-immutable)
- tmpl-approval-fields: unsupported (claims: tmpl-approval-fields-prior, nygard-adr-status)
- tmpl-appearance-properties: supported (claims: material-attribute-table, fluent-contrast-in-all-states)
- tmpl-states-table: supported (claims: material-states-list, apple-press-state, flutter-interactive-states, wcag-name-role-value)
- tmpl-accessibility-min-tap-target: contradicted (claims: tmpl-accessibility-min-tap-target-prior, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40, wcag-target-size-minimum-24)
- tmpl-test-vector-id-format: supported (claims: oasis-ta-identifier, w3c-qa-test-assertions)
- tmpl-deep-linking-patterns: contradicted (claims: tmpl-deep-linking-patterns-prior, apple-universal-links-recommended, apple-url-scheme-attack-vector)
- tmpl-localization-table: supported (claims: android-string-context)
- tmpl-accessibility-options: supported (claims: apple-reduce-motion, apple-increase-contrast, apple-more-than-color, mq5-prefers-reduced-motion, mq5-prefers-contrast, wcag-use-of-color, wcag-animation-from-interactions)
- tmpl-feature-flags-table: supported (claims: openfeature-flag-key-and-default)
- tmpl-analytics-events: contradicted (claims: tmpl-analytics-events-prior, firebase-event-name-charset)
- tmpl-privacy-fields: supported (claims: apple-collect-definition, play-ephemeral-processing, play-form-even-if-no-data)
- tmpl-logging-subsystem-category: supported (claims: apple-logger-subsystem-category)
- tmpl-platform-notes-platforms: supported (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40)
- tmpl-design-decisions-approved: supported (claims: nygard-adr-status)
- tmpl-compliance-link-form: supported (claims: oasis-ta-normative-source, uuid-unique-identifier)
- component-recipe-sections-in-order: unsupported (claims: component-recipe-sections-in-order-prior, rfc-order-strongly-recommended-in-body, rfc-some-sections-required, patternfly-template-omit-but-fixed-headings, json-schema-if-then)
- inapplicable-section-stated-not-omitted: new (claims: rfc-empty-iana-section-kept, rfc-no-actions-statement, w3c-qa-label-optional-features, apple-platform-considerations-none, play-form-even-if-no-data, rfc-editor-removes-empty-iana, govuk-template-empty-fields-hidden)
- section-structure-machine-checked: new (claims: md043-enforces-heading-structure, md043-wildcards-only, markdownlint-custom-rules, vale-occurrence-min-flags-absence, vale-script-arbitrary-rules, json-schema-required-properties, json-schema-prefixitems-positional, json-schema-objects-unordered, respec-privsec-lint, respec-headingless-lint)
- short-required-core-labelled-optional-rest: new (claims: rfc-some-sections-required, rfc-security-considerations-required, rfc3552-security-section-required, act-required-items, act-optional-items, w3c-qa-label-optional-features, patternfly-template-omit-but-fixed-headings)
- compliance-status-includes-inapplicable: new (claims: earl-outcome-values, act-outcome-types)
- test-vectors-cover-pass-fail-inapplicable: new (claims: act-examples-pass-fail-inapplicable, act-outcome-types)
- overview-states-when-not-to-use: new (claims: govuk-when-not-to-use, patternfly-usage-when-to-use)
- per-platform-target-sizes: new (claims: apple-min-control-size-per-platform, apple-strive-min-control-size, apple-button-hit-region-44, android-touch-target-48dp, android-touch-target-spacing, windows-touch-target-40, wcag-target-size-minimum-24, wcag-target-size-enhanced-44)
- accessibility-options-include-text-size: new (claims: wcag-resize-text, apple-dynamic-type)
- states-include-hover-and-selected: new (claims: flutter-hover-state, flutter-selected-state, material-states-list, fluent-rest-selected-states)
- appearance-contrast-in-all-states: new (claims: fluent-contrast-in-all-states)
- accessibility-keyboard-interaction: new (claims: apg-keyboard-interaction-section)
- deep-links-use-verified-https-links: new (claims: apple-universal-links-recommended, android-app-links-recommended, apple-url-scheme-attack-vector)
- analytics-event-names-fit-platform-limits: new (claims: firebase-event-name-charset)
- privacy-states-encryption-in-transit: new (claims: play-encryption-in-transit)
- assumptions-and-limitations-stated: new (claims: act-assumptions-listed, rfc3552-out-of-scope-stated)
- informative-sections-labelled: new (claims: respec-informative-marking)
- released-version-immutable: new (claims: semver-released-immutable)
- change-history-iso-dates: new (claims: kac-iso-dates)

Second-check corrections, refuted (criteria 3 applies to these claims):
- rfc-no-actions-statement: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- md043-wildcards-only: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- rfc-security-considerations-required: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- patternfly-usage-when-to-use: refuted (quote-found yes, supports-claim partly); trust 74 -> 54; a rule citing it cannot carry MUST
- apple-dynamic-type: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST
- material-states-list: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- apg-keyboard-interaction-section: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **if-applicability** — verdict `unsupported` (claims: if-applicability-prior, json-schema-const, json-schema-if-then). Prior text, kept word for word: "This category applies to any file with `type: ingredient` in its frontmatter. All files in `ingredients/` (and its subdirectories) MUST have this type, except `_template.md`."
  - against: JSON Schema's `const` pins a value, such as `type: ingredient`.
  - against: JSON Schema's `if` selects between `then` and `else` subschemas, so one schema can apply UI-only checks to UI ingredients and skip them for infrastructure ones.
- **if-section-order** — verdict `unsupported` (claims: if-section-order-prior, rfc-order-strongly-recommended-in-body, patternfly-template-omit-but-fixed-headings, md043-enforces-heading-structure, ubl-template-clarity, ubl-form-fits-project). Prior text, kept word for word: "Ingredients MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear out of order.

1. YAML frontmatter
2. `# Title`
3. `## Overview`
4. `## Behavioral Requirements`
5. `## Appearance`
6. `## States`
7. `## Accessibility`
8. `## Conformance Test Vectors`
9. `## Edge Cases`
10. `## Configuration`
11. `## Deep Linking` (MAY omit)
12. `## Localization` (MAY omit)
13. `## Accessibility Options` (MAY omit)
14. `## Feature Flags` (MAY omit)
15. `## Analytics` (MAY omit)
16. `## Privacy` (MAY omit)
17. `## Logging`
18. `## Platform Notes`
19. `## Reference Implementations` (MAY: derived from `index.json` when compiled; never authored)
20. `## Design Decisions`
21. `## Compliance`
22. `## Change History`"
  - against: The RFC Style Guide gives a fixed element order but only strongly recommends it inside the document body; the order is required only outside the body (front and back matter).
  - against: PatternFly's guideline template fixes section order and names. Sections may be omitted, but a section that is present must use the specified heading and level.
  - against: markdownlint's MD043 checks a file's headings against a configured list, enforcing one heading structure across a set of files.
  - against: The same author: a template does no harm, but clarity is what matters.
  - against: An experienced design-doc author at Google says such documents should take whatever form suits the project, not follow a strict guideline.
- **if-frontmatter-complete** — verdict `unsupported` (claims: if-frontmatter-complete-prior, jekyll-front-matter-first, json-schema-required-properties). Prior text, kept word for word: "All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.

The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

**Applies when:** always.

**Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references."
  - against: Tools that read YAML front matter require it to come first in the file, between triple-dashed lines.
  - against: JSON Schema's `required` keyword checks that every named property is present, which fits a frontmatter field list.
- **if-type-field** — verdict `unsupported` (claims: if-type-field-prior, json-schema-const). Prior text, kept word for word: "The `type` field MUST be `ingredient`.

**Applies when:** always."
  - against: JSON Schema's `const` pins a value, such as `type: ingredient`.
- **if-title-heading** — verdict `unsupported` (claims: if-title-heading-prior, md041-first-line-h1, md025-front-matter-title-is-h1, markdownlint-custom-rules). Prior text, kept word for word: "The first H1 heading MUST match the frontmatter `title` field exactly.

**Applies when:** always."
  - against: markdownlint's MD041 checks that a document has a title by requiring its first line to be a top-level heading. No built-in rule checks that the H1 equals the front-matter title.
  - against: markdownlint treats a front-matter `title` as the document's top-level heading, so by default a following `# Title` H1 is reported as a second top-level heading.
  - against: markdownlint custom rules can do anything the built-in rules can, so title equality or a section order with named optional sections can be checked by a custom rule.
- **if-appearance** — verdict `unsupported` (claims: if-appearance-prior, material-attribute-table). Prior text, kept word for word: "The ingredient MUST have a `## Appearance` section defining visual properties: corner radius, padding, font, background, foreground, border, shadow, and size constraints.

**Applies when:** UI ingredients (components, panels, windows). MAY be omitted for infrastructure ingredients."
  - against: Material documents a component's visual properties as attribute tables, with a default value for each attribute.
- **if-states** — verdict `unsupported` (claims: if-states-prior, apple-press-state, material-states-list, flutter-interactive-states). Prior text, kept word for word: "The ingredient MUST have a `## States` section with a table defining visual state changes (default, pressed, disabled, focused, loading, etc.).

**Applies when:** UI ingredients with interactive states. MAY be omitted for infrastructure ingredients."
  - against: Apple requires a press state for a custom button.
  - against: Material's component documentation lists the interactive states a component has: enabled, disabled, hover, focused and pressed, plus its selection states.
  - against: Flutter defines a standard set of interactive widget states: hovered, focused, pressed, dragged, selected, scrolledUnder, disabled and error.
- **if-edge-cases** — verdict `unsupported` (claims: if-edge-cases-prior, act-assumptions-listed, rfc3552-out-of-scope-stated). Prior text, kept word for word: "The ingredient MUST have a `## Edge Cases` section describing boundary conditions, error states, and unexpected input scenarios.

**Applies when:** always."
  - against: An ACT rule must list its known assumptions, limitations and exceptions.
  - against: A specification's required security section must say what is out of scope and why, not only what is covered.
- **if-configuration** — verdict `unsupported` (claims: if-configuration-prior, rfc-empty-iana-section-kept, w3c-qa-label-optional-features, material-attribute-table). Prior text, kept word for word: "The ingredient MUST have a `## Configuration` section with a table listing configurable options: Option, Type, Default, Description. If the ingredient has no configurable options, the section MUST be present with a note stating "This ingredient has no configurable options."

**Applies when:** always."
  - against: IANA prefers that an IANA Considerations section with nothing to say be kept, saying so, rather than omitted, so a reader can tell a deliberate 'none' from an omission.
  - against: Optional features should be labelled so they can all be found, and when there are none the conformance section should say so rather than stay silent.
  - against: Material documents a component's visual properties as attribute tables, with a default value for each attribute.
- **if-logging** — verdict `unsupported` (claims: if-logging-prior, apple-logger-optional, apple-logger-subsystem-category). Prior text, kept word for word: "The ingredient MUST have a `## Logging` section defining: subsystem, category, and a table of log events with columns: Event, Level, Message.

**Applies when:** always."
  - against: On Apple's Logger the subsystem and category are optional.
  - against: On Apple platforms a logger's subsystem is a large functional area of the app, and its category a specific area within that subsystem.
- **if-platform-notes** — verdict `unsupported` (claims: if-platform-notes-prior, apple-platform-considerations-none, apple-min-control-size-per-platform). Prior text, kept word for word: "The ingredient MUST have a `## Platform Notes` section with per-platform implementation guidance. At minimum: SwiftUI, Compose, React/Web.

**Applies when:** always. Single-platform ingredients list only the target platform."
  - against: Apple's per-platform section names each platform and says so explicitly when a platform has nothing extra.
  - against: Apple gives a default and a smaller minimum control size for each platform: iOS and iPadOS 44x44 pt default, 28x28 pt minimum; macOS 28 and 20; tvOS 66 and 56; visionOS 60 and 28; watchOS 44 and 28.
- **if-reference-implementations** — verdict `unsupported` (claims: if-reference-implementations-prior, act-optional-items). Prior text, kept word for word: "The ingredient MUST NOT carry an authored `## Reference Implementations` section. The code that implements it is recorded in its cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>` (`--remove <location>` drops a row), and `cookr confirm <uuid|rdid>` records it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section after `## Platform Notes`. `platform` is one of `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`; a location is a repo-relative file, a directory ending with `/` (which claims every source file below it), or a URL. Every recorded location MUST exist, unless the row is `planned`.

**Applies when:** the repo's `.cookr.json` declares `roots` (a cookbook that lives beside its source). `cookr validate` checks that every recorded location exists."
  - against: The ACT Rules Format separates its required items from a short list of items it labels optional, implementations among them.
- **if-design-decisions** — verdict `unsupported` (claims: if-design-decisions-prior, nygard-adr-status, nygard-consequences-listed). Prior text, kept word for word: "The ingredient MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

**Applies when:** always. New ingredients start with an empty section; decisions are added as they arise."
  - against: A decision record carries a status: proposed until the stakeholders agree, accepted after.
  - against: A decision record lists all of the decision's consequences.
- **if-compliance** — verdict `contradicted` (claims: if-compliance-prior, earl-outcome-values, act-outcome-types). Prior text, kept word for word: "The ingredient MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

**Applies when:** always."
  - against: W3C's EARL recommends five outcome values for a test result: passed, failed, cantTell, inapplicable and untested. It has no 'partial'.
  - against: ACT outcomes include 'inapplicable' alongside passed and failed.
- **if-change-history** — verdict `unsupported` (claims: if-change-history-prior, kac-guiding-principles, semver-released-immutable). Prior text, kept word for word: "The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always."
  - against: A change history has an entry for every version, newest first, each with its release date.
  - against: Under Semantic Versioning, a released version's contents must not change; any change is a new version.
- **tmpl-approval-fields** — verdict `unsupported` (claims: tmpl-approval-fields-prior, nygard-adr-status). Prior text, kept word for word: "the template's frontmatter carries two fields the draft's required list lacks: "approved-by: \"\"" and "approved-date: \"\""." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: A decision record carries a status: proposed until the stakeholders agree, accepted after.
- **tmpl-accessibility-min-tap-target** — verdict `contradicted` (claims: tmpl-accessibility-min-tap-target-prior, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40, wcag-target-size-minimum-24). Prior text, kept word for word: ""- Role/trait (e.g., button, heading, text field)
- Label requirements
- Announce state changes (e.g., loading, disabled)
- Minimum tap target: 44×44pt"" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Apple gives a default and a smaller minimum control size for each platform: iOS and iPadOS 44x44 pt default, 28x28 pt minimum; macOS 28 and 20; tvOS 66 and 56; visionOS 60 and 28; watchOS 44 and 28.
  - against: Android recommends touch targets of at least 48x48 dp.
  - against: Windows sets touch targets at about 7.5 mm square (40x40 pixels at 135 PPI and 1.0x scale).
  - against: WCAG 2.2's Level AA target size is 24 by 24 CSS pixels.
- **tmpl-deep-linking-patterns** — verdict `contradicted` (claims: tmpl-deep-linking-patterns-prior, apple-universal-links-recommended, apple-url-scheme-attack-vector). Prior text, kept word for word: ""| Platform | URL Pattern |" with rows "| Apple | `{{app_scheme}}://component-name` |", "| Android | `https://{{app_domain}}/component-name` |", "| Web | `/component-name` |"." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Apple accepts custom URL schemes for deep links but strongly recommends universal links.
  - against: Apple warns that a custom URL scheme is an attack vector into the app.
- **tmpl-analytics-events** — verdict `contradicted` (claims: tmpl-analytics-events-prior, firebase-event-name-charset). Prior text, kept word for word: ""| Event | Properties | When |" with rows "| `component_name.viewed` | `{}` | Component appears on screen |" and "| `component_name.interacted` | `{ action: string }` | User interacts with component |"." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Firebase Analytics event names may hold only letters, digits and underscores, must start with a letter, and run to at most 40 characters, so a dotted name such as `component_name.viewed` is invalid there.
- **component-recipe-sections-in-order** — verdict `unsupported` (claims: component-recipe-sections-in-order-prior, rfc-order-strongly-recommended-in-body, rfc-some-sections-required, patternfly-template-omit-but-fixed-headings, json-schema-if-then). Prior text, kept word for word: "- **must-contain-template-sections-in-order**: The recipe MUST contain all sections defined in the standard template, in the prescribed order.
  - For component recipes, the required sections in order are: **Overview**, **Behavioral Requirements**, **Appearance**, **States**, **Accessibility**, **Conformance Test Vectors**, **Edge Cases**."
  - against: The RFC Style Guide gives a fixed element order but only strongly recommends it inside the document body; the order is required only outside the body (front and back matter).
  - against: In the RFC series only some of the listed sections are required; the rest appear when they apply.
  - against: PatternFly's guideline template fixes section order and names. Sections may be omitted, but a section that is present must use the specified heading and level.
  - against: JSON Schema's `if` selects between `then` and `else` subschemas, so one schema can apply UI-only checks to UI ingredients and skip them for infrastructure ones.

## Open questions

- Should an inapplicable section be omitted, or kept with a one-line 'not applicable' note in the source (IETF/W3C practice) and hidden only in a rendered form (GOV.UK practice)?
- Should ingredients split into UI and infrastructure variants with their own section lists, or keep one schema that applies UI-only sections conditionally (JSON Schema if/then)?
- Which of the formatting checks should become a schema or lint rule rather than prose: the section order, the frontmatter fields, the H1-equals-title check?
- Should the template's tap-target default be one value, a per-platform table (Apple per platform, Android 48dp, Windows 40px) or the WCAG 2.2 AA 24px floor with 44px as the enhanced target?
- Should analytics event names use dots, or underscores to fit Firebase's naming limits?
- Should the Apple deep-linking row show a universal link instead of a custom URL scheme?
- Should the compliance status vocabulary keep 'partial', or adopt EARL's passed/failed/cantTell/inapplicable/untested?
- Should the section-order and section-presence rules stay MUST where the sources support only recommended strength?
- Should the template keep approved-by and approved-date, which no source and no required-field list prescribes?
- Should 'loading' stay among the default states, given that no platform's state list includes it?
- Should the H1 duplicate the frontmatter title, given that markdownlint's default treats a front-matter title as the top-level heading?

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `rules.md` (source fidelity, strength rule): four rules that are not on the owner list carry MUST, but the weakest claim each one cites is only a recommendation or advice. Every instance:
    - `if-overview` cites `govuk-when-to-use`. That claim is an unmarked template prompt ("Briefly describe the situation(s) when to use this component"). The same template marks only the description as required (`govuk-description-required`: "It is required to display the description"), and `govuk-template-empty-fields-hidden` shows its other fields are optional. So "when to use it" is at MUST without support.
    - `if-behavioral-requirements` cites `oasis-ta-identifier` (an OASIS Committee Note; "It is recommended that the identifier be made universally unique") and `respec-conformance-lint` (a tool that only "will warn you").
    - `if-accessibility` cites `apple-strive-min-control-size` ("Strive to meet …") and `android-touch-target-48dp` ("we recommend …"). These two are the only claims behind its "minimum tap target size" item. `apg-button-role` is descriptive.
    - `if-test-vectors` cites `w3c-qa-test-assertions` (good practice GP12, "not a requirement"), `w3c-qa-template-test-assertion-section` ("advisory") and `oasis-ta-normative-source` (Committee Note).
    - Fix: in each rule, keep MUST only on the part a MUST-strength claim carries, and move the rest to SHOULD:
      - `if-overview`: MUST for what the component is (`govuk-description-required`); "when to use it" becomes SHOULD, in this rule or in `overview-states-when-not-to-use`.
      - `if-accessibility`: MUST for role, label and announced state changes (`wcag-name-role-value`); the tap-target item becomes SHOULD (`per-platform-target-sizes` already holds it at SHOULD).
      - `if-behavioral-requirements` and `if-test-vectors`: lower to SHOULD, or cite only their MUST-strength claims (`w3c-qa-conformance-clause`, `w3c-qa-consistent-requirement-style`, `w3c-qa-indicate-levels`, `act-examples-pass-fail-inapplicable`) for the MUST part and give the rest SHOULD.
    - I checked the other non-owner MUST rules and they hold: `accessibility-options-include-text-size` (WCAG AA), `analytics-event-names-fit-platform-limits` (Firebase's hard limits), `released-version-immutable` (SemVer MUST).
- R1.2: `rules.md`, `tmpl-feature-flags-table` (source fidelity): the MUST covers the table layout `| Flag Key | Default | Description |`. `openfeature-flag-key-and-default` supports only that a flag has a key and a default value, and it says that about the client evaluation API, not about a documentation table. The build-bar line already leaves the table out ("every flag … has its key and its default value"). Fix: keep the MUST on "give each flag its key and its default value". Put the table at SHOULD, or drop it.
- R1.3: `rules.md` (source fidelity: every rule follows from the claims it cites): three rules cite a claim their text does not use, or say more than the claim supports. Every instance:
    - `tmpl-appearance-properties` cites `fluent-contrast-in-all-states` but says nothing about contrast. Contrast is `appearance-contrast-in-all-states`'s subject.
    - `tmpl-states-table` cites `wcag-name-role-value`. That claim is about states being programmatically determinable and announced, not about a visual table of appearance changes.
    - `tmpl-design-decisions-approved`: its first SHOULD ("Each decision … SHOULD be recorded in `## Design Decisions`") has no supporting claim, because `nygard-adr-status` covers only a decision's status. Its second SHOULD says "approved by the user", but the claim says "project stakeholders".
    - Fix:
      - Drop `fluent-contrast-in-all-states` from `tmpl-appearance-properties`. `appearance-contrast-in-all-states` still cites it.
      - Drop `wcag-name-role-value` from `tmpl-states-table` (`if-accessibility` still cites it), or add the programmatic-state point the claim actually makes.
      - Reduce `tmpl-design-decisions-approved` to the status the claim supports, for example "Each decision in `## Design Decisions` SHOULD carry its status: pending (proposed) until its stakeholders agree, then yes (accepted)." Change its build-bar line to match.
- R1.4: `rules.md`, `accessibility-options-include-text-size` (internal consistency): the rule says an ingredient that shows text MUST give its text-resize behaviour "in `## Accessibility Options`". `if-section-order` marks that section "(MAY omit)", and nothing tells the author that such an ingredient must therefore carry it. Its build-bar line also leaves out where the statement goes. Fix: say so in the rule, for example "… MUST carry `## Accessibility Options` and say there how its text resizes …". Alternatively, put the statement in `## Accessibility`, which is always present. Make the build-bar line name the section either way.
- R1.5: `a-build-must-establish.md` (the build bar must match the rule it checks): four lines for owner-list rules leave out values that the kept rule text requires. Each omission quietly leans toward an open question that belongs to the owner. Every instance:
    - `tmpl-accessibility-min-tap-target` drops "44×44pt" (open question 4).
    - `tmpl-deep-linking-patterns` drops the three URL patterns, among them `{{app_scheme}}://component-name` (open question 6).
    - `tmpl-analytics-events` drops the two template rows and their dotted names (open question 5).
    - `if-compliance` drops the status values `passed`, `failed`, `partial` (open question 7).
    - Fix: restore each value as the rule states it, for example "`## Accessibility` holds the template's items: …, and a minimum tap target of 44×44pt" and "… Status values `passed`, `failed`, `partial`, each check linked to its definition".
- R1.6: `rules.md` (behavioral-requirements `must-not-bundle-behaviors-into-one-requirement`): rules that are not on the owner list bundle separately testable behaviours into one bullet. Every instance:
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
- R1.7: `rationale.md` (behavioral-requirements `must-explain-rationale-for-should-requirements`): the Rationale covers 11 of 53 rules. These SHOULD rules give no reason, either inline or in the Rationale: `tmpl-approval-fields`, `overview-states-when-not-to-use`, `appearance-contrast-in-all-states`, `tmpl-states-table`, `states-include-hover-and-selected`, `accessibility-keyboard-interaction`, `tmpl-test-vector-id-format`, `assumptions-and-limitations-stated`, `tmpl-deep-linking-patterns`, `tmpl-accessibility-options`, `tmpl-analytics-events`, `tmpl-privacy-fields`, `privacy-states-encryption-in-transit`, `tmpl-logging-subsystem-category`, `tmpl-design-decisions-approved`, `tmpl-compliance-link-form`, `change-history-iso-dates`. The ones that do give a reason are `tmpl-localization-table` ("for the translator"), `tmpl-platform-notes-platforms` ("since each platform's own guidelines differ") and those in `rationale.md`. Fix: add one Rationale bullet per rule, or an inline "so that …" clause, drawn from the cited claim. Examples:
    - `change-history-iso-dates`: an ISO standard date format, per Keep a Changelog.
    - `tmpl-compliance-link-form`: a UUID is unique across space and time, so the link survives renames.
    - `accessibility-keyboard-interaction`: APG documents keyboard interaction beside roles, states and properties.
- R1.8: `rules.md` `short-required-core-labelled-optional-rest` and `intro.md` (behavioral-requirements `should-not-use-unanchored-relative-terms`): "a short core of sections" gives no threshold and names no core, so a build cannot test "short". Fix: define the core as the sections `if-section-order` does not mark "(MAY omit)", or drop "short" in both places.

## Round 2 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R2.1: `rules.md`, `accessibility-role`, `accessibility-label`, `accessibility-state-announcements` (source fidelity, internal consistency). These rules are new this round. Each is a MUST with no "Applies when", so it binds every ingredient. `if-accessibility` says "Applies when: always". `wcag-name-role-value` covers only "user interface components". `accessibility-not-applicable-stated` and the new "Saying a section has nothing to say" bullet tell an infrastructure ingredient to say accessibility is out of scope. Under the three MUSTs, that same ingredient must also give a role, a label and its state announcements. The two sets of rules contradict each other, and the MUSTs reach past the claim's scope. The build-bar lines for all three repeat the gap. Fix: scope each of the three rules, and its build-bar line, to an ingredient with a user interface, for example "**Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`."
- R2.2: `rules.md`, `short-required-core-labelled-optional-rest` (internal consistency). This text changed this round. It defines the required sections as "carried by every ingredient" and as those `if-section-order` leaves unmarked. `## Appearance` and `## States` are unmarked there, but `if-appearance` and `if-states` say they "MAY be omitted for infrastructure ingredients". So the rule calls two sections required by every ingredient when another rule lets some ingredients omit them. Fix: drop "carried by every ingredient", or qualify it, for example "(`## Appearance` and `## States` by UI ingredients only, per `if-appearance` and `if-states`)". If the build-bar line names the exception, make it match.
- R2.3: `rationale.md` (factual error against cited claims; every Rationale bullet is new this round). Three bullets say more than the claims they draw on. Every instance:
      - `tmpl-states-table`, `states-include-hover-and-selected`: the bullet says "Flutter's, Material's and Fluent's state lists include hover and selected". `fluent-rest-selected-states` names only rest and selected, and has no hover. Fix: "Flutter's and Material's state lists include hover and selected, and Fluent's includes selected."
      - `tmpl-logging-subsystem-category`: the bullet says "so that log messages can be filtered by functional area". Neither `apple-logger-subsystem-category` nor `apple-logger-optional` mentions filtering. The second claim says only that the two strings "add context to all messages you log". Fix: "so that each message carries the context of its functional area".
      - `section-structure-machine-checked`: the bullet says "MD043's wildcards stand only for unspecified headings, so named optional sections take a custom rule". `md043-wildcards-only`'s second check refuted exactly that inference: the doc also lists `%` regex headings and `^` loops, and never says a named heading cannot be optional or that a custom rule is needed. Fix: "MD043's wildcards `*`, `+` and `?` stand for unspecified headings; a custom rule can name an optional section".

## Round 3 findings

Verdict: pass. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

none
