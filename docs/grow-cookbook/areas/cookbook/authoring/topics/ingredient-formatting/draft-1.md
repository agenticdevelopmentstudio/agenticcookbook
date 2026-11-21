---
id: 2c5ee8e0-9da5-4b44-9f87-51962abe76ab
title: "Ingredient Formatting"
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-21
modified: 2026-11-21
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "How a cookbook ingredient is laid out: frontmatter, title, section order, what each section holds, and platform defaults for targets, links and events."
platforms: []
tags:
  - cookbook
  - authoring
  - ingredient
  - formatting
depends-on: []
related:
  - e48a04d7-c479-427d-9d8e-fe9e9b990c77
  - 04fe1298-3880-4584-8a4a-c7a538eb5193
references:
  - https://www.rfc-editor.org/rfc/rfc7322
  - https://www.rfc-editor.org/rfc/rfc8126
  - https://www.rfc-editor.org/rfc/rfc3552
  - https://www.w3.org/TR/qaframe-spec/
  - https://www.w3.org/TR/act-rules-format/
  - https://www.w3.org/TR/EARL10-Schema/
  - http://docs.oasis-open.org/tag/guidelines/v1.0/cn02/guidelines-v1.0-cn02.html
  - https://semver.org/spec/v2.0.0.html
  - https://www.rfc-editor.org/rfc/rfc9562
  - https://github.com/DavidAnson/markdownlint/blob/main/doc/md043.md
  - https://github.com/DavidAnson/markdownlint/blob/main/doc/md025.md
  - https://github.com/DavidAnson/markdownlint/blob/main/doc/md041.md
  - https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md
  - https://docs.vale.sh/checks/occurrence.md
  - https://docs.vale.sh/checks/script.md
  - https://json-schema.org/draft/2020-12/json-schema-validation
  - https://json-schema.org/draft/2020-12/json-schema-core
  - https://respec.org/docs/
  - https://jekyllrb.com/docs/front-matter/
  - https://github.com/open-feature/spec/blob/main/specification/sections/01-flag-evaluation.md
  - https://github.com/patternfly/patternfly-org/blob/main/packages/documentation-site/patternfly-docs/content/content-design/writing-guides/patternfly-design-guidelines.md
  - https://docs.publishing.service.gov.uk/repos/govuk-design-guide/components/*component-documentation-template.html
  - https://github.com/material-components/material-components-android/blob/master/docs/components/Checkbox.md
  - https://api.flutter.dev/flutter/widgets/WidgetState.html
  - https://developer.apple.com/design/human-interface-guidelines/accessibility
  - https://developer.apple.com/design/human-interface-guidelines/buttons
  - https://developer.apple.com/design/human-interface-guidelines/typography
  - https://developer.apple.com/documentation/xcode/defining-a-custom-url-scheme-for-your-app
  - https://developer.apple.com/documentation/os/logger
  - https://developer.apple.com/app-store/app-privacy-details/
  - https://developer.android.com/guide/topics/ui/accessibility/apps
  - https://support.google.com/accessibility/android/answer/7101858
  - https://developer.android.com/training/app-links
  - https://developer.android.com/guide/topics/resources/localization
  - https://firebase.google.com/docs/reference/android/com/google/firebase/analytics/FirebaseAnalytics.Event
  - https://support.google.com/googleplay/android-developer/answer/10787469
  - https://learn.microsoft.com/en-us/windows/apps/design/input/guidelines-for-targeting
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/TR/mediaqueries-5/
  - https://www.w3.org/WAI/ARIA/apg/patterns/button/
  - https://fluent2.microsoft.design/components/web/react/core/button/usage
  - https://www.industrialempathy.com/posts/design-docs-at-google/
  - https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://keepachangelog.com/en/1.1.0/
approved-by: ""
approved-date: ""
triggers:
  - recipe-authoring
---

# Ingredient Formatting

An ingredient is a component spec laid out in one fixed order of named sections, from its frontmatter and title through Overview, Behavioral Requirements, Accessibility and Conformance Test Vectors to Compliance and Change History. Keep a short core of required sections and label the rest optional; when a section you carry has nothing to say, say so in one line; and take target sizes, deep links and analytics event names from each platform's own guidelines, not from one default.

## Rules

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
- **short-required-core-labelled-optional-rest**: The ingredient format SHOULD keep a short core of sections every ingredient carries and label each other section optional, so that every optional section can be found; a section that is present SHOULD use its specified heading and heading level. (claims: rfc-some-sections-required, rfc3552-security-section-required, rfc-security-considerations-required, act-required-items, act-optional-items, w3c-qa-label-optional-features, patternfly-template-omit-but-fixed-headings)
- **inapplicable-section-stated-not-omitted**: A section an ingredient carries that has nothing to say for it SHOULD say so in one line, as Apple's "No additional considerations for tvOS." does, rather than stand empty, so that a reader can tell a deliberate 'none' from an omission. This holds for the source, even where a published or rendered form drops the empty section, as the RFC Editor does at publication and GOV.UK's template does on its website. (claims: rfc-empty-iana-section-kept, rfc-editor-removes-empty-iana, govuk-template-empty-fields-hidden, rfc-no-actions-statement, w3c-qa-label-optional-features, apple-platform-considerations-none, play-form-even-if-no-data)
- **informative-sections-labelled**: A section that states no requirements MAY be marked non-normative, with the line "This section is non-normative." (claim: respec-informative-marking)
- **section-structure-machine-checked**: An ingredient's structure MAY be checked by a tool rather than by a reader: its headings against a fixed list (markdownlint's MD043), a required heading's absence (Vale's occurrence check), a missing required section or a section with no heading (as ReSpec lints a specification), and named optional sections, which MD043's wildcards cannot name, by a custom rule (markdownlint custom rules, Vale's script check); its frontmatter fields with JSON Schema's `required`, and its section order with `prefixItems` once the sections are parsed into an ordered array, since a schema cannot check the order of an object's keys. (claims: md043-enforces-heading-structure, md043-wildcards-only, markdownlint-custom-rules, vale-occurrence-min-flags-absence, vale-script-arbitrary-rules, respec-privsec-lint, respec-headingless-lint, json-schema-required-properties, json-schema-prefixitems-positional, json-schema-objects-unordered)
- **component-recipe-sections-in-order**: - **must-contain-template-sections-in-order**: The recipe MUST contain all sections defined in the standard template, in the prescribed order.
    - For component recipes, the required sections in order are: **Overview**, **Behavioral Requirements**, **Appearance**, **States**, **Accessibility**, **Conformance Test Vectors**, **Edge Cases**. (claim: component-recipe-sections-in-order-prior)

### Overview and Behavioral Requirements

- **if-overview**: The ingredient MUST have a `## Overview` section with a brief description of what the component is and when to use it.

  **Applies when:** always. (claims: govuk-description-required, govuk-when-to-use)
- **overview-states-when-not-to-use**: The `## Overview` SHOULD also say when not to use the component, and why to use it. (claims: govuk-when-not-to-use, patternfly-usage-when-to-use)
- **if-behavioral-requirements**: The ingredient MUST have a `## Behavioral Requirements` section containing named requirements using RFC 2119 keywords. Requirements use kebab-case names in bold: `**must-do-something**: Component MUST ...`

  **Applies when:** always. (claims: w3c-qa-conformance-clause, w3c-qa-consistent-requirement-style, w3c-qa-indicate-levels, oasis-ta-identifier, respec-conformance-lint)

### Appearance and States

- **if-appearance**: The ingredient MUST have a `## Appearance` section defining visual properties: corner radius, padding, font, background, foreground, border, shadow, and size constraints.

  **Applies when:** UI ingredients (components, panels, windows). MAY be omitted for infrastructure ingredients. (claim: if-appearance-prior)
- **tmpl-appearance-properties**: An `## Appearance` section MAY give a value for each visual property the template lists: corner radius; padding (vertical × horizontal); font (weight, size); background (color value or description); foreground/text (color value or description); border (width, color, if any); shadow (offset, blur, color, if any); and min/max size (constraints, if any). (claims: material-attribute-table, fluent-contrast-in-all-states)
- **appearance-contrast-in-all-states**: The colors an `## Appearance` section gives SHOULD keep text at 4.5:1 and icons at 3:1 contrast against their background in every interactive state. (claim: fluent-contrast-in-all-states)
- **if-states**: The ingredient MUST have a `## States` section with a table defining visual state changes (default, pressed, disabled, focused, loading, etc.).

  **Applies when:** UI ingredients with interactive states. MAY be omitted for infrastructure ingredients. (claim: if-states-prior)
- **tmpl-states-table**: A `## States` section SHOULD be a table of `| State | Appearance change |` with a row for each state the component takes; the template's rows are Default, Pressed, Disabled, Focused and Loading. (claims: apple-press-state, flutter-interactive-states, material-states-list, wcag-name-role-value)
- **states-include-hover-and-selected**: A component that can be hovered or selected SHOULD have Hover and Selected rows in its `## States` table. (claims: flutter-interactive-states, flutter-hover-state, flutter-selected-state, material-states-list, fluent-rest-selected-states)

### Accessibility

- **if-accessibility**: The ingredient MUST have a `## Accessibility` section defining: role/trait, label requirements, state change announcements, and minimum tap target size.

  **Applies when:** always. Infrastructure ingredients define accessibility as "not applicable" with justification. (claims: wcag-name-role-value, apg-button-role, wcag-target-size-minimum-24, apple-strive-min-control-size, android-touch-target-48dp)
- **accessibility-keyboard-interaction**: The `## Accessibility` section SHOULD describe the component's keyboard interaction, beside its role, states and properties. (claim: apg-keyboard-interaction-section)
- **per-platform-target-sizes**: The minimum target size the `## Accessibility` section gives SHOULD be stated for each platform from that platform's own guidelines, not as one value: Apple's per-platform control sizes (default and minimum: iOS and iPadOS 44x44 pt and 28x28 pt; macOS 28 and 20; tvOS 66 and 56; visionOS 60 and 28; watchOS 44 and 28), with a button's hit region at least 44x44 pt (60x60 pt in visionOS); Android's 48x48 dp, 8 dp apart; Windows' 7.5 mm square (40x40 pixels at 135 PPI and 1.0x scale); and on the web WCAG 2.2's 24 by 24 CSS pixels at Level AA, 44 by 44 at Level AAA. (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, apple-button-hit-region-44, android-touch-target-48dp, android-touch-target-spacing, windows-touch-target-40, wcag-target-size-minimum-24, wcag-target-size-enhanced-44)
- **tmpl-accessibility-min-tap-target**: An ingredient's `## Accessibility` section SHOULD hold the template's items: "- Role/trait (e.g., button, heading, text field)
  - Label requirements
  - Announce state changes (e.g., loading, disabled)
  - Minimum tap target: 44×44pt" (claim: tmpl-accessibility-min-tap-target-prior)

### Conformance Test Vectors and Edge Cases

- **if-test-vectors**: The ingredient MUST have a `## Conformance Test Vectors` section with a table containing columns: ID, Requirements, Input, Expected. Each test vector maps to one or more named requirements from `## Behavioral Requirements`.

  **Applies when:** always. (claims: act-examples-pass-fail-inapplicable, oasis-ta-normative-source, oasis-ta-identifier, w3c-qa-test-assertions, w3c-qa-template-test-assertion-section)
- **tmpl-test-vector-id-format**: Each test vector SHOULD carry a unique ID in the template's form, `component-001`, and name in its Requirements column the named requirements it tests (the template's `do-something`), in a table of `| ID | Requirements | Input | Expected |`. (claims: oasis-ta-identifier, w3c-qa-test-assertions)
- **test-vectors-cover-pass-fail-inapplicable**: The `## Conformance Test Vectors` section SHOULD give each requirement vectors whose expected outcome is passed, failed and inapplicable, each pairing an input with the outcome expected for it. (claims: act-examples-pass-fail-inapplicable, act-outcome-types, w3c-qa-template-test-assertion-section)
- **if-edge-cases**: The ingredient MUST have a `## Edge Cases` section describing boundary conditions, error states, and unexpected input scenarios.

  **Applies when:** always. (claim: if-edge-cases-prior)
- **assumptions-and-limitations-stated**: The `## Edge Cases` section SHOULD also list the ingredient's known assumptions, limitations and exceptions, and say which cases are out of scope and why. (claims: act-assumptions-listed, rfc3552-out-of-scope-stated)

### Configuration and the optional sections

- **if-configuration**: The ingredient MUST have a `## Configuration` section with a table listing configurable options: Option, Type, Default, Description. If the ingredient has no configurable options, the section MUST be present with a note stating "This ingredient has no configurable options."

  **Applies when:** always. (claim: if-configuration-prior)
- **tmpl-deep-linking-patterns**: An ingredient's `## Deep Linking` section SHOULD follow the template's table: "| Platform | URL Pattern |" with rows "| Apple | `{{app_scheme}}://component-name` |", "| Android | `https://{{app_domain}}/component-name` |", "| Web | `/component-name` |". (claim: tmpl-deep-linking-patterns-prior)
- **deep-links-use-verified-https-links**: The deep links a `## Deep Linking` section defines SHOULD be verified https links: universal links on Apple platforms and App Links on Android. Apple accepts a custom URL scheme but strongly recommends universal links, and a custom URL scheme is a potential attack vector into the app. (claims: apple-universal-links-recommended, android-app-links-recommended, apple-url-scheme-attack-vector)
- **tmpl-localization-table**: A `## Localization` section SHOULD list each string in a table of `| String Key | Default (en) | Context |`, its Context describing where the string is used, for the translator. (claim: android-string-context)
- **tmpl-accessibility-options**: An `## Accessibility Options` section SHOULD document which accessibility display options the component responds to, in a table of `| Option | Behavior |` with rows for Reduce Motion (fewer automatic and repetitive animations, and motion triggered by interaction can be disabled unless it is essential), Increase Contrast (a higher-contrast color scheme), Differentiate Without Color (information conveyed by more than color alone) and, on Apple platforms that offer it, Dynamic Type (text the person resizes); on the web, Reduce Motion and Increase Contrast are read with the `prefers-reduced-motion` and `prefers-contrast` media features. (claims: apple-reduce-motion, apple-increase-contrast, apple-more-than-color, wcag-use-of-color, apple-dynamic-type, mq5-prefers-reduced-motion, mq5-prefers-contrast, wcag-animation-from-interactions)
- **accessibility-options-include-text-size**: An ingredient that shows text MUST say, in `## Accessibility Options`, how its text resizes up to 200 percent without loss of content or function (WCAG Level AA). (claim: wcag-resize-text)
- **tmpl-feature-flags-table**: A `## Feature Flags` section MUST give each flag its key and its default value, in a table of `| Flag Key | Default | Description |` (the template's row: `{{app_prefix}}.component_name`, `true`, Enables this component). (claim: openfeature-flag-key-and-default)
- **tmpl-analytics-events**: An ingredient's `## Analytics` section SHOULD follow the template's table: "| Event | Properties | When |" with rows "| `component_name.viewed` | `{}` | Component appears on screen |" and "| `component_name.interacted` | `{ action: string }` | User interacts with component |". (claim: tmpl-analytics-events-prior)
- **analytics-event-names-fit-platform-limits**: Where an ingredient's analytics events are sent to Firebase Analytics, each event name MUST hold only letters, digits and underscores, start with a letter and run to at most 40 characters. (claim: firebase-event-name-charset)
- **tmpl-privacy-fields**: A `## Privacy` section SHOULD state **Data collected** (None, or what is collected), **Storage** (where and how data is stored), **Transmission** (whether data leaves the device) and **Retention** (how long data is kept), and an ingredient that collects nothing says so. Transmission and Retention together say whether data is collected: sent off the device and kept longer than servicing the request in real time needs, rather than processed ephemerally, in memory only. (claims: apple-collect-definition, play-ephemeral-processing, play-form-even-if-no-data)
- **privacy-states-encryption-in-transit**: A `## Privacy` section SHOULD also say whether data that leaves the device is encrypted in transit. (claim: play-encryption-in-transit)

### Logging, Platform Notes and Reference Implementations

- **if-logging**: The ingredient MUST have a `## Logging` section defining: subsystem, category, and a table of log events with columns: Event, Level, Message.

  **Applies when:** always. (claim: if-logging-prior)
- **tmpl-logging-subsystem-category**: Where the `## Logging` section names a subsystem and a category (both optional on Apple's Logger), they SHOULD carry Apple's meaning: the subsystem a large functional area of the app, the category a specific area within it (the template's `{{bundle_id}}` and `ComponentName`); its log events are a table of `| Event | Level | Message |` (the template's row: `debug`, `ComponentName: `). (claims: apple-logger-subsystem-category, apple-logger-optional)
- **if-platform-notes**: The ingredient MUST have a `## Platform Notes` section with per-platform implementation guidance. At minimum: SwiftUI, Compose, React/Web.

  **Applies when:** always. Single-platform ingredients list only the target platform. (claim: if-platform-notes-prior)
- **tmpl-platform-notes-platforms**: `## Platform Notes` SHOULD carry an entry for each platform the ingredient targets among those the template lists (SwiftUI, Compose, React/Web, AppKit / UIKit, WinUI 3), since each platform's own guidelines differ (Apple, Android and Windows each set their own control and touch-target sizes); a platform with nothing to add says so ("No additional considerations for tvOS."). (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40, apple-platform-considerations-none)
- **if-reference-implementations**: The ingredient MUST NOT carry an authored `## Reference Implementations` section. The code that implements it is recorded in its cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>` (`--remove <location>` drops a row), and `cookr confirm <uuid|rdid>` records it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section after `## Platform Notes`. `platform` is one of `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`; a location is a repo-relative file, a directory ending with `/` (which claims every source file below it), or a URL. Every recorded location MUST exist, unless the row is `planned`.

  **Applies when:** the repo's `.cookr.json` declares `roots` (a cookbook that lives beside its source). `cookr validate` checks that every recorded location exists. (claim: if-reference-implementations-prior)

### Design Decisions and Compliance

- **if-design-decisions**: The ingredient MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

  **Applies when:** always. New ingredients start with an empty section; decisions are added as they arise. (claim: if-design-decisions-prior)
- **tmpl-design-decisions-approved**: Each decision made during implementation that affects visual or behavioral outcome SHOULD be recorded in `## Design Decisions`, and each SHOULD be approved by the user: pending (proposed) until the user agrees, then yes (accepted). (claim: nygard-adr-status)
- **if-compliance**: The ingredient MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

  **Applies when:** always. (claim: if-compliance-prior)
- **tmpl-compliance-link-form**: Each row of the `## Compliance` table (`| Check | Status | Category |`) SHOULD link the precise check it reports on by that check's UUID: `[adc.check.<document>.<check-name>](cookbook:<check-uuid>)`. (claims: oasis-ta-normative-source, uuid-unique-identifier)
- **compliance-status-includes-inapplicable**: The `## Compliance` status values SHOULD include `inapplicable`, for a check that does not apply to the ingredient, beside `passed` and `failed`. (claims: earl-outcome-values, act-outcome-types)

### Versions and Change History

- **if-change-history**: The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

  **Applies when:** always. (claim: if-change-history-prior)
- **change-history-iso-dates**: Each `## Change History` date SHOULD be an ISO 8601 date. (claim: kac-iso-dates)
- **released-version-immutable**: Once a version of an ingredient is released, its contents MUST NOT be modified; any modification MUST be released as a new version. (claim: semver-released-immutable)

## Saying a section has nothing to say

- Write one line that names what is absent, in the section itself: "No additional considerations for tvOS." (Apple's per-platform sections), "This ingredient has no configurable options." (`## Configuration`), or, in `## Privacy`, that no user data is collected or shared (Google Play's Data safety form).
- Name every targeted platform in `## Platform Notes`, and give the line to a platform with nothing extra, so a reader sees it was considered.
- A line is not a heading with nothing under it: an empty section reads as an omission.

## Checking the structure with a tool

| Check | Tool | Limit |
|---|---|---|
| Frontmatter comes first | Any front-matter reader (Jekyll and its kin) | It must be the first thing in the file, valid YAML between triple-dashed lines |
| Required frontmatter fields | JSON Schema `required` | Checks presence only; key order cannot be checked, since objects are unordered |
| `type: ingredient` | JSON Schema `const` | |
| UI-only sections for UI ingredients | JSON Schema `if` / `then` / `else` | One schema applies the UI checks and skips them for infrastructure ingredients |
| Section order | JSON Schema `prefixItems` | Only once the sections are parsed into an ordered array |
| Heading list | markdownlint MD043 | Optional headings only as wildcards (`*`, `+`, `?`), never by name |
| Named optional sections, H1 equals the title | markdownlint custom rule, Vale `script` | Custom code |
| A required heading is present | Vale `occurrence` with `min` | |
| The document starts with an H1 | markdownlint MD041 | Does not compare the H1 with the front-matter `title` |
| One top-level heading | markdownlint MD025 | Treats a front-matter `title` as the H1, so by default flags the `# Title` after it |

## Examples

A States table for a toggle that can be hovered and selected:

```markdown
| State | Appearance change |
|-------|-------------------|
| Default | Track grey, thumb left |
| Hover | Track one step darker |
| Pressed | Thumb grows 10% |
| Selected | Track accent color, thumb right |
| Disabled | 40% opacity, no hover or press |
| Focused | 2pt focus ring outside the track |
```

Conformance test vectors with all three outcomes for one requirement:

```markdown
| ID | Requirements | Input | Expected |
|----|--------------|-------|----------|
| toggle-001 | must-announce-state | A screen reader focuses the toggle while it is on | "On" is announced: passed |
| toggle-002 | must-announce-state | The toggle announces nothing when focused | failed |
| toggle-003 | must-announce-state | The toggle is hidden from the accessibility tree by its container | inapplicable |
```

A Privacy section for a component that collects nothing:

```markdown
## Privacy

- **Data collected**: None
- **Storage**: None
- **Transmission**: No data leaves the device
- **Retention**: None
- **Encryption in transit**: Not applicable: nothing is transmitted
```

Event names that Firebase Analytics accepts:

```markdown
| Event | Properties | When |
|-------|------------|------|
| `toggle_viewed` | `{}` | Component appears on screen |
| `toggle_changed` | `{ value: boolean }` | User changes the toggle |
```

## What a reviewer looks for

- Frontmatter first, complete, `type: ingredient`, and the H1 equal to the `title`.
- Sections in the prescribed order, each present one under its specified heading and level, and none left empty without a one-line "none".
- An Overview that says what the component is, when to use it and when not to.
- Behavioral requirements that are named and carry RFC 2119 keywords, and test vectors that map to them, with passed, failed and inapplicable outcomes.
- Accessibility that covers role, label, state announcements, keyboard interaction and a target size per platform, not one value.
- States that include every state the component takes, hover and selected among them where they apply, with contrast holding in each.
- Platform specifics taken from the platform: verified https deep links, Firebase-valid event names, Apple's meaning for subsystem and category.
- Privacy that says what is collected, kept, transmitted and encrypted, even when the answer is none.
- Compliance rows linked by UUID, with `inapplicable` for a check that does not apply.
- A Change History row per version with ISO 8601 dates, and no released version edited in place.

## A complete review must establish

- Every MUST rule was checked against the ingredient, with no exception: `if-applicability`, `if-frontmatter-complete`, `if-type-field`, `if-title-heading`, `if-section-order`, `component-recipe-sections-in-order`, `if-overview`, `if-behavioral-requirements`, `if-appearance`, `if-states`, `if-accessibility`, `if-test-vectors`, `if-edge-cases`, `if-configuration`, `accessibility-options-include-text-size`, `tmpl-feature-flags-table`, `analytics-event-names-fit-platform-limits`, `if-logging`, `if-platform-notes`, `if-reference-implementations`, `if-design-decisions`, `if-compliance`, `if-change-history`, `released-version-immutable`
- Every SHOULD rule was checked, and each one the ingredient does not keep is named with the reason given: `tmpl-approval-fields`, `short-required-core-labelled-optional-rest`, `inapplicable-section-stated-not-omitted`, `overview-states-when-not-to-use`, `appearance-contrast-in-all-states`, `tmpl-states-table`, `states-include-hover-and-selected`, `accessibility-keyboard-interaction`, `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`, `tmpl-test-vector-id-format`, `test-vectors-cover-pass-fail-inapplicable`, `assumptions-and-limitations-stated`, `tmpl-deep-linking-patterns`, `deep-links-use-verified-https-links`, `tmpl-localization-table`, `tmpl-accessibility-options`, `tmpl-analytics-events`, `tmpl-privacy-fields`, `privacy-states-encryption-in-transit`, `tmpl-logging-subsystem-category`, `tmpl-platform-notes-platforms`, `tmpl-design-decisions-approved`, `tmpl-compliance-link-form`, `compliance-status-includes-inapplicable`, `change-history-iso-dates`
- Every MAY rule the ingredient uses is used as written: `informative-sections-labelled`, `section-structure-machine-checked`, `tmpl-appearance-properties`
- Each finding names the section it is in and the rule it breaks.

## A build must establish

- `if-applicability`: every file under `ingredients/` but `_template.md` has `type: ingredient`, and every file with that type is checked as an ingredient
- `if-frontmatter-complete`: the frontmatter holds every required field the conventions list, and no `domain` field
- `tmpl-approval-fields`: the frontmatter carries `approved-by` and `approved-date`, as the template does
- `if-type-field`: the `type` field is `ingredient`
- `if-title-heading`: the first H1 is the frontmatter `title`, exactly
- `if-section-order`: the sections appear in the 22-entry order, every section not marked MAY is present, and none is out of order
- `short-required-core-labelled-optional-rest`: every section is either in the required core or labelled optional, and each present section uses its specified heading and level
- `inapplicable-section-stated-not-omitted`: no section the ingredient carries is empty: each with nothing to say says so in one line
- `informative-sections-labelled`: any section marked non-normative states no requirement
- `section-structure-machine-checked`: any tool check of the structure (heading list, required headings, frontmatter schema, ordered sections) passes
- `component-recipe-sections-in-order`: a component recipe carries Overview, Behavioral Requirements, Appearance, States, Accessibility, Conformance Test Vectors and Edge Cases, in that order
- `if-overview`: `## Overview` says briefly what the component is and when to use it
- `overview-states-when-not-to-use`: `## Overview` also says when not to use the component, and why to use it
- `if-behavioral-requirements`: `## Behavioral Requirements` holds named, bold kebab-case requirements, each with an RFC 2119 keyword
- `if-appearance`: a UI ingredient's `## Appearance` defines corner radius, padding, font, background, foreground, border, shadow and size constraints
- `tmpl-appearance-properties`: any visual property `## Appearance` gives carries its value
- `appearance-contrast-in-all-states`: the colors given keep text at 4.5:1 and icons at 3:1 against their background in every interactive state
- `if-states`: a UI ingredient with interactive states has a `## States` table of its visual state changes
- `tmpl-states-table`: `## States` is a `| State | Appearance change |` table with a row for each state the component takes
- `states-include-hover-and-selected`: a component that can be hovered or selected has Hover and Selected rows
- `if-accessibility`: `## Accessibility` defines role/trait, label requirements, state change announcements and minimum tap target size, or says "not applicable" with a justification for an infrastructure ingredient
- `accessibility-keyboard-interaction`: `## Accessibility` describes the component's keyboard interaction
- `per-platform-target-sizes`: the minimum target size is given for each platform from that platform's own guidelines
- `tmpl-accessibility-min-tap-target`: `## Accessibility` holds the template's items: role/trait, label requirements, state-change announcements and a minimum tap target
- `if-test-vectors`: `## Conformance Test Vectors` is an ID, Requirements, Input, Expected table, each vector mapped to a named requirement
- `tmpl-test-vector-id-format`: every test vector has a unique ID in the `component-001` form and names the requirements it tests
- `test-vectors-cover-pass-fail-inapplicable`: each requirement has vectors expecting passed, failed and inapplicable
- `if-edge-cases`: `## Edge Cases` describes boundary conditions, error states and unexpected input
- `assumptions-and-limitations-stated`: `## Edge Cases` lists the known assumptions, limitations and exceptions, and what is out of scope and why
- `if-configuration`: `## Configuration` is an Option, Type, Default, Description table, or the note "This ingredient has no configurable options."
- `tmpl-deep-linking-patterns`: `## Deep Linking` is a Platform, URL Pattern table with Apple, Android and Web rows
- `deep-links-use-verified-https-links`: each deep link is a verified https link (universal link, App Link), or the ingredient says why not
- `tmpl-localization-table`: `## Localization` is a String Key, Default (en), Context table with each string's context
- `tmpl-accessibility-options`: `## Accessibility Options` is an Option, Behavior table covering Reduce Motion, Increase Contrast, Differentiate Without Color and, where offered, Dynamic Type
- `accessibility-options-include-text-size`: an ingredient that shows text says how its text resizes to 200 percent without loss of content or function
- `tmpl-feature-flags-table`: every flag in `## Feature Flags` has its key and its default value
- `tmpl-analytics-events`: `## Analytics` is an Event, Properties, When table
- `analytics-event-names-fit-platform-limits`: every event sent to Firebase Analytics has a name of letters, digits and underscores, starting with a letter, at most 40 characters
- `tmpl-privacy-fields`: `## Privacy` states Data collected, Storage, Transmission and Retention, and says so when nothing is collected
- `privacy-states-encryption-in-transit`: `## Privacy` says whether data leaving the device is encrypted in transit
- `if-logging`: `## Logging` defines subsystem, category and an Event, Level, Message table
- `tmpl-logging-subsystem-category`: any subsystem named is a large functional area and any category a specific area within it
- `if-platform-notes`: `## Platform Notes` gives per-platform guidance for SwiftUI, Compose and React/Web at least, or only the target platform of a single-platform ingredient
- `tmpl-platform-notes-platforms`: each targeted platform has an entry, and one with nothing to add says so
- `if-reference-implementations`: no authored `## Reference Implementations` section exists, and every implementation recorded in `index.json` exists unless `planned`
- `if-design-decisions`: `## Design Decisions` exists, each decision in the Decision, Rationale, Approved form
- `tmpl-design-decisions-approved`: each decision affecting visual or behavioral outcome is recorded and marked pending or approved by the user
- `if-compliance`: `## Compliance` is a Check, Status, Category table, each check linked to its definition
- `tmpl-compliance-link-form`: each compliance row links its check by UUID, `[adc.check.<document>.<check-name>](cookbook:<check-uuid>)`
- `compliance-status-includes-inapplicable`: a check that does not apply is reported `inapplicable`, not passed
- `if-change-history`: the file ends with a Version, Date, Author, Summary `## Change History` table
- `change-history-iso-dates`: every Change History date is ISO 8601
- `released-version-immutable`: no released version's contents were changed; every change is a new version

## Rationale

- `if-section-order`, `short-required-core-labelled-optional-rest`: specification style guides and design-system templates fix an order of named sections so readers and tools can navigate them, but RFC 7322 only strongly recommends its order inside the body, the RFC series and the ACT Rules Format require only a short core, and an experienced design-doc author warns that a template serves clarity, not the other way round.
- `inapplicable-section-stated-not-omitted`: IANA asks that a section with nothing to say be kept and say so, so that a later reader can tell a deliberate "none" from a section that was simply left out; Apple and Google Play do the same for platforms and data collection.
- `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`: the platforms disagree on the minimum target (Apple by platform, Android 48dp, Windows 40px, WCAG 24px at AA), so one value is wrong for most of them.
- `deep-links-use-verified-https-links`: Apple strongly recommends universal links over custom URL schemes, which are a potential attack vector; Android recommends App Links.
- `analytics-event-names-fit-platform-limits`: Firebase Analytics accepts only letters, digits and underscores in an event name, so a dotted name is invalid there.
- `test-vectors-cover-pass-fail-inapplicable`, `compliance-status-includes-inapplicable`: W3C's ACT and EARL outcome vocabularies include "inapplicable", so a check that cannot apply is not reported as a pass.
- `section-structure-machine-checked`: a structural check a tool can decide (headings, required fields, order) need not be left to a reader, though MD043 alone cannot name an optional heading.
- `released-version-immutable`: Semantic Versioning forbids changing a released version, so every reader of a version sees the same text.

## References

- [RFC 7322: RFC Style Guide](https://www.rfc-editor.org/rfc/rfc7322) (RFC Editor)
- [RFC 8126: Guidelines for Writing an IANA Considerations Section in RFCs](https://www.rfc-editor.org/rfc/rfc8126) (IETF)
- [RFC 3552: Guidelines for Writing RFC Text on Security Considerations](https://www.rfc-editor.org/rfc/rfc3552) (IETF)
- [QA Framework: Specification Guidelines](https://www.w3.org/TR/qaframe-spec/) (W3C)
- [Accessibility Conformance Testing (ACT) Rules Format 1.1](https://www.w3.org/TR/act-rules-format/) (W3C)
- [Evaluation and Report Language (EARL) 1.0 Schema](https://www.w3.org/TR/EARL10-Schema/) (W3C)
- [Test Assertions Guidelines Version 1.0 (Committee Note 02)](http://docs.oasis-open.org/tag/guidelines/v1.0/cn02/guidelines-v1.0-cn02.html) (OASIS)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) (semver.org)
- [RFC 9562: Universally Unique IDentifiers (UUIDs)](https://www.rfc-editor.org/rfc/rfc9562) (IETF)
- [MD043 - Required heading structure](https://github.com/DavidAnson/markdownlint/blob/main/doc/md043.md) (markdownlint (GitHub))
- [MD025 - Multiple top-level headings in the same document](https://github.com/DavidAnson/markdownlint/blob/main/doc/md025.md) (markdownlint (GitHub))
- [MD041 - First line in a file should be a top-level heading](https://github.com/DavidAnson/markdownlint/blob/main/doc/md041.md) (markdownlint (GitHub))
- [Custom Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md) (markdownlint (GitHub))
- [occurrence](https://docs.vale.sh/checks/occurrence.md) (Vale documentation (docs.vale.sh))
- [script](https://docs.vale.sh/checks/script.md) (Vale documentation (docs.vale.sh))
- [JSON Schema Validation: A Vocabulary for Structural Validation of JSON (draft 2020-12)](https://json-schema.org/draft/2020-12/json-schema-validation) (JSON Schema)
- [JSON Schema: A Media Type for Describing JSON Documents (draft 2020-12)](https://json-schema.org/draft/2020-12/json-schema-core) (JSON Schema)
- [ReSpec documentation](https://respec.org/docs/) (respec.org)
- [Front Matter](https://jekyllrb.com/docs/front-matter/) (jekyllrb.com)
- [Flag Evaluation API (OpenFeature specification)](https://github.com/open-feature/spec/blob/main/specification/sections/01-flag-evaluation.md) (open-feature/spec (GitHub))
- [PatternFly design guidelines (content design writing guide)](https://github.com/patternfly/patternfly-org/blob/main/packages/documentation-site/patternfly-docs/content/content-design/writing-guides/patternfly-design-guidelines.md) (patternfly-org (GitHub))
- [Component documentation template](https://docs.publishing.service.gov.uk/repos/govuk-design-guide/components/*component-documentation-template.html) (GOV.UK Developer Documentation)
- [Checkbox (Material Components for Android documentation)](https://github.com/material-components/material-components-android/blob/master/docs/components/Checkbox.md) (material-components-android (GitHub))
- [WidgetState enum](https://api.flutter.dev/flutter/widgets/WidgetState.html) (Flutter API documentation)
- [Accessibility - Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/accessibility) (Apple Developer)
- [Buttons - Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/buttons) (Apple Developer)
- [Typography - Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/typography) (Apple Developer)
- [Defining a custom URL scheme for your app](https://developer.apple.com/documentation/xcode/defining-a-custom-url-scheme-for-your-app) (Apple Developer Documentation)
- [Logger](https://developer.apple.com/documentation/os/logger) (Apple Developer Documentation)
- [App privacy details on the App Store](https://developer.apple.com/app-store/app-privacy-details/) (Apple Developer)
- [Make apps more accessible](https://developer.android.com/guide/topics/ui/accessibility/apps) (Android Developers)
- [Touch target size](https://support.google.com/accessibility/android/answer/7101858) (Android Accessibility Help)
- [About deep links](https://developer.android.com/training/app-links) (Android Developers)
- [Localize your app](https://developer.android.com/guide/topics/resources/localization) (Android Developers)
- [FirebaseAnalytics.Event](https://firebase.google.com/docs/reference/android/com/google/firebase/analytics/FirebaseAnalytics.Event) (Firebase)
- [Provide information for Google Play's Data safety section](https://support.google.com/googleplay/android-developer/answer/10787469) (Play Console Help)
- [Targeting - Windows apps](https://learn.microsoft.com/en-us/windows/apps/design/input/guidelines-for-targeting) (Microsoft Learn)
- [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/) (W3C)
- [Media Queries Level 5](https://www.w3.org/TR/mediaqueries-5/) (W3C)
- [Button Pattern (ARIA Authoring Practices Guide)](https://www.w3.org/WAI/ARIA/apg/patterns/button/) (W3C WAI)
- [Button usage - Fluent 2 Design System (React)](https://fluent2.microsoft.design/components/web/react/core/button/usage) (Fluent 2 Design System)
- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) (industrialempathy.com)
- [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) (Cognitect)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) (keepachangelog.com)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-21 | Mike Fullerton | Initial creation, from the ingredient-formatting research |
