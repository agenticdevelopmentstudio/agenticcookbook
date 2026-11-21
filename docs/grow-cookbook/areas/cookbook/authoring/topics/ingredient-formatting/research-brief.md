# Research brief: ingredient-formatting

- **Area:** `cookbook/authoring`
- **Topic:** `ingredient-formatting` (new)
- **Artifact:** `cookbook/guidelines/cookbook/authoring/ingredient-formatting`
- **Base commit:** `071e52f9572bf4b7c534cfcf95fb111282abc423` (from `base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain technical
  writing; method practitioner and standards sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner ruling,
  Owner question 3: "no escalation for any topic. Each keeps its proposed bar.").

## Scope

The structure of a cookbook ingredient: the atomic component spec in
`cookbook/ingredients/`, for UI elements, infrastructure patterns and
autonomous dev bots. The research covers its frontmatter, its title, its
section list and order, which sections may be omitted and how an omission
is marked, what each section holds, and which checks a tool can decide.

Out of scope, cited and never restated: the case of the RFC 2119 keywords
(MUST, SHOULD, MAY) and the lint severity a rule's keyword gives a failed
check belong to the sibling topic `requirement-keywords`
(`cookbook/guidelines/cookbook/authoring/requirement-keywords`, owner ruling
Q10 + Q11). This topic's rules cite that topic for both; the research here
records no claim about either.

## Research questions (from the area plan, verbatim)

1. Best practice: how do component specification templates (design-system component pages, interface specs) order their sections, and which sections may be omitted for a component without UI?
2. Known solutions: how do JSON Schema, markdownlint's required-headings rule and Vale check a long fixed section order with optional sections, and which of the draft's 17 checks can a tool decide?
3. Platform guidelines: what do published design-system documentation guides (Material, Apple Human Interface Guidelines, Fluent) and W3C's specification conventions require of a component specification's sections?
4. The expert's view: what do specification authors say about long mandatory templates, empty sections and "not applicable" markers?
5. **Ingredient section order rationale**: for each of the 21 sections, find the reason its place and its MAY-omit status rest on, and state the order and the optional set the research supports.
6. `template-conformance`'s component-recipe section list (Overview, Behavioral Requirements, Appearance, States, Accessibility, Conformance Test Vectors, Edge Cases) moves here (owner ruling Q8): research it with the ingredient template's sections, state how the two lists reconcile, and record that `template-conformance` drops the list when it is next written.

Note on question 5: the draft's *Section Order* list has 22 entries: YAML
frontmatter, `# Title` and 20 `##` sections (one of them, `## Reference
Implementations`, derived and never authored). Research each entry.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

## Method

- Research to `cookbook/guidelines/researching/process/research-methodology-and-sources`,
  using its source catalogue for technical writing and data-format
  validation. Primary sources (specifications, standards, vendor and
  platform-owner documentation: W3C, IETF, JSON Schema, markdownlint, Vale,
  Material Design, Apple Human Interface Guidelines, Microsoft Fluent, the
  design-system sites themselves) come before secondary ones.
- Verify every rule listed below. Each is quoted **verbatim**, with its file
  and the base commit, as a claim to check, never as a source. The names are
  fixed: verdicts key on them.
- Score each claim 0–100 per `cookbook/guidelines/researching/evidence/verification-and-trust-scoring`,
  applying `cite-the-claim-not-the-document`, `independence-before-corroboration`,
  `domain-stratified-trust`, `suppress-unsupported-confidence` and
  `provenance-at-generation-time`.
- `supported` means supported at the rule's stated strength. Judge the
  strength only as "required", "recommended" or "optional"; how the keyword
  is cased and what severity it gives is `requirement-keywords`' ground.
- Find what the topic is missing: practice the research finds that no rule
  below covers (for example how an inapplicable section is marked, a
  per-section purpose statement, or a machine-checkable section schema), each
  a `new` verdict.

## Rules to verify

Files, all at base commit `071e52f9572bf4b7c534cfcf95fb111282abc423`:
- **D** = `tbd/compliance/artifact-formatting/ingredient-formatting.md` (the
  draft; 17 checks plus its *Applicability* and *Section Order* sections);
- **T** = `cookbook/ingredients/_template.md` (the ingredient template);
- **C** = `cookbook/guidelines/cookbook/recipe-quality/template-conformance/rules.md`
  (the component-recipe section list, which moves here by owner ruling Q8).

Each rule: its name, the file, the text verbatim. A rule whose text holds
no MUST, SHOULD or MAY (in any case) is marked **no RFC keyword**.

### From D: applicability and section order

- **if-applicability** (D, *Applicability*): "This category applies to any file with `type: ingredient` in its frontmatter. All files in `ingredients/` (and its subdirectories) MUST have this type, except `_template.md`."
- **if-section-order** (D, *Section Order*): "Ingredients MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear out of order.

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

### From D: the 17 checks

- **if-frontmatter-complete** (D): "All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.

  The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

  **Applies when:** always.

  **Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references."
- **if-type-field** (D): "The `type` field MUST be `ingredient`.

  **Applies when:** always."
- **if-title-heading** (D): "The first H1 heading MUST match the frontmatter `title` field exactly.

  **Applies when:** always."
- **if-overview** (D): "The ingredient MUST have a `## Overview` section with a brief description of what the component is and when to use it.

  **Applies when:** always."
- **if-behavioral-requirements** (D): "The ingredient MUST have a `## Behavioral Requirements` section containing named requirements using RFC 2119 keywords. Requirements use kebab-case names in bold: `**must-do-something**: Component MUST ...`

  **Applies when:** always."
- **if-appearance** (D): "The ingredient MUST have a `## Appearance` section defining visual properties: corner radius, padding, font, background, foreground, border, shadow, and size constraints.

  **Applies when:** UI ingredients (components, panels, windows). MAY be omitted for infrastructure ingredients."
- **if-states** (D): "The ingredient MUST have a `## States` section with a table defining visual state changes (default, pressed, disabled, focused, loading, etc.).

  **Applies when:** UI ingredients with interactive states. MAY be omitted for infrastructure ingredients."
- **if-accessibility** (D): "The ingredient MUST have a `## Accessibility` section defining: role/trait, label requirements, state change announcements, and minimum tap target size.

  **Applies when:** always. Infrastructure ingredients define accessibility as "not applicable" with justification."
- **if-test-vectors** (D): "The ingredient MUST have a `## Conformance Test Vectors` section with a table containing columns: ID, Requirements, Input, Expected. Each test vector maps to one or more named requirements from `## Behavioral Requirements`.

  **Applies when:** always."
- **if-edge-cases** (D): "The ingredient MUST have a `## Edge Cases` section describing boundary conditions, error states, and unexpected input scenarios.

  **Applies when:** always."
- **if-configuration** (D): "The ingredient MUST have a `## Configuration` section with a table listing configurable options: Option, Type, Default, Description. If the ingredient has no configurable options, the section MUST be present with a note stating "This ingredient has no configurable options."

  **Applies when:** always."
- **if-logging** (D): "The ingredient MUST have a `## Logging` section defining: subsystem, category, and a table of log events with columns: Event, Level, Message.

  **Applies when:** always."
- **if-platform-notes** (D): "The ingredient MUST have a `## Platform Notes` section with per-platform implementation guidance. At minimum: SwiftUI, Compose, React/Web.

  **Applies when:** always. Single-platform ingredients list only the target platform."
- **if-reference-implementations** (D): "The ingredient MUST NOT carry an authored `## Reference Implementations` section. The code that implements it is recorded in its cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>` (`--remove <location>` drops a row), and `cookr confirm <uuid|rdid>` records it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section after `## Platform Notes`. `platform` is one of `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`; a location is a repo-relative file, a directory ending with `/` (which claims every source file below it), or a URL. Every recorded location MUST exist, unless the row is `planned`.

  **Applies when:** the repo's `.cookr.json` declares `roots` (a cookbook that lives beside its source). `cookr validate` checks that every recorded location exists."
- **if-design-decisions** (D): "The ingredient MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

  **Applies when:** always. New ingredients start with an empty section; decisions are added as they arise."
- **if-compliance** (D): "The ingredient MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

  **Applies when:** always."
- **if-change-history** (D): "The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

  **Applies when:** always."

### From T: the template's own guidance

Text the template states beyond the draft's checks. Each is quoted from T.

- **tmpl-approval-fields** (T, frontmatter): the template's frontmatter carries two fields the draft's required list lacks: "approved-by: \"\"" and "approved-date: \"\"". **No RFC keyword.**
- **tmpl-appearance-properties** (T, `## Appearance`): "- **Corner radius**:
  - **Padding**: vertical × horizontal
  - **Font**: weight, size
  - **Background**: color value or description
  - **Foreground/Text**: color value or description
  - **Border**: width, color (if any)
  - **Shadow**: offset, blur, color (if any)
  - **Min/Max size**: constraints (if any)" **No RFC keyword.**
- **tmpl-states-table** (T, `## States`): "| State | Appearance change |" with rows "Default", "Pressed", "Disabled", "Focused", "Loading". **No RFC keyword.**
- **tmpl-accessibility-min-tap-target** (T, `## Accessibility`): "- Role/trait (e.g., button, heading, text field)
  - Label requirements
  - Announce state changes (e.g., loading, disabled)
  - Minimum tap target: 44×44pt" **No RFC keyword.**
- **tmpl-test-vector-id-format** (T, `## Conformance Test Vectors`): "| ID | Requirements | Input | Expected |" with the example row "| component-001 | do-something | | |". **No RFC keyword.**
- **tmpl-deep-linking-patterns** (T, `## Deep Linking`): "| Platform | URL Pattern |" with rows "| Apple | `{{app_scheme}}://component-name` |", "| Android | `https://{{app_domain}}/component-name` |", "| Web | `/component-name` |". **No RFC keyword.**
- **tmpl-localization-table** (T, `## Localization`): "| String Key | Default (en) | Context |". **No RFC keyword.**
- **tmpl-accessibility-options** (T, `## Accessibility Options`): "Document which accessibility display options (Rule 15) this component responds to:" with "| Option | Behavior |" and rows "Reduce Motion", "Increase Contrast", "Differentiate Without Color". **No RFC keyword.**
- **tmpl-feature-flags-table** (T, `## Feature Flags`): "| Flag Key | Default | Description |" with the row "| `{{app_prefix}}.component_name` | `true` | Enables this component |". **No RFC keyword.**
- **tmpl-analytics-events** (T, `## Analytics`): "| Event | Properties | When |" with rows "| `component_name.viewed` | `{}` | Component appears on screen |" and "| `component_name.interacted` | `{ action: string }` | User interacts with component |". **No RFC keyword.**
- **tmpl-privacy-fields** (T, `## Privacy`): "- **Data collected**: None / describe what is collected
  - **Storage**: Where and how data is stored
  - **Transmission**: Whether data leaves the device
  - **Retention**: How long data is kept" **No RFC keyword.**
- **tmpl-logging-subsystem-category** (T, `## Logging`): "Subsystem: `{{bundle_id}}` | Category: `ComponentName`" with "| Event | Level | Message |" and the row "| | debug | `ComponentName: ` |". **No RFC keyword.**
- **tmpl-platform-notes-platforms** (T, `## Platform Notes`): "- **SwiftUI**:
  - **Compose**:
  - **React/Web**:
  - **AppKit / UIKit**:
  - **WinUI 3**:" **No RFC keyword.**
- **tmpl-design-decisions-approved** (T, `## Design Decisions`): "Record any decisions made during implementation that affect visual or behavioral outcome. Each decision should be approved by the user." **No RFC keyword** (the "should" is lowercase; whether that carries a keyword's meaning is `requirement-keywords`' question).
- **tmpl-compliance-link-form** (T, `## Compliance`): "| Check | Status | Category |" with the row "| [adc.check.<document>.<check-name>](cookbook:<check-uuid>) | passed | Category |". **No RFC keyword.**

### From C: the component-recipe section list (moves here, owner ruling Q8)

- **component-recipe-sections-in-order** (C, `rules.md`, the sub-bullet of
  `must-contain-template-sections-in-order`): "- **must-contain-template-sections-in-order**: The recipe MUST contain all sections defined in the standard template, in the prescribed order.
    - For component recipes, the required sections in order are: **Overview**, **Behavioral Requirements**, **Appearance**, **States**, **Accessibility**, **Conformance Test Vectors**, **Edge Cases**."

  Only the sub-bullet's component list is this topic's; the parent rule stays
  in `template-conformance` for the recipe's own list. Research how this
  7-section list reconciles with D's section order and T's sections, and
  record that `template-conformance` drops the list when it is next written.

## Open questions to raise, if the research leaves them to policy

Put each policy choice the owner must make under `open_questions`, one entry
each: for example whether inapplicable sections are omitted or kept with a
"not applicable" note, whether UI-only sections split the ingredient into UI
and infrastructure variants, and which checks become a schema or lint rule
rather than prose.
