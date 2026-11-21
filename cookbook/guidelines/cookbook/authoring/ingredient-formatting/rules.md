
### The file, its frontmatter and its title

- **if-applicability**: This category applies to any file with `type: ingredient` in its frontmatter. All files in `ingredients/` (and its subdirectories) MUST have this type, except `_template.md`. (claim: if-applicability-prior)
- **if-frontmatter-complete**: All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.

  The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

  **Applies when:** always.

  **Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references. (claim: if-frontmatter-complete-prior)
- **tmpl-approval-fields**: An ingredient's frontmatter SHOULD carry the template's approval fields: the template's frontmatter carries two fields the draft's required list lacks: "approved-by: \"\"" and "approved-date: \"\"". (claim: tmpl-approval-fields-prior)
- **if-type-field**: The `type` field MUST be `ingredient`.

  **Applies when:** always. (claim: if-type-field-prior)
- **if-title-heading**: The first H1 heading MUST match the frontmatter `title` field exactly.

  **Applies when:** always. (claim: if-title-heading-prior)

### Which sections, in which order

- **if-section-order**: Ingredients MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear out of order.

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
  22. `## Change History` (claim: if-section-order-prior)
- **short-required-core-labelled-optional-rest**: The ingredient format SHOULD label every section either required or optional, so that every optional section can be found: the required sections are those `if-section-order` does not mark "(MAY omit)" or "(MAY: …)" (`## Appearance` and `## States` by UI ingredients only, per `if-appearance` and `if-states`), and the optional sections are those it marks. (claims: rfc-some-sections-required, rfc3552-security-section-required, rfc-security-considerations-required, act-required-items, act-optional-items, w3c-qa-label-optional-features)
- **present-section-uses-specified-heading**: A section that is present SHOULD use its specified heading and heading level. (claim: patternfly-template-omit-but-fixed-headings)
- **inapplicable-section-stated-not-omitted**: A section an ingredient carries that has nothing to say for it SHOULD say so in one line, as Apple's "No additional considerations for tvOS." does, rather than stand empty, so that a reader can tell a deliberate 'none' from an omission. This holds for the source, even where a published or rendered form drops the empty section, as the RFC Editor does at publication and GOV.UK's template does on its website. (claims: rfc-empty-iana-section-kept, rfc-editor-removes-empty-iana, govuk-template-empty-fields-hidden, rfc-no-actions-statement, w3c-qa-label-optional-features, apple-platform-considerations-none, play-form-even-if-no-data)
- **informative-sections-labelled**: A section that states no requirements MAY be marked non-normative, with the line "This section is non-normative." (claim: respec-informative-marking)
- **section-structure-machine-checked**: An ingredient's structure MAY be checked by a tool rather than by a reader: its headings against a fixed list (markdownlint's MD043, whose wildcards `*`, `+` and `?` stand for unspecified headings), a required heading's absence (Vale's occurrence check), a missing required section or a section with no heading (as ReSpec lints a specification), and named optional sections by a custom rule (markdownlint custom rules, Vale's script check); its frontmatter fields with JSON Schema's `required`, and its section order with `prefixItems` once the sections are parsed into an ordered array, since a schema cannot check the order of an object's keys. (claims: md043-enforces-heading-structure, md043-wildcards-only, markdownlint-custom-rules, vale-occurrence-min-flags-absence, vale-script-arbitrary-rules, respec-privsec-lint, respec-headingless-lint, json-schema-required-properties, json-schema-prefixitems-positional, json-schema-objects-unordered)
- **requirement-keywords-without-section-flagged**: A tool MAY warn when an ingredient uses RFC 2119 keywords but has no `## Behavioral Requirements` section, as ReSpec warns when RFC 2119 keywords are present but the conformance section is missing. (claim: respec-conformance-lint)
- **component-recipe-sections-in-order**: - **must-contain-template-sections-in-order**: The recipe MUST contain all sections defined in the standard template, in the prescribed order.
    - For component recipes, the required sections in order are: **Overview**, **Behavioral Requirements**, **Appearance**, **States**, **Accessibility**, **Conformance Test Vectors**, **Edge Cases**. (claim: component-recipe-sections-in-order-prior)

### Overview and Behavioral Requirements

- **if-overview**: The ingredient MUST have a `## Overview` section with a brief description of what the component is.

  **Applies when:** always. (claim: govuk-description-required)
- **overview-states-when-to-use**: The `## Overview` SHOULD say when to use the component. (claims: govuk-when-to-use, patternfly-usage-when-to-use)
- **overview-states-when-not-to-use**: The `## Overview` SHOULD say when not to use the component. (claim: govuk-when-not-to-use)
- **overview-states-why-to-use**: The `## Overview` SHOULD say why the component should be used. (claim: patternfly-usage-when-to-use)
- **if-behavioral-requirements**: The ingredient MUST have a `## Behavioral Requirements` section that states its conformance requirements.

  **Applies when:** always. (claim: w3c-qa-conformance-clause)
- **behavioral-requirements-keyword-levels**: Each requirement in `## Behavioral Requirements` MUST carry an RFC 2119 keyword that indicates whether it is mandatory (MUST), recommended (SHOULD) or optional (MAY). (claim: w3c-qa-indicate-levels)
- **behavioral-requirements-one-style**: Every requirement in `## Behavioral Requirements` MUST be written in one consistent style that tells it apart from the section's other text. (claim: w3c-qa-consistent-requirement-style)
- **behavioral-requirements-named**: Each requirement SHOULD carry a unique name in bold kebab-case, `**must-do-something**: Component MUST ...`, so that each test vector can map to the requirement it tests. (claims: oasis-ta-identifier, w3c-qa-consistent-requirement-style)

### Appearance and States

- **if-appearance**: The ingredient MUST have a `## Appearance` section defining visual properties: corner radius, padding, font, background, foreground, border, shadow, and size constraints.

  **Applies when:** UI ingredients (components, panels, windows). MAY be omitted for infrastructure ingredients. (claim: if-appearance-prior)
- **tmpl-appearance-properties**: An `## Appearance` section MAY give a value for each visual property the template lists: corner radius; padding (vertical × horizontal); font (weight, size); background (color value or description); foreground/text (color value or description); border (width, color, if any); shadow (offset, blur, color, if any); and min/max size (constraints, if any). (claim: material-attribute-table)
- **appearance-contrast-in-all-states**: The colors an `## Appearance` section gives SHOULD keep text at 4.5:1 and icons at 3:1 contrast against their background in every interactive state. (claim: fluent-contrast-in-all-states)
- **if-states**: The ingredient MUST have a `## States` section with a table defining visual state changes (default, pressed, disabled, focused, loading, etc.).

  **Applies when:** UI ingredients with interactive states. MAY be omitted for infrastructure ingredients. (claim: if-states-prior)
- **tmpl-states-table**: A `## States` section SHOULD be a table of `| State | Appearance change |` with a row for each state the component takes; the template's rows are Default, Pressed, Disabled, Focused and Loading. (claims: apple-press-state, flutter-interactive-states, material-states-list)
- **states-include-hover-and-selected**: A component that can be hovered or selected SHOULD have Hover and Selected rows in its `## States` table. (claims: flutter-interactive-states, flutter-hover-state, flutter-selected-state, material-states-list, fluent-rest-selected-states)

### Accessibility

- **if-accessibility**: The ingredient MUST have a `## Accessibility` section.

  **Applies when:** always. (claim: wcag-name-role-value)
- **accessibility-role**: The `## Accessibility` section MUST give the component's role or trait (for example, button, heading, text field), the role assistive technologies determine programmatically.

  **Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`. (claim: wcag-name-role-value)
- **accessibility-role-from-apg**: Where the ARIA Authoring Practices Guide has a pattern for the component, the role given SHOULD be the one that pattern states (a button has role `button`). (claim: apg-button-role)
- **accessibility-label**: The `## Accessibility` section MUST state the component's label requirements: the name assistive technologies determine programmatically for it.

  **Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`. (claim: wcag-name-role-value)
- **accessibility-state-announcements**: The `## Accessibility` section MUST state how each change to the component's states (for example, loading, disabled) is notified to assistive technologies.

  **Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`. (claim: wcag-name-role-value)
- **accessibility-min-target-size**: The `## Accessibility` section SHOULD give the component's minimum target size. (claims: apple-strive-min-control-size, android-touch-target-48dp, wcag-target-size-minimum-24)
- **accessibility-not-applicable-stated**: An infrastructure ingredient's `## Accessibility` section SHOULD say that accessibility is out of scope for it, and why, rather than stand empty. (claims: rfc3552-out-of-scope-stated, rfc-empty-iana-section-kept)
- **accessibility-keyboard-interaction**: The `## Accessibility` section SHOULD describe the component's keyboard interaction, beside its role, states and properties. (claim: apg-keyboard-interaction-section)
- **per-platform-target-sizes**: The minimum target size the `## Accessibility` section gives SHOULD be stated for each platform from that platform's own guidelines, not as one value: Apple's per-platform control sizes (default and minimum: iOS and iPadOS 44x44 pt and 28x28 pt; macOS 28 and 20; tvOS 66 and 56; visionOS 60 and 28; watchOS 44 and 28), with a button's hit region at least 44x44 pt (60x60 pt in visionOS); Android's 48x48 dp, 8 dp apart; Windows' 7.5 mm square (40x40 pixels at 135 PPI and 1.0x scale); and on the web WCAG 2.2's 24 by 24 CSS pixels at Level AA, 44 by 44 at Level AAA. (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, apple-button-hit-region-44, android-touch-target-48dp, android-touch-target-spacing, windows-touch-target-40, wcag-target-size-minimum-24, wcag-target-size-enhanced-44)
- **tmpl-accessibility-min-tap-target**: An ingredient's `## Accessibility` section SHOULD hold the template's items: "- Role/trait (e.g., button, heading, text field)
  - Label requirements
  - Announce state changes (e.g., loading, disabled)
  - Minimum tap target: 44×44pt" (claim: tmpl-accessibility-min-tap-target-prior)

### Conformance Test Vectors and Edge Cases

- **if-test-vectors**: The ingredient MUST have a `## Conformance Test Vectors` section whose vectors each pair an input with the outcome expected for it.

  **Applies when:** always. (claim: act-examples-pass-fail-inapplicable)
- **test-vectors-table**: The `## Conformance Test Vectors` SHOULD be a table of `| ID | Requirements | Input | Expected |`: each vector's identifier, the requirements it tests, its input and its expected outcome. (claims: oasis-ta-identifier, oasis-ta-normative-source, act-examples-pass-fail-inapplicable)
- **tmpl-test-vector-id-format**: Each test vector SHOULD carry a unique ID in the template's form, `component-001`. (claim: oasis-ta-identifier)
- **test-vectors-map-to-requirements**: Each test vector SHOULD name, in its Requirements column, the named requirements of `## Behavioral Requirements` it tests (the template's `do-something`). (claims: oasis-ta-normative-source, w3c-qa-test-assertions)
- **test-vectors-cover-pass-fail-inapplicable**: The `## Conformance Test Vectors` section SHOULD give each requirement vectors whose expected outcome is passed, failed and inapplicable. (claims: act-examples-pass-fail-inapplicable, act-outcome-types)
- **template-carries-test-vectors**: The ingredient template, `_template.md`, SHOULD carry a `## Conformance Test Vectors` section, so that each new ingredient starts with a place for its test vectors. (claim: w3c-qa-template-test-assertion-section)
- **if-edge-cases**: The ingredient MUST have a `## Edge Cases` section describing boundary conditions, error states, and unexpected input scenarios.

  **Applies when:** always. (claim: if-edge-cases-prior)
- **assumptions-and-limitations-stated**: The `## Edge Cases` section SHOULD also list the ingredient's known assumptions, limitations and exceptions. (claim: act-assumptions-listed)
- **out-of-scope-cases-stated**: The `## Edge Cases` section SHOULD say which cases are out of scope, and why. (claim: rfc3552-out-of-scope-stated)

### Configuration and the optional sections

- **if-configuration**: The ingredient MUST have a `## Configuration` section with a table listing configurable options: Option, Type, Default, Description. If the ingredient has no configurable options, the section MUST be present with a note stating "This ingredient has no configurable options."

  **Applies when:** always. (claim: if-configuration-prior)
- **tmpl-deep-linking-patterns**: An ingredient's `## Deep Linking` section SHOULD follow the template's table: "| Platform | URL Pattern |" with rows "| Apple | `{{app_scheme}}://component-name` |", "| Android | `https://{{app_domain}}/component-name` |", "| Web | `/component-name` |". (claim: tmpl-deep-linking-patterns-prior)
- **deep-links-use-verified-https-links**: The deep links a `## Deep Linking` section defines SHOULD be verified https links: universal links on Apple platforms and App Links on Android. Apple accepts a custom URL scheme but strongly recommends universal links, and a custom URL scheme is a potential attack vector into the app. (claims: apple-universal-links-recommended, android-app-links-recommended, apple-url-scheme-attack-vector)
- **tmpl-localization-table**: A `## Localization` section SHOULD list each string in a table of `| String Key | Default (en) | Context |`, its Context describing where the string is used, for the translator. (claim: android-string-context)
- **tmpl-accessibility-options**: An `## Accessibility Options` section SHOULD document which accessibility display options the component responds to, in a table of `| Option | Behavior |` with rows for Reduce Motion (fewer automatic and repetitive animations, and motion triggered by interaction can be disabled unless it is essential), Increase Contrast (a higher-contrast color scheme), Differentiate Without Color (information conveyed by more than color alone) and, on Apple platforms that offer it, Dynamic Type (text the person resizes); on the web, Reduce Motion and Increase Contrast are read with the `prefers-reduced-motion` and `prefers-contrast` media features. (claims: apple-reduce-motion, apple-increase-contrast, apple-more-than-color, wcag-use-of-color, apple-dynamic-type, mq5-prefers-reduced-motion, mq5-prefers-contrast, wcag-animation-from-interactions)
- **accessibility-options-include-text-size**: An ingredient that shows text MUST state in `## Accessibility Options` how its text resizes up to 200 percent without loss of content or function (WCAG Level AA), so that section, which `if-section-order` lets other ingredients omit, is present in it. (claim: wcag-resize-text)
- **tmpl-feature-flags-table**: A `## Feature Flags` section MUST give each flag its key and its default value. (claim: openfeature-flag-key-and-default)
- **tmpl-analytics-events**: An ingredient's `## Analytics` section SHOULD follow the template's table: "| Event | Properties | When |" with rows "| `component_name.viewed` | `{}` | Component appears on screen |" and "| `component_name.interacted` | `{ action: string }` | User interacts with component |". (claim: tmpl-analytics-events-prior)
- **analytics-event-names-fit-platform-limits**: Where an ingredient's analytics events are sent to Firebase Analytics, each event name MUST hold only letters, digits and underscores, start with a letter and run to at most 40 characters. (claim: firebase-event-name-charset)
- **tmpl-privacy-fields**: A `## Privacy` section SHOULD state **Data collected** (None, or what is collected), **Storage** (where and how data is stored), **Transmission** (whether data leaves the device) and **Retention** (how long data is kept), so that a reader can tell whether data is collected: sent off the device and kept longer than servicing the request in real time needs, rather than processed ephemerally, in memory only. (claims: apple-collect-definition, play-ephemeral-processing)
- **privacy-states-none-collected**: The `## Privacy` section of an ingredient that collects no data SHOULD say that no data is collected. (claim: play-form-even-if-no-data)
- **privacy-states-encryption-in-transit**: A `## Privacy` section SHOULD also say whether data that leaves the device is encrypted in transit. (claim: play-encryption-in-transit)

### Logging, Platform Notes and Reference Implementations

- **if-logging**: The ingredient MUST have a `## Logging` section defining: subsystem, category, and a table of log events with columns: Event, Level, Message.

  **Applies when:** always. (claim: if-logging-prior)
- **tmpl-logging-subsystem-category**: Where the `## Logging` section names a subsystem and a category (both optional on Apple's Logger), they SHOULD carry Apple's meaning: the subsystem a large functional area of the app, the category a specific area within it (the template's `{{bundle_id}}` and `ComponentName`). (claims: apple-logger-subsystem-category, apple-logger-optional)
- **if-platform-notes**: The ingredient MUST have a `## Platform Notes` section with per-platform implementation guidance. At minimum: SwiftUI, Compose, React/Web.

  **Applies when:** always. Single-platform ingredients list only the target platform. (claim: if-platform-notes-prior)
- **tmpl-platform-notes-platforms**: `## Platform Notes` SHOULD carry an entry for each platform the ingredient targets among those the template lists (SwiftUI, Compose, React/Web, AppKit / UIKit, WinUI 3), since each platform's own guidelines differ (Apple, Android and Windows each set their own control and touch-target sizes). (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40)
- **platform-notes-none-stated**: A platform in `## Platform Notes` with nothing to add SHOULD say so in one line, as Apple's "No additional considerations for tvOS." does. (claim: apple-platform-considerations-none)
- **if-reference-implementations**: The ingredient MUST NOT carry an authored `## Reference Implementations` section. The code that implements it is recorded in its cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>` (`--remove <location>` drops a row), and `cookr confirm <uuid|rdid>` records it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section after `## Platform Notes`. `platform` is one of `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`; a location is a repo-relative file, a directory ending with `/` (which claims every source file below it), or a URL. Every recorded location MUST exist, unless the row is `planned`.

  **Applies when:** the repo's `.cookr.json` declares `roots` (a cookbook that lives beside its source). `cookr validate` checks that every recorded location exists. (claim: if-reference-implementations-prior)

### Design Decisions and Compliance

- **if-design-decisions**: The ingredient MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

  **Applies when:** always. New ingredients start with an empty section; decisions are added as they arise. (claim: if-design-decisions-prior)
- **tmpl-design-decisions-approved**: Each decision in `## Design Decisions` SHOULD carry its status: pending (proposed) until its stakeholders agree, then yes (accepted). (claim: nygard-adr-status)
- **if-compliance**: The ingredient MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

  **Applies when:** always. (claim: if-compliance-prior)
- **tmpl-compliance-link-form**: Each row of the `## Compliance` table (`| Check | Status | Category |`) SHOULD link the precise check it reports on by that check's UUID: `[adc.check.<document>.<check-name>](cookbook:<check-uuid>)`. (claims: oasis-ta-normative-source, uuid-unique-identifier)
- **compliance-status-includes-inapplicable**: The `## Compliance` status values SHOULD include `inapplicable`, for a check that does not apply to the ingredient, beside `passed` and `failed`. (claims: earl-outcome-values, act-outcome-types)

### Versions and Change History

- **if-change-history**: The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

  **Applies when:** always. (claim: if-change-history-prior)
- **change-history-iso-dates**: Each `## Change History` date SHOULD be an ISO 8601 date. (claim: kac-iso-dates)
- **released-version-immutable**: Once a version of an ingredient is released, its contents MUST NOT be modified; any modification MUST be released as a new version. (claim: semver-released-immutable)

