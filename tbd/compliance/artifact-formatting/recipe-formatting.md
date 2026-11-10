---
id: 328D96C6-20DE-495E-8977-733441B97F81
title: "Recipe Formatting Compliance"
type: compliance
version: 3.0.0
status: draft
language: en
created: 2026-04-04
modified: 2026-11-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Structural formatting checks for recipe artifacts — composition specs that combine configured ingredients into coherent features."
platforms: []
tags:
  - compliance
  - artifact-formatting
  - recipe
depends-on:
  - guide/introduction/conventions.md
related:
  - tbd/compliance/artifact-formatting/principle-formatting.md
  - tbd/compliance/artifact-formatting/guideline-formatting.md
references: []
---

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
11. `## Reference Implementations` (MAY: derived from `index.json` when compiled; never authored)
12. `## Design Decisions`
13. `## Compliance`
14. `## Change History`

## Checks

### rf-frontmatter-complete

All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field. Additionally, the `ingredients` field MUST be present and list at least one ingredient UUID (an rdid may be authored; `cookr update` stores the UUID).

The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

**Applies when:** always.

**Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, ingredients, depends-on, related, references.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

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

The recipe MUST have a `## Ingredients` section with a table containing columns: Name, Ingredient, Role, Required, Configuration. The Ingredient column holds an in-text link to the ingredient, `[<rdid>](cookbook:<uuid>)`, and every ingredient MUST resolve to an ingredient entry in the cookbook's `index.json` (or, as `cookbook:<cookbook-uuid>/<uuid>`, in a dependency's). Each row's ingredient MUST also be listed in the `ingredients` meta field.

**Applies when:** always.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

---

### rf-integration-requirements

The recipe MUST have a `## Integration Requirements` section containing named requirements using RFC 2119 keywords for how ingredients wire together.

**Applies when:** always.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

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

### rf-reference-implementations

The recipe MUST NOT carry an authored `## Reference Implementations` section. The code that implements it is recorded in its cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>` (`--remove <location>` drops a row), and `cookr confirm <uuid|rdid>` records it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section after `## Platform Notes`. `platform` is one of `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`; a location is a repo-relative file, a directory ending with `/` (which claims every source file below it), or a URL. Every recorded location MUST exist, unless the row is `planned`.

**Applies when:** the repo's `.cookr.json` declares `roots` (a cookbook that lives beside its source). `cookr validate` checks that every recorded location exists.

**Guidelines:**
- [Cookbook Formatting](cookbook-formatting.md)

---

### rf-design-decisions

The recipe MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

**Applies when:** always. New recipes start with an empty section; decisions are added as they arise.

---

### rf-compliance

The recipe MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

**Applies when:** always.

**Guidelines:**
- [Compliance INDEX](../INDEX.md)

---

### rf-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-04 | Mike Fullerton | Initial creation |
| 2.0.0 | 2026-04-05 | Mike Fullerton | Rewrite for composition-focused recipe format |
| 2.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 3.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID identity and rdids replace `domain`; implementations live in index.json |
