---
id: 39931D07-F23F-4980-A055-6916E722A01F
title: "Guideline Formatting Compliance"
type: compliance
version: 2.0.0
status: draft
language: en
created: 2026-04-04
modified: 2026-11-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Structural formatting checks for guideline artifacts — frontmatter, summary, structured guidance, RFC keywords, and change history."
platforms: []
tags:
  - compliance
  - artifact-formatting
  - guideline
depends-on:
  - guide/introduction/conventions.md
related:
  - tbd/compliance/artifact-formatting/principle-formatting.md
  - tbd/compliance/artifact-formatting/recipe-formatting.md
references: []
---

# Guideline Formatting Compliance

Guidelines are topic-oriented rules that apply during planning and implementation. They are more detailed than principles but less prescriptive than recipes — structured guidance with clear requirements.

## Applicability

This category applies to any file with `type: guideline` in its frontmatter. All files in `guidelines/` (and its subdirectories) MUST have this type.

## Checks

### gf-frontmatter-complete

All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.

The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

**Applies when:** always.

**Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

---

### gf-type-field

The `type` field MUST be `guideline`.

**Applies when:** always.

---

### gf-title-heading

The first H1 heading MUST match the frontmatter `title` field exactly.

**Applies when:** always.

---

### gf-summary-statement

A summary statement MUST appear immediately after the H1 heading. This is the guideline's core message — typically 1-3 sentences that a reader can act on without reading further.

**Applies when:** always.

---

### gf-structured-guidance

The guideline MUST include structured guidance in the form of bullet points, tables, subsections, or a combination. Unstructured prose without actionable items is not sufficient.

**Applies when:** always.

---

### gf-rfc-keywords

Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels. Keywords MUST be bold or uppercase when used normatively.

**Applies when:** the guideline contains requirements or rules (not purely informational content).

---

### gf-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

---

### gf-compliance-section

The guideline MAY include a `## Compliance` section listing evaluated compliance checks and their status. This is recommended when the guideline is referenced by compliance checks in other categories.

**Applies when:** the guideline is referenced by one or more compliance check definitions.

---

### gf-triggers-field

The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`. Empty list `[]` is acceptable for guidelines not yet classified.

**Applies when:** always.

**Guidelines:**
- [Trigger Guide](../../../guide/introduction/trigger-guide.md)
- [Conventions](../../../guide/introduction/conventions.md)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID identity and rdids replace `domain`; implementations live in index.json |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Add triggers field compliance check |
| 1.0.0 | 2026-04-04 | Mike Fullerton | Initial creation |
