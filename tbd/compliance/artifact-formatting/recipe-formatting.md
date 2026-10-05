---
id: 328D96C6-20DE-495E-8977-733441B97F81
title: "Recipe Formatting Compliance"
domain: agenticdevelopercookbook://compliance/artifact-formatting/recipe-formatting
type: compliance
version: 2.1.0
status: draft
language: en
created: 2026-04-04
modified: 2026-09-25
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
  - agenticdevelopercookbook://introduction/conventions
related:
  - agenticdevelopercookbook://compliance/artifact-formatting/principle-formatting
  - agenticdevelopercookbook://compliance/artifact-formatting/guideline-formatting
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
11. `## Reference Implementations` (MAY omit in a cookbook with no code)
12. `## Design Decisions`
13. `## Compliance`
14. `## Change History`

## Checks

### rf-frontmatter-complete

All required YAML frontmatter fields MUST be present per `introduction/conventions.md`. Additionally, the `ingredients` field MUST be present and list at least one ingredient domain.

**Applies when:** always.

**Required fields:** id, title, domain, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, ingredients, depends-on, related, references.

**Guidelines:**
- [Conventions](agenticdevelopercookbook://introduction/conventions)

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
- [Conventions](agenticdevelopercookbook://introduction/conventions)

---

### rf-integration-requirements

The recipe MUST have a `## Integration Requirements` section containing named requirements using RFC 2119 keywords for how ingredients wire together.

**Applies when:** always.

**Guidelines:**
- [Conventions](agenticdevelopercookbook://introduction/conventions)

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

The recipe MUST have a `## Reference Implementations` section, directly after `## Platform Notes`, when its cookbook's repository implements it: a `| Platform | Path |` table with one row per implementing source file or directory. `Platform` is one of `web`, `apple`, `android`, `windows`, `python`; `Path` is a backticked path relative to the repository root, and a directory path ends with `/` and claims every source file below it. Every path MUST exist. In a cookbook with no code of its own the section MAY be omitted, or MAY be the one line `Not applicable: this cookbook carries no implementations.`

**Applies when:** the cookbook's `cookbook.json` declares `code` (a library or app cookbook that lives beside its source). `cookbook validate` checks that every listed path exists.

**Guidelines:**
- [Cookbook Formatting](agenticdevelopercookbook://compliance/artifact-formatting/cookbook-formatting)

---

### rf-design-decisions

The recipe MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

**Applies when:** always. New recipes start with an empty section; decisions are added as they arise.

---

### rf-compliance

The recipe MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

**Applies when:** always.

**Guidelines:**
- [Compliance INDEX](agenticdevelopercookbook://compliance/INDEX)

---

### rf-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- [Conventions](agenticdevelopercookbook://introduction/conventions)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-04 | Mike Fullerton | Initial creation |
| 2.0.0 | 2026-04-05 | Mike Fullerton | Rewrite for composition-focused recipe format |
| 2.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
