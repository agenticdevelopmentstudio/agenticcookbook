<!-- leaf: compliance/artifact-formatting-ingredient-formatting · source: compliance/artifact-formatting/ingredient-formatting.md -->

**Rules** (cite as `compliance/artifact-formatting-ingredient-formatting#<slug>`):

- `files-ingredients-subdirectories-have-type-except-template` MUST — This category applies to any file with type: ingredient in its frontmatter. All files in ingredients/ (and its …
- `ingredients-follow-section-order-optional` MUST — Ingredients MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear …
- `deep-linking-omit` MAY — ## Deep Linking (MAY omit)
- `localization-omit` MAY — ## Localization (MAY omit)
- `accessibility-options-omit` MAY — ## Accessibility Options (MAY omit)
- `feature-flags-omit` MAY — ## Feature Flags (MAY omit)
- `analytics-omit` MAY — ## Analytics (MAY omit)
- `privacy-omit` MAY — ## Privacy (MAY omit)
- `yaml-frontmatter-fields-present-per-introduction-conventions` MUST — All required YAML frontmatter fields MUST be present per introduction/conventions.md.
- `type-field-ingredient` MUST — The type field MUST be ingredient.
- `first-h1-heading-match-frontmatter-title-field` MUST — The first H1 heading MUST match the frontmatter title field exactly.
- `ingredient-have-overview-section-brief` MUST — The ingredient MUST have a ## Overview section with a brief description of what the component is and when to use it.
- `ingredient-have-behavioral-requirements-section` MUST — The ingredient MUST have a ## Behavioral Requirements section containing named requirements using RFC 2119 keywords. …
- `ingredient-have-appearance-section-defining` MUST — The ingredient MUST have a ## Appearance section defining visual properties: corner radius, padding, font, background, …
- `applies-when` MAY — UI ingredients (components, panels, windows). MAY be omitted for infrastructure ingredients.
- `ingredient-have-states-section-table` MUST — The ingredient MUST have a ## States section with a table defining visual state changes (default, pressed, disabled, …
- `applies-when-2` MAY — UI ingredients with interactive states. MAY be omitted for infrastructure ingredients.
- `ingredient-have-accessibility-section-defining` MUST — The ingredient MUST have a ## Accessibility section defining: role/trait, label requirements, state change …
- `ingredient-have-conformance-test-vectors` MUST — The ingredient MUST have a ## Conformance Test Vectors section with a table containing columns: ID, Requirements, …
- `ingredient-have-edge-cases-section` MUST — The ingredient MUST have a ## Edge Cases section describing boundary conditions, error states, and unexpected input …
- `ingredient-have-configuration-section-table` MUST — The ingredient MUST have a ## Configuration section with a table listing configurable options: Option, Type, Default, …
- `ingredient-have-logging-section-defining` MUST — The ingredient MUST have a ## Logging section defining: subsystem, category, and a table of log events with columns: …
- `ingredient-have-platform-notes-section` MUST — The ingredient MUST have a ## Platform Notes section with per-platform implementation guidance. At minimum: SwiftUI, …
- `ingredient-have-design-decisions-section` MUST — The ingredient MUST have a ## Design Decisions section. Each decision follows the format: Decision: Description. …
- `ingredient-have-compliance-section-table` MUST — The ingredient MUST have a ## Compliance section with a table containing columns: Check, Status, Category. Status …
- `file-end-change-history-section` MUST — The file MUST end with a ## Change History section containing a table with columns: Version, Date, Author, Summary.

# Ingredient Formatting Compliance

Ingredients are atomic component specs for UI elements, infrastructure patterns, and autonomous dev bots. They are the most structured artifact type — every ingredient follows a consistent section order so that agents and humans can navigate them predictably.

## Applicability

This category applies to any file with `type: ingredient` in its frontmatter. All files in `ingredients/` (and its subdirectories) MUST have this type, except `_template.md`.

## Section Order

Ingredients MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear out of order.

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
19. `## Design Decisions`
20. `## Compliance`
21. `## Change History`

## Checks

### if-frontmatter-complete

All required YAML frontmatter fields MUST be present per `introduction/conventions.md`.

**Applies when:** always.

**Required fields:** id, title, domain, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

**Guidelines:**
- Conventions

---

### if-type-field

The `type` field MUST be `ingredient`.

**Applies when:** always.

---

### if-title-heading

The first H1 heading MUST match the frontmatter `title` field exactly.

**Applies when:** always.

---

### if-overview

The ingredient MUST have a `## Overview` section with a brief description of what the component is and when to use it.

**Applies when:** always.

---

### if-behavioral-requirements

The ingredient MUST have a `## Behavioral Requirements` section containing named requirements using RFC 2119 keywords. Requirements use kebab-case names in bold: `**must-do-something**: Component MUST ...`

**Applies when:** always.

**Guidelines:**
- Conventions

---

### if-appearance

The ingredient MUST have a `## Appearance` section defining visual properties: corner radius, padding, font, background, foreground, border, shadow, and size constraints.

**Applies when:** UI ingredients (components, panels, windows). MAY be omitted for infrastructure ingredients.

---

### if-states

The ingredient MUST have a `## States` section with a table defining visual state changes (default, pressed, disabled, focused, loading, etc.).

**Applies when:** UI ingredients with interactive states. MAY be omitted for infrastructure ingredients.

---

### if-accessibility

The ingredient MUST have a `## Accessibility` section defining: role/trait, label requirements, state change announcements, and minimum tap target size.

**Applies when:** always. Infrastructure ingredients define accessibility as "not applicable" with justification.

---

### if-test-vectors

The ingredient MUST have a `## Conformance Test Vectors` section with a table containing columns: ID, Requirements, Input, Expected. Each test vector maps to one or more named requirements from `## Behavioral Requirements`.

**Applies when:** always.

---

### if-edge-cases

The ingredient MUST have a `## Edge Cases` section describing boundary conditions, error states, and unexpected input scenarios.

**Applies when:** always.

---

### if-configuration

The ingredient MUST have a `## Configuration` section with a table listing configurable options: Option, Type, Default, Description. If the ingredient has no configurable options, the section MUST be present with a note stating "This ingredient has no configurable options."

**Applies when:** always.

---

### if-logging

The ingredient MUST have a `## Logging` section defining: subsystem, category, and a table of log events with columns: Event, Level, Message.

**Applies when:** always.

**Guidelines:**
- Structured Logging

---

### if-platform-notes

The ingredient MUST have a `## Platform Notes` section with per-platform implementation guidance. At minimum: SwiftUI, Compose, React/Web.

**Applies when:** always. Single-platform ingredients list only the target platform.

---

### if-design-decisions

The ingredient MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

**Applies when:** always. New ingredients start with an empty section; decisions are added as they arise.

---

### if-compliance

The ingredient MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

**Applies when:** always.

**Guidelines:**
- Compliance INDEX

---

### if-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- Conventions
