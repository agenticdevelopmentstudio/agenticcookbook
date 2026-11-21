# Owner list: ingredient-formatting

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
- **tmpl-approval-fields** — verdict `unsupported` (claims: tmpl-approval-fields-prior, nygard-adr-status). Prior text, kept word for word: "the template's frontmatter carries two fields the draft's required list lacks: "approved-by: \"\"" and "approved-date: \"\""." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "An ingredient's frontmatter SHOULD carry the template's approval fields:" (the one change the reviewer accepts)
  - against: A decision record carries a status: proposed until the stakeholders agree, accepted after.
- **tmpl-accessibility-min-tap-target** — verdict `contradicted` (claims: tmpl-accessibility-min-tap-target-prior, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40, wcag-target-size-minimum-24). Prior text, kept word for word: ""- Role/trait (e.g., button, heading, text field)
- Label requirements
- Announce state changes (e.g., loading, disabled)
- Minimum tap target: 44×44pt"" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "An ingredient's `## Accessibility` section SHOULD hold the template's items:" (the one change the reviewer accepts)
  - against: Apple gives a default and a smaller minimum control size for each platform: iOS and iPadOS 44x44 pt default, 28x28 pt minimum; macOS 28 and 20; tvOS 66 and 56; visionOS 60 and 28; watchOS 44 and 28.
  - against: Android recommends touch targets of at least 48x48 dp.
  - against: Windows sets touch targets at about 7.5 mm square (40x40 pixels at 135 PPI and 1.0x scale).
  - against: WCAG 2.2's Level AA target size is 24 by 24 CSS pixels.
- **tmpl-deep-linking-patterns** — verdict `contradicted` (claims: tmpl-deep-linking-patterns-prior, apple-universal-links-recommended, apple-url-scheme-attack-vector). Prior text, kept word for word: ""| Platform | URL Pattern |" with rows "| Apple | `{{app_scheme}}://component-name` |", "| Android | `https://{{app_domain}}/component-name` |", "| Web | `/component-name` |"." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "An ingredient's `## Deep Linking` section SHOULD follow the template's table:" (the one change the reviewer accepts)
  - against: Apple accepts custom URL schemes for deep links but strongly recommends universal links.
  - against: Apple warns that a custom URL scheme is an attack vector into the app.
- **tmpl-analytics-events** — verdict `contradicted` (claims: tmpl-analytics-events-prior, firebase-event-name-charset). Prior text, kept word for word: ""| Event | Properties | When |" with rows "| `component_name.viewed` | `{}` | Component appears on screen |" and "| `component_name.interacted` | `{ action: string }` | User interacts with component |"." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "An ingredient's `## Analytics` section SHOULD follow the template's table:" (the one change the reviewer accepts)
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
