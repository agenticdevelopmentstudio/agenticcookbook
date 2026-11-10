---
id: E10E9785-E7D9-47F9-BA8C-A85E745BF294
title: "Ingredient Formatting Compliance"
type: compliance
version: 2.0.0
status: draft
language: en
created: 2026-04-05
modified: 2026-11-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Structural formatting checks for ingredient artifacts — the most detailed artifact type with ~16 required sections."
platforms: []
tags:
  - compliance
  - artifact-formatting
  - ingredient
depends-on:
  - guide/introduction/conventions.md
related:
  - tbd/compliance/artifact-formatting/principle-formatting.md
  - tbd/compliance/artifact-formatting/guideline-formatting.md
  - tbd/compliance/artifact-formatting/recipe-formatting.md
references: []
---

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
19. `## Reference Implementations` (MAY: derived from `index.json` when compiled; never authored)
20. `## Design Decisions`
21. `## Compliance`
22. `## Change History`

## Checks

### if-frontmatter-complete

All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.

The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

**Applies when:** always.

**Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

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
- [Conventions](../../../guide/introduction/conventions.md)

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
- [adc.guideline.implementing.observability.logging](cookbook:0f0c1da3-1c53-417b-890d-0259d7513c65)

---

### if-platform-notes

The ingredient MUST have a `## Platform Notes` section with per-platform implementation guidance. At minimum: SwiftUI, Compose, React/Web.

**Applies when:** always. Single-platform ingredients list only the target platform.

---

### if-reference-implementations

The ingredient MUST NOT carry an authored `## Reference Implementations` section. The code that implements it is recorded in its cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>` (`--remove <location>` drops a row), and `cookr confirm <uuid|rdid>` records it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section after `## Platform Notes`. `platform` is one of `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`; a location is a repo-relative file, a directory ending with `/` (which claims every source file below it), or a URL. Every recorded location MUST exist, unless the row is `planned`.

**Applies when:** the repo's `.cookr.json` declares `roots` (a cookbook that lives beside its source). `cookr validate` checks that every recorded location exists.

**Guidelines:**
- [Cookbook Formatting](cookbook-formatting.md)

---

### if-design-decisions

The ingredient MUST have a `## Design Decisions` section. Each decision follows the format: **Decision**: Description. **Rationale**: Why. **Approved**: yes | pending.

**Applies when:** always. New ingredients start with an empty section; decisions are added as they arise.

---

### if-compliance

The ingredient MUST have a `## Compliance` section with a table containing columns: Check, Status, Category. Status values: `passed`, `failed`, `partial`. Each check links to its definition in the relevant compliance category file.

**Applies when:** always.

**Guidelines:**
- [Compliance INDEX](../INDEX.md)

---

### if-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID identity and rdids replace `domain`; implementations live in index.json |
| 1.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-04-05 | Mike Fullerton | Initial creation |
