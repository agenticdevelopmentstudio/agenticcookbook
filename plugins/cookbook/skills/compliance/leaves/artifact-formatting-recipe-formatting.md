<!-- leaf: compliance/artifact-formatting-recipe-formatting · source: compliance/artifact-formatting/recipe-formatting.md -->

**Rules** (cite as `compliance/artifact-formatting-recipe-formatting#<slug>`):

- `files-recipes-subdirectories-have-type-except-template` MUST — This category applies to any file with type: recipe in its frontmatter. All files in recipes/ (and its subdirectories) …
- `recipes-follow-section-order-optional` MUST — Recipes MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear out …
- `yaml-frontmatter-fields-present-per-introduction-conventions` MUST — All required YAML frontmatter fields MUST be present per introduction/conventions.md. Additionally, the ingredients …
- `type-field-recipe` MUST — The type field MUST be recipe.
- `first-h1-heading-match-frontmatter-title-field` MUST — The first H1 heading MUST match the frontmatter title field exactly.
- `recipe-have-overview-section-describing` MUST — The recipe MUST have a ## Overview section describing what the composition is and when to use it.
- `recipe-have-ingredients-section-table` MUST — The recipe MUST have a ## Ingredients section with a table containing columns: Name, Domain, Role, Required, …
- `recipe-have-integration-requirements-section` MUST — The recipe MUST have a ## Integration Requirements section containing named requirements using RFC 2119 keywords for …
- `recipe-have-layout-section-describing` MUST — The recipe MUST have a ## Layout section describing spatial or logical arrangement of ingredients. UI recipes SHOULD …
- `recipe-have-shared-state-section` MUST — The recipe MUST have a ## Shared State section with a table defining state flow between ingredients: State, Source, …
- `recipe-have-integration-test-vectors` MUST — The recipe MUST have a ## Integration Test Vectors section with a table containing columns: ID, Requirements, Input, …
- `recipe-have-edge-cases-section` MUST — The recipe MUST have a ## Edge Cases section describing composition-level boundary conditions.
- `recipe-have-platform-notes-section` MUST — The recipe MUST have a ## Platform Notes section with per-platform integration guidance. At minimum: SwiftUI, Compose, …
- `recipe-have-design-decisions-section` MUST — The recipe MUST have a ## Design Decisions section. Each decision follows the format: Decision: Description. Rationale: …
- `recipe-have-compliance-section-table` MUST — The recipe MUST have a ## Compliance section with a table containing columns: Check, Status, Category. Status values: …
- `file-end-change-history-section` MUST — The file MUST end with a ## Change History section containing a table with columns: Version, Date, Author, Summary.

# Recipe Formatting Compliance

Recipes are compositions of configured ingredients wired together into coherent features. Each recipe specifies which ingredients it uses, how they connect, what state flows between them, and how they are arranged spatially or logically. Every recipe follows a consistent section order so that agents and humans can navigate them predictably.

## Applicability

This category applies to any file with `type: recipe` in its frontmatter. All files in `recipes/` (and its subdirectories) MUST have this type, except `_template.md`.

## Section Order

Recipes MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear out of order.

1. YAML frontmatter
2. `# Title`
3. `## Overview`
4. `## Ingredients`
5. `## Integration Requirements`
6. `## Layout`
7. `## Shared State`
8. `## Integration Test Vectors`
9. `## Edge Cases`
10. `## Platform Notes`
11. `## Design Decisions`
12. `## Compliance`
13. `## Change History`

## Checks

### rf-frontmatter-complete

All required YAML frontmatter fields MUST be present per `introduction/conventions.md`. Additionally, the `ingredients` field MUST be present and list at least one ingredient domain.

**Applies when:** always.

**Required fields:** id, title, domain, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, ingredients, depends-on, related, references.

**Guidelines:**
- Conventions

---

### rf-type-field

The `type` field MUST be `recipe`.

**Applies when:** always.

---

### rf-title-heading

The first H1 heading MUST match the frontmatter `title` field exactly.

**Applies when:** always.

---

### rf-overview

The recipe MUST have a `## Overview` section describing what the composition is and when to use it.

**Applies when:** always.

---

### rf-ingredients

The recipe MUST have a `## Ingredients` section with a table containing columns: Name, Domain, Role, Required, Configuration. Each ingredient MUST reference a valid `agenticdevelopercookbook://ingredients/` domain.

**Applies when:** always.

**Guidelines:**
- Conventions

---

### rf-integration-requirements

The recipe MUST have a `## Integration Requirements` section containing named requirements using RFC 2119 keywords for how ingredients wire together.

**Applies when:** always.

**Guidelines:**
- Conventions

---

### rf-layout

The recipe MUST have a `## Layout` section describing spatial or logical arrangement of ingredients. UI recipes SHOULD include an ASCII diagram.

**Applies when:** always.

---

### rf-shared-state

The recipe MUST have a `## Shared State` section with a table defining state flow between ingredients: State, Source, Consumer, Direction, Mechanism.

**Applies when:** always.

---

### rf-integration-test-vectors

The recipe MUST have a `## Integration Test Vectors` section with a table containing columns: ID, Requirements, Input, Expected. Tests validate ingredient interactions, not individual ingredient behavior.

**Applies when:** always.

---

### rf-edge-cases

The recipe MUST have a `## Edge Cases` section describing composition-level boundary conditions.

**Applies when:** always.

---

### rf-platform-notes

The recipe MUST have a `## Platform Notes` section with per-platform integration guidance. At minimum: SwiftUI, Compose, React/Web.

**Applies when:** always. Single-platform recipes list only the target platform.

---

### rf-design-decisions

The recipe MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

**Applies when:** always. New recipes start with an empty section; decisions are added as they arise.

---

### rf-compliance

The recipe MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

**Applies when:** always.

**Guidelines:**
- Compliance INDEX

---

### rf-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- Conventions
