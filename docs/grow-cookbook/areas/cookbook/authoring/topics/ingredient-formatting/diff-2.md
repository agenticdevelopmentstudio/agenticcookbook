--- draft-1.md
+++ draft.md
@@ -10,7 +10,7 @@
 author: Mike Fullerton
 copyright: 2026 Mike Fullerton
 license: MIT
-summary: "How a cookbook ingredient is laid out: frontmatter, title, section order, what each section holds, and platform defaults for targets, links and events."
+summary: "How a cookbook ingredient is laid out: frontmatter, title, section order, what each section holds, and per-platform target sizes, deep links and event names."
 platforms: []
 tags:
   - cookbook
@@ -74,7 +74,7 @@
 
 # Ingredient Formatting
 
-An ingredient is a component spec laid out in one fixed order of named sections, from its frontmatter and title through Overview, Behavioral Requirements, Accessibility and Conformance Test Vectors to Compliance and Change History. Keep a short core of required sections and label the rest optional; when a section you carry has nothing to say, say so in one line; and take target sizes, deep links and analytics event names from each platform's own guidelines, not from one default.
+An ingredient is a component spec laid out in one fixed order of named sections, from its frontmatter and title through Overview, Behavioral Requirements, Accessibility and Conformance Test Vectors to Compliance and Change History. Label each section required or optional; when a section you carry has nothing to say, say so in one line; and take target sizes, deep links and analytics event names from each platform's own guidelines, not from one default.
 
 ## Rules
 
@@ -122,41 +122,54 @@
   20. `## Design Decisions`
   21. `## Compliance`
   22. `## Change History` (claim: if-section-order-prior)
-- **short-required-core-labelled-optional-rest**: The ingredient format SHOULD keep a short core of sections every ingredient carries and label each other section optional, so that every optional section can be found; a section that is present SHOULD use its specified heading and heading level. (claims: rfc-some-sections-required, rfc3552-security-section-required, rfc-security-considerations-required, act-required-items, act-optional-items, w3c-qa-label-optional-features, patternfly-template-omit-but-fixed-headings)
+- **short-required-core-labelled-optional-rest**: The ingredient format SHOULD label every section either required, carried by every ingredient, or optional, so that every optional section can be found: the required sections are those `if-section-order` does not mark "(MAY omit)" or "(MAY: …)", and the optional sections are those it marks. (claims: rfc-some-sections-required, rfc3552-security-section-required, rfc-security-considerations-required, act-required-items, act-optional-items, w3c-qa-label-optional-features)
+- **present-section-uses-specified-heading**: A section that is present SHOULD use its specified heading and heading level. (claim: patternfly-template-omit-but-fixed-headings)
 - **inapplicable-section-stated-not-omitted**: A section an ingredient carries that has nothing to say for it SHOULD say so in one line, as Apple's "No additional considerations for tvOS." does, rather than stand empty, so that a reader can tell a deliberate 'none' from an omission. This holds for the source, even where a published or rendered form drops the empty section, as the RFC Editor does at publication and GOV.UK's template does on its website. (claims: rfc-empty-iana-section-kept, rfc-editor-removes-empty-iana, govuk-template-empty-fields-hidden, rfc-no-actions-statement, w3c-qa-label-optional-features, apple-platform-considerations-none, play-form-even-if-no-data)
 - **informative-sections-labelled**: A section that states no requirements MAY be marked non-normative, with the line "This section is non-normative." (claim: respec-informative-marking)
-- **section-structure-machine-checked**: An ingredient's structure MAY be checked by a tool rather than by a reader: its headings against a fixed list (markdownlint's MD043), a required heading's absence (Vale's occurrence check), a missing required section or a section with no heading (as ReSpec lints a specification), and named optional sections, which MD043's wildcards cannot name, by a custom rule (markdownlint custom rules, Vale's script check); its frontmatter fields with JSON Schema's `required`, and its section order with `prefixItems` once the sections are parsed into an ordered array, since a schema cannot check the order of an object's keys. (claims: md043-enforces-heading-structure, md043-wildcards-only, markdownlint-custom-rules, vale-occurrence-min-flags-absence, vale-script-arbitrary-rules, respec-privsec-lint, respec-headingless-lint, json-schema-required-properties, json-schema-prefixitems-positional, json-schema-objects-unordered)
+- **section-structure-machine-checked**: An ingredient's structure MAY be checked by a tool rather than by a reader: its headings against a fixed list (markdownlint's MD043, whose wildcards `*`, `+` and `?` stand for unspecified headings), a required heading's absence (Vale's occurrence check), a missing required section or a section with no heading (as ReSpec lints a specification), and named optional sections by a custom rule (markdownlint custom rules, Vale's script check); its frontmatter fields with JSON Schema's `required`, and its section order with `prefixItems` once the sections are parsed into an ordered array, since a schema cannot check the order of an object's keys. (claims: md043-enforces-heading-structure, md043-wildcards-only, markdownlint-custom-rules, vale-occurrence-min-flags-absence, vale-script-arbitrary-rules, respec-privsec-lint, respec-headingless-lint, json-schema-required-properties, json-schema-prefixitems-positional, json-schema-objects-unordered)
+- **requirement-keywords-without-section-flagged**: A tool MAY warn when an ingredient uses RFC 2119 keywords but has no `## Behavioral Requirements` section, as ReSpec warns when RFC 2119 keywords are present but the conformance section is missing. (claim: respec-conformance-lint)
 - **component-recipe-sections-in-order**: - **must-contain-template-sections-in-order**: The recipe MUST contain all sections defined in the standard template, in the prescribed order.
     - For component recipes, the required sections in order are: **Overview**, **Behavioral Requirements**, **Appearance**, **States**, **Accessibility**, **Conformance Test Vectors**, **Edge Cases**. (claim: component-recipe-sections-in-order-prior)
 
 ### Overview and Behavioral Requirements
 
-- **if-overview**: The ingredient MUST have a `## Overview` section with a brief description of what the component is and when to use it.
-
-  **Applies when:** always. (claims: govuk-description-required, govuk-when-to-use)
-- **overview-states-when-not-to-use**: The `## Overview` SHOULD also say when not to use the component, and why to use it. (claims: govuk-when-not-to-use, patternfly-usage-when-to-use)
-- **if-behavioral-requirements**: The ingredient MUST have a `## Behavioral Requirements` section containing named requirements using RFC 2119 keywords. Requirements use kebab-case names in bold: `**must-do-something**: Component MUST ...`
-
-  **Applies when:** always. (claims: w3c-qa-conformance-clause, w3c-qa-consistent-requirement-style, w3c-qa-indicate-levels, oasis-ta-identifier, respec-conformance-lint)
+- **if-overview**: The ingredient MUST have a `## Overview` section with a brief description of what the component is.
+
+  **Applies when:** always. (claim: govuk-description-required)
+- **overview-states-when-to-use**: The `## Overview` SHOULD say when to use the component. (claims: govuk-when-to-use, patternfly-usage-when-to-use)
+- **overview-states-when-not-to-use**: The `## Overview` SHOULD say when not to use the component. (claim: govuk-when-not-to-use)
+- **overview-states-why-to-use**: The `## Overview` SHOULD say why the component should be used. (claim: patternfly-usage-when-to-use)
+- **if-behavioral-requirements**: The ingredient MUST have a `## Behavioral Requirements` section that states its conformance requirements.
+
+  **Applies when:** always. (claim: w3c-qa-conformance-clause)
+- **behavioral-requirements-keyword-levels**: Each requirement in `## Behavioral Requirements` MUST carry an RFC 2119 keyword that indicates whether it is mandatory (MUST), recommended (SHOULD) or optional (MAY). (claim: w3c-qa-indicate-levels)
+- **behavioral-requirements-one-style**: Every requirement in `## Behavioral Requirements` MUST be written in one consistent style that tells it apart from the section's other text. (claim: w3c-qa-consistent-requirement-style)
+- **behavioral-requirements-named**: Each requirement SHOULD carry a unique name in bold kebab-case, `**must-do-something**: Component MUST ...`, so that each test vector can map to the requirement it tests. (claims: oasis-ta-identifier, w3c-qa-consistent-requirement-style)
 
 ### Appearance and States
 
 - **if-appearance**: The ingredient MUST have a `## Appearance` section defining visual properties: corner radius, padding, font, background, foreground, border, shadow, and size constraints.
 
   **Applies when:** UI ingredients (components, panels, windows). MAY be omitted for infrastructure ingredients. (claim: if-appearance-prior)
-- **tmpl-appearance-properties**: An `## Appearance` section MAY give a value for each visual property the template lists: corner radius; padding (vertical × horizontal); font (weight, size); background (color value or description); foreground/text (color value or description); border (width, color, if any); shadow (offset, blur, color, if any); and min/max size (constraints, if any). (claims: material-attribute-table, fluent-contrast-in-all-states)
+- **tmpl-appearance-properties**: An `## Appearance` section MAY give a value for each visual property the template lists: corner radius; padding (vertical × horizontal); font (weight, size); background (color value or description); foreground/text (color value or description); border (width, color, if any); shadow (offset, blur, color, if any); and min/max size (constraints, if any). (claim: material-attribute-table)
 - **appearance-contrast-in-all-states**: The colors an `## Appearance` section gives SHOULD keep text at 4.5:1 and icons at 3:1 contrast against their background in every interactive state. (claim: fluent-contrast-in-all-states)
 - **if-states**: The ingredient MUST have a `## States` section with a table defining visual state changes (default, pressed, disabled, focused, loading, etc.).
 
   **Applies when:** UI ingredients with interactive states. MAY be omitted for infrastructure ingredients. (claim: if-states-prior)
-- **tmpl-states-table**: A `## States` section SHOULD be a table of `| State | Appearance change |` with a row for each state the component takes; the template's rows are Default, Pressed, Disabled, Focused and Loading. (claims: apple-press-state, flutter-interactive-states, material-states-list, wcag-name-role-value)
+- **tmpl-states-table**: A `## States` section SHOULD be a table of `| State | Appearance change |` with a row for each state the component takes; the template's rows are Default, Pressed, Disabled, Focused and Loading. (claims: apple-press-state, flutter-interactive-states, material-states-list)
 - **states-include-hover-and-selected**: A component that can be hovered or selected SHOULD have Hover and Selected rows in its `## States` table. (claims: flutter-interactive-states, flutter-hover-state, flutter-selected-state, material-states-list, fluent-rest-selected-states)
 
 ### Accessibility
 
-- **if-accessibility**: The ingredient MUST have a `## Accessibility` section defining: role/trait, label requirements, state change announcements, and minimum tap target size.
-
-  **Applies when:** always. Infrastructure ingredients define accessibility as "not applicable" with justification. (claims: wcag-name-role-value, apg-button-role, wcag-target-size-minimum-24, apple-strive-min-control-size, android-touch-target-48dp)
+- **if-accessibility**: The ingredient MUST have a `## Accessibility` section.
+
+  **Applies when:** always. (claim: wcag-name-role-value)
+- **accessibility-role**: The `## Accessibility` section MUST give the component's role or trait (for example, button, heading, text field), the role assistive technologies determine programmatically. (claim: wcag-name-role-value)
+- **accessibility-role-from-apg**: Where the ARIA Authoring Practices Guide has a pattern for the component, the role given SHOULD be the one that pattern states (a button has role `button`). (claim: apg-button-role)
+- **accessibility-label**: The `## Accessibility` section MUST state the component's label requirements: the name assistive technologies determine programmatically for it. (claim: wcag-name-role-value)
+- **accessibility-state-announcements**: The `## Accessibility` section MUST state how each change to the component's states (for example, loading, disabled) is notified to assistive technologies. (claim: wcag-name-role-value)
+- **accessibility-min-target-size**: The `## Accessibility` section SHOULD give the component's minimum target size. (claims: apple-strive-min-control-size, android-touch-target-48dp, wcag-target-size-minimum-24)
+- **accessibility-not-applicable-stated**: An infrastructure ingredient's `## Accessibility` section SHOULD say that accessibility is out of scope for it, and why, rather than stand empty. (claims: rfc3552-out-of-scope-stated, rfc-empty-iana-section-kept)
 - **accessibility-keyboard-interaction**: The `## Accessibility` section SHOULD describe the component's keyboard interaction, beside its role, states and properties. (claim: apg-keyboard-interaction-section)
 - **per-platform-target-sizes**: The minimum target size the `## Accessibility` section gives SHOULD be stated for each platform from that platform's own guidelines, not as one value: Apple's per-platform control sizes (default and minimum: iOS and iPadOS 44x44 pt and 28x28 pt; macOS 28 and 20; tvOS 66 and 56; visionOS 60 and 28; watchOS 44 and 28), with a button's hit region at least 44x44 pt (60x60 pt in visionOS); Android's 48x48 dp, 8 dp apart; Windows' 7.5 mm square (40x40 pixels at 135 PPI and 1.0x scale); and on the web WCAG 2.2's 24 by 24 CSS pixels at Level AA, 44 by 44 at Level AAA. (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, apple-button-hit-region-44, android-touch-target-48dp, android-touch-target-spacing, windows-touch-target-40, wcag-target-size-minimum-24, wcag-target-size-enhanced-44)
 - **tmpl-accessibility-min-tap-target**: An ingredient's `## Accessibility` section SHOULD hold the template's items: "- Role/trait (e.g., button, heading, text field)
@@ -166,15 +179,19 @@
 
 ### Conformance Test Vectors and Edge Cases
 
-- **if-test-vectors**: The ingredient MUST have a `## Conformance Test Vectors` section with a table containing columns: ID, Requirements, Input, Expected. Each test vector maps to one or more named requirements from `## Behavioral Requirements`.
-
-  **Applies when:** always. (claims: act-examples-pass-fail-inapplicable, oasis-ta-normative-source, oasis-ta-identifier, w3c-qa-test-assertions, w3c-qa-template-test-assertion-section)
-- **tmpl-test-vector-id-format**: Each test vector SHOULD carry a unique ID in the template's form, `component-001`, and name in its Requirements column the named requirements it tests (the template's `do-something`), in a table of `| ID | Requirements | Input | Expected |`. (claims: oasis-ta-identifier, w3c-qa-test-assertions)
-- **test-vectors-cover-pass-fail-inapplicable**: The `## Conformance Test Vectors` section SHOULD give each requirement vectors whose expected outcome is passed, failed and inapplicable, each pairing an input with the outcome expected for it. (claims: act-examples-pass-fail-inapplicable, act-outcome-types, w3c-qa-template-test-assertion-section)
+- **if-test-vectors**: The ingredient MUST have a `## Conformance Test Vectors` section whose vectors each pair an input with the outcome expected for it.
+
+  **Applies when:** always. (claim: act-examples-pass-fail-inapplicable)
+- **test-vectors-table**: The `## Conformance Test Vectors` SHOULD be a table of `| ID | Requirements | Input | Expected |`: each vector's identifier, the requirements it tests, its input and its expected outcome. (claims: oasis-ta-identifier, oasis-ta-normative-source, act-examples-pass-fail-inapplicable)
+- **tmpl-test-vector-id-format**: Each test vector SHOULD carry a unique ID in the template's form, `component-001`. (claim: oasis-ta-identifier)
+- **test-vectors-map-to-requirements**: Each test vector SHOULD name, in its Requirements column, the named requirements of `## Behavioral Requirements` it tests (the template's `do-something`). (claims: oasis-ta-normative-source, w3c-qa-test-assertions)
+- **test-vectors-cover-pass-fail-inapplicable**: The `## Conformance Test Vectors` section SHOULD give each requirement vectors whose expected outcome is passed, failed and inapplicable. (claims: act-examples-pass-fail-inapplicable, act-outcome-types)
+- **template-carries-test-vectors**: The ingredient template, `_template.md`, SHOULD carry a `## Conformance Test Vectors` section, so that each new ingredient starts with a place for its test vectors. (claim: w3c-qa-template-test-assertion-section)
 - **if-edge-cases**: The ingredient MUST have a `## Edge Cases` section describing boundary conditions, error states, and unexpected input scenarios.
 
   **Applies when:** always. (claim: if-edge-cases-prior)
-- **assumptions-and-limitations-stated**: The `## Edge Cases` section SHOULD also list the ingredient's known assumptions, limitations and exceptions, and say which cases are out of scope and why. (claims: act-assumptions-listed, rfc3552-out-of-scope-stated)
+- **assumptions-and-limitations-stated**: The `## Edge Cases` section SHOULD also list the ingredient's known assumptions, limitations and exceptions. (claim: act-assumptions-listed)
+- **out-of-scope-cases-stated**: The `## Edge Cases` section SHOULD say which cases are out of scope, and why. (claim: rfc3552-out-of-scope-stated)
 
 ### Configuration and the optional sections
 
@@ -185,11 +202,12 @@
 - **deep-links-use-verified-https-links**: The deep links a `## Deep Linking` section defines SHOULD be verified https links: universal links on Apple platforms and App Links on Android. Apple accepts a custom URL scheme but strongly recommends universal links, and a custom URL scheme is a potential attack vector into the app. (claims: apple-universal-links-recommended, android-app-links-recommended, apple-url-scheme-attack-vector)
 - **tmpl-localization-table**: A `## Localization` section SHOULD list each string in a table of `| String Key | Default (en) | Context |`, its Context describing where the string is used, for the translator. (claim: android-string-context)
 - **tmpl-accessibility-options**: An `## Accessibility Options` section SHOULD document which accessibility display options the component responds to, in a table of `| Option | Behavior |` with rows for Reduce Motion (fewer automatic and repetitive animations, and motion triggered by interaction can be disabled unless it is essential), Increase Contrast (a higher-contrast color scheme), Differentiate Without Color (information conveyed by more than color alone) and, on Apple platforms that offer it, Dynamic Type (text the person resizes); on the web, Reduce Motion and Increase Contrast are read with the `prefers-reduced-motion` and `prefers-contrast` media features. (claims: apple-reduce-motion, apple-increase-contrast, apple-more-than-color, wcag-use-of-color, apple-dynamic-type, mq5-prefers-reduced-motion, mq5-prefers-contrast, wcag-animation-from-interactions)
-- **accessibility-options-include-text-size**: An ingredient that shows text MUST say, in `## Accessibility Options`, how its text resizes up to 200 percent without loss of content or function (WCAG Level AA). (claim: wcag-resize-text)
-- **tmpl-feature-flags-table**: A `## Feature Flags` section MUST give each flag its key and its default value, in a table of `| Flag Key | Default | Description |` (the template's row: `{{app_prefix}}.component_name`, `true`, Enables this component). (claim: openfeature-flag-key-and-default)
+- **accessibility-options-include-text-size**: An ingredient that shows text MUST state in `## Accessibility Options` how its text resizes up to 200 percent without loss of content or function (WCAG Level AA), so that section, which `if-section-order` lets other ingredients omit, is present in it. (claim: wcag-resize-text)
+- **tmpl-feature-flags-table**: A `## Feature Flags` section MUST give each flag its key and its default value. (claim: openfeature-flag-key-and-default)
 - **tmpl-analytics-events**: An ingredient's `## Analytics` section SHOULD follow the template's table: "| Event | Properties | When |" with rows "| `component_name.viewed` | `{}` | Component appears on screen |" and "| `component_name.interacted` | `{ action: string }` | User interacts with component |". (claim: tmpl-analytics-events-prior)
 - **analytics-event-names-fit-platform-limits**: Where an ingredient's analytics events are sent to Firebase Analytics, each event name MUST hold only letters, digits and underscores, start with a letter and run to at most 40 characters. (claim: firebase-event-name-charset)
-- **tmpl-privacy-fields**: A `## Privacy` section SHOULD state **Data collected** (None, or what is collected), **Storage** (where and how data is stored), **Transmission** (whether data leaves the device) and **Retention** (how long data is kept), and an ingredient that collects nothing says so. Transmission and Retention together say whether data is collected: sent off the device and kept longer than servicing the request in real time needs, rather than processed ephemerally, in memory only. (claims: apple-collect-definition, play-ephemeral-processing, play-form-even-if-no-data)
+- **tmpl-privacy-fields**: A `## Privacy` section SHOULD state **Data collected** (None, or what is collected), **Storage** (where and how data is stored), **Transmission** (whether data leaves the device) and **Retention** (how long data is kept), so that a reader can tell whether data is collected: sent off the device and kept longer than servicing the request in real time needs, rather than processed ephemerally, in memory only. (claims: apple-collect-definition, play-ephemeral-processing)
+- **privacy-states-none-collected**: The `## Privacy` section of an ingredient that collects no data SHOULD say that no data is collected. (claim: play-form-even-if-no-data)
 - **privacy-states-encryption-in-transit**: A `## Privacy` section SHOULD also say whether data that leaves the device is encrypted in transit. (claim: play-encryption-in-transit)
 
 ### Logging, Platform Notes and Reference Implementations
@@ -197,11 +215,12 @@
 - **if-logging**: The ingredient MUST have a `## Logging` section defining: subsystem, category, and a table of log events with columns: Event, Level, Message.
 
   **Applies when:** always. (claim: if-logging-prior)
-- **tmpl-logging-subsystem-category**: Where the `## Logging` section names a subsystem and a category (both optional on Apple's Logger), they SHOULD carry Apple's meaning: the subsystem a large functional area of the app, the category a specific area within it (the template's `{{bundle_id}}` and `ComponentName`); its log events are a table of `| Event | Level | Message |` (the template's row: `debug`, `ComponentName: `). (claims: apple-logger-subsystem-category, apple-logger-optional)
+- **tmpl-logging-subsystem-category**: Where the `## Logging` section names a subsystem and a category (both optional on Apple's Logger), they SHOULD carry Apple's meaning: the subsystem a large functional area of the app, the category a specific area within it (the template's `{{bundle_id}}` and `ComponentName`). (claims: apple-logger-subsystem-category, apple-logger-optional)
 - **if-platform-notes**: The ingredient MUST have a `## Platform Notes` section with per-platform implementation guidance. At minimum: SwiftUI, Compose, React/Web.
 
   **Applies when:** always. Single-platform ingredients list only the target platform. (claim: if-platform-notes-prior)
-- **tmpl-platform-notes-platforms**: `## Platform Notes` SHOULD carry an entry for each platform the ingredient targets among those the template lists (SwiftUI, Compose, React/Web, AppKit / UIKit, WinUI 3), since each platform's own guidelines differ (Apple, Android and Windows each set their own control and touch-target sizes); a platform with nothing to add says so ("No additional considerations for tvOS."). (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40, apple-platform-considerations-none)
+- **tmpl-platform-notes-platforms**: `## Platform Notes` SHOULD carry an entry for each platform the ingredient targets among those the template lists (SwiftUI, Compose, React/Web, AppKit / UIKit, WinUI 3), since each platform's own guidelines differ (Apple, Android and Windows each set their own control and touch-target sizes). (claims: apple-strive-min-control-size, apple-min-control-size-per-platform, android-touch-target-48dp, windows-touch-target-40)
+- **platform-notes-none-stated**: A platform in `## Platform Notes` with nothing to add SHOULD say so in one line, as Apple's "No additional considerations for tvOS." does. (claim: apple-platform-considerations-none)
 - **if-reference-implementations**: The ingredient MUST NOT carry an authored `## Reference Implementations` section. The code that implements it is recorded in its cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>` (`--remove <location>` drops a row), and `cookr confirm <uuid|rdid>` records it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section after `## Platform Notes`. `platform` is one of `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`; a location is a repo-relative file, a directory ending with `/` (which claims every source file below it), or a URL. Every recorded location MUST exist, unless the row is `planned`.
 
   **Applies when:** the repo's `.cookr.json` declares `roots` (a cookbook that lives beside its source). `cookr validate` checks that every recorded location exists. (claim: if-reference-implementations-prior)
@@ -211,7 +230,7 @@
 - **if-design-decisions**: The ingredient MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.
 
   **Applies when:** always. New ingredients start with an empty section; decisions are added as they arise. (claim: if-design-decisions-prior)
-- **tmpl-design-decisions-approved**: Each decision made during implementation that affects visual or behavioral outcome SHOULD be recorded in `## Design Decisions`, and each SHOULD be approved by the user: pending (proposed) until the user agrees, then yes (accepted). (claim: nygard-adr-status)
+- **tmpl-design-decisions-approved**: Each decision in `## Design Decisions` SHOULD carry its status: pending (proposed) until its stakeholders agree, then yes (accepted). (claim: nygard-adr-status)
 - **if-compliance**: The ingredient MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.
 
   **Applies when:** always. (claim: if-compliance-prior)
@@ -230,6 +249,7 @@
 
 - Write one line that names what is absent, in the section itself: "No additional considerations for tvOS." (Apple's per-platform sections), "This ingredient has no configurable options." (`## Configuration`), or, in `## Privacy`, that no user data is collected or shared (Google Play's Data safety form).
 - Name every targeted platform in `## Platform Notes`, and give the line to a platform with nothing extra, so a reader sees it was considered.
+- For an infrastructure ingredient, say in `## Accessibility` that accessibility is out of scope for it and why, for example "Not applicable: this ingredient has no user interface; it is a background sync service."
 - A line is not a heading with nothing under it: an empty section reads as an omission.
 
 ## Checking the structure with a tool
@@ -241,9 +261,10 @@
 | `type: ingredient` | JSON Schema `const` | |
 | UI-only sections for UI ingredients | JSON Schema `if` / `then` / `else` | One schema applies the UI checks and skips them for infrastructure ingredients |
 | Section order | JSON Schema `prefixItems` | Only once the sections are parsed into an ordered array |
-| Heading list | markdownlint MD043 | Optional headings only as wildcards (`*`, `+`, `?`), never by name |
+| Heading list | markdownlint MD043 | Unspecified headings as wildcards: `*` zero or more, `+` one or more, `?` exactly one |
 | Named optional sections, H1 equals the title | markdownlint custom rule, Vale `script` | Custom code |
 | A required heading is present | Vale `occurrence` with `min` | |
+| RFC 2119 keywords with no `## Behavioral Requirements` | A custom rule, as ReSpec does for a conformance section | |
 | The document starts with an H1 | markdownlint MD041 | Does not compare the H1 with the front-matter `title` |
 | One top-level heading | markdownlint MD025 | Treats a front-matter `title` as the H1, so by default flags the `# Title` after it |
 
@@ -272,6 +293,14 @@
 | toggle-003 | must-announce-state | The toggle is hidden from the accessibility tree by its container | inapplicable |
 ```
 
+A Feature Flags section, in the template's table, each flag with its key and its default:
+
+```markdown
+| Flag Key | Default | Description |
+|----------|---------|-------------|
+| `{{app_prefix}}.component_name` | `true` | Enables this component |
+```
+
 A Privacy section for a component that collects nothing:
 
 ```markdown
@@ -293,76 +322,103 @@
 | `toggle_changed` | `{ value: boolean }` | User changes the toggle |
 ```
 
+A Design Decisions entry with its status:
+
+```markdown
+- **Decision**: The toggle animates its thumb over 150 ms. **Rationale**: Matches the platform switch. **Approved**: pending
+```
+
 ## What a reviewer looks for
 
 - Frontmatter first, complete, `type: ingredient`, and the H1 equal to the `title`.
 - Sections in the prescribed order, each present one under its specified heading and level, and none left empty without a one-line "none".
-- An Overview that says what the component is, when to use it and when not to.
-- Behavioral requirements that are named and carry RFC 2119 keywords, and test vectors that map to them, with passed, failed and inapplicable outcomes.
-- Accessibility that covers role, label, state announcements, keyboard interaction and a target size per platform, not one value.
+- An Overview that says what the component is, when to use it, when not to and why to.
+- Behavioral requirements in one style, each named and carrying the RFC 2119 keyword of its level, and test vectors that pair an input with its outcome, name the requirements they test, and cover passed, failed and inapplicable.
+- Accessibility that gives role, label, how state changes are announced, keyboard interaction and a target size per platform, not one value; and, for an infrastructure ingredient, why accessibility is out of scope.
 - States that include every state the component takes, hover and selected among them where they apply, with contrast holding in each.
-- Platform specifics taken from the platform: verified https deep links, Firebase-valid event names, Apple's meaning for subsystem and category.
+- An ingredient that shows text carrying `## Accessibility Options` with its 200 percent text resizing.
+- Edge cases that list assumptions, limitations and exceptions, and what is out of scope and why.
+- Platform specifics taken from the platform: verified https deep links, Firebase-valid event names, Apple's meaning for subsystem and category, an entry per targeted platform.
 - Privacy that says what is collected, kept, transmitted and encrypted, even when the answer is none.
-- Compliance rows linked by UUID, with `inapplicable` for a check that does not apply.
+- Design decisions that carry their status; compliance rows linked by UUID, with `inapplicable` for a check that does not apply.
 - A Change History row per version with ISO 8601 dates, and no released version edited in place.
 
 ## A complete review must establish
 
-- Every MUST rule was checked against the ingredient, with no exception: `if-applicability`, `if-frontmatter-complete`, `if-type-field`, `if-title-heading`, `if-section-order`, `component-recipe-sections-in-order`, `if-overview`, `if-behavioral-requirements`, `if-appearance`, `if-states`, `if-accessibility`, `if-test-vectors`, `if-edge-cases`, `if-configuration`, `accessibility-options-include-text-size`, `tmpl-feature-flags-table`, `analytics-event-names-fit-platform-limits`, `if-logging`, `if-platform-notes`, `if-reference-implementations`, `if-design-decisions`, `if-compliance`, `if-change-history`, `released-version-immutable`
-- Every SHOULD rule was checked, and each one the ingredient does not keep is named with the reason given: `tmpl-approval-fields`, `short-required-core-labelled-optional-rest`, `inapplicable-section-stated-not-omitted`, `overview-states-when-not-to-use`, `appearance-contrast-in-all-states`, `tmpl-states-table`, `states-include-hover-and-selected`, `accessibility-keyboard-interaction`, `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`, `tmpl-test-vector-id-format`, `test-vectors-cover-pass-fail-inapplicable`, `assumptions-and-limitations-stated`, `tmpl-deep-linking-patterns`, `deep-links-use-verified-https-links`, `tmpl-localization-table`, `tmpl-accessibility-options`, `tmpl-analytics-events`, `tmpl-privacy-fields`, `privacy-states-encryption-in-transit`, `tmpl-logging-subsystem-category`, `tmpl-platform-notes-platforms`, `tmpl-design-decisions-approved`, `tmpl-compliance-link-form`, `compliance-status-includes-inapplicable`, `change-history-iso-dates`
-- Every MAY rule the ingredient uses is used as written: `informative-sections-labelled`, `section-structure-machine-checked`, `tmpl-appearance-properties`
+- Every MUST rule was checked against the ingredient, with no exception: `if-applicability`, `if-frontmatter-complete`, `if-type-field`, `if-title-heading`, `if-section-order`, `component-recipe-sections-in-order`, `if-overview`, `if-behavioral-requirements`, `behavioral-requirements-keyword-levels`, `behavioral-requirements-one-style`, `if-appearance`, `if-states`, `if-accessibility`, `accessibility-role`, `accessibility-label`, `accessibility-state-announcements`, `if-test-vectors`, `if-edge-cases`, `if-configuration`, `accessibility-options-include-text-size`, `tmpl-feature-flags-table`, `analytics-event-names-fit-platform-limits`, `if-logging`, `if-platform-notes`, `if-reference-implementations`, `if-design-decisions`, `if-compliance`, `if-change-history`, `released-version-immutable`
+- Every SHOULD rule was checked, and each one the ingredient does not keep is named with the reason given: `tmpl-approval-fields`, `short-required-core-labelled-optional-rest`, `present-section-uses-specified-heading`, `inapplicable-section-stated-not-omitted`, `overview-states-when-to-use`, `overview-states-when-not-to-use`, `overview-states-why-to-use`, `behavioral-requirements-named`, `appearance-contrast-in-all-states`, `tmpl-states-table`, `states-include-hover-and-selected`, `accessibility-role-from-apg`, `accessibility-min-target-size`, `accessibility-not-applicable-stated`, `accessibility-keyboard-interaction`, `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`, `test-vectors-table`, `tmpl-test-vector-id-format`, `test-vectors-map-to-requirements`, `test-vectors-cover-pass-fail-inapplicable`, `template-carries-test-vectors`, `assumptions-and-limitations-stated`, `out-of-scope-cases-stated`, `tmpl-deep-linking-patterns`, `deep-links-use-verified-https-links`, `tmpl-localization-table`, `tmpl-accessibility-options`, `tmpl-analytics-events`, `tmpl-privacy-fields`, `privacy-states-none-collected`, `privacy-states-encryption-in-transit`, `tmpl-logging-subsystem-category`, `tmpl-platform-notes-platforms`, `platform-notes-none-stated`, `tmpl-design-decisions-approved`, `tmpl-compliance-link-form`, `compliance-status-includes-inapplicable`, `change-history-iso-dates`
+- Every MAY rule the ingredient uses is used as written: `informative-sections-labelled`, `section-structure-machine-checked`, `requirement-keywords-without-section-flagged`, `tmpl-appearance-properties`
 - Each finding names the section it is in and the rule it breaks.
 
 ## A build must establish
 
 - `if-applicability`: every file under `ingredients/` but `_template.md` has `type: ingredient`, and every file with that type is checked as an ingredient
 - `if-frontmatter-complete`: the frontmatter holds every required field the conventions list, and no `domain` field
-- `tmpl-approval-fields`: the frontmatter carries `approved-by` and `approved-date`, as the template does
+- `tmpl-approval-fields`: the frontmatter carries `approved-by: ""` and `approved-date: ""`, as the template does
 - `if-type-field`: the `type` field is `ingredient`
 - `if-title-heading`: the first H1 is the frontmatter `title`, exactly
 - `if-section-order`: the sections appear in the 22-entry order, every section not marked MAY is present, and none is out of order
-- `short-required-core-labelled-optional-rest`: every section is either in the required core or labelled optional, and each present section uses its specified heading and level
+- `short-required-core-labelled-optional-rest`: every section of the format is either required (unmarked in `if-section-order`) or labelled optional (marked MAY there)
+- `present-section-uses-specified-heading`: each present section uses its specified heading and heading level
 - `inapplicable-section-stated-not-omitted`: no section the ingredient carries is empty: each with nothing to say says so in one line
 - `informative-sections-labelled`: any section marked non-normative states no requirement
 - `section-structure-machine-checked`: any tool check of the structure (heading list, required headings, frontmatter schema, ordered sections) passes
+- `requirement-keywords-without-section-flagged`: any tool check for RFC 2119 keywords without a `## Behavioral Requirements` section passes
 - `component-recipe-sections-in-order`: a component recipe carries Overview, Behavioral Requirements, Appearance, States, Accessibility, Conformance Test Vectors and Edge Cases, in that order
-- `if-overview`: `## Overview` says briefly what the component is and when to use it
-- `overview-states-when-not-to-use`: `## Overview` also says when not to use the component, and why to use it
-- `if-behavioral-requirements`: `## Behavioral Requirements` holds named, bold kebab-case requirements, each with an RFC 2119 keyword
+- `if-overview`: `## Overview` describes briefly what the component is
+- `overview-states-when-to-use`: `## Overview` says when to use the component
+- `overview-states-when-not-to-use`: `## Overview` says when not to use the component
+- `overview-states-why-to-use`: `## Overview` says why the component should be used
+- `if-behavioral-requirements`: a `## Behavioral Requirements` section states the ingredient's conformance requirements
+- `behavioral-requirements-keyword-levels`: every requirement carries an RFC 2119 keyword giving its level: MUST, SHOULD or MAY
+- `behavioral-requirements-one-style`: every requirement is written in the same style, set apart from the section's other text
+- `behavioral-requirements-named`: every requirement carries a unique bold kebab-case name
 - `if-appearance`: a UI ingredient's `## Appearance` defines corner radius, padding, font, background, foreground, border, shadow and size constraints
 - `tmpl-appearance-properties`: any visual property `## Appearance` gives carries its value
 - `appearance-contrast-in-all-states`: the colors given keep text at 4.5:1 and icons at 3:1 against their background in every interactive state
-- `if-states`: a UI ingredient with interactive states has a `## States` table of its visual state changes
+- `if-states`: a UI ingredient with interactive states has a `## States` table defining its visual state changes (default, pressed, disabled, focused, loading, etc.)
 - `tmpl-states-table`: `## States` is a `| State | Appearance change |` table with a row for each state the component takes
 - `states-include-hover-and-selected`: a component that can be hovered or selected has Hover and Selected rows
-- `if-accessibility`: `## Accessibility` defines role/trait, label requirements, state change announcements and minimum tap target size, or says "not applicable" with a justification for an infrastructure ingredient
+- `if-accessibility`: a `## Accessibility` section is present
+- `accessibility-role`: `## Accessibility` gives the component's role or trait
+- `accessibility-role-from-apg`: where APG has a pattern for the component, the role given is that pattern's
+- `accessibility-label`: `## Accessibility` states the component's label requirements
+- `accessibility-state-announcements`: `## Accessibility` states how each change to the component's states is notified to assistive technologies
+- `accessibility-min-target-size`: `## Accessibility` gives a minimum target size
+- `accessibility-not-applicable-stated`: an infrastructure ingredient's `## Accessibility` says accessibility is out of scope for it, and why
 - `accessibility-keyboard-interaction`: `## Accessibility` describes the component's keyboard interaction
 - `per-platform-target-sizes`: the minimum target size is given for each platform from that platform's own guidelines
-- `tmpl-accessibility-min-tap-target`: `## Accessibility` holds the template's items: role/trait, label requirements, state-change announcements and a minimum tap target
-- `if-test-vectors`: `## Conformance Test Vectors` is an ID, Requirements, Input, Expected table, each vector mapped to a named requirement
-- `tmpl-test-vector-id-format`: every test vector has a unique ID in the `component-001` form and names the requirements it tests
+- `tmpl-accessibility-min-tap-target`: `## Accessibility` holds the template's items: role/trait, label requirements, announced state changes and a minimum tap target of 44×44pt
+- `if-test-vectors`: `## Conformance Test Vectors` is present, each vector pairing an input with its expected outcome
+- `test-vectors-table`: the vectors are a `| ID | Requirements | Input | Expected |` table
+- `tmpl-test-vector-id-format`: every test vector has a unique ID in the `component-001` form
+- `test-vectors-map-to-requirements`: every test vector names in its Requirements column the named requirements it tests
 - `test-vectors-cover-pass-fail-inapplicable`: each requirement has vectors expecting passed, failed and inapplicable
+- `template-carries-test-vectors`: `_template.md` carries a `## Conformance Test Vectors` section
 - `if-edge-cases`: `## Edge Cases` describes boundary conditions, error states and unexpected input
-- `assumptions-and-limitations-stated`: `## Edge Cases` lists the known assumptions, limitations and exceptions, and what is out of scope and why
+- `assumptions-and-limitations-stated`: `## Edge Cases` lists the known assumptions, limitations and exceptions
+- `out-of-scope-cases-stated`: `## Edge Cases` says which cases are out of scope, and why
 - `if-configuration`: `## Configuration` is an Option, Type, Default, Description table, or the note "This ingredient has no configurable options."
-- `tmpl-deep-linking-patterns`: `## Deep Linking` is a Platform, URL Pattern table with Apple, Android and Web rows
-- `deep-links-use-verified-https-links`: each deep link is a verified https link (universal link, App Link), or the ingredient says why not
+- `tmpl-deep-linking-patterns`: `## Deep Linking` is a Platform, URL Pattern table with the template's rows: Apple `{{app_scheme}}://component-name`, Android `https://{{app_domain}}/component-name` and Web `/component-name`
+- `deep-links-use-verified-https-links`: each deep link is a verified https link (a universal link on Apple platforms, an App Link on Android)
 - `tmpl-localization-table`: `## Localization` is a String Key, Default (en), Context table with each string's context
 - `tmpl-accessibility-options`: `## Accessibility Options` is an Option, Behavior table covering Reduce Motion, Increase Contrast, Differentiate Without Color and, where offered, Dynamic Type
-- `accessibility-options-include-text-size`: an ingredient that shows text says how its text resizes to 200 percent without loss of content or function
+- `accessibility-options-include-text-size`: an ingredient that shows text carries `## Accessibility Options`, and it says how the text resizes to 200 percent without loss of content or function
 - `tmpl-feature-flags-table`: every flag in `## Feature Flags` has its key and its default value
-- `tmpl-analytics-events`: `## Analytics` is an Event, Properties, When table
+- `tmpl-analytics-events`: `## Analytics` is an Event, Properties, When table with the template's rows: `component_name.viewed` (`{}`, Component appears on screen) and `component_name.interacted` (`{ action: string }`, User interacts with component)
 - `analytics-event-names-fit-platform-limits`: every event sent to Firebase Analytics has a name of letters, digits and underscores, starting with a letter, at most 40 characters
-- `tmpl-privacy-fields`: `## Privacy` states Data collected, Storage, Transmission and Retention, and says so when nothing is collected
+- `tmpl-privacy-fields`: `## Privacy` states Data collected, Storage, Transmission and Retention
+- `privacy-states-none-collected`: the `## Privacy` of an ingredient that collects no data says that none is collected
 - `privacy-states-encryption-in-transit`: `## Privacy` says whether data leaving the device is encrypted in transit
 - `if-logging`: `## Logging` defines subsystem, category and an Event, Level, Message table
 - `tmpl-logging-subsystem-category`: any subsystem named is a large functional area and any category a specific area within it
 - `if-platform-notes`: `## Platform Notes` gives per-platform guidance for SwiftUI, Compose and React/Web at least, or only the target platform of a single-platform ingredient
-- `tmpl-platform-notes-platforms`: each targeted platform has an entry, and one with nothing to add says so
+- `tmpl-platform-notes-platforms`: each targeted platform the template lists has an entry
+- `platform-notes-none-stated`: a platform with nothing to add says so in one line
 - `if-reference-implementations`: no authored `## Reference Implementations` section exists, and every implementation recorded in `index.json` exists unless `planned`
-- `if-design-decisions`: `## Design Decisions` exists, each decision in the Decision, Rationale, Approved form
-- `tmpl-design-decisions-approved`: each decision affecting visual or behavioral outcome is recorded and marked pending or approved by the user
-- `if-compliance`: `## Compliance` is a Check, Status, Category table, each check linked to its definition
+- `if-design-decisions`: `## Design Decisions` exists, each decision in the form **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending
+- `tmpl-design-decisions-approved`: each decision carries its status: pending until its stakeholders agree, then yes
+- `if-compliance`: `## Compliance` is a Check, Status, Category table, its status values `passed`, `failed`, `partial`, each check linked to its definition in the relevant compliance category file
 - `tmpl-compliance-link-form`: each compliance row links its check by UUID, `[adc.check.<document>.<check-name>](cookbook:<check-uuid>)`
 - `compliance-status-includes-inapplicable`: a check that does not apply is reported `inapplicable`, not passed
 - `if-change-history`: the file ends with a Version, Date, Author, Summary `## Change History` table
@@ -371,13 +427,32 @@
 
 ## Rationale
 
-- `if-section-order`, `short-required-core-labelled-optional-rest`: specification style guides and design-system templates fix an order of named sections so readers and tools can navigate them, but RFC 7322 only strongly recommends its order inside the body, the RFC series and the ACT Rules Format require only a short core, and an experienced design-doc author warns that a template serves clarity, not the other way round.
-- `inapplicable-section-stated-not-omitted`: IANA asks that a section with nothing to say be kept and say so, so that a later reader can tell a deliberate "none" from a section that was simply left out; Apple and Google Play do the same for platforms and data collection.
-- `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`: the platforms disagree on the minimum target (Apple by platform, Android 48dp, Windows 40px, WCAG 24px at AA), so one value is wrong for most of them.
-- `deep-links-use-verified-https-links`: Apple strongly recommends universal links over custom URL schemes, which are a potential attack vector; Android recommends App Links.
-- `analytics-event-names-fit-platform-limits`: Firebase Analytics accepts only letters, digits and underscores in an event name, so a dotted name is invalid there.
-- `test-vectors-cover-pass-fail-inapplicable`, `compliance-status-includes-inapplicable`: W3C's ACT and EARL outcome vocabularies include "inapplicable", so a check that cannot apply is not reported as a pass.
-- `section-structure-machine-checked`: a structural check a tool can decide (headings, required fields, order) need not be left to a reader, though MD043 alone cannot name an optional heading.
+- `if-section-order`, `short-required-core-labelled-optional-rest`: specification style guides and design-system templates fix an order of named sections so readers and tools can navigate them, but RFC 7322 only strongly recommends its order inside the body, the RFC series and the ACT Rules Format require only some of their sections and label the rest optional, and an experienced design-doc author warns that a template serves clarity, not the other way round. Labelling each section required or optional lets a reader find every optional one, as W3C asks of optional features; it is a SHOULD because the sources recommend it for their own formats rather than require it of every template.
+- `present-section-uses-specified-heading`: PatternFly fixes each section's heading and level so information sits in consistently named sections; a renamed heading hides the section from readers and from heading checks. SHOULD, since only one design system's template states it.
+- `inapplicable-section-stated-not-omitted`, `accessibility-not-applicable-stated`, `platform-notes-none-stated`, `privacy-states-none-collected`: IANA asks that a section with nothing to say be kept and say so, so that a later reader can tell a deliberate "none" from a section that was simply left out; Apple does the same for a platform with nothing extra and Google Play for an app that collects no data. They are SHOULD because GOV.UK and the RFC Editor drop such sections from what they publish, so the practice is one of drafting, not of every rendered form.
+- `accessibility-not-applicable-stated`, `out-of-scope-cases-stated`: RFC 3552 requires its authors to say what is out of scope and why, so a reader knows the gap was a decision; SHOULD here, since that requirement is the IETF's for its security sections.
+- `overview-states-when-to-use`, `overview-states-when-not-to-use`, `overview-states-why-to-use`: GOV.UK's template asks when to use a component and when not to, and PatternFly's asks how it is used, when and why, so a reader can choose the right component before reading its rules. Only the description is required by GOV.UK; the rest are prompts, hence SHOULD.
+- `behavioral-requirements-named`: OASIS gives each test assertion a unique identifier that maps it to the statement it tests; a unique name does that for a requirement and its test vectors. SHOULD, since the Committee Note only recommends universal uniqueness.
+- `appearance-contrast-in-all-states`: Fluent requires 4.5:1 text and 3:1 icon contrast in every interactive state, because a state change that drops contrast makes the control unreadable in that state. SHOULD, since it is one design system's requirement for its own buttons.
+- `tmpl-states-table`, `states-include-hover-and-selected`: Apple requires a press state so a button does not feel unresponsive, and Flutter's, Material's and Fluent's state lists include hover and selected; a row per state lets a builder style each one. SHOULD, because which states apply depends on the component.
+- `accessibility-role-from-apg`: APG states the role for each pattern, so the role need not be invented; SHOULD, since a component may have no APG pattern or a platform name for the role.
+- `accessibility-min-target-size`, `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`, `tmpl-platform-notes-platforms`: Apple asks for each platform's recommended minimum control size so controls are comfortable to tap and click; the platforms disagree on the value (Apple by platform, Android 48dp, Windows 40px, WCAG 24px at AA and 44px at AAA), so one value is wrong for most of them and each targeted platform needs its own entry. They are SHOULD because Apple and Android recommend rather than require their sizes. `tmpl-accessibility-min-tap-target` keeps the template's 44×44pt word for word; which default the template should give is the owner's open question.
+- `accessibility-keyboard-interaction`: APG's Button pattern documents keyboard interaction beside roles, states and properties, so a keyboard user's path is specified with the rest; SHOULD, since that is one APG page's layout.
+- `test-vectors-table`, `tmpl-test-vector-id-format`, `test-vectors-map-to-requirements`: a test assertion carries a unique identifier and names the precise normative statement it tests (OASIS), and is derived from the requirements (W3C), so a failing vector points at its requirement in a bug report. SHOULD, since OASIS and W3C give these as recommendation and good practice.
+- `test-vectors-cover-pass-fail-inapplicable`, `compliance-status-includes-inapplicable`: W3C's ACT and EARL outcome vocabularies include "inapplicable", so a check that cannot apply is not reported as a pass; SHOULD, since ACT requires the three outcomes only of its own rules.
+- `template-carries-test-vectors`: W3C suggests that the template for new proposals carry a section for test assertions, so every new spec starts with a place for them; SHOULD, since W3C gives it as advice.
+- `assumptions-and-limitations-stated`: an ACT rule must list its known assumptions, limitations and exceptions, so an implementer knows where the rule stops; SHOULD here, since that requirement is ACT's for its own rules.
+- `tmpl-deep-linking-patterns`, `deep-links-use-verified-https-links`: Apple strongly recommends universal links over custom URL schemes, which are a potential attack vector, and Android recommends App Links; both are recommendations, hence SHOULD. `tmpl-deep-linking-patterns` keeps the template's table word for word; whether its Apple row should show a universal link is the owner's open question.
+- `tmpl-localization-table`: Android asks that each string's context be described, because it is invaluable to the translator and gives a better translation; SHOULD, as Android's own advice.
+- `tmpl-accessibility-options`: Apple asks apps to respond to Reduce Motion and Increase Contrast and not to convey information by color alone, and WCAG forbids color as the only means; the web reads the same settings through media features, so one table covers every platform. SHOULD, because which options apply depends on the component.
+- `tmpl-analytics-events`, `analytics-event-names-fit-platform-limits`: the template's table is kept word for word for the owner, who decides whether its names should use dots or underscores; where events go to Firebase Analytics, which accepts only letters, digits and underscores, the MUST rule governs, so `tmpl-analytics-events` is a SHOULD such an ingredient departs from.
+- `tmpl-privacy-fields`, `privacy-states-encryption-in-transit`: Apple counts data as collected only when it leaves the device and is kept longer than the request needs, and Google Play defines ephemeral processing and asks whether data is encrypted in transit, so these fields answer the stores' privacy questions. SHOULD, since `## Privacy` is itself optional in `if-section-order`.
+- `tmpl-logging-subsystem-category`: Apple defines subsystem and category so that log messages can be filtered by functional area; SHOULD, since both are optional on Apple's Logger and other platforms name them differently.
+- `tmpl-design-decisions-approved`: a decision record carries its status, proposed until the stakeholders agree and accepted after (Nygard), so a reader can tell an agreed decision from a proposal. SHOULD, since the source is one practitioner's practice.
+- `tmpl-approval-fields`: kept word for word as the template has it, for the owner, who decides whether the template keeps them; no source and no required-field list prescribes them, hence SHOULD.
+- `tmpl-compliance-link-form`: a test assertion names the precise statement it tests (OASIS), and a UUID is unique across space and time (RFC 9562), so a link by UUID survives a check's rename. SHOULD, since a link by rdid still resolves.
+- `change-history-iso-dates`: Keep a Changelog recommends ISO 8601 dates, an international standard, so every reader reads a date the same way. SHOULD, as Keep a Changelog's own recommendation.
+- `section-structure-machine-checked`: a structural check a tool can decide (headings, required fields, order) need not be left to a reader; MD043's wildcards stand only for unspecified headings, so named optional sections take a custom rule.
 - `released-version-immutable`: Semantic Versioning forbids changing a released version, so every reader of a version sees the same text.
 
 ## References
